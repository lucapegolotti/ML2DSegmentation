cmake_minimum_required(VERSION 3.12)
cmake_policy(SET CMP0074 NEW)
project(mylib VERSION 1.0.0 DESCRIPTION "Machine Learning Segmentation Plugin for SimVascular")

find_package(Python COMPONENTS Interpreter Development)

include_directories(${Python_INCLUDE_DIRS})

add_library(ml2dsegmentation STATIC
            src/ML2DSegmentationInterface.cpp)

set_target_properties(ml2dsegmentation PROPERTIES VERSION ${PROJECT_VERSION})
target_include_directories(ml2dsegmentation PRIVATE include)
target_link_libraries(ml2dsegmentation ${Python_LIBRARIES})
set_target_properties(ml2dsegmentation PROPERTIES PUBLIC_HEADER include/ML2DSegmentationInterface.h)

include(GNUInstallDirs)

install(TARGETS ml2dsegmentation
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# test 
include_directories(include)
add_executable(test test_main.cpp)
target_link_libraries(test ml2dsegmentation ${Python_LIBRARIES} ${Python_RUNTIME_LIBRARY_DIRS})
message(STATUS ${Python_RUNTIME_LIBRARY_DIRS})