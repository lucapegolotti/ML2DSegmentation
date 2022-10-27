#ifndef ML2DSEGMENTATIONINTERFACE_H
#define ML2DSEGMENTATIONINTERFACE_H

#include <Python.h>
#include <string>
#include <iostream>

class ML2DSegmentationInterface 
{
public:
    static ML2DSegmentationInterface* getInstance(std::string network_type);

private:
    ML2DSegmentationInterface(std::string network_type);
    static ML2DSegmentationInterface* instance;

    PyObject* py_wrapper_mod;
    PyObject* py_wrapper_class;
    PyObject* py_wrapper_inst;
};

#endif // ML2DSEGMENTATIONINTERFACE_H