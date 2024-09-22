#ifndef particle3D_manager_header
#define particle3D_manager_header

#include<iostream>
#include "particlePLK13D.h"
#include <boost/python.hpp>

typedef std::vector<double> MyList;

class particle3D_managerPLK1{
    
    public:
    particle3D_managerPLK1();
    particle3D_managerPLK1(int particles);
    ~particle3D_managerPLK1();
    
    void Move(double, double, double, double, boost::python::list&, boost::python::list&, boost::python::list&, boost::python::list&, bool, int);
    //void Shuffle(double a[][3]);

    void Shuffle(boost::python::list& );
    std::vector<double> GetXpos();
    std::vector<double> GetYpos();
    std::vector<double> GetZpos();
    std::vector<double> GetID();

    std::vector<double> vec();
    
    void SetSettings(float, float, float, float, float, float );
    void MEXpSetSettings(float, float, float );

    private:
    std::vector<particlePLK13D*> list_of_particles;
    
    std::mt19937 gen;

};

#endif
