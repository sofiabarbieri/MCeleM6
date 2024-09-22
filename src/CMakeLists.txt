INCLUDE_DIRECTORIES(../include)
PYTHON_ADD_MODULE(particle3D_manager particle3D.cpp particle_manager.cpp)
PYTHON_ADD_MODULE(particle3D_managerPLK1 particlePLK13D.cpp particle_managerPLK1.cpp)

install(TARGETS particle3D_manager LIBRARY DESTINATION .)
install(TARGETS particle3D_managerPLK1 LIBRARY DESTINATION .)
