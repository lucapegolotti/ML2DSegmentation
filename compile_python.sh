#!/bin/bash

rm -r -f python-install

CURDIR=$(pwd)
PYTHONINSTALL=$CURDIR/python-install

git clone https://github.com/python-cmake-buildsystem/python-cmake-buildsystem

cd python-cmake-buildsystem
mkdir build
cd build
      # -DWITH_STATIC_DEPENDENCIES=ON \
cmake -DCMAKE_INSTALL_PREFIX=$PYTHONINSTALL \
      -DPYTHON_VERSION=3.9.10 \
      -DBUILD_LIBPYTHON_SHARED:BOOL=ON \
      -DCMAKE_INSTALL_RPATH:PATH=$CURDIR/python-install/lib:$CURDIR/python-install/lib/python3.9/lib-dynload/ \
      ..
make install

rm -r -f $CURDIR/python-cmake-buildsystem

cd $PYTHONINSTALL/bin

# this may be necessary to import torch in the newly installed python
# sudo apt-get install libffi-dev

wget https://bootstrap.pypa.io/get-pip.py
./python get-pip.py
# ./python -s -m ensurepip --default
REPLACEME_SV_TOP_BIN_DIR_PYTHON/bin/pip cache purge
./python -m pip install Cython --install-option="--no-cython-compile"
./python -m pip install numpy
./python -m pip install torch
./python -m pip install pyyaml
./python -m pip install vtk
./python -m pip install opencv-python
./python -m pip install scipy