#!/bin/bash

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX=/home/luca/repositories/ML2DSegmentation-install ..

make 
make install