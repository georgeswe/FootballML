""" 
    This will be where the actual code for the svm classifier goes
"""
from FootballML.Dataset import cleaned_data as cd
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as p



# read in the data and split
data_read_2009 = cd.read_game_data_from_files(2009)
data_read_2010 = cd.read_game_data_from_files(2010)
data2010clean = cd.clean_data(np.array(data_read_2010[0]))
data2009clean = cd.clean_data(np.array(data_read_2009[0]))
X, Y = cd.get_training(data2009clean, data2010clean, np.array(data_read_2010[0]), 2010)
j = 0
while(j < 100):
    # # scaling for RBF kernel
    for i in range(0, 5):
        if i == 0:
            scaler = p.MinMaxScaler()
        elif i == 1:
            scaler = p.RobustScaler()
        elif i == 2:
            scaler = p.QuantileTransformer()
        elif i == 3:
            scaler = p.PowerTransformer()
        else:
            scaler = p.StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)

        X_train, x_test, y_train, y_test = train_test_split(X_scaled, Y, test_size = 0.20)


        # params to "search"
        param_grid = {'C': [0.1, 1, 10, 100, 1000],
                      'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
                      'kernel': ['rbf', 'sigmoid', 'poly']}

        # train the model on train set
        model = SVC()
        model.fit(X_train, y_train)

        # print prediction results
        predictions = model.predict(x_test)
        print(classification_report(y_test, predictions))

        # n_jobs = -1 will maximize the use of your CPU, remove for slower but less taxing computations
        grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=3, n_jobs=-1)

        # fitting the model for grid search
        grid.fit(X_train, y_train)
        print(grid.best_params_)
        print(grid.best_estimator_)
        grid_predictions = grid.predict(x_test)

        # print classification report
        data_best_params = grid.best_params_
        data_best_estimator_ = grid.best_estimator_
        data_classification_report = classification_report(y_test, grid_predictions)
        print(data_classification_report)

        # totals file
        out_file = open("svm_params_totals.txt", "a")
        out_file.write("USING THE: " + str(type(scaler)) + "\n")
        out_file.write("params = " + str(data_best_params) + "\n")
        out_file.write("best estimator = " + str(data_best_estimator_) + "\n")
        out_file.write(str(data_classification_report) + "\n")
        out_file.close()

        out_file = open("svm_acc_totals.txt", "a")
        out_file.write("USING THE: " + str(type(scaler)) + "AND " + str(data_best_estimator_) + "\n")
        out_file.write(str(grid.best_score_) + "\n")
    j += 1
