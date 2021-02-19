import numpy
from sklearn import linear_model, tree
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import NearestCentroid

REGRESSORS = (
    "linear_regression", "elastic_net", "bayesian_ridge", "Support_Vector_Machine", "Decision_tree", "KNN", "Gaussian",
    "Random_Forest")


def initialize(method, coef=None):
    regressor = None
    if method == "linear_regression":
        regressor = linear_model.LinearRegression(normalize=True)
    if method == "elastic_net":
        regressor = linear_model.ElasticNet(normalize=True)
    if method == "bayesian_ridge":
        regressor = linear_model.BayesianRidge(normalize=True)
    if method == "Support_Vector_Machine":
        regressor = svm.SVR()
    if method == "Decision_tree":
        regressor = tree.DecisionTreeClassifier()
    if method == "KNN":
        regressor = NearestCentroid()
    if method == "Gaussian":
        regressor = GaussianNB()
    if method == "Random_Forest":
        if coef == None:
            regressor = RandomForestRegressor(n_estimators=30)
        else:
            regressor = RandomForestRegressor(n_estimators=coef)
    else:
        if "Random_Forest" in method:
            trees = method.split("t")[1]
            regressor = RandomForestRegressor(n_estimators=int(trees))
    if method == "ensemble":
        r1 = initialize("linear_regression")
        r2 = initialize("Random_Forest")
        r3 = initialize("bayesian_ridge")
        if coef == None:
            regressor = VotingRegressor([('lr', r1), ('rf', r2), ('br', r3)])
        else:
            regressor = VotingRegressor(estimators=[('lr', r1), ('rf', r2), ('br', r3)], weights=coef)

    return regressor


def fit(regressor, x, y, tuples_dimension, features_dimension):
    shaped_x = numpy.array(x).reshape(tuples_dimension, features_dimension)
    shaped_y = numpy.array(y).reshape(tuples_dimension, 1).ravel()
    return regressor.fit(shaped_x, shaped_y)


def predict(regressor, x, tuples_dimension, features_dimension):
    shaped_x = numpy.array(x).reshape(tuples_dimension, features_dimension)
    y = regressor.predict(shaped_x)
    return y
