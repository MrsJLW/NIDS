
# coding: utf-8

# In[1]:


# Here are some imports that are used along this notebook
import math
import itertools
import pandas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time
from collections import OrderedDict
import glob
get_ipython().magic('matplotlib inline')
gt0 = time()


# In[2]:


train20_nsl_kdd_dataset_path = "C:/Users/user/MSDS/Capstone/NSL_KDD-master/NSL_KDD-master/KDDTrain+_20Percent.txt"
train_nsl_kdd_dataset_path = "C:/Users/user/MSDS/Capstone/NSL_KDD-master/NSL_KDD-master/KDDTrain+.txt"
test_nsl_kdd_dataset_path = "C:/Users/user/MSDS/Capstone/NSL_KDD-master/NSL_KDD-master/KDDTest+.txt"

col_names = np.array(["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","labels","attrib43"])


nominal_inx = [1, 2, 3]
binary_inx = [6, 11, 13, 14, 20, 21]
numeric_inx = list(set(range(41)).difference(nominal_inx).difference(binary_inx))

nominal_cols = col_names[nominal_inx].tolist()
binary_cols = col_names[binary_inx].tolist()
numeric_cols = col_names[numeric_inx].tolist()

# Dictionary that contains mapping of various attacks to the four main categories
attack_dict = {
    'normal': 'normal',
    
    'back': 'DoS',
    'land': 'DoS',
    'neptune': 'DoS',
    'pod': 'DoS',
    'smurf': 'DoS',
    'teardrop': 'DoS',
    'mailbomb': 'DoS',
    'apache2': 'DoS',
    'processtable': 'DoS',
    'udpstorm': 'DoS',
    
    'ipsweep': 'Probe',
    'nmap': 'Probe',
    'portsweep': 'Probe',
    'satan': 'Probe',
    'mscan': 'Probe',
    'saint': 'Probe',

    'ftp_write': 'R2L',
    'guess_passwd': 'R2L',
    'imap': 'R2L',
    'multihop': 'R2L',
    'phf': 'R2L',
    'spy': 'R2L',
    'warezclient': 'R2L',
    'warezmaster': 'R2L',
    'sendmail': 'R2L',
    'named': 'R2L',
    'snmpgetattack': 'R2L',
    'snmpguess': 'R2L',
    'xlock': 'R2L',
    'xsnoop': 'R2L',
    'worm': 'R2L',
    
    'buffer_overflow': 'U2R',
    'loadmodule': 'U2R',
    'perl': 'U2R',
    'rootkit': 'U2R',
    'httptunnel': 'U2R',
    'ps': 'U2R',    
    'sqlattack': 'U2R',
    'xterm': 'U2R'
}


# In[3]:


def _label2(x):
    if x['labels'] == 'normal':
        return 'normal'
    else:
        return 'attack'

def returnvalue(x):
    return attack_dict.get(x['labels'])


# In[4]:


df_kdd_dataset_train = pd.read_csv(train20_nsl_kdd_dataset_path, index_col=None, header=0, names=col_names)
df_kdd_dataset_train['label2'] = df_kdd_dataset_train.apply(_label2,axis=1)
df_kdd_dataset_train['label3'] = df_kdd_dataset_train.apply(returnvalue,axis=1)


# In[5]:


from sklearn import preprocessing
le = preprocessing.LabelEncoder()

# 2/3. FIT AND TRANSFORM
# use df.apply() to apply le.fit_transform to all columns
df_kdd_dataset_train_tranformed = df_kdd_dataset_train.apply(le.fit_transform)
df_kdd_dataset_train_tranformed.head()
df_kdd_dataset_train_saved = df_kdd_dataset_train_tranformed


# In[59]:


def one_hot_encode(x, n_classes):
    """
    One hot encode a list of sample labels. Return a one-hot encoded vector for each label.
    : x: List of sample Labels
    : return: Numpy array of one-hot encoded labels
     """
    return np.eye(n_classes)[x]


# In[60]:


y = df_kdd_dataset_train['label2']
print(y[1])
le.fit(y)
y = le.transform(y)
print(y)
y = one_hot_encode(y,2)
print(y)


# In[6]:


df_kdd_dataset_train_tranformed.drop('labels', axis=1, inplace=True)
df_kdd_dataset_train_tranformed.drop('attrib43',axis=1,inplace=True)
df_kdd_dataset_train_tranformed.drop('label2',axis=1,inplace=True)
df_kdd_dataset_train_tranformed.drop('label3',axis=1,inplace=True)

enc = preprocessing.OneHotEncoder(categorical_features=[1, 2, 3])

# 2. FIT
enc.fit(df_kdd_dataset_train_tranformed)

# 3. Transform
onehotlabels = enc.transform(df_kdd_dataset_train_tranformed).toarray()
onehotlabels.shape


# In[7]:


import csv
csvfile = "C:/Users/user/MSDS/Capstone/NSL_KDD-master/NSL_KDD-master/output.txt"

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in onehotlabels:
        writer.writerow([val])   


# In[8]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_train_transform = scaler.fit_transform(onehotlabels)


# In[9]:


print(df_train_transform.shape[0])


# In[31]:


# create the training set with labels
df_train_transform_with_label = np.hstack((df_train_transform,y.T))


# In[62]:


y = np.array(y)


# In[63]:


print(y.shape)


# In[66]:


print(y.shape)
df_train_transform_with_label=np.c_[df_train_transform,y]
print(df_train_transform_with_label.shape)


# In[10]:


def get_next_batch(i,batch_size):
    start = i*batch_size
    end = (i+1)*batch_size
    return df_train_transform[start:end]


# In[38]:


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Import MNIST data
nisd_data_set = df_train_transform

# Parameters
learning_rate = 0.01
training_epochs = 20
batch_size = 55
display_step = 1
examples_to_show = 10

# Network Parameters
n_hidden_1 = 55 # 1st layer num features
n_hidden_2 = 25 # 2nd layer num features
n_input = 118 # Number of features

# tf Graph input (only pictures)
X = tf.placeholder("float", [None, n_input])
autoencoder_op = tf.placeholder("float", [None, n_input])

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'encoder_h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'decoder_h1': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_1])),
    'decoder_h2': tf.Variable(tf.random_normal([n_hidden_1, n_input])),
}
biases = {
    'encoder_b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'encoder_b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'decoder_b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'decoder_b2': tf.Variable(tf.random_normal([n_input])),
}


# Building the encoder
def encoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   biases['encoder_b1']))
    # Encoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']),
                                   biases['encoder_b2']))
    print('encoder')
    return layer_2


# Building the decoder
def decoder(x):
    # Decoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']),
                                   biases['decoder_b1']))
    # Decoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']),
                                   biases['decoder_b2']))
    print('decoder')
    return layer_2

# Construct model
encoder_op = encoder(X)
decoder_op = decoder(encoder_op)
    
model_path = "C:\\users\\user\MSDS\\Capstone\\Models"

# Prediction
y_pred = decoder_op
# Targets (Labels) are the input data.
y_true = X

# Define loss and optimizer, minimize the squared error
cost = tf.reduce_mean(tf.pow(y_true - y_pred, 2))
optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(cost)
# Initializing the variables
init = tf.global_variables_initializer()
saver = tf.train.Saver()
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    total_batch = int(df_train_transform.shape[0]/batch_size)
    # Training cycle
    for epoch in range(training_epochs):
        # Loop over all batches
        for i in range(total_batch):
            batch_xs = get_next_batch(i,batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={X: batch_xs}) 
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1),
                  "cost=", "{:.9f}".format(c))            
    print("Optimization Finished!")
    c2,dec_op2 = sess.run([cost,decoder_op], feed_dict={X: df_train_transform}) 
    save_path = saver.save(sess,model_path)
    # model has been trained pass the training data with labels
    cost_train,dec_op_train_label = sess.run([cost,decoder_op], feed_dict={X: df_train_transform_with_label}) 


# In[39]:


def get_next_batch_label(i,batch_size):
    start = i*batch_size
    end = (i+1)*batch_size
    return df_train_transform_with_label[start:end]


# In[41]:


# Parameters
learning_rate = 0.01
training_epochs = 20
batch_size = 55
display_step = 1
examples_to_show = 10

# Network Parameters
n_hidden_1 = 55 # 1st layer num features
n_hidden_2 = 25 # 2nd layer num features
n_input = 119 # Number of features

# tf Graph input (only pictures)
X = tf.placeholder("float", [None, n_input])
autoencoder_op = tf.placeholder("float", [None, n_input])

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'encoder_h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'decoder_h1': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_1])),
    'decoder_h2': tf.Variable(tf.random_normal([n_hidden_1, n_input])),
}
biases = {
    'encoder_b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'encoder_b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'decoder_b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'decoder_b2': tf.Variable(tf.random_normal([n_input])),
}


# Building the encoder
def encoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   biases['encoder_b1']))
    # Encoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']),
                                   biases['encoder_b2']))
    print('encoder')
    return layer_2


# Building the decoder
def decoder(x):
    # Decoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']),
                                   biases['decoder_b1']))
    # Decoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']),
                                   biases['decoder_b2']))
    print('decoder')
    return layer_2

# Construct model
encoder_op = encoder(X)
decoder_op = decoder(encoder_op)
    
model_path = "C:\\users\\user\MSDS\\Capstone\\Models"

# Prediction
y_pred = decoder_op
# Targets (Labels) are the input data.
y_true = X

# Define loss and optimizer, minimize the squared error
cost = tf.reduce_mean(tf.pow(y_true - y_pred, 2))
optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(cost)
# Initializing the variables
init = tf.global_variables_initializer()
saver = tf.train.Saver()
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    total_batch = int(df_train_transform_with_label.shape[0]/batch_size)
    # Training cycle
    for epoch in range(training_epochs):
        # Loop over all batches
        for i in range(total_batch):
            batch_xs = get_next_batch_label(i,batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={X: batch_xs}) 
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1),
                  "cost=", "{:.9f}".format(c))            
    print("Optimization Finished!")
    cost_train,dec_op_train_label = sess.run([cost,decoder_op], feed_dict={X: df_train_transform_with_label}) 
    save_path = saver.save(sess,model_path)
    # model has been trained pass the training data with labels
    


# In[42]:


print(dec_op_train_label.shape)


# In[ ]:





# In[70]:


def get_next_batch_sftmax(i,batch_size):
    start = i*batch_size
    end = (i+1)*batch_size
    return df_train_transform_with_label[start:end,0:118],df_train_transform_with_label[start:end,118:120]


# In[71]:


## Now we build the softmax regressor

# Parameters
learning_rate = 0.01
training_epochs = 25
batch_size = 55
display_step = 1

# tf Graph Input
x = tf.placeholder(tf.float32, [None, 118]) # 118 features
y = tf.placeholder(tf.float32, [None, 2]) # 0-9 digits recognition => 10 classes

# Set model weights
W = tf.Variable(tf.zeros([118, 2]))
b = tf.Variable(tf.zeros([2]))

# Construct model
pred = tf.nn.softmax(tf.matmul(x, W) + b) # Softmax

# Minimize error using cross entropy
cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
# Gradient Descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(df_train_transform_with_label.shape[0]/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = get_next_batch_sftmax(i,batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                          y: batch_ys})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    print("Optimization Finished!")

    


# In[ ]:



