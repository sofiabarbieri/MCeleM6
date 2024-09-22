cmake_minimum_required(VERSION 3.1)


option(Boost_DEBUG "Set to ON to enable debug output from FindBoost." ON)
option(Boost_DETAILED_FAILURE_MSG "Set to ON to get detailed information" ON)

FIND_PACKAGE(PythonInterp)

if (PYTHONINTERP_FOUND)
  if (UNIX AND NOT APPLE)
      FIND_PACKAGE(Boost COMPONENTS python)
      FIND_PACKAGE(PythonInterp)
      FIND_PACKAGE(PythonLibs REQUIRED)
  else()	
       message("Only UNIX NO-APPLE is supported")
  endif()
else()
    message("Python not found")
endif()


message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")

SET(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/install CACHE PATH "install path" FORCE)

set (CMAKE_CXX_STANDARD 11)


ENABLE_TESTING()
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
LINK_LIBRARIES(${Boost_LIBRARIES} ${PYTHON_LIBRARIES}) # Deprecated but so convenient!

ADD_SUBDIRECTORY(src)
ADD_SUBDIRECTORY(python)

