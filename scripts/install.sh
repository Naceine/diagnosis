#!/bin/bash

#To use CPU FAISS use
wget  https://anaconda.org/pytorch/faiss-cpu/1.2.1/download/linux-64/faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2

#To use GPU FAISS use
# wget  https://anaconda.org/pytorch/faiss-gpu/1.2.1/download/linux-64/faiss-gpu-1.2.1-py36_cuda9.0.176_1.tar.bz2

tar xvjf faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
cp -r lib/python3.6/site-packages/* /usr/local/lib/python3.6/dist-packages/

pip install mkl
pip install tensorflow-gpu==2.0.0-alpha0

pip install https://github.com/re-search/DocProduct/archive/v0.2.0_dev.zip
pip install https://github.com/re-search/gpt2-estimator/archive/master.zip
