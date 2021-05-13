"""
    Ensemble classifier model.

    This is to be imported in the testing notebook for the  
    ensemble classifier.
"""
# Data structures and manipulation
import numpy  as np
import pandas as pd

# Model and learning operations
import sklearn.preprocessing as scalers
import sklearn.metrics       as metrics
from sklearn.ensemble import StackingClassifier

# FootballML imports
from FootballML.Classifiers.Individual.logistic_regression_classifier import hyperparam_tuned_log_reg_classifier
from FootballML.Classifiers.Individual.neural_network_classifier      import hyperparam_tuned_neural_network
from FootballML.Classifiers.Individual.random_forest_classifier       import hyperparam_tuned_random_forest
from FootballML.Classifiers.Individual.svm.svm_classifier             import hyperparam_tuned_svm_classifier


# Example 
# ------------------------
# 1) Load data in this file and split it here and do any necessary
#    scaling
#X_train, X_test, Y_train, Y_test = train_test_split()

# Individual classifiers
log_reg_classifier = hyperparam_tuned_log_reg_classifier()
nrl_net_classifier = hyperparam_tuned_neural_network()
ran_fst_classifier = hyperparam_tuned_random_forest()
svm_classifier     = hyperparam_tuned_svm_classifier()

# List of the classifiers to be used in the ensemble classifier
# with their names
estimators = [('Log Reg', log_reg_classifier),
              ('Nrl Net', nrl_net_classifier),
              ('RForest', ran_fst_classifier),
              ('SVM'    , svm_classifier    )] 

# Ensemble classifier
ensemble_classifier = StackingClassifier(estimators=estimators)

# 5) Fit the data
# Call ensemble.fit(X, Y)

# 6) Test on the testing data
# Test ensemble on test data and get results
