#ifndef ML2DSEGMENTATIONINTERFACE_H
#define ML2DSEGMENTATIONINTERFACE_H

#include <string>
#include <iostream>

class ML2DSegmentationInterface 
{
public:
    static ML2DSegmentationInterface* getInstance(std::string network_type);

private:
    ML2DSegmentationInterface(std::string network_type);

    static ML2DSegmentationInterface* instance;
};

#endif // ML2DSEGMENTATIONINTERFACE_H