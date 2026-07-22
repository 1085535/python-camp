import matplotlib.pyplot as plt
import numpy as np

# 1. Put your own data here (numbers between 1 and 10)
my_data = [1, 2,2,2,2,2,2,2, 3, 3, 3,3,3,3,3, 4,4,4,4,4,4,4, 6, 7,7, 9,9,9, 10]

# 2. Set the bar boundaries so they align perfectly with the numbers
bins = np.arange(0.5, 11.5, 1)

# 3. Create the histogram
plt.hist(my_data, bins=bins, edgecolor='black', color='blue')

# 4. FORCE the x-axis to show exactly 1 through 10
plt.xticks(range(1, 11))

# 5. Add labels and show the plot
plt.xlabel('Number of shoes')
plt.ylabel('People')
plt.show()
