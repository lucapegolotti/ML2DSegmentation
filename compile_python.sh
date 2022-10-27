#!/bin/bash

rm python-install

CURDIR=$(pwd)
PYTHONINSTALL=$CURDIR/python-install

git clone https://github.com/python-cmake-buildsystem/python-cmake-buildsystem

cd python-cmake-buildsystem
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$PYTHONINSTALL \
      -DWITH_STATIC_DEPENDENCIES=ON \
      ..
make install

rm -r -f $CURDIR/python-cmake-buildsystem

cd $PYTHONINSTALL/bin

# this may be necessary to import torch in the newly installed python
# sudo apt-get install libffi-dev

wget https://bootstrap.pypa.io/get-pip.py
./python get-pip.py
./python -m pip install torch

