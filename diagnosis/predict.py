from .models.docproduct.predictor import GenerateQADoc, RetreiveQADoc
from config.util import Log
"""Takes raw symptoms text and obtains appropriate diagnosis text.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Researcher.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: predict.py
     Package: diagnosis
     Created on 10 July, 2019 @ 02:19 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""
# import sys
# sys.path.append('..')

from config.util import Log
from config.consts import FS

from diagnosis.models.docproduct.predictor import GenerateQADoc, RetreiveQADoc


def generateQADoc(pretrained_path=FS.PRE_TRAINED.PUB_MED, ffn_weight_file=None,
                  bert_ffn_weight_file=FS.MODELS.BERT_FFN,
                  embedding_file=FS.EMBEDDINGS.BERT_FFN_PKL):

    doc = GenerateQADoc(pretrained_path=pretrained_path,
                        ffn_weight_file=None,
                        bert_ffn_weight_file=bert_ffn_weight_file,
                        embedding_file=embedding_file)
    Log.debug(doc.predict('my eyes hurts and i have a headache.',
                          search_by='answer', topk=5, answer_only=False))
    Log.debug(doc.predict('my eyes hurts and i have a headache.',
                          search_by='question', topk=5, answer_only=False))


def retrieveQADoc(pretrained_path=FS.PRE_TRAINED.PUB_MED, ffn_weight_file=None,
                  bert_ffn_weight_file=FS.MODELS.BERT_FFN,
                  embedding_file=FS.EMBEDDINGS.BERT_FFN_PKL):

    doc = RetreiveQADoc(pretrained_path=pretrained_path,
                        ffn_weight_file=None,
                        bert_ffn_weight_file=bert_ffn_weight_file,
                        embedding_file=embedding_file)

    Log.debug(doc.predict('my eyes hurts and i have a headache.',
                          search_by='answer', topk=5, answer_only=True))
    Log.debug(doc.predict('my eyes hurts and i have a headache.',
                          search_by='question', topk=5, answer_only=True))


if __name__ == '__main__':
    retrieveQADoc()
    generateQADoc()
