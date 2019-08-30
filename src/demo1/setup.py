# -*- coding: UTF-8 -*-
# setup.py
# @author wanger
# @description
# @created 2019-08-28T10:19:49.664Z+08:00
# @last-modified 2019-08-29T22:38:32.528Z+08:00
#

from setuptools import setup
import os
import glob
from torch.utils.cpp_extension import BuildExtension, CppExtension

root_dir = os.path.dirname(os.path.abspath(__file__))
# 头文件目录
include_dirs = os.path.join(root_dir, 'src', 'include')
cpu_dirs     = os.path.join(root_dir, 'src', 'cpu')
gpu_dirs     = os.path.join(root_dir, 'src', 'gpu')

# 源代码目录
source_cpu = glob.glob(os.path.join(cpu_dirs, '*.cpp'))
source_gpu = glob.glob(os.path.join(gpu_dirs, '*.cu'))

# CppExtension是setuptools.Extension的一个便利的包装器（wrapper），
# 它传递正确的包含路径并将扩展语言设置为 C++
# BuildExtension执行许多必需的配置步骤和检查，并在混合 C++/CUDA
# 扩展的情况下管理混合编译。 这就是我们现在真正需要了解的关于构建
# C++ 扩展的所有内容！现在让我们来看看我们的 C++ 扩展的实现，
# 它扩展到了 *.cpp中。

setup(
    name='test_cpp',  # 模块名称，需要在python中调用
    version="0.1",
    ext_modules=[
        CppExtension('test_cpp', sources=source_cpu, include_dirs=[include_dirs]),
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
