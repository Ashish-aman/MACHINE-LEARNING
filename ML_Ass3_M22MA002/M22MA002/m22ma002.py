# -*- coding: utf-8 -*-
"""m22ma002.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zl4hb2IBeq4Xzgcx25Nd-we8mG49forW
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import io
import matplotlib.pyplot as plot
from sklearn.metrics import log_loss
from google.colab import files 
# files =files.upload()
from pydrive.auth import GoogleAuth
from google.colab import drive
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

file_id = '1OZmjNH5TrTsRDQfFUYRvuSZNPA0WAE57'
download = drive.CreateFile({'id': file_id})
download.GetContentFile('mnist_train.csv')
df  = pd.read_csv("mnist_train.csv")
# trn_data = pd.read_csv(io.BytesIO(files['input_file.csv']))
trn_data=df
trn_data.head()
# train_df = pd.read_csv("mnist_train.csv")
# train_df.head()

trn_data=np.array(trn_data)
trn_data.shape
row,col=trn_data.shape
print(row)

np.random.shuffle(trn_data)
x_train=trn_data[:,1:col]
y_train=trn_data[:,0]
y_train.shape
print(y_train.size)

trn_x=x_train.T
print(np.max(trn_x))
trn_x=trn_x/255.0
print(np.max(trn_x))
len(y_train.shape)
col_x=trn_data[0]
row_x=trn_data[1:row]

def one_hot_enc(y):
    #return np.array(Y[:] == np.arange(Y.size))
    one_hot_y = np.zeros((y.size, y.max() + 1))
    one_hot_y[np.arange(y.size), y] = 1
    return one_hot_y.T

def init_param(inp_node, hid_node):
    outp_node = len(set(y_train)) #no. of classes
    W1 = np.random.randn(hid_node, inp_node) * np.sqrt(1./hid_node)
    #print(W1.shape)
    b1 = np.random.randn(hid_node, 1)
    print(b1.shape)
    W2 = np.random.randn(outp_node, hid_node) * np.sqrt(1./outp_node)
    b2 = np.random.randn(outp_node, 1)
    
    
    return W1, b1, W2, b2 

init_param(10,10)

#sigmoid fn defining
def sigmoid(z):
    return 1/(1 + np.exp(-z))


def deriv_sig(y):
    
    t1 = 1 - sigmoid(y)
    return sigmoid(y) * t1
#defining softmax fn
import math
def softmax(y):
    exps = np.exp(y - y.max())
    return exps / np.sum(exps, axis = 0)

#forward propagation defining
import math
def frwd_prop(w1, b1, w2, b2, x):
    print(w1.shape)
    print(b1.shape)
    z1 = np.matmul(w1, x) + b1
    #print(Z1.shape)
    a1 = sigmoid(z1)
    z2 = np.matmul(w2, a1) + b2
    a2 = softmax(z2) 
    return z1 , a1, z2, a2


#defining backward fn
def back_prop(Z1, A1, Z2, A2, W1, b1, W2, b2, X, Y, learning_rate):
    one_hot_encoded_Y = one_hot_enc(Y)
    dZ2 = A2 - one_hot_encoded_Y
    #print(dZ2)
    dW2 = 1/ Y.size * np.matmul(dZ2, A1.T)
    db2 = 1/ Y.size * np.sum(dZ2, axis = 1, keepdims = True)
    
    dA1 = np.matmul(W2.T, dZ2)
    dZ1 = dA1 * deriv_sig(Z1)
    
    dW1 = 1/ Y.size * np.matmul(dZ1, X.T)
    db1 = 1/ Y.size * np.sum(dZ1, axis = 1, keepdims = True)
    #print(db1.shape)
    W1 = W1 - learning_rate *dW1
    b1 = b1 - learning_rate *db1
    #print(b1.shape)
    W2 = W2 - learning_rate *dW2
    b2 = b2 - learning_rate *db2
    
    #return dW1, db1, dW2, db2
    return W1, b1, W2, b2, one_hot_encoded_Y

#predicted value of output defining 
def pred(out_prb):
  return np.argmax(out_prb,0)

#defining accuracy of the model
def accuracy(y_pred,y):
  sum=np.sum(y_pred == y)
  return sum/row

#defining loss fn of the model
def crossentrp_los(out_prb,y):
   sum = np.sum(np.multiply(y, np.log(out_prb)))
   r = y.shape[0]
   return -(1./(r * 10000)) * sum

#gradient descent optimiser fn
def train_gradoptimiser(X, Y, epoch, learning_rate, W1, b1, W2, b2):
    
    best_accuracy = 0
    old_loss = 0
    loss = 0
    acc_ls = []
    loss_ls = []
    for i in range(epoch):
        Z1, A1, Z2, A2 = frwd_prop(W1, b1, W2, b2, X)
        print("Z1 is ",Z1)
        Y_predicted = pred(A2)
        acc = accuracy(Y_predicted, Y)
        #print(set(Y_predicted))
        
        W1, b1, W2, b2, one_hot_encoded_Y = back_prop(Z1, A1, Z2, A2, W1, b1, W2, b2, X, Y, learning_rate)
        
        old_loss = loss
        #loss = crossentropy_loss(A2, Y)
        loss = crossentrp_los(A2, one_hot_encoded_Y)
        #loss = log_loss(Y, A2)
        loss_ls.append(loss)
        acc_ls.append(acc)
        
        if i % 50 == 0 or i == epoch-1:
            print(("Epoch {}: Accuracy = {:.2f}, Loss = {:.3f}").format(i, acc, loss))
            
        #best_accuracy = max(best_accuracy, acc)
        #if(loss < old_loss):
        #    print(("Epoch {}: Accuracy = {:.2f}, Loss = {:.3f}").format(i, acc, loss))
        #    break
        #if(acc < best_accuracy): 
        #   print(("Epoch {}: Accuracy = {:.2f}, Loss = {:.3f}").format(i, acc, loss))
        #   break 
        #params = {"W1" : W1, "b1" : b1, "W2": W2, "b2": b2}
    
    #print(best_accuracy)
    return W1, b1, W2, b2, A2, acc_ls, loss_ls

#input nodes of neurons
N = 784
#neurons in hidden layer  
H = 10   
#no. of epochs
E = 1000 
#learning rate of the back propagation 
n = 0.1  

W1, b1, W2, b2 = init_param(N, H)
Z1, A1, Z2, A2 = frwd_prop(W1, b1, W2, b2, trn_x)
#print(Z1,A1,Z2,A2)
W1, b1, W2, b2, one_hot_encoded_Y = back_prop(Z1, A1, Z2, A2, W1, b1, W2, b2, trn_x, y_train, n)

Z1, A1, Z2, A2 = frwd_prop(W1, b1, W2, b2, trn_x)
#print(Z1,A1,Z2,A2)
W1, b1, W2, b2, one_hot_encoded_Y = back_prop(Z1, A1, Z2, A2, W1, b1, W2, b2, trn_x, y_train, n)
W1, b1, W2, b2, A2, acc_ls, loss_ls = train_gradoptimiser(trn_x, y_train, E, n, W1, b1, W2, b2)

H_list = [10, 10, 20, 2, 4]
n_list = [0.01, 0.1, 0.02, 0.01, 0.5]
E_list = [20, 50, 50, 10, 25]
for i in range(5):
    W1, b1, W2, b2 = init_param(N, H_list[i])
    print(("Epoch = {}, N = {}, H = {}, learning_rate = {}").format(E_list[i], N, H_list[i], n_list[i]))
     
    W1, b1, W2, b2, A2, acc_list, loss_list = train_gradoptimiser(trn_x, y_train, E_list[i], n_list[i], W1, b1, W2, b2)
    
    print(W1)
    print(b1)
    print(W2)
    print(b2)
    
    plot.plot(range(E_list[i]), acc_list)
    #plot.ylim(0,0.5)
    plot.title("Accuracy vs Epoch")
    plot.show()
    
    plot.plot(range(E_list[i]), loss_list)
    #plot.ylim(0, 5)
    plot.title("Loss vs Epoch")
    plot.show()