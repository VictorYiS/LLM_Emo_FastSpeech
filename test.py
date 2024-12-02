import numpy as np
from sklearn.preprocessing import StandardScaler

# Sample data
data = np.array([[1, 2], [3, 4], [5, 6]])

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler to the data and transform it
scaled_data = scaler.fit_transform(data)

print(scaled_data)