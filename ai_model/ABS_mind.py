from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
from sklearn.metrics import confusion_matrix, accuracy_score
import numpy as np
import pandas as pd
import sys
import makeDataset
import matplotlib.pyplot as plt

def main():
    
    df = makeDataset.makeDataSet("/home/rob-spin5/AudioMNIST/data/08")

    y = df['class']
    X = df.iloc[:, 1:10]

    # print("y is: \n", y)
    # print("X is: \n", X)

    if(input("Dataset complete. Continue? ") != 'y'):
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

    #krr_model = KernelRidge(alpha=alpha, kernel=kernel, gamma=gamma)
    accuracy = []
    accuracySeries = []
    bestAccuracy = 0
    bestK = 0
    kMax = 100

    for k in range(1,kMax+1):
        #print("k=", k)
        knn_model = KNeighborsClassifier(n_neighbors=k)

        # Train the model
        #krr_model.fit(X_train, y_train)
        #print("Fitting...")
        knn_model.fit(X_train, y_train)

        #print(X_train, y_train, X_test, y_test, sep='\n')

        # Predict on the test set
        #y_pred = krr_model.predict(X_test)
        #print("Actual: ", y_test, "Predicted: ", krr_model.predict(X_test))
        #print("Predicting...")
        knn_y_pred = knn_model.predict(X_test)

        accuracy = accuracy_score(y_test, knn_y_pred)
        accuracySeries.append(accuracy)

        #print("KNN ACC for (", k, "): ", accuracy, sep='')

        if(accuracy > bestAccuracy):
            bestAccuracy = accuracy
            bestK = k
        loadingBar = "\u2588" * int((k/kMax)*100) + "\u2591" * (100 - int((k/kMax)*100))
        print("Testing k =", k, "of", kMax,f"[Best ACC {bestAccuracy} (k={bestK})]", f"|{loadingBar}|", end="\r")

    print(f"\nBest model was k={bestK} with ACC = {bestAccuracy}.")
    

    plt.figure(0)
    p = plt.plot(range(1,kMax+1), accuracySeries)
    plt.ylabel("Accuracy")
    plt.xlabel("k")

    #print(zeros)

    #plt.figure(1)
    
    plt.show()

    print("End of Program...")


        #cm = confusion_matrix(y_test, knn_y_pred)

        #print("Confusion Matrix:\n", cm)






if __name__ == '__main__':
    main()
