# Filtering Noise Using SVM in Process Mining
## Introduction
This repo is the source code of ECE269 project 
## Noise generation
```generate.py``` is the core program to generate 7 types of noise and should be the first to run.
```nums = [210,210,220,220,210,220,210]```
indicates number of different noise which can be defined by the user.
The result will be stores in```repeat.xes```
which is a extension of the original downsampled data ```smaller.xes```. 
## Vector space formation
```main.py``` should be run next to generated the purposed vector space. The result is stores in ```vec.npy```
## Binary classifier
```svm.py``` ```logi.py``` and ```bayes.py``` are three classifiers used in this project. After running```svm.py``` , it will produce classified vector to ```x_test.npy```
## Precision calculation 
```validate.py``` use data from the svm classifier to calculate weighted accuracy.