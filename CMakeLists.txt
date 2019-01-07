cmake_minimum_required(VERSION 3.12)
project(CVATXMLParser C CXX)

include_directories("${PROJECT_BINARY_DIR}")
find_package(LibXml2 REQUIRED)



add_executable(CVATXMLParser main.cpp structures.cpp)

target_link_libraries(CVATXMLParser ${LIBXML2_LIBRARIES})
