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


import torch

class Test(torch.nn.Module):

    def __init__(self):
        super(Test, self).__init__()

    def forward(self, inputA, inputB):
        return TestFunction.apply(inputA, inputB)
