from __future__ import annotations

import numpy as np
from src.NN.function import Function
from enum import Enum, auto


class PaddingType(Enum):
    SAME = auto()
    VALID = auto()


class MaxPool2D(Function):
    def __init__(self, kernelSize, strides, padding=PaddingType.SAME, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(kernelSize, int):
            kernelSize = (kernelSize, kernelSize)
        if isinstance(strides, int):
            strides = (strides, strides)
        # General format (x,y)
        self.kernelSize: tuple = kernelSize
        # General format (x,y)
        self.strides: tuple = strides
        self.padding: PaddingType = padding

    def __call__(self, x, *args, **kwargs):
        return self._forward(x)

    def _forward(self, x, *args, **kwargs):
        # numOfBatches, numOfChannels, height, width = x.shape
        height, width = x.shape
        # Calculate the size of the output
        # ouputSize = (0, 0)
        # padding = (0, 0)
        # newInput = None
        if self.padding == PaddingType.VALID:
            outputHeight = (height - self.kernelSize[0]) // self.strides[0] + 1
            outputWidth = (width - self.kernelSize[1]) // self.strides[1] + 1
            outputSize = (outputHeight, outputWidth)
            newInput = x
        else:
            outputSize = (height, width)
            paddingHeight = ((self.strides[0] - 1) * height - self.strides[0] + self.kernelSize[0]) // 2
            paddingWidth = ((self.strides[1] - 1) * width - self.strides[1] + self.kernelSize[1]) // 2
            newInput = np.zeros(outputSize)
            newInput[paddingHeight:paddingWidth + height, paddingWidth:paddingWidth + width] = x
        output = np.zeros(outputSize)
        outputHeight = outputSize[0]
        outputWidth = outputSize[1]
        for i in range(outputHeight):
            for j in range(outputWidth):
                heightStart = i * self.strides[0]
                heightEnd = heightStart + self.strides[0]
                widthStart = j * self.strides[1]
                widthEnd = widthStart + self.strides[1]
                output[i][j] = np.max(newInput[heightStart:heightEnd, widthStart:widthEnd])


class AvgPool2D(Function):
    def __init__(self, kernelSize, strides, padding=PaddingType.SAME, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(kernelSize, int):
            kernelSize = (kernelSize, kernelSize)
        if isinstance(strides, int):
            strides = (strides, strides)
        # General format (x,y)
        self.kernelSize: tuple = kernelSize
        # General format (x,y)
        self.strides: tuple = strides
        self.padding: PaddingType = padding

    def __call__(self, x, *args, **kwargs):
        return self._forward(x)

    def forward(self, x):
        # numOfBatches, numOfChannels, height, width = x.shape
        height, width = x.shape
        # Calculate the size of the output
        # ouputSize = (0, 0)
        # padding = (0, 0)
        # newInput = None
        if self.padding == PaddingType.VALID:
            outputHeight = (height - self.kernelSize[0]) // self.strides[0] + 1
            outputWidth = (width - self.kernelSize[1]) // self.strides[1] + 1
            outputSize = (outputHeight, outputWidth)
            newInput = x
        else:
            outputSize = (height, width)
            paddingHeight = ((self.strides[0] - 1) * height - self.strides[0] + self.kernelSize[0]) // 2
            paddingWidth = ((self.strides[1] - 1) * width - self.strides[1] + self.kernelSize[1]) // 2
            newInput = np.zeros(outputSize)
            newInput[paddingHeight:paddingWidth + height, paddingWidth:paddingWidth + width] = x
        output = np.zeros(outputSize)
        outputHeight = outputSize[0]
        outputWidth = outputSize[1]
        for i in range(outputHeight):
            for j in range(outputWidth):
                heightStart = i * self.strides[0]
                heightEnd = heightStart + self.strides[0]
                widthStart = j * self.strides[1]
                widthEnd = widthStart + self.strides[1]
                output[i][j] = np.average(newInput[heightStart:heightEnd, widthStart:widthEnd])
