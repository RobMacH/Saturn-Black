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
import pickle as pk

class ABS_Mind(object):
    
    numFeatures = 0
    maxNumFrames = 0
    knn_model = {0}
    number = 4
    databaseLocation = {0}

    def __init__(self, databaseLocation, numFeatures=0):
        self.number = 2
        self.knn_model = self.ABS_Mind_test(databaseLocation)

    def setFeatures(self):
        self.numFeatures = self.knn_model.n_features_in_()

    def predict(self, dataframe):
        return self.knn_model.predict(dataframe)

    def prepareDataframe(self, filelocation):
        frame, axis = makeDataset.fourierAnalysis(filelocation, self.maxNumFrames)
        df = pd.DataFrame(data=frame, columns=axis)


        index = 0
        for column in df.columns:
            if (float(column) > 7000):
                break
            index += 1
        
        if(index % 2):
            index-=1
        

        df = df.iloc[:, :index]
        df = df.iloc[:,:] * np.hamming(len(df.columns))
        return df
    
    def brine(self):
        with open("ABSPickleJar.txt", 'wb') as pickleJar:
            pk.dump(self, pickleJar)

    def ABS_Mind_test(self, input, all=0):
        
        df, self.maxNumFrames = makeDataset.makeDataSet(f"{input}")
        

        y = df['class']
        X = df.iloc[:, 1:]

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
            loadingBar = "\u2588" * int((k/kMax)*50) + "\u2591" * (50 - int((k/kMax)*50))
            print("Testing k =", k, "of", kMax,f"[Best ACC {bestAccuracy} (k={bestK})]", f"|{loadingBar}|", end="\r")

        print(f"\nBest model was k={bestK} with ACC = {bestAccuracy}.")
        #print("Confusion Matrix:\n", cm)

        plt.figure(0)
        p = plt.plot(range(1,kMax+1), accuracySeries)
        plt.ylabel("Accuracy")
        plt.xlabel("k")

        ConfusionMatrixDisplay(cm).plot()
        plt.show()

        return bestBoy

def ABS_factory(filename=None, *args, **kwargs):
    if filename:
        mind = pk.load(filename)
    else:
        mind = ABS_Mind(*args, **kwargs)
    return mind

if __name__ == '__main__':
    if((sys.argv[1] == 'c') & (len(sys.argv) == 3)):
        mind = ABS_Mind(f"/home/rob-spin5/AudioMNIST/data/{sys.argv[2]}")
        mind.brine()
    elif((sys.argv[1] == 'l') & (len(sys.argv) == 5)):  
        print("Doing a think...")      
        with open("ABSPickleJar.txt", 'rb') as PickleJar:
            mind = ABS_factory(PickleJar)
        df = mind.prepareDataframe(f"/home/rob-spin5/AudioMNIST/data/{sys.argv[3]}/{sys.argv[2]}_{sys.argv[3]}_{sys.argv[4]}.wav")
        print("It is", mind.predict(df)[0])
    else:
        print("Bad Args.")

