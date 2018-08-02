from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor


# RBF Kernel Support Vector Regression (SVR)
def svr_rbf(train_x, train_y):
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    model = svr_rbf.fit(train_x, train_y)
    return model


# Linear Kernel Support Vector Regression (SVR)
def svr_lin(train_x, train_y):
    svr_lin = SVR(kernel='linear', C=1e3)
    model = svr_lin.fit(train_x, train_y)
    return model


# Poly Kernel Support Vector Regression (SVR)
def svr_poly(train_x, train_y):
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    model = svr_poly.fit(train_x, train_y)
    return model


# Random forest
def random_forest_regressor(train_x, train_y):
    random_forest = RandomForestRegressor(max_depth=2, random_state=0)
    model = random_forest.fit(train_x, train_y)
    return model


# KNeighborsRegressor
def k_neighbor_regressor(train_x, train_y):
    k_neighbor = KNeighborsRegressor(n_neighbors=2)
    model = k_neighbor.fit(train_x, train_y)
    return model


# Linear Regressor
def linear_regressor(train_x, train_y):
    linear = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
    model = linear.fit(train_x, train_y)
    return model


# Adaboost Regressor
def adaboost_regressor(train_x, train_y):
    adaboost = AdaBoostRegressor(base_estimator=None, n_estimators=50, learning_rate=1.0, loss='linear', random_state=None)
    model = adaboost.fit(train_x, train_y)
    return model


# gradient boosting Regressor
def gradient_boosting_regressor(train_x, train_y):
    gradient_boosting = GradientBoostingRegressor(loss='ls', learning_rate=0.1, n_estimators=100, subsample=1.0,
        criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3,
        min_impurity_decrease=0.0, min_impurity_split=None, init=None, random_state=None, max_features=None, alpha=0.9,
        verbose=0, max_leaf_nodes=None, warm_start=False, presort='auto')
    model = gradient_boosting.fit(train_x, train_y)
    return model


# API for predictor
def regressor(train_x, train_y, name):
    name = name.strip(" ").lower()
    if name == "svr_rbf":
        model = svr_rbf(train_x, train_y)
    elif name == "svr_poly":
        model = svr_poly(train_x, train_y)
    elif name == "svr_lin":
        model = svr_lin(train_x, train_y)
    elif name == "random_forest":
        model = random_forest_regressor(train_x, train_y)
    elif name == "k_neighbor":
        model = k_neighbor_regressor(train_x, train_y)
    elif name == "linear":
        model = linear_regressor(train_x, train_y)
    elif name == "adaboost":
        model = adaboost_regressor(train_x, train_y)
    elif name == "gradient_boosting":
        model = gradient_boosting_regressor(train_x, train_y)
    return model