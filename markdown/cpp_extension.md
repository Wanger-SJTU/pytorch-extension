
在 PyTorch 中扩展 C++/CUDA 主要分为几步：

- 安装好 `pybind11` 模块（通过 `pip` 或者 `conda` 等安装，[源码安装](./pybind11.md)），这个模块会负责 `python` 和 C++ 之间的绑定；
- 用 C++ 写好自定义层的功能，包括前向传播forward和反向传播backward；
- 写好 `setup.py`，并用 python 提供的`setuptools`来编译并加载 C++ 代码。
- 编译安装，在 python 中调用 C++ 扩展接口。

接下来，我们就用一个简单的例子（z=2x+y）来演示这几个步骤。

**第一步**
我们先写好 C++ 相关的文件：

头文件` test.h`
```cpp
#include <torch/extension.h>
#include <vector>

// 前向传播
torch::Tensor Test_forward_cpu(const torch::Tensor& inputA,
                            const torch::Tensor& inputB);
// 反向传播
std::vector<torch::Tensor> Test_backward_cpu(const torch::Tensor& gradOutput);
```
注意，这里引用的`<torch/extension.h>`头文件至关重要，它主要包括三个重要模块：

- `pybind11`，用于 `C++` 和 `python` 交互；
- `ATen`，包含 `Tensor` 等重要的函数和类；
- 一些辅助的头文件，用于实现 `ATen` 和 `pybind11` 之间的交互。

源文件 `test.cpp` 如下：

```cpp
#include "test.h"

// 前向传播，两个 Tensor 相加。这里只关注 C++ 扩展的流程，具体实现不深入探讨
torch::Tensor Test_forward_cpu(const torch::Tensor& x,  const torch::Tensor& y) {
    AT_ASSERTM(x.sizes() == y.sizes(), "x must be the same size as y");
    torch::Tensor z = torch::zeros(x.sizes());
    z = 2 * x + y;
    return z;
}

// 反向传播
// 在这个例子中，z对x的导数是2，z对y的导数是1。
// 至于这个backward函数的接口（参数，返回值）为何要这样设计，后面会讲。
std::vector<torch::Tensor> Test_backward_cpu(const torch::Tensor& gradOutput) {
    torch::Tensor gradOutputX = 2 * gradOutput * torch::ones(gradOutput.sizes());
    torch::Tensor gradOutputY = gradOutput * torch::ones(gradOutput.sizes());
    return {gradOutputX, gradOutputY};
}

// pybind11 绑定
PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("forward", &Test_forward_cpu, "TEST forward");
  m.def("backward", &Test_backward_cpu, "TEST backward");
}
```

第二步
新建一个编译安装的配置文件 `setup.py`，文件目录安排如下：
```
└── csrc
    ├── cpu
    │   ├── test.cpp
    │   └── test.h
    └── setup.py
```
以下是 setup.py 中的内容：

```python
from setuptools import setup
import os
import glob
from torch.utils.cpp_extension import BuildExtension, CppExtension

# 头文件目录
include_dirs = os.path.dirname(os.path.abspath(__file__))
# 源代码目录
source_cpu = glob.glob(os.path.join(include_dirs, 'cpu', '*.cpp'))

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
```

注意，这个 C++ 扩展被命名为test_cpp，意思是说，在 python 中可以通过test_cpp模块来调用 C++ 函数。

**第三步**

在 cpu 这个目录下，执行下面的命令编译安装 C++ 代码：

`python setup.py install`

之后，可以看到一堆输出，该 C++ 模块会被安装在 python 的 site-packages 中。

完成上面几步后，就可以在 python 中调用 C++ 代码了。在 PyTorch 中，按照惯例需要先把 C++ 中的前向传播和反向传播封装成一个函数op（以下代码放在 test.py 文件中）：

```python
from torch.autograd import Function

import test_cpp

class TestFunction(Function):

    @staticmethod
    def forward(ctx, x, y):
        return test_cpp.forward(x, y)

    @staticmethod
    def backward(ctx, gradOutput):
        gradX, gradY = test_cpp.backward(gradOutput)
        return gradX, gradY
```
这样一来，我们相当于把 C++ 扩展的函数嵌入到 PyTorch 自己的框架内。


