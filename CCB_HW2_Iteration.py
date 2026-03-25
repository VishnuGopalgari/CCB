def fibonacci_crn(a, b, steps=12):
    history = []
    for i in range(steps):
        history.append((i, a, b))
        a, b = b, a + b
    history.append((steps, a, b))
    return history

# Test case 1: (0,1)
result1 = fibonacci_crn(0, 1)

# Test case 2: (3,7)
result2 = fibonacci_crn(3, 7)

print("Start (0,1):")
for step, a, b in result1:
    print(f"Step {step}: A={a}, B={b}")

print("\nStart (3,7):")
for step, a, b in result2:
    print(f"Step {step}: A={a}, B={b}")