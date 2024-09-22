#include "particle_manager.h"
#include "particle3D.h"
#include <thread>
#include <boost/python.hpp>



typedef std::vector<double> MyList;



particle3D_manager::particle3D_manager(){
    
}


particle3D_manager::particle3D_manager(int particles){
    
    gen.seed(std::random_device()());

    for(unsigned int i=0; i<particles;  i++ ){
        
        list_of_particles.push_back(new particle3D(&gen));
        
    }

}

particle3D_manager::~particle3D_manager(){
    
    
}

void particle3D_manager::Shuffle(boost::python::list& list){

   std::vector<double> temp;
   for(unsigned int i=0; i<len(list);  i++ ){
        
       temp.push_back(boost::python::extract<double>(list[i])); 
    }
    double limits [2][3] = {{temp[0],temp[1],temp[2]},{temp[3],temp[4],temp[5]}};
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        list_of_particles[i]->Shuffle(limits);
        
    }
}

void particle3D_manager::Move(double v0, double v1, double dt, boost::python::list& list, bool nobound, double t){
    
	
   std::vector<double> temp;
    
    std::vector<std::thread> thrs;

   for(unsigned int i=0; i<len(list);  i++ ){
        
       temp.push_back(boost::python::extract<double>(list[i])); 
    }
    
    double limits [2][3] = {{temp[0],temp[1],temp[2]},{temp[3],temp[4],temp[5]}};

    // Create a function object
    
    
    
    for (unsigned id=0; id<5; id++) {
        
        std::thread th = std::thread([&, id](){
            
            for(unsigned int i=list_of_particles.size()/5*id; i<list_of_particles.size()/5*(id+1);  i++ ){
                
                list_of_particles[i]->Move( v0,  v1,  dt,  limits,  nobound, t);
                
            }});
        thrs.push_back(std::move(th));
    }

    
    for (std::thread & th : thrs)
    {
        // If thread Object is Joinable then Join that thread.
        if (th.joinable())
        th.join();
    }
    
//    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
//
//        list_of_particles[i]->Move( v0,  v1,  dt,  limits,  nobound);
//
//    }
}

std::vector<double> particle3D_manager::GetXpos(){
    
    std::vector<double> Xpos;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        Xpos.push_back(list_of_particles[i]->GetXpos());
        
    }
    
    return Xpos;
}

std::vector<double> particle3D_manager::GetYpos(){
    
    std::vector<double> Ypos;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        Ypos.push_back(list_of_particles[i]->GetYpos());
        
    }
    
    return Ypos;
}

std::vector<double> particle3D_manager::GetZpos(){
    
    std::vector<double> Zpos;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        Zpos.push_back(list_of_particles[i]->GetZpos());
        
    }
    
    return Zpos;
}

std::vector<double> particle3D_manager::GetID(){
    
    std::vector<double> ID_list;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        ID_list.push_back(list_of_particles[i]->GetID());
        
    }
    
    return ID_list;
}

std::vector<double> particle3D_manager::vec(){
	std::vector<double> ff;
	ff.push_back(1);
	ff.push_back(1);
	ff.push_back(1);
	return ff;
}

void particle3D_manager::SetSettings(float initial_slow, float initial_fast, float k_fast_slow, float k_slow_fast_low, float k_slow_fast_high){
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        list_of_particles[i]->SetSettings(initial_slow, initial_fast, k_fast_slow, k_slow_fast_low, k_slow_fast_high);
        
    }
    
}
//namespace py = boost::python;
//
//py::list std_vector_to_py_list(const std::vector<T>& v)
//{
//    py::object get_iter = py::iterator<std::vector<T> >();
//    py::object iter = get_iter(v);
//    py::list l(iter);
//    return l;
//}

#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace boost::python;

BOOST_PYTHON_MODULE(particle3D_manager)
{
   

    class_<MyList>("MyList")
        .def(vector_indexing_suite<MyList>() );

 class_<particle3D_manager>("particle3D_manager", init<int>())
    .def("Move", &particle3D_manager::Move)
    .def("Shuffle", &particle3D_manager::Shuffle)
    .def("GetXpos", &particle3D_manager::GetXpos)
    .def("GetYpos", &particle3D_manager::GetYpos)
    .def("GetZpos", &particle3D_manager::GetZpos)
    .def("GetID", &particle3D_manager::GetID)
    .def("vec", &particle3D_manager::vec)
    .def("SetSettings", &particle3D_manager::SetSettings)

    ;
}
