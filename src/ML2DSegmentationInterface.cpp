#include "ML2DSegmentationInterface.h"
#include <json.hxx>

using json = nlohmann::json;

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
    PyRun_SimpleString("import os");
    PyRun_SimpleString("print(os.path.dirname(sys.executable))");
    PyRun_SimpleString("import sv_ml.sv_wrapper");

    py_wrapper_mod = PyImport_ImportModule("sv_ml.sv_wrapper");
    if (py_wrapper_mod == NULL){
        std::cout << "error failed to import sv_wrapper module\n";
    }

    py_wrapper_class = PyObject_GetAttrString(py_wrapper_mod, "SVWrapper");
    if (py_wrapper_class == NULL){
        std::cout << "error SVWrapper class not loaded\n";
    }

    PyObject* pargs  = Py_BuildValue("(s)", network_type.c_str());
    if (pargs == NULL){
        std::cout << "error SVWrapper args not loaded\n";
    }

    py_wrapper_inst  = PyEval_CallObject(py_wrapper_class, pargs);
    if (py_wrapper_inst == NULL){
      std::cout << "error SVWrapper instance not loaded\n";
    }

    Py_DECREF(pargs);
}

std::vector<std::vector<double>> ML2DSegmentationInterface::segmentPathPoint(double pos[3], double tangent[3], double rotation[3]){

  std::vector<std::vector<double>> empty_points;

  json msg;
  msg["p"]     = {pos[0], pos[1], pos[2]};
  msg["tx"]    = {tangent[0], tangent[1], tangent[2]};
  msg["n"]     = {rotation[0], rotation[1], rotation[2]};

  std::string msg_string = msg.dump();

  PyObject* py_res = PyObject_CallMethod(py_wrapper_inst, "segment",
                        "s", msg_string.c_str());

  if (py_res == NULL){
    std::cout << "Error calling sv_wrapper.segment\n";
    return empty_points;
  }

  char* cstr;
  bool parse_success = PyArg_Parse(py_res, "s", &cstr);
  if(!parse_success){
    std::cout << "Error parsing return result of sv_wrapper.segment\n";
    return empty_points;
  }

  std::string result = std::string(cstr);

  //std::cout << "result " << result << "\n";

  if (result == ""){
    std::cout << "Error segmenting, sv_wrapper returned null\n";
    return empty_points;
  }

  json result_json = json::parse(result);
  std::vector<std::vector<double>> points = result_json["points"];

  return points;
}