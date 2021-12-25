#!/usr/bin/env python3

#####################################################################
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Kenta Yonekura (a.k.a. yoneken),
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

THIS_PACKAGE = "rosserial_stm32"

__usage__ = """
make_libraries.py generates the STM32 rosserial library files for SW4STM32.
It requires the location of your SWSTM32 project folder.

rosrun rosserial_stm32 make_libraries.py <stm32_proj_path>
"""

import rospkg
import rosserial_client
from rosserial_client.make_library import *

# for copying files
import shutil

ROS_TO_EMBEDDED_TYPES = {
    "bool": ("bool", 1, PrimitiveDataType, []),
    "byte": ("int8_t", 1, PrimitiveDataType, []),
    "int8": ("int8_t", 1, PrimitiveDataType, []),
    "char": ("uint8_t", 1, PrimitiveDataType, []),
    "uint8": ("uint8_t", 1, PrimitiveDataType, []),
    "int16": ("int16_t", 2, PrimitiveDataType, []),
    "uint16": ("uint16_t", 2, PrimitiveDataType, []),
    "int32": ("int32_t", 4, PrimitiveDataType, []),
    "uint32": ("uint32_t", 4, PrimitiveDataType, []),
    "int64": ("int64_t", 8, PrimitiveDataType, []),
    "uint64": ("uint64_t", 8, PrimitiveDataType, []),
    "float32": ("float", 4, PrimitiveDataType, []),
    "float64": ("double", 8, PrimitiveDataType, []),
    "time": ("ros::Time", 8, TimeDataType, ["ros/time"]),
    "duration": ("ros::Duration", 8, TimeDataType, ["ros/duration"]),
    "string": ("char*", 0, StringDataType, []),
    "Header": ("std_msgs::Header", 0, MessageDataType, ["std_msgs/Header"]),
}

# need correct inputs
if len(sys.argv) < 2:
    print(__usage__)
    exit()

# check if path is correct
if not os.path.exists(os.path.join(sys.argv[1], "Core", "Inc")):
    print("\033[91m", "Path not existing: %s" % os.path.join(sys.argv[1], "Core", "Inc"), "\033[0m")
    exit()

# get output path
roslib_path = os.path.join("Core", "Inc", "ROSLib")
output_path = os.path.join(sys.argv[1], roslib_path)
print("\033[93m", "\nExporting to: %s" % output_path, "\033[0m")

rospack = rospkg.RosPack()
rosserial_stm32_dir = rospack.get_path(THIS_PACKAGE)

# copy ros library for STM32 hardware in
if os.path.exists(output_path):
    # delete duplicated folder
    print("\033[93m", "\nDelete old folder: %s" % output_path, "\033[0m")
    shutil.rmtree(output_path, ignore_errors=True)
shutil.copytree(os.path.join(rosserial_stm32_dir, "src", "ros_lib"), output_path)

# copy ros_lib stuff in
rosserial_client_copy_files(rospack, output_path)

# generate messages
rosserial_generate(rospack, output_path, ROS_TO_EMBEDDED_TYPES)

# Move '*.cpp' files in 'Src/' folder:
cppfiles = [files for files in os.listdir(output_path) if files.endswith(".cpp")]
stmsrc_path = os.path.normpath(os.path.join(output_path, "..", "..", "Src"))
if os.path.exists(stmsrc_path):
    os.makedirs(os.path.join(stmsrc_path, "ROSLib"))
    for file in cppfiles:
        shutil.move(os.path.join(output_path, file), os.path.join(stmsrc_path, "ROSLib"))
else:
    print("\033[91m", "Path not existing: %s\n Source files are not moved" % stmsrc_path, "\033[0m")
    exit()
