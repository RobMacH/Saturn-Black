from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import numpy as np
import pandas as pd
import sys

def main():
    
    df = pd.read_csv(sys.argv[1])

    print(f"{df.head()}\n")
    print(f"{df.info()}\n")
    print(f"{df.isnull().sum()}\n")

    y = df['abilities']
    X = df.loc[:, 'against_bug':]

    print("y is: \n", y)
    print("X is: \n", X)

    if(input("Continue? ") != 'y'):
        print("Exiting...")
        return

    # Generate synthetic data for demonstration
    # X, y = make_regression(n_samples=100, n_features=1, noise=0.1, random_state=42)

    # for i in range(X.size):
    #     print("X: ", X[i], "Y: ", y[i])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define kernel ridge regression model
    kernel = 'rbf'  # You can choose 'linear', 'poly', 'rbf', 'sigmoid', or custom kernel
    alpha = 0.1  # Regularization parameter
    gamma = 0.001  # Kernel coefficient, only used for 'rbf', 'poly', and 'sigmoid' kernels

    krr_model = KernelRidge(alpha=alpha, kernel=kernel, gamma=gamma)

    knn_model = NearestNeighbors(n_neighbors=3)

    # Train the model
    krr_model.fit(X_train, y_train)

    knn_model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = krr_model.predict(X_test)
    print("Actual: ", y_test, "Predicted: ", krr_model.predict(X_test))

    knn_y_pred = knn_model.kneighbors(X_test)

    distances, indices = mean_squared_error(y_test, knn_y_pred)

    #print("KNN MSE: " )

    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)






if __name__ == '__main__':
    main()
