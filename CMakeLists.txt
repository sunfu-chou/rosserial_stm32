cmake_minimum_required(VERSION 2.8.3)
project(rosserial_stm32)

find_package(catkin REQUIRED COMPONENTS
  message_generation
)

generate_messages()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY
  src/ros_lib
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/src
)
