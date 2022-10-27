#include "ML2DSegmentationInterface.h"

ML2DSegmentationInterface* ML2DSegmentationInterface::instance = 0;

ML2DSegmentationInterface* ML2DSegmentationInterface::getInstance(std::string network_type)
{
    if (instance == 0)
    {
        instance = new ML2DSegmentationInterface(network_type);
    }
    std::cout << "Getting instance!" << std::endl << std::flush;
    return instance;
}

ML2DSegmentationInterface::ML2DSegmentationInterface(std::string network_type)
{
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("print(sys.path)");
    PyRun_SimpleString("print(sys.version)");

    // py_wrapper_mod = PyImport_ImportModule("sv_ml.sv_wrapper");
    // if (py_wrapper_mod == NULL){
    //     std::cout << "error failed to import sv_wrapper module\n";
    // }

    // py_wrapper_class = PyObject_GetAttrString(py_wrapper_mod, "SVWrapper");
    // if (py_wrapper_class == NULL){
    //     std::cout << "error SVWrapper class not loaded\n";
    // }

    // PyObject* pargs  = Py_BuildValue("(s)", network_type.c_str());
    // if (pargs == NULL){
    //     std::cout << "error SVWrapper args not loaded\n";
    // }

    // py_wrapper_inst  = PyEval_CallObject(py_wrapper_class, pargs);
    // if (py_wrapper_inst == NULL){
    //   std::cout << "error SVWrapper instance not loaded\n";
    // }

    // Py_DECREF(pargs);
}