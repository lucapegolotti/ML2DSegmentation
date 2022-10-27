cmake_minimum_required(VERSION 3.0)

project(mylib VERSION 1.0.0 DESCRIPTION "Machine Learning Segmentation Plugin for SimVascular")

include_directories(python-install/include/python3.9)

add_library(ml2dsegmentation SHARED
            src/ML2DSegmentationInterface.cpp)

set_target_properties(ml2dsegmentation PROPERTIES VERSION ${PROJECT_VERSION})
target_include_directories(ml2dsegmentation PRIVATE include)
set_target_properties(ml2dsegmentation PROPERTIES PUBLIC_HEADER include/ML2DSegmentationInterface.h)

include(GNUInstallDirs)

install(TARGETS ml2dsegmentation
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})