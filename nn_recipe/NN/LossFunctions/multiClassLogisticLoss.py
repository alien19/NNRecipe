from .__loss_function import LossFunction
import numpy as np


class MClassLogisticLoss(LossFunction):
    def _compute_loss(self, Y, Y_hat):
        expZ = np.exp(Y_hat - np.max(Y_hat)) # softmax here is a row vector for each example
        self.__softmax_value = expZ / np.sum(expZ, axis=1).reshape(-1, 1)
        return -1*np.log(self.__softmax_value[0, np.argmax(Y.T, axis=1)].reshape(-1,1))

    def _compute_local_grad(self, Y, Y_Hat): #finally worked
        self.__softmax_value.T[np.argmax(Y, axis=0), range(self.__softmax_value.shape[0])] -= 1
        print(self.__softmax_value)
        return self.__softmax_value
