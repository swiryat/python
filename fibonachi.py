import matplotlib.pyplot as plt

# Function to calculate Fibonacci numbers
def fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Calculate the first 100 Fibonacci numbers
fib_sequence = fibonacci(100)

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, 101), fib_sequence, marker='o', linestyle='-')
plt.title('First 100 Fibonacci Numbers')
plt.xlabel('Index')
plt.ylabel('Fibonacci Number')
plt.grid(True)
plt.show()