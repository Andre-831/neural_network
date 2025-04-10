import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
# *************************************************************** #
# This version of the neural network includes TWO hidden layers  #
# instead of ONE like the original version.                      #
#                                                               #
# Key Differences from the First Version:                       #
# ------------------------------------------------------------- #
# 1. Network Architecture:                                      #
#    - Original: Input -> Hidden (10 neurons) -> Output         #
#    - This version:                                            #
#      Input -> Hidden Layer 1 (64 neurons)                     #
#             -> Hidden Layer 2 (32 neurons)                    #
#             -> Output Layer (10 neurons)                     #
#                                                               #
# 2. Forward Propagation:                                       #
#    - Two activation steps using ReLU instead of one           #
#    - Additional matrix multiplications for second hidden layer#
#                                                               #
# 3. Backward Propagation:                                      #
#    - Extra gradient computations for the second hidden layer  #
#    - Chain rule is applied across both hidden layers          #
#                                                               #
# 4. Parameter Initialization:                                  #
#    - Additional weights and biases added for the new layer    #
#                                                               #
# Benefits:                                                     #
#    - Deeper network allows for more complex learning          #
#    - Typically results in higher training and validation acc. #
#                                                               #                                   #
# *************************************************************** #

#load the training data and shuffle it
data = pd.read_csv('train.csv')

data = np.array(data)
m, n = data.shape
np.random.shuffle(data)

# Split the data into training and validation sets
data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]


data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]

# Normalize pixel values to [0, 1]
X_train = X_train / 255.
X_dev = X_dev / 255.


#print(X_train[:,0].shape)

# Initialize parameters for the neural network for 3 layers
def init_params():
    W1 = np.random.rand(64, 784) - 0.5
    b1 = np.zeros((64, 1))
    W2 = np.random.rand(32, 64) - 0.5
    b2 = np.zeros((32, 1))
    W3 = np.random.rand(10, 32) - 0.5
    b3 = np.zeros((10, 1))
    return W1, b1, W2, b2, W3, b3

# ReLU activation function
# This function replaces negative values with zero

def ReLU(Z):
    return np.maximum(Z, 0)

# Softmax activation function
# This function converts the output layer into probabilities
def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A

# Forward propagation through all layers
def forward_prop(W1, b1, W2, b2, W3, b3, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = ReLU(Z2)
    Z3 = W3.dot(A2) + b3
    A3 = softmax(Z3)
    return Z1, A1, Z2, A2, Z3, A3

# ReLU derivative for backpropagation
# This function returns 1 for positive values and 0 for negative values
def ReLU_deriv(Z):
    return Z > 0

# Converts labels into one-hot encoded matrix
def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    one_hot_Y = one_hot_Y.T
    return one_hot_Y

# Backward propagation through all layers
def backward_prop(Z1, A1, Z2, A2, Z3, A3, W1, W2, W3, X, Y):
    one_hot_Y = one_hot(Y)
    dZ3 = A3 - one_hot_Y
    dW3 = 1 / m * dZ3.dot(A2.T)
    db3 = 1 / m * np.sum(dZ3, axis=1, keepdims=True)

    dZ2 = W3.T.dot(dZ3) * ReLU_deriv(Z2)
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)

    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)

    return dW1, db1, dW2, db2, dW3, db3

# Updates weights and biases using gradients from backpropagation  
# Applies gradient descent with the learning rate to minimize error
def update_params(W1, b1, W2, b2, W3, b3, dW1, db1, dW2, db2, dW3, db3, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1    
    W2 = W2 - alpha * dW2  
    b2 = b2 - alpha * db2   
    W3 = W3 - alpha * dW3
    b3 = b3 - alpha * db3 
    return W1, b1, W2, b2, W3, b3

# Get predictions from the output layer
def get_predictions(A2):
    return np.argmax(A2, 0)


#accuracy of the neural networks predictions in the final output layer
def get_accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size

#Trains the model using gradient descent
# The model is trained for a specified number of iterations
def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2, W3, b3 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2, Z3, A3 = forward_prop(W1, b1, W2, b2, W3, b3, X)
        dW1, db1, dW2, db2, dW3, db3 = backward_prop(Z1, A1, Z2, A2, Z3, A3, W1, W2, W3, X, Y)
        W1, b1, W2, b2, W3, b3 = update_params(W1, b1, W2, b2, W3, b3, dW1, db1, dW2, db2, dW3, db3, alpha)
        if i % 10 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A3)
            print("Accuracy: ", get_accuracy(predictions, Y))
            # Validation accuracy
            #_, _, _, _, _, A3_dev = forward_prop(W1, b1, W2, b2, W3, b3, X_dev)
            #val_preds = get_predictions(A3_dev)

            #print("Validation Accuracy:", get_accuracy(val_preds, Y_dev))
    return W1, b1, W2, b2, W3, b3

#run training
W1, b1, W2, b2, W3, b3 = gradient_descent(X_train, Y_train, 0.10, 500)

# Make predictions on the training set
def make_predictions(X, W1, b1, W2, b2, W3, b3):
    _, _, _, _, _, A3 = forward_prop(W1, b1, W2, b2, W3, b3, X)
    predictions = get_predictions(A3)
    return predictions

# Test prediction on a specific training sample
# This function displays the predicted label and the actual label
def test_prediction(index, W1, b1, W2, b2, W3, b3):
    current_image = X_train[:, index, None]
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2, W3, b3)
    label = Y_train[index]
    print("Prediction: ", prediction)
    print("Label: ", label)
    
    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()

# Show prediction for index
test_prediction(119, W1, b1, W2, b2, W3, b3)



