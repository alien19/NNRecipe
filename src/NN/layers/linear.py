from __future__ import annotations
import numpy as np
from src.NN.layers.layer import Layer
from src.NN.function import Function


class Linear(Layer):
    """
    This Class represents a Linear Layer (Dense - Fully connected)

    Linear Layer is responsible for:
        - Calculating the forward path              Z = W * X.T
        - Calculating activation of the layer       Y = Act(Z)
        - Calculating local gradients that will be used by the optimizers

    Gradient Calculated are:
        1. dW: ∂Y/∂Z * ∂Z/∂W = activation gradient * X
        2. dX: ∂Y/∂Z * ∂Z/∂X = activation gradient * W
        3. dB: ∂Y/∂Z * ∂Z/∂B = activation gradient * 1
    """
    def __init__(self, in_dim, out_dim, activation, batch_size=1, **kwargs):
        """
        Initializes the layer by calling base class constructor to create weights and bias and initialize them

        :param in_dim: number of neurons of the previous layer
        :type in_dim: int
        :param out_dim: number of neurons of the current layer
        :type out_dim: int
        :param activation: activation function that will be used
        :type activation: Function
        :param batch_size: batch size
        :type batch_size: int
        :keyword weights: Initial value for layer weights
        :keyword bias:  Initial value for layer bias

        :raise TypeError: When the given initial data doesn't have the expected type
        :raise ShapeError: When the given initial data doesn't have the expected shape

        """
        self.__activation = activation
        self.__batch_size = batch_size
        super(Linear, self).__init__(in_dim, out_dim, **kwargs)

    
    def _init_params(self):
        """
        Initializes layer parameters (weights and bias)

        Many different initialize schemes could be used:        # TODO add different init_factors that can be used (mar)
            -
            -
            -

        """
        factor = np.tanh(1/self._in_dim) # factor that will be used to normalize params
        self._weights = np.random.rand(self._out_dim, self._in_dim) * factor # init weights
        # TODO make initializing bias and weights with a pre defined values a feature
        self._bias = np.random.rand(self._out_dim, 1) * factor
        # self._bias = np.ones((self._out_dim, self.__batch_size)) # init bias

    def _forward(self, x):
        """
        Calculates forward path (W*X.t) then apply activation function
        :param x: input to the layer (output from the previous layer)
        :type x: np.ndarray
        :rtype: np.ndarray
        """
        # print("weights", self._weights.shape, "X", x.T.shape, "bias", self._bias.shape)
        return self.__activation(np.dot(self._weights, x.T) + self._bias).T

    def _calc_local_grad(self, x):
        """
        Local gradient calculations

        Gradient Calculated are:
            1. dW: ∂Z/∂W = X
            2. dX: ∂Z/∂X = W
            3. dZ: ∂Y/∂Z = activation gradient

        :note: No need to return ∂Z/∂B as it's always 1
        :param x: input to the layer (output from the previous layer)
        :type x: np.ndarray
        :rtype: dict[str, np.ndarray]
        """
        return {
            'dW': x,
            'dX': np.copy(self.weights),
            'dZ': self.__activation.local_grad
        }