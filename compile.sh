#!/bin/bash

CURDIR=$(pwd)

rm -r -f build
mkdir build
cd build

cmake \
    -DCMAKE_INSTALL_PREFIX=/home/luca/repositories/ML2DSegmentation-install \
    -DPython_ROOT_DIR=$CURDIR/python-install/ \
    -DPython3_EXECUTABLE=$CURDIR/python-install/bin/python \
    -DCMAKE_INSTALL_RPATH:PATH=$CURDIR/python-install/bin:$CURDIR/python-install/lib/ \
    ..

make VERBOSE=1
make install

cp -r $CURDIR/sv_ml $CURDIR/python-install/lib/python3.9/site-packages/