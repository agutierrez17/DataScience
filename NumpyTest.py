import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_curve, auc

a = np.arange(6)
a2 = a[np.newaxis, :]
print(a2.shape)

# Create an array
a = np.array([1,2,3,4,5,6])
a2 = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print(a)
print(a[0])
print(a2[0])

# Create an array of zeroes
print(np.zeros(2))

# Create an array of ones (specify data type as int)
print(np.ones(2, dtype=np.int64))

# Create an empty array with 2 elements
print(np.empty(2))

# Create an array with a range of elements
print(np.arange(4))

# Create an array that contains a range of evenly spaced intervals
# First number, last number, step size
print(np.arange(2,9,2))

# Create an array with values that are spaced linearly in a specified interval
print(np.linspace(0,10, num=5))

# Sort an array
arr = np.array([2,1,5,3,7,4,6,8])
print(np.sort(arr))

# Concatenate two arrays
a = np.array([1,2,3,4])
b = np.array([5,6,7,8])
print(np.concatenate((a,b)))

# Concatenate two arrays
a = np.array([[1,2],[3,4]])
b = np.array([[5,6]])
print(np.concatenate((a,b),axis=0))

array = np.array([[[0,1,2,3],[4,5,6,7]],
                  [[0,1,2,3],
                   [4,5,6,7]],
                  [[0,1,2,3],
                   [4,5,6,7]]])

# Find the number of dimensions for the array
print(array.ndim)

# Find the number of elements in the array
print(array.size)

# Find the shape of your array
print(array.shape)

# Reshape your array
a = np.arange(6)
b = a.reshape(3,2)
print(b)
print(np.reshape(a, newshape=(1, 6), order='C'))

# Add a new axis to an array
a = np.array([1,2,3,4,5,6])
a2 = a[np.newaxis,:]
print(a2.shape)

# Convert 1-dimension array to row vector
row_vector = a[np.newaxis, :]
print(row_vector.shape)

# Convert 1-dimension array to column vector
col_vector = a[:, np.newaxis]
print(col_vector.shape)

# Expand an array, add a new axis at specified position
a = np.array([1,2,3,4,5,6])
b = np.expand_dims(a, axis=1)
print(b.shape)



