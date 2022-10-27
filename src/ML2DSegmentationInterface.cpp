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

}