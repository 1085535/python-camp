
a = 0
b = 1


print("Fibonacci number 1:", a)
print("Fibonacci number 2:", b)

# Loop 49 times to generate the remaining 98 numbers (2 per loop)
for i in range(3, 101, 2):
    # Add them and store the result in the first variable
    a = a + b
    print(f"Fibonacci number {i}:", a)
    
    # Add them again and store the result in the second variable
    b = a + b
    print(f"Fibonacci number {i + 1}:", b)
