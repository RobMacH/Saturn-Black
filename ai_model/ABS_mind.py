from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import numpy as np

# Generate synthetic data for demonstration
X, y = make_regression(n_samples=100, n_features=50, noise=0.1, random_state=42)



# for i in range(X.size-1):
#     if i == 100:
#         break
#     print("X: ", X[i], "Y: ", y[i])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define kernel ridge regression model
kernel = 'sigmoid'  # You can choose 'linear', 'poly', 'rbf', 'sigmoid', or custom kernel
alpha = 0.01  # Regularization parameter
gamma = 0.001  # Kernel coefficient, only used for 'rbf', 'poly', and 'sigmoid' kernels

krr_model = KernelRidge(alpha=alpha, kernel=kernel, gamma=gamma)

knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train, y_train)

# Train the model
krr_model.fit(X_train, y_train)

# Predict on the test set
y_pred = krr_model.predict(X_test)

print("KRR - Actual: ", y_test, "\nPredicted: ", krr_model.predict(X_test))

print("KNN - Actual: ", y_test, "\nPredicted: ", knn_model.predict(X_test))

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
