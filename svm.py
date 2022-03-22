#Import scikit-learn dataset library
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics
#Load dataset
data = np.load("vec.npy")
label = np.ones(np.shape(data)[0])
label[:15000] = 0
#print("Datashape",np.shape(data))
lens = np.shape(data)[0]
#print("MEAN",np.mean(data,axis=0))
#print("VAR",np.var(data,axis=0))
# Split dataset into training set and test set
lens_lis = np.arange(500,15000,500)
#print(lens_lis)
#exit(0)
#inds = np.random.choice(range(lens),j)
Data = data
#print(np.shape(Data),np.shape(inds),666)
Label = label
X_train, X_test, y_train, y_test= train_test_split(Data,Label, test_size=0.3,shuffle=True) # 70% training and 30% test
print("Train and test shape",np.shape(X_train),np.shape(X_test),np.shape(data))

#Create a svm Classifier
clf = SVC(kernel='rbf') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)
#print(clf.get_params())
#Predict the response for test dataset
y_pred = clf.predict(X_test)
f1 = metrics.f1_score(y_test, y_pred)
#plt.plot(lens_lis,f1s)
#plt.xlabel("number of data point")
#plt.ylabel("f1 score")
#plt.show()
y_filt = np.squeeze(np.argwhere(y_pred==0))
#print(sum(y_pred),sum(y_test))
x_test  = X_test[y_filt,:]
print(np.shape(x_test),np.shape(X_test))
np.save('X_test.npy',x_test)
#data
np.save('X_origin.npy',X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))
print("f1 score:",metrics.f1_score(y_test, y_pred))

#plot_confusion_matrix(clf, X_test, y_test)  
#plt.show()
#exit(0)
tuned_parameters = [
    {"kernel": ["rbf"], "gamma": [1,1e-1,1e-2], "C": [1e-1,1,100]},
]

scores = ["precision", "recall"]

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(), tuned_parameters, scoring="%s_macro" % score)
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_["mean_test_score"]
    stds = clf.cv_results_["std_test_score"]
    for mean, std, params in zip(means, stds, clf.cv_results_["params"]):
        print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()
