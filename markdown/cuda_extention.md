
### TORCH.UTILS.CPP_EXTENSION

为了方便编写pytorch的扩展，pytorch提供了`CppExtension`和`CUDAExtension`两部分。

>torch.utils.cpp_extension.CppExtension(name, sources, *args, **kwargs)

创建pytorch的C++扩展。
更方便的创建`setuptools.Extension`，可以使用最少（但通常是足够的）参数来构建 C++ 扩展。

**示例**
```python
>>> from setuptools import setup
>>> from torch.utils.cpp_extension import BuildExtension, CppExtension
>>> setup(
        name='extension',
        ext_modules=[
            CppExtension(
                name='extension',
                sources=['extension.cpp'],
                extra_compile_args=['-g']),
        ],
        cmdclass={
            'build_ext': BuildExtension
        })
```

>torch.utils.cpp_extension.CUDAExtension(name, sources, *args, **kwargs)

创建cuda/c++扩展。

```python
>>> from setuptools import setup
>>> from torch.utils.cpp_extension import BuildExtension, CUDAExtension
>>> setup(
        name='cuda_extension',
        ext_modules=[
            CUDAExtension(
                    name='cuda_extension',
                    sources=['extension.cpp', 'extension_kernel.cu'],
                    extra_compile_args={'cxx': ['-g'],
                                        'nvcc': ['-O2']})
        ],
        cmdclass={
            'build_ext': BuildExtension
        })
```
>torch.utils.cpp_extension.BuildExtension(*args, **kwargs)

自定义setuptools构建扩展。

这个`setuptools.build_ext`子类负责传递最小的必需编译器标志（例如`-std = c ++ 11`）以及混合`C++ / CUDA`编译。
使用`BuildExtension`时，允许为`extra_compile_args`（不是list）提供字典形式的参数，该字典从语言（cxx或cuda）映射到要提供给编译器的其他编译器标志的list。

这使得在混合编译期间可以向C++和CUDA编译器提供不同的标志。




>torch.utils.cpp_extension.load(name, sources, extra_cflags=None, extra_cuda_cflags=None, extra_ldflags=None, extra_include_paths=None, build_directory=None, verbose=False, with_cuda=None, is_python_module=True)

TODO
Loads a PyTorch C++ extension just-in-time (JIT).

>torch.utils.cpp_extension.load_inline(name, cpp_sources, cuda_sources=None, functions=None, extra_cflags=None, extra_cuda_cflags=None, extra_ldflags=None, extra_include_paths=None, build_directory=None, verbose=False, with_cuda=None, is_python_module=True)

>torch.utils.cpp_extension.include_paths(cuda=False)

获得必须的include路径。
**参数**
cuda – 如果是 `True`， 包含的是cuda路径。

**返回值**
include路径（list）

>torch.utils.cpp_extension.check_compiler_abi_compatibility(compiler)

检查ABI兼容性

>torch.utils.cpp_extension.verify_ninja_availability()

ninga 可用时候返回`True`




---
ref:
1. https://oldpan.me/archives/pytorch-combine-c-and-cuda
2. https://oldpan.me/archives/pytorch-cuda-c-plus-plus
3. https://www.cnblogs.com/jermmyhsu/p/10962987.html
4.
