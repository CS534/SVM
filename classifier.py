import numpy as np
from sklearn import metrics
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, \
    GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def get_label(path='./images/train/labels.txt'):
    with open(path, 'r') as f:
        names = f.readlines()
    names = [n.strip() for n in names]
    return names


def svc_classifier(x_train, y_train, x_test=None, y_test=None):
    if x_test is None and y_test is None:
        x_train, x_test, y_train, y_test = train_test_split(
            x_train, y_train, test_size=0.2, random_state=6)
        print("Spliting train:{}/test:{} from training data".format(
            len(x_train), len(x_test)))
    C_range = 10.0 ** np.arange(-3, 3)
    gamma_range = 10.0 ** np.arange(-3, 3)
    param_grid = dict(gamma=list(gamma_range), C=list(C_range))

    # Grid search for C, gamma, 5-fold CV
    print("Tuning hyper-parameters\n")
    clf = GridSearchCV(svm.SVC(), param_grid, cv=5, n_jobs=-2)
    clf.fit(x_train, y_train)
    print("Best parameters set found on development set:\n")
    print(clf.best_estimator_)
    print("\nGrid scores on development set:\n")

    # for params, mean_score, scores in clf.grid_scores_:
    #     print("%0.3f (+/-%0.03f) for %r"
    #           % (mean_score, scores.std() * 2, params))
    n_candidates = len(clf.cv_results_['params'])
    for i in range(n_candidates):
        print(i, 'params - %s; mean - %0.2f; std - %0.2f'
              % (clf.cv_results_['params'][i],
                 clf.cv_results_['mean_test_score'][i],
                 clf.cv_results_['std_test_score'][i]))

    print("\nDetailed classification report:\n")
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.\n")
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred, target_names=get_label()))
    # print(classification_report(y_true, y_pred))


def knn_classifier(x_train, y_train, x_test=None, y_test=None):
    if x_test is None and y_test is None:
        x_train, x_test, y_train, y_test = train_test_split(
            x_train, y_train, test_size=0.2, random_state=6)
        print("Spliting train:{}/test:{} from training data".format(
            len(x_train), len(x_test)))
    param_grid = dict(n_neighbors=[5 * i for i in range(1, 10)])

    # Grid search for C, gamma, 5-fold CV
    print("Tuning hyper-parameters\n")
    clf = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, n_jobs=-2)
    clf.fit(x_train, y_train)
    print("Best parameters set found on development set:\n")
    print(clf.best_estimator_)
    print("\nGrid scores on development set:\n")

    # for params, mean_score, scores in clf.grid_scores_:
    #     print("%0.3f (+/-%0.03f) for %r"
    #           % (mean_score, scores.std() * 2, params))
    n_candidates = len(clf.cv_results_['params'])
    for i in range(n_candidates):
        print(i, 'params - %s; mean - %0.2f; std - %0.2f'
              % (clf.cv_results_['params'][i],
                 clf.cv_results_['mean_test_score'][i],
                 clf.cv_results_['std_test_score'][i]))

    print("\nDetailed classification report:\n")
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.\n")
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred, target_names=get_label()))
    # print(classification_report(y_true, y_pred))


def classifiers(x_train, y_train, x_test=None, y_test=None):
    if x_test is None and y_test is None:
        x_train, x_test, y_train, y_test = train_test_split(
            x_train, y_train, test_size=0.2, random_state=6)
        print("Spliting train:{}/test:{} from training data".format(
            len(x_train), len(x_test)))

    # print(classification_report(y_true, y_pred))
    clf = [DecisionTreeClassifier(),
           RandomForestClassifier(max_features=None, max_depth=None),
           SVC(),
           LogisticRegression(),
           ExtraTreesClassifier(),
           GradientBoostingClassifier(),
           MLPClassifier(activation="relu",
                         alpha=0.001,
                         tol=1e-6,
                         batch_size=135,
                         hidden_layer_sizes=20,
                         solver="adam",
                         learning_rate="constant",
                         max_iter=100)]

    for c in clf:
        print(c)
        print(cross_val_score(c, x_train, y_train))
        c.fit(x_train, y_train)
        y_predicted = c.predict(x_test)

        cm = metrics.confusion_matrix(y_test, y_predicted)
        print(cm)
        print(metrics.classification_report(y_test, y_predicted))
