import matplotlib.pyplot as plt
import numpy as np

# Generate 1000 random data points
data = np.random.randn(1000)

# Create the histogram
plt.hist(data, bins=30, edgecolor='black', color='skyblue')

# Add labels and a title
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Basic Histogram Example')

# Display the plot
plt.show()
