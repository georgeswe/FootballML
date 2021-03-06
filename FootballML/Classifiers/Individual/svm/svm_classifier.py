from FootballML.Dataset import cleaned_data as cd
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as p
import matplotlib.pyplot as plt
plt.set_cmap("Oranges")


START_YEAR = 2003
END_YEAR = 2019

# G VAL Sets the scaler.
# valid scalers:
# quantile
# robust
# gaussian
# minmax
# standard (or any invalid value will give you this)
G_VAL = 'quantile'

# sets the SVM kernel
SVM_KERNEL = 'rbf'

# sets the C and gamma value
SVM_C = 10
SVM_GAMMA = 0.001
SVM_TEST_SIZE = 0.25


def hyperparam_tuned_support_vector():
    """SVM classifier with custom hyperparameters.

    This is to be imported and implemented in the ensemble
    classifier.

    Returns
    -------
    sklearn SVC object
        The svm classifier with custom hyperparameters
    """
    return SVC(kernel=SVM_KERNEL, gamma=SVM_GAMMA, C=SVM_C)


def custom_precision_recall(conf_matrix):
    # conf matrix composition:
    # by definition a confusion matrix C
    # is such that C i,j is equal to the number of observations known to be in group i and predicted to be in group j.
    # get our true positives
    rows, cols = np.shape(conf_matrix)
    # we will need to track these
    tp_array = []
    fp_array = []
    fn_array = []
    p_array = []
    r_array = []
    # so the i,j value where i = j should be our true positives
    # our false negative should be every other case in a row,
    # our false positive should be every other case in a column.
    for i in range(0, rows):
        row_sum = 0
        col_sum = 0
        for j in range(0, cols):
            if i == j:
                tp_array.append(conf_matrix[i, j])
            else:
                row_sum += conf_matrix[j, i]
                col_sum += conf_matrix[i, j]
        fp_array.append(row_sum)
        fn_array.append(col_sum)

    for k in range(0, cols):
        # precision = tp / (tp + fp)
        p_array.append(tp_array[k] / (tp_array[k] + fp_array[k]))
        # recall = tp / (tp + fn)
        r_array.append(tp_array[k] / (tp_array[k] + fn_array[k]))

    metrix = pd.DataFrame(p_array, columns=['Precision'])
    metrix['Recall'] = r_array
    return metrix


def f1_score(conf_matrix):
    # get some metrics
    metrix = custom_precision_recall(conf_matrix)
    p_array = []
    r_array = []
    f1_array = []
    # calculate the F1 score
    for p in metrix['Precision']:
        p_array.append(p)
    for r in metrix['Recall']:
        r_array.append(r)

    # F1 score = 2 * PR / (P + R)
    for i in range(0, len(p_array)):
        f1_array.append(2 * p_array[i] * r_array[i] / (p_array[i] + r_array[i]))
    return pd.DataFrame(f1_array, columns=["F1 Score"])


def return_training_data():
    """
    Returns
    -------
    X,Y -- lists of data to play with
    """
    start_year = 2018
    end_year = 2019
    data_read = cd.read_game_data_from_files(start_year, end_year)
    # create big X and big Y
    for i in range(0, (end_year - start_year)):
        if i == 0:
            X, Y = cd.get_training(cd.clean_data(np.array(data_read[i])), cd.clean_data(np.array(data_read[i + 1])),
                                   np.array(data_read[i + 1]), start_year + i + 1)
        else:
            X_temp, Y_temp = cd.get_training(cd.clean_data(np.array(data_read[i])),
                                             cd.clean_data(np.array(data_read[i + 1])),
                                             np.array(data_read[i + 1]), start_year + i + 1)
            X += X_temp
            Y += Y_temp

    return X, Y


def svm_tuned(start_year=START_YEAR, end_year=END_YEAR, g_val=G_VAL, svm_kernel=SVM_KERNEL, svm_c=SVM_C,
              svm_gamma=SVM_GAMMA,svm_test_size=SVM_TEST_SIZE, display_output=False):
    """
    Parameters
    @param start_year -- int start_year [DEFAULT = 2003]
    @param end_year -- int end_year [DEFAULT = 2019]
    @param g_val -- string for the scaler type [DEFAULT = 'standard', ACCEPTS = ['gaussian', 'quantile', 'minmax',
                                                                                'robust']]
    @param svm_kernel -- string for kernel type [DEFAULT = 'rbf', ACCEPTS = valid SVM kernels supported by sklearn]
    @param svm_c -- int for the C value [DEFAULT = 10]
    @param svm_gamma -- int for the gamma value [DEFAULT = 0.001]
    @param svm_test_size -- float < 1 for the test split size [DEFAULT = 0.25]
    @param display_output -- set to True to display some output metrics and a heatmap [DEFAULT = False]

    Returns
    @return clf2 -- returns the classifier fit to the training data
    """
    # read in data
    data_read = cd.read_game_data_from_files(start_year, end_year)
    # create big X and big Y
    for i in range(0, (end_year - start_year)):
        if i == 0:
            X, Y = cd.get_training(cd.clean_data(np.array(data_read[i])), cd.clean_data(np.array(data_read[i+1])),
                                   np.array(data_read[i+1]), start_year+i+1)
        else:
            X_temp, Y_temp = cd.get_training(cd.clean_data(np.array(data_read[i])), cd.clean_data(np.array(data_read[i+1])),
                                   np.array(data_read[i+1]), start_year+i+1)
            X += X_temp
            Y += Y_temp

    # apply scaling
    # From HypeParam testing, we will use this scaler:
    # QuantileTransformer with normalized Gaussian output
    # however, we will allow the option to use the stricter scaler.
    if g_val == 'gaussian':
        scaler = p.QuantileTransformer(output_distribution='normal')
        X_scaled = scaler.fit_transform(X, Y)
    elif g_val == "quantile":
        scaler = p.QuantileTransformer()
        X_scaled = scaler.fit_transform(X, Y)
    elif g_val == 'robust':
        scaler = p.RobustScaler()
        X_scaled = scaler.fit_transform(X, Y)
    elif g_val == 'minmax':
        scaler = p.MinMaxScaler()
        X_scaled = scaler.fit_transform(X, Y)
    else:
        scaler = p.StandardScaler()
        X_scaled = scaler.fit_transform(X, Y)

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y,shuffle=False, test_size=svm_test_size)

    # make the SVC object using our tested for HyperParams
    svc_obj = SVC(kernel=svm_kernel, gamma=svm_gamma, C=svm_c)

    clf_2 = svc_obj.fit(X_train, y_train)
    if display_output:
        predicted_2 = clf_2.predict(X_test)
        # do some predictions
        print("SVC accuracy:" + str(svc_obj.score(X_test, y_test)))
        cm_2 = confusion_matrix(y_test, predicted_2)
        cm_df_2 = pd.DataFrame(cm_2)
        plt.imshow(cm_df_2)
        print("SVC confusion matrix\n" + str(cm_df_2))
        plt.show()
        print("SVC Metrics\n" + str(f1_score(cm_2)))
        print(custom_precision_recall(cm_2))
    return clf_2


# svm_tuned()
