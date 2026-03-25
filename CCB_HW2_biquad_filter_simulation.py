def biquad_filter_simulation(inputs):
    # Store previous values (delay line)
    delay = [0, 0, 0, 0]   # represents X[n-1], X[n-2], X[n-3], X[n-4]
    
    outputs = []
    
    for cycle, x in enumerate(inputs):
        # Compute output (1/8 scaling)
        y = (x + sum(delay)) / 8.0
        
        outputs.append(y)
        
        print(f"Cycle {cycle+1}:")
        print(f"Input X = {x}")
        print(f"Delay state = {delay}")
        print(f"Output Y = {y}")
        print("----------------------")
        
        # Update delay line (shift right)
        delay = [x] + delay[:-1]
    
    return outputs


# Given input sequence
inputs = [100, 5, 500, 20, 250]

# Run simulation
outputs = biquad_filter_simulation(inputs)

print("\nFinal Outputs:", outputs)