from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay
import numpy as np
import pandas as pd
import sys
import makeDataset
import matplotlib.pyplot as plt

class ABS_Mind:
    
    def __init__(self, databaseLocation):
        self.knn_model = self.ABS_Mind_test(databaseLocation)
        
    def predict(self, dataframe):
        return self.knn_model.predict(dataframe)

    def prepareDataframe(self, filelocation):
        frame = makeDataset.fourierAnalysis(filelocation, self.maxFrameNum)
        return frame

    def ABS_Mind_test(self, input):
        
        df = makeDataset.makeDataSet(f"{input}")

        y = df['class']
        X = df.iloc[:, 1:]

        self.maxFrameNum = len(X)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        #krr_model = KernelRidge(alpha=alpha, kernel=kernel, gamma=gamma)
        accuracy = []
        accuracySeries = []
        bestAccuracy = 0
        bestK = 0
        kMax = 100
        bestBoy = KNeighborsClassifier()

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
                cm = confusion_matrix(y_test, knn_y_pred)
                bestBoy = knn_model
            loadingBar = "\u2588" * int((k/kMax)*100) + "\u2591" * (100 - int((k/kMax)*100))
            print("Testing k =", k, "of", kMax,f"[Best ACC {bestAccuracy} (k={bestK})]", f"|{loadingBar}|", end="\r")

        print(f"\nBest model was k={bestK} with ACC = {bestAccuracy}.")
        print("Confusion Matrix:\n", cm)

        plt.figure(0)
        p = plt.plot(range(1,kMax+1), accuracySeries)
        plt.ylabel("Accuracy")
        plt.xlabel("k")

        ConfusionMatrixDisplay(cm).plot()
        plt.show()

        return bestBoy


if __name__ == '__main__':
    print("No.")
