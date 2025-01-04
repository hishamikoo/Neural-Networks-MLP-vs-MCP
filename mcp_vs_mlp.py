# -*- coding: utf-8 -*-
"""MCP vs MLP

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lp5k1Ui6bIyHq2v9c_uV3zh-WDQVxwPE

#Installing Libraries and preparing dataset
"""

!pip install palmerpenguins

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

penguins = load_penguins()
penguins.head()

data = penguins.drop(columns=["sex","year","island"])

data["bill_length_mm"].fillna(round(data["bill_length_mm"].mean(),2), inplace=True)
data["bill_depth_mm"].fillna(round(data["bill_depth_mm"].mean(),2), inplace=True)
data["flipper_length_mm"].fillna(round(data["flipper_length_mm"].mean(),2), inplace=True)
data["body_mass_g"].fillna(round(data["body_mass_g"].mean(),2), inplace=True)

data.head()

data.drop(columns='species').hist(bins=20, figsize=(12, 10))
plt.suptitle("Feature Distributions")
plt.show()

X = data.drop(columns='species')
y = data['species']

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
X_scaled_df["species"] = y

data = X_scaled_df

data.head()

data.drop(columns='species').hist(bins=20, figsize=(12, 10))
plt.suptitle("Feature Distributions")
plt.show()

"""#Multiclass Perceptron Model (MCP)"""

X = data.drop(columns='species')
y = data['species']

class_mapping = {species: idx for idx, species in enumerate(np.unique(y))}
y_int = np.array([class_mapping[species] for species in y])  #Map to integers

y_one_hot = np.eye(3)[y_int] #One-hot encoding of the labels

X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.2, random_state=42) # Split data into training and testing sets

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def GaussianFunction(x):
    return np.exp(-x**2)

def GaussianDerivative(x):
    return -2*x*np.exp(-x**2)

def categorical_cross_entropy(y_true, y_pred):
    m = y_true.shape[0]
    return -np.sum(y_true * np.log(y_pred + 1e-9)) / m  # Added small epsilon (1e-9) to avoid log(0)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

class MulticlassPerceptron:
    def __init__(self, input_size, output_size, learning_rate):

        self.input_size = input_size
        self.output_size = output_size
        self.learning_rate = learning_rate


        self.weights = np.random.randn(input_size, output_size) * 0.01 # Initialise weights randomly with small values
        self.bias = np.zeros((1, output_size))

    def forward(self, X):
        #Forward propagation
        self.input = X
        self.z = np.dot(X, self.weights) + self.bias  # Linear combination
        self.output = relu(self.z)  # Sigmoid activation
        return self.output

    def backward(self, X, Y):
        #Backward propagation (gradient calculation and weight update)
        output_error = self.output - Y  # Error term (difference from true values)
        output_delta = output_error * relu_derivative(self.output)  # Gradient at the output

        self.weights -= np.dot(self.input.T, output_delta) * self.learning_rate  # Weight update
        self.bias -= np.sum(output_delta, axis=0, keepdims=True) * self.learning_rate  # Bias update

    def train(self, X_train, y_train, X_test, y_test, epochs):
        #Train the perceptron using backpropagation
        self.train_errors = []
        self.test_errors = []

        for epoch in range(epochs):

            y_pred = self.forward(X_train) # Forward pass


            self.backward(X_train, y_train) # Backward pass

            train_loss = categorical_cross_entropy(y_train, y_pred) # Calculate training error (loss)
            self.train_errors.append(train_loss)

            # Calculate test error (loss) at every epoch for evaluation
            y_test_pred = self.forward(X_test)
            test_loss = categorical_cross_entropy(y_test, y_test_pred)
            self.test_errors.append(test_loss)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Training Loss: {train_loss}, Test Loss: {test_loss}")

    def predict(self, X):
        #Predict the class for given input
        output = self.forward(X)
        return np.argmax(output, axis=1)  # Return class with the highest probability

# Declare learning rate and epochs outside the class
learning_rate = 0.0015
epochs = 2000

# Initialisation of multiclass perceptron
input_size = X_train.shape[1]  # 4 features per sample
output_size = y_train.shape[1]  # 3 classes
model = MulticlassPerceptron(input_size, output_size, learning_rate)

# Train the model
model.train(X_train, y_train, X_test, y_test, epochs)

def calculate_accuracy(y_true, y_pred):
    """Calculate accuracy."""
    correct = np.sum(np.argmax(y_true, axis=1) == y_pred)
    return correct / y_true.shape[0]

# Predict the test data
y_test_pred = model.predict(X_test)

# Calculate accuracy
accuracy = calculate_accuracy(y_test, y_test_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Plot training and test error curves
plt.plot(model.train_errors, label='Training Error')
plt.plot(model.test_errors, label='Test Error')
plt.xlabel('Epochs')
plt.ylabel('Error Rates')
plt.legend()
plt.title('Training and Test Error Curves')
plt.show()

learning_rates = np.linspace(0.001, 0.05, 100)  # 50 values between 0.001 and 0.05
train_errors = []
test_errors = []
accuracies = []

# Iterate over learning rates
for lr in learning_rates:
    # Initialize and train the model
    model = MulticlassPerceptron(input_size, output_size, lr)
    model.train(X_train, y_train, X_test, y_test, epochs)

    # Append the last training and testing error for this learning rate
    train_errors.append(model.train_errors[-1])  # Last training error
    test_errors.append(model.test_errors[-1])    # Last testing error

    # Predict on test set and calculate accuracy
    y_test_pred = model.predict(X_test)
    accuracy = calculate_accuracy(y_test, y_test_pred)
    accuracies.append(accuracy * 100)  # Convert to percentage

# Find the learning rate corresponding to the minimum testing error
min_test_error = min(test_errors)
optimal_lr = learning_rates[test_errors.index(min_test_error)]

# Plot Training and Testing Errors
plt.figure(figsize=(12, 6))
plt.plot(learning_rates, train_errors, label='Training Error', marker='o', linestyle='-', color='blue')
plt.plot(learning_rates, test_errors, label='Testing Error', marker='o', linestyle='-', color='orange')
plt.axvline(optimal_lr, color='red', linestyle='--', label=f'Optimal LR: {optimal_lr:.4f}')
plt.title('Learning Rate vs Training/Testing Error', fontsize=16)
plt.xlabel('Learning Rate', fontsize=14)
plt.ylabel('Error', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

# Plot Learning Rate vs Accuracy
plt.figure(figsize=(12, 6))
plt.plot(learning_rates, accuracies, marker='o', linestyle='-', color='green')
plt.axvline(optimal_lr, color='red', linestyle='--', label=f'Optimal LR: {optimal_lr:.4f}')
plt.title('Learning Rate vs Model Accuracy', fontsize=16)
plt.xlabel('Learning Rate', fontsize=14)
plt.ylabel('Accuracy (%)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

optimal_lr = 0.0015
optimal_epochs = 2000

split_ratios = [0.5, 0.6, 0.7, 0.8, 0.9]

accuracies = []

for split_ratio in split_ratios:
    X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=1 - split_ratio, random_state=42)

    model = MulticlassPerceptron(input_size, output_size, optimal_lr)

    model.train(X_train, y_train, X_test, y_test, optimal_epochs)

    y_test_pred = model.predict(X_test)
    accuracy = calculate_accuracy(y_test, y_test_pred)
    accuracies.append(accuracy * 100)  # Convert to percentage

print("\nTraining/Test Split Ratio and Accuracy")
print("-" * 40)
print("{:<20} {:<10}".format("Training Ratio", "Accuracy (%)"))
for split_ratio, acc in zip(split_ratios, accuracies):
    print(f"{split_ratio:<20} {acc:.2f}")

plt.figure(figsize=(10, 6))
plt.plot(split_ratios, accuracies, marker='o', linestyle='-', color='blue', label='Accuracy')
plt.title("Model Accuracy vs Training/Test Split Ratio", fontsize=16)
plt.xlabel("Training Ratio", fontsize=14)
plt.ylabel("Accuracy (%)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(split_ratios, labels=[f"{int(r*100)}/{int((1-r)*100)}" for r in split_ratios], fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.show()

"""#MCP + Cross Validation"""

class MulticlassPerceptron:
    def __init__(self, input_size, output_size, learning_rate):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.bias = np.zeros((1, output_size))
        self.learning_rate = learning_rate

    def forward(self, X):
        self.z = np.dot(X, self.weights) + self.bias
        self.output = relu(self.z)
        return self.output

    def backward(self, X, Y):
        error = self.output - Y
        delta = error * relu_derivative(self.output)
        self.weights -= np.dot(X.T, delta) * self.learning_rate
        self.bias -= np.sum(delta, axis=0, keepdims=True) * self.learning_rate

    def train(self, X, Y, epochs):
        losses = []
        for _ in range(epochs):
            self.forward(X)
            self.backward(X, Y)
            losses.append(categorical_cross_entropy(Y, self.output))
        return losses

    def predict(self, X):
        predictions = self.forward(X)
        return np.argmax(predictions, axis=1)

def calculate_accuracy(y_true, y_pred):
    correct = np.sum(np.argmax(y_true, axis=1) == y_pred)
    return correct / y_true.shape[0]

fixed_learning_rate = 0.0015
epochs = 2000

# Cross-validation setup
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

# Lists to store errors
validation_errors = []
test_errors = []

all_true_labels = []
all_predicted_labels = []

# Iterate over K-Folds
for train_index, test_index in kfold.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y_one_hot[train_index], y_one_hot[test_index]

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

    model = MulticlassPerceptron(input_size=X.shape[1], output_size=y_one_hot.shape[1], learning_rate=fixed_learning_rate)

    model.train(X_train, y_train, epochs)

    val_loss = categorical_cross_entropy(y_val, model.forward(X_val))
    validation_errors.append(val_loss)

    test_loss = categorical_cross_entropy(y_test, model.forward(X_test))
    test_errors.append(test_loss)

    y_pred = model.predict(X_test)

    # Store true and predicted labels
    all_true_labels.extend(np.argmax(y_test, axis=1))
    all_predicted_labels.extend(y_pred)


cm = confusion_matrix(all_true_labels, all_predicted_labels)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(np.argmax(y_one_hot, axis=1)))
disp.plot(cmap="viridis", colorbar=True)
plt.title("Confusion Matrix")
plt.show()

# Calculate mean errors across folds
mean_validation_error = np.mean(validation_errors)
mean_test_error = np.mean(test_errors)

# Display results
print(f"Mean Validation Error: {mean_validation_error:.6f}")
print(f"Mean Test Error: {mean_test_error:.6f}")

# Plot validation and test errors
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(validation_errors) + 1), validation_errors, label="Validation Error", marker='o', color="orange")
plt.plot(range(1, len(test_errors) + 1), test_errors, label="Test Error", marker='x', color="blue")
plt.xlabel("Fold", fontsize=14)
plt.ylabel("Error Rate", fontsize=14)
plt.title("Validation and Test Errors Across Folds", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

"""#MLP with CV (1 Hidden Layer)"""

X = data.drop(columns='species')
y = data['species']

class_mapping = {species: idx for idx, species in enumerate(np.unique(y))}
y_int = np.array([class_mapping[species] for species in y])  #Map to integers

y_one_hot = np.eye(3)[y_int] #One-hot encoding of the labels

X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.1, random_state=42) # Split data into training and testing sets

def categorical_cross_entropy(y_true, y_pred):
    m = y_true.shape[0]
    return -np.sum(y_true * np.log(y_pred + 1e-9)) / m  # Adding small epsilon to avoid log(0)

# MLP class with sigmoid activation for both layers
class MLP:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        # Initialize weights and biases
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.01
        self.bias1 = np.zeros((1, hidden_size))

        self.weights2 = np.random.randn(hidden_size, output_size) * 0.01
        self.bias2 = np.zeros((1, output_size))

    def forward(self, X):
        self.input = X
        self.hidden = relu(np.dot(X, self.weights1) + self.bias1)  # Hidden layer
        self.output = relu(np.dot(self.hidden, self.weights2) + self.bias2)  # Output layer
        return self.output

    def backward(self, X, Y):
        # Output layer error
        output_error = self.output - Y
        output_delta = output_error * relu_derivative(self.output)

        # Hidden layer error
        hidden_error = np.dot(output_delta, self.weights2.T)
        hidden_delta = hidden_error * relu_derivative(self.hidden)

        # Update weights and biases
        self.weights2 -= np.dot(self.hidden.T, output_delta) * self.learning_rate
        self.bias2 -= np.sum(output_delta, axis=0, keepdims=True) * self.learning_rate

        self.weights1 -= np.dot(X.T, hidden_delta) * self.learning_rate
        self.bias1 -= np.sum(hidden_delta, axis=0, keepdims=True) * self.learning_rate

    def train_with_cross_validation(self, X, y, kfolds, epochs):
        kf = KFold(n_splits=kfolds, shuffle=True, random_state=42)
        self.train_errors = np.zeros(epochs)
        self.val_errors = np.zeros(epochs)

        for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
            print(f"Training Fold {fold + 1}/{kfolds}")
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            for epoch in range(epochs):
                y_pred = self.forward(X_train)
                self.backward(X_train, y_train)

                train_loss = categorical_cross_entropy(y_train, y_pred)
                self.train_errors[epoch] += train_loss / kfolds

                y_val_pred = self.forward(X_val)
                val_loss = categorical_cross_entropy(y_val, y_val_pred)
                self.val_errors[epoch] += val_loss / kfolds

            print(f"Fold {fold + 1} completed.")

    def predict(self, X):
        output = self.forward(X)
        return np.argmax(output, axis=1)

input_size = X_train.shape[1]
hidden_size = 3  # Number of perceptrons in the hidden layer
output_size = y_train.shape[1]
learning_rate = 0.0015
epochs = 2000
kfolds = 5

# Create and train the MLP model
model = MLP(input_size, hidden_size, output_size, learning_rate)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Train the model using K-Fold Cross-Validation
model.train_with_cross_validation(X_train, y_train, kfolds, epochs)

# Calculate accuracy on test set
def calculate_accuracy(y_true, y_pred):
    correct = np.sum(np.argmax(y_true, axis=1) == y_pred)
    return correct / y_true.shape[0]

y_test_pred = model.predict(X_test)
accuracy = calculate_accuracy(y_test, y_test_pred)
print(f"Model Accuracy on Test Set: {accuracy * 100:.2f}%")

# Plot training and validation error curves
plt.plot(model.train_errors, label='Training Error')
plt.plot(model.val_errors, label='Validation Error')
plt.xlabel('Epochs')
plt.ylabel('Error Rates')
plt.legend()
plt.title('Training and Validation Error Curves')
plt.show()

true_labels = np.argmax(y_test, axis=1)  # Convert one-hot to class labels
conf_matrix = confusion_matrix(true_labels, y_test_pred)

#confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=np.unique(true_labels))
disp.plot(cmap="viridis", colorbar=True)
plt.title("Confusion Matrix")
plt.show()

"""#MLP with CV (Multiple Hidden Layers)"""

class ExtendedMLP:
    def __init__(self, layer_sizes, learning_rate):

        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate

        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            self.weights.append(np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * 0.01)
            self.biases.append(np.zeros((1, layer_sizes[i + 1])))

    def forward(self, X):

        self.activations = [X]  # Storing activations for all layers (input included)
        for i in range(len(self.weights) - 1):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            self.activations.append(relu(z))

        # Output layer
        z_output = np.dot(self.activations[-1], self.weights[-1]) + self.biases[-1]
        self.activations.append(relu(z_output))
        return self.activations[-1]

    def backward(self, Y):

        m = Y.shape[0]  # Number of samples
        deltas = [self.activations[-1] - Y]

        # Backpropagate through all layers
        for i in reversed(range(len(self.weights))):
            delta = deltas[0]  # Current layer delta
            grad_weights = np.dot(self.activations[i].T, delta) / m
            grad_biases = np.sum(delta, axis=0, keepdims=True) / m


            self.weights[i] -= self.learning_rate * grad_weights
            self.biases[i] -= self.learning_rate * grad_biases


            if i > 0:
                deltas.insert(0, np.dot(delta, self.weights[i].T) * relu_derivative(self.activations[i]))

    def train_with_cross_validation(self, X, y, kfolds, epochs):

        kf = KFold(n_splits=kfolds, shuffle=True, random_state=42)
        self.train_errors = np.zeros(epochs)
        self.val_errors = np.zeros(epochs)

        for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
            print(f"Training Fold {fold + 1}/{kfolds}")
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            for epoch in range(epochs):
                self.forward(X_train)
                self.backward(y_train)

                train_loss = categorical_cross_entropy(y_train, self.activations[-1])
                self.train_errors[epoch] += train_loss / kfolds

                val_loss = categorical_cross_entropy(y_val, self.forward(X_val))
                self.val_errors[epoch] += val_loss / kfolds

            print(f"Fold {fold + 1} completed.")

    def predict(self, X):
        """
        Predict class labels for given input data.
        Args:
            X: Input data.
        Returns:
            Predicted class labels.
        """
        output = self.forward(X)
        return np.argmax(output, axis=1)


layer_sizes = [X_train.shape[1], 4, 3, 3]  # Input, two hidden layers (4 and 3 neurons), output
learning_rate = 0.0015
epochs = 2000
kfolds = 5

model = ExtendedMLP(layer_sizes=layer_sizes, learning_rate=learning_rate)

X_train = np.array(X_train)
y_train = np.array(y_train)

model.train_with_cross_validation(X_train, y_train, kfolds, epochs)

y_test_pred = model.predict(X_test)
accuracy = calculate_accuracy(y_test, y_test_pred)
print(f"Model Accuracy on Test Set: {accuracy * 100:.2f}%")

plt.plot(model.train_errors, label='Training Error')
plt.plot(model.val_errors, label='Validation Error')
plt.xlabel('Epochs')
plt.ylabel('Error Rates')
plt.legend()
plt.title('Training and Validation Error Curves')
plt.show()

# Confusion Matrix
true_labels = np.argmax(y_test, axis=1)
conf_matrix = confusion_matrix(true_labels, y_test_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=np.unique(true_labels))
disp.plot(cmap="viridis", colorbar=True)
plt.title("Confusion Matrix")
plt.show()