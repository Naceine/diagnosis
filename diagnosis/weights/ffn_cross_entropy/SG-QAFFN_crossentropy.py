#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'diagnosis/weights/ffn_cross_entropy'))
	print(os.getcwd())
except:
	pass

#%%
from google.colab import drive
drive.mount('/content/gdrive')


#%%
# install tf 2.0
from __future__ import absolute_import, division, print_function, unicode_literals

get_ipython().system('pip install tensorflow-gpu==2.0.0-alpha0')
import tensorflow as tf
# tf.compat.v1.disable_eager_execution()

print(tf.__version__)


#%%
import os
from glob import glob

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

SEED = 42


def _float_list_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def _int64_list_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def create_generator_for_ffn(
        file_list,
        mode='train'):

    # file_list = glob(os.path.join(data_dir, '*.csv'))

    for full_file_path in file_list:
        # full_file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(full_file_path):
            raise FileNotFoundError("File %s not found" % full_file_path)
        df = pd.read_csv(full_file_path, encoding='utf8')

        # so train test split
        if mode == 'train':
            df, _ = train_test_split(df, test_size=0.2, random_state=SEED)
        else:
            _, df = train_test_split(df, test_size=0.2, random_state=SEED)

        for _, row in df.iterrows():
            q_vectors = np.fromstring(row.question_bert.replace(
                '[[', '').replace(']]', ''), sep=' ')
            a_vectors = np.fromstring(row.answer_bert.replace(
                '[[', '').replace(']]', ''), sep=' ')
            vectors = np.stack([q_vectors, a_vectors], axis=0)
            if mode in ['train', 'eval']:
                yield vectors, 1
            else:
                yield vectors


def ffn_serialize_fn(features):
    features_tuple = {'features': _float_list_feature(
        features[0].flatten()), 'labels': _int64_feature(features[1])}
    example_proto = tf.train.Example(
        features=tf.train.Features(feature=features_tuple))
    return example_proto.SerializeToString()


def make_tfrecord(data_dir, generator_fn, serialize_fn, suffix='', **kwargs):
    """Function to make TF Records from csv files
    This function will take all csv files in data_dir, convert them
    to tf example and write to *_{suffix}_train/eval.tfrecord to data_dir.

    Arguments:
        data_dir {str} -- dir that has csv files and store tf record
        generator_fn {fn} -- A function that takes a list of filepath and yield the
        parsed recored from file.
        serialize_fn {fn} -- A function that takes output of generator fn and convert to tf example

    Keyword Arguments:
        suffix {str} -- suffix to add to tf record files (default: {''})
    """
    file_list = glob(os.path.join(data_dir, '*.csv'))
    train_tf_record_file_list = [
        f.replace('.csv', '_{0}_train.tfrecord'.format(suffix)) for f in file_list]
    test_tf_record_file_list = [
        f.replace('.csv', '_{0}_eval.tfrecord'.format(suffix)) for f in file_list]
    for full_file_path, train_tf_record_file_path, test_tf_record_file_path in zip(file_list, train_tf_record_file_list, test_tf_record_file_list):
        print('Converting file {0} to TF Record'.format(full_file_path))
        with tf.io.TFRecordWriter(train_tf_record_file_path) as writer:
            for features in generator_fn([full_file_path], mode='train', **kwargs):
                example = serialize_fn(features)
                writer.write(example)
        with tf.io.TFRecordWriter(test_tf_record_file_path) as writer:
            for features in generator_fn([full_file_path], mode='eval', **kwargs):
                example = serialize_fn(features)
                writer.write(example)


def create_dataset_for_ffn(
        data_dir,
        mode='train',
        hidden_size=768,
        shuffle_buffer=10000,
        prefetch=10000,
        batch_size=32):

    tfrecord_file_list = glob(os.path.join(
        data_dir, '*_FFN_{0}.tfrecord'.format((mode))))
    if not tfrecord_file_list:
        print('TF Record not found')
        make_tfrecord(
            data_dir, create_generator_for_ffn,
            ffn_serialize_fn, 'FFN')

    dataset = tf.data.TFRecordDataset(tfrecord_file_list)

    def _parse_ffn_example(example_proto):
        feature_description = {
            'features': tf.io.FixedLenFeature([2*768], tf.float32),
            'labels': tf.io.FixedLenFeature([], tf.int64, default_value=0),
        }
        feature_dict = tf.io.parse_single_example(
            example_proto, feature_description)
        return tf.reshape(feature_dict['features'], (2, 768)), feature_dict['labels']
    dataset = dataset.map(_parse_ffn_example)

    dataset = dataset.shuffle(shuffle_buffer)

    dataset = dataset.prefetch(prefetch)

    dataset = dataset.batch(batch_size)
    return dataset


#%%
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

import tensorflow as tf
import tensorflow.keras.backend as K


class FFN(tf.keras.layers.Layer):
    def __init__(
            self,
            hidden_size=768,                                                                #SG edit from 768 4-24-19
            dropout=0.2,
            residual=True,
            name='FFN',
            **kwargs):
        """Simple Dense wrapped with various layers
        """

        super(FFN, self).__init__(name=name, **kwargs)
        self.hidden_size = hidden_size
        self.dropout = dropout
        self.residual = residual
        self.ffn_layer = tf.keras.layers.Dense(
            units=hidden_size,
            use_bias=True
        )

    def call(self, inputs):
        ffn_embedding = self.ffn_layer(inputs)
        ffn_embedding = tf.keras.layers.ReLU()(ffn_embedding)
        if self.dropout > 0:
            ffn_embedding = tf.keras.layers.Dropout(
                self.dropout)(ffn_embedding)
#         ffn_embedding = self.ffn_layer(inputs)  #SG edit from 768 4-24-19
#         ffn_embedding = tf.keras.layers.ReLU()(ffn_embedding)  #SG edit from 768 4-24-19
#         if self.dropout > 0:  #SG edit from 768 4-24-19
#             ffn_embedding = tf.keras.layers.Dropout(  #SG edit from 768 4-24-19
#                 self.dropout)(ffn_embedding)  #SG edit from 768 4-24-19


        if self.residual:
            ffn_embedding += inputs
        return ffn_embedding


class MedicalQAModel(tf.keras.Model):
    def __init__(self, name=''):
        super(MedicalQAModel, self).__init__(name=name)
        self.q_ffn = FFN(name='QFFN', input_shape=(768,))
        self.a_ffn = FFN(name='AFFN', input_shape=(768,))

    def call(self, inputs):
        q_bert_embedding, a_bert_embedding = tf.unstack(inputs, axis=1)
        q_embedding, a_embedding = self.q_ffn(
            q_bert_embedding), self.a_ffn(a_bert_embedding)
        return tf.stack([q_embedding, a_embedding], axis=1)


class BioBert(tf.keras.Model):
    def __init__(self, name=''):
        super(BioBert, self).__init__(name=name)

    def call(self, inputs):

        # inputs is dict with input features
        input_ids, input_masks, segment_ids = inputs
        # pass to bert
        # with shape of (batch_size/2*batch_size, max_seq_len, hidden_size)
        # TODO(Alex): Add true bert model
        # Input: input_ids, input_masks, segment_ids all with shape (None, max_seq_len)
        # Output: a tensor with shape (None, max_seq_len, hidden_size)
        fake_bert_output = tf.expand_dims(tf.ones_like(
            input_ids, dtype=tf.float32), axis=-1)*tf.ones([1, 1, 768], dtype=tf.float32)
        max_seq_length = tf.shape(fake_bert_output)[-2]
        hidden_size = tf.shape(fake_bert_output)[-1]

        bert_output = tf.reshape(
            fake_bert_output, (-1, 2, max_seq_length, hidden_size))
        return bert_output


class MedicalQAModelwithBert(tf.keras.Model):
    def __init__(
            self,
            hidden_size=768,
            dropout=0.2,
            residual=True,
            activation=tf.keras.layers.ReLU(),
            name=''):
        super(MedicalQAModelwithBert, self).__init__(name=name)
        self.biobert = BioBert()
        self.q_ffn_layer = FFN(
            hidden_size=hidden_size,
            dropout=dropout,
            residual=residual,
            activation=activation)
        self.a_ffn_layer = FFN(
            hidden_size=hidden_size,
            dropout=dropout,
            residual=residual,
            activation=activation)

    def _avg_across_token(self, tensor):
        if tensor is not None:
            tensor = tf.reduce_mean(tensor, axis=1)
        return tensor

    def call(self, inputs):

        q_bert_embedding, a_bert_embedding = self.biobert(inputs)

        # according to USE, the DAN network average embedding across tokens
        q_bert_embedding = self._avg_across_token(q_bert_embedding)
        a_bert_embedding = self._avg_across_token(a_bert_embedding)

        q_embedding = self.q_ffn_layer(q_bert_embedding)
        a_embedding = self.a_ffn_layer(a_bert_embedding)

        return tf.stack([q_embedding, a_embedding], axis=1)



# def qa_pair_cross_entropy_loss(y_true, y_pred):
#     y_true = tf.eye(tf.shape(y_pred)[0])
#     q_embedding, a_embedding = tf.unstack(y_pred, axis=1)
#     similarity_matrix = tf.matmul(
#         q_embedding, a_embedding, transpose_b=True)
#     similarity_matrix_logits = tf.math.sigmoid(similarity_matrix)
#     return tf.keras.losses.categorical_crossentropy(y_true, similarity_matrix_logits, from_logits=True)

def qa_pair_cross_entropy_loss(y_true, y_pred):
    y_true = tf.eye(tf.shape(y_pred)[0])
    q_embedding, a_embedding = tf.unstack(y_pred, axis=1)
    similarity_matrix = tf.matmul(
        a = q_embedding, b = a_embedding, transpose_b=True)
    similarity_matrix_softmaxed = tf.nn.softmax(similarity_matrix)
    K.print_tensor(similarity_matrix_softmaxed, message="similarity_matrix_softmaxed is: ")
    return tf.keras.losses.categorical_crossentropy(y_true, similarity_matrix_softmaxed, from_logits=False)

#     y_true = tf.reshape(tf.eye(tf.shape(y_pred)[0])*2-1, (-1,))
#     q_embedding, a_embedding = tf.unstack(y_pred, axis=1)
#     similarity_matrix = tf.nn.softmax(tf.matmul(
#         q_embedding, a_embedding, transpose_b=True))
#     similarity_vector = tf.reshape(similarity_matrix, (-1, 1))
#     return tf.nn.softmax_cross_entropy_with_logits(similarity_vector, y_true)

#to try, with and without softmax
# catagorical cross entropy vs binary cross entropy
#with and without sigmoid pre transformation
#1 layer vs 2 layer

#prioritize what he said. so softmax, then catagorical vs binary


#%%
# training config
batch_size = 128
num_epochs=35
learning_rate=0.0001
validation_split=0.2
shuffle_buffer=50000
prefetch=50000
data_path='/content/gdrive/My Drive/mqa_tf_record'
model_path = '/content/gdrive/My Drive/mqa_models/ffn_model_cross_entropy'


#%%
d = create_dataset_for_ffn(
    data_path, batch_size=batch_size, shuffle_buffer=shuffle_buffer, prefetch=prefetch)
eval_d = create_dataset_for_ffn(
    data_path, batch_size=batch_size, mode='eval')
medical_qa_model = MedicalQAModel()
optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
medical_qa_model.compile(
    optimizer=optimizer, loss=qa_pair_cross_entropy_loss)

epochs = num_epochs
loss_metric = tf.keras.metrics.Mean()

#   history = medical_qa_model.fit(d, epochs=epochs, validation_data=eval_d)


#%%

model_path2 = '/content/gdrive/My Drive/mqa_models/ffn_model_cross_entropy.ckpt'

checkpoint = tf.keras.callbacks.ModelCheckpoint(model_path2, monitor='loss', verbose=1, save_best_only=True)


#%%
checkpoint_dir = os.path.dirname(model_path2)
print(checkpoint_dir)


#%%
medical_qa_model.load_weights(model_path2)


#%%
history = medical_qa_model.fit(d, epochs=80, validation_data=eval_d,  callbacks=[checkpoint])


#%%
import matplotlib.pyplot as plt
# summarize history for accuracy
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


#%%
input_data = next(iter(d))
print('input data is ', input_data)


#%%
K.set_learning_phase(0)

input_data = next(iter(d))[0]
print('input data is ', input_data)


q_embedding, a_embedding = tf.unstack(medical_qa_model(input_data), axis=1)

q_embedding = q_embedding / tf.norm(q_embedding, axis=-1, keepdims=True)
a_embedding = a_embedding / tf.norm(a_embedding, axis=-1, keepdims=True)

print('q_embedding', q_embedding)
print('a_embedding', a_embedding)

batch_score = tf.reduce_sum(q_embedding*a_embedding, axis=-1)
baseline_score = tf.reduce_mean(tf.matmul(q_embedding,tf.transpose(a_embedding)))

print('Training Batch Cos similarity')
print(tf.reduce_mean(batch_score))
print('Baseline: {0}'.format(baseline_score))


#%%
eval_d = create_dataset_for_ffn(data_dir='/content/gdrive/My Drive/mqa-biobert', mode='eval', batch_size=64)
q_embedding, a_embedding = medical_qa_model(next(iter(eval_d)))

q_embedding = q_embedding / tf.norm(q_embedding, axis=-1, keepdims=True)
a_embedding = a_embedding / tf.norm(a_embedding, axis=-1, keepdims=True)

batch_score = tf.reduce_sum(q_embedding*a_embedding, axis=-1)
baseline_score = tf.reduce_mean(tf.matmul(q_embedding,tf.transpose(a_embedding)))

print('Eval Batch Cos similarity')
print(tf.reduce_mean(batch_score))
print('Baseline: {0}'.format(baseline_score))


#%%
d = create_dataset_for_ffn(
  data_path, batch_size=batch_size, shuffle_buffer=shuffle_buffer, prefetch=prefetch)
eval_d = create_dataset_for_ffn(
  data_path, batch_size=batch_size, mode='eval')

# save arrays
from itertools import chain

q_embedding_list = []
a_embedding_list = []

for feature_dict in chain(iter(d), iter(eval_d)):
  q_embedding, a_embedding = tf.unstack(medical_qa_model(feature_dict[0]), axis=1)

  q_embedding_list.append(q_embedding / tf.norm(q_embedding, axis=-1, keepdims=True))
  a_embedding_list.append(a_embedding / tf.norm(a_embedding, axis=-1, keepdims=True))


#%%
result_path = '/content/gdrive/My Drive/mqa_ffn_results/'
os.makedirs(result_path, exist_ok=True)
np.save(os.path.join(result_path, 'q_embedding.npz'), np.concatenate(q_embedding_list, axis=0))


np.save(os.path.join(result_path, 'a_embedding.npz'), np.concatenate(a_embedding_list, axis=0) )



#%%
# medical_qa_model.save_weights(model_path)


