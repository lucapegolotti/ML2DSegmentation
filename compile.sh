#!/bin/bash

CURDIR=$(pwd)

rm -r -f build
mkdir build
cd build


cmake \
    -DCMAKE_INSTALL_PREFIX=/home/luca/repositories/ML2DSegmentation-install \
    -DPython_ROOT_DIR=$CURDIR/python-install/ \
    ..

make 
make install