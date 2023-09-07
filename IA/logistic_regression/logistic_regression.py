import numpy as np
import pandas as pd

class LogisticRegression:

    def __init__(self, learning_rate=0.01, num_iterations=1000):
        """
        Initialize the Logistic Regression model with hyperparameters.

        Args:
            learning_rate (float): The learning rate for gradient descent.
            num_iterations (int): The number of training iterations.
        """
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """
        Estimates parameters for the classifier using gradient descent.

        Args:
            X (array<m,n>): a matrix of floats with m rows (#samples) and n columns (#features)
            y (array<m>): a vector of floats containing m binary 0.0/1.0 labels
        """
        self.weights = np.zeros(X.shape[1])
        self.bias = 0

        for _ in range(self.num_iterations):
            # Compute predictions
            y_pred = sigmoid(np.dot(X, self.weights) + self.bias)

            # Compute gradients
            dw = (1 / X.shape[0]) * np.dot(X.T, (y_pred - y))
            db = (1 / X.shape[0]) * np.sum(y_pred - y)

            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        """
        Generates predictions.

        Note: should be called after .fit()

        Args:
            X (array<m,n>): a matrix of floats with m rows (#samples) and n columns (#features)

        Returns:
            A length m array of floats in the range [0, 1] with probability-like predictions
        """
        if self.weights is None or self.bias is None:
            raise ValueError("Model not trained. Call fit() first.")

        y_pred = sigmoid(np.dot(X, self.weights) + self.bias)
        return y_pred

        

        
# --- Some utility functions 

def binary_accuracy(y_true, y_pred, threshold=0.5):
    """
    Computes binary classification accuracy
    
    Args:
        y_true (array<m>): m 0/1 floats with ground truth labels
        y_pred (array<m>): m [0,1] floats with "soft" predictions
        
    Returns:
        The average number of correct predictions
    """
    assert y_true.shape == y_pred.shape
    y_pred_thresholded = (y_pred >= threshold).astype(float)
    correct_predictions = y_pred_thresholded == y_true 
    return correct_predictions.mean()
    

def binary_cross_entropy(y_true, y_pred, eps=1e-15):
    """
    Computes binary cross entropy 
    
    Args:
        y_true (array<m>): m 0/1 floats with ground truth labels
        y_pred (array<m>): m [0,1] floats with "soft" predictions
        
    Returns:
        Binary cross entropy averaged over the input elements
    """
    assert y_true.shape == y_pred.shape
    y_pred = np.clip(y_pred, eps, 1 - eps)  # Avoid log(0)
    return - np.mean(
        y_true * np.log(y_pred) + 
        (1 - y_true) * (np.log(1 - y_pred))
    )


def sigmoid(x):
    """
    Applies the logistic function element-wise
    
    Hint: highly related to cross-entropy loss 
    
    Args:
        x (float or array): input to the logistic function
            the function is vectorized, so it is acceptible
            to pass an array of any shape.
    
    Returns:
        Element-wise sigmoid activations of the input 
    """
    return 1. / (1. + np.exp(-x))