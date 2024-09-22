#include "particle_managerPLK1.h"
#include "particlePLK13D.h"
#include <thread>
#include <boost/python.hpp>



typedef std::vector<double> MyList;



particle3D_managerPLK1::particle3D_managerPLK1(){
    
}


particle3D_managerPLK1::particle3D_managerPLK1(int particles){
    
    gen.seed(std::random_device()());

    for(unsigned int i=0; i<particles;  i++ ){
        
        list_of_particles.push_back(new particlePLK13D(&gen));
        
    }
    
}

particle3D_managerPLK1::~particle3D_managerPLK1(){
    
    
}

void particle3D_managerPLK1::Shuffle(boost::python::list& list){

   std::vector<double> temp;
   for(unsigned int i=0; i<len(list);  i++ ){
        
       temp.push_back(boost::python::extract<double>(list[i])); 
    }
    double limits [2][3] = {{temp[0],temp[1],temp[2]},{temp[3],temp[4],temp[5]}};
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        list_of_particles[i]->Shuffle(limits);
        
    }
}

void particle3D_managerPLK1::Move(double v0, double v1, double v2, double dt, boost::python::list& list_ratio, boost::python::list& listid0, boost::python::list& listid1, boost::python::list& list_limits, bool nobound, int time){
    
	
    
    std::vector<std::thread> thrs;

    std::vector<double> temp_ratio;
    for(unsigned int i=0; i<len(list_ratio);  i++ ){
        
        temp_ratio.push_back(boost::python::extract<double>(list_ratio[i]));
    }
    
    std::vector<double> temp_list_limits;
    for(unsigned int i=0; i<len(list_limits);  i++ ){
        
       temp_list_limits.push_back(boost::python::extract<double>(list_limits[i])); 
    }
    
    std::vector<double> con_vec_id0;
    for(unsigned int i=0; i<len(listid0);  i++ ){
        
        con_vec_id0.push_back(boost::python::extract<double>(listid0[i]));
    }
    
    std::vector<double> con_vec_id1;
    for(unsigned int i=0; i<len(listid1);  i++ ){
        
        con_vec_id1.push_back(boost::python::extract<double>(listid1[i]));
    }
    
    double limits [2][3] = {{temp_list_limits[0],temp_list_limits[1],temp_list_limits[2]},{temp_list_limits[3],temp_list_limits[4],temp_list_limits[5]}};

    // Create a function object
    
    
    
    for (unsigned id=0; id<5; id++) { // Change the id limit to increase the number of threads
        
        std::thread th = std::thread([&, id](){
            
            for(unsigned int i=list_of_particles.size()/5*id; i<list_of_particles.size()/5*(id+1);  i++ ){
                
                list_of_particles[i]->Move( v0,  v1, v2, dt, temp_ratio, con_vec_id0, con_vec_id1, limits,  nobound, time);
                
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

std::vector<double> particle3D_managerPLK1::GetXpos(){
    
    std::vector<double> Xpos;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        Xpos.push_back(list_of_particles[i]->GetXpos());
        
    }
    
    return Xpos;
}

std::vector<double> particle3D_managerPLK1::GetYpos(){
    
    std::vector<double> Ypos;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        Ypos.push_back(list_of_particles[i]->GetYpos());
        
    }
    
    return Ypos;
}

std::vector<double> particle3D_managerPLK1::GetZpos(){
    
    std::vector<double> Zpos;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        Zpos.push_back(list_of_particles[i]->GetZpos());
        
    }
    
    return Zpos;
}

std::vector<double> particle3D_managerPLK1::GetID(){
    
    std::vector<double> ID_list;
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        ID_list.push_back(list_of_particles[i]->GetID());
        
    }
    
    return ID_list;
}

std::vector<double> particle3D_managerPLK1::vec(){
	std::vector<double> ff;
	ff.push_back(1);
	ff.push_back(1);
	ff.push_back(1);
	return ff;
}

void particle3D_managerPLK1::SetSettings(float k_to_slow_, float k_to_fast_, float k_decay_, float plk1_detached_when_MEXp_changes_, float plk1_delay_start_time_, float plk1_delay_end_time_){
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        list_of_particles[i]->SetSettings(k_to_slow_, k_to_fast_, k_decay_, plk1_detached_when_MEXp_changes_, plk1_delay_start_time_, plk1_delay_end_time_);
        
    }
    
}

void particle3D_managerPLK1::MEXpSetSettings(float k_fast_slow_, float k_slow_fast_low_, float k_slow_fast_high_){
    
    for(unsigned int i=0; i<list_of_particles.size();  i++ ){
        
        list_of_particles[i]->MEXpSetSettings(k_fast_slow_,  k_slow_fast_low_,  k_slow_fast_high_);
        
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

BOOST_PYTHON_MODULE(particle3D_managerPLK1)
{
   

    class_<MyList>("MyList")
        .def(vector_indexing_suite<MyList>() );

 class_<particle3D_managerPLK1>("particle3D_managerPLK1", init<int>())
    .def("Move", &particle3D_managerPLK1::Move)
    .def("Shuffle", &particle3D_managerPLK1::Shuffle)
    .def("GetXpos", &particle3D_managerPLK1::GetXpos)
    .def("GetYpos", &particle3D_managerPLK1::GetYpos)
    .def("GetZpos", &particle3D_managerPLK1::GetZpos)
    .def("GetID", &particle3D_managerPLK1::GetID)
    .def("vec", &particle3D_managerPLK1::vec)
    .def("SetSettings", &particle3D_managerPLK1::SetSettings)
    .def("MEXpSetSettings", &particle3D_managerPLK1::MEXpSetSettings)

    ;
}
