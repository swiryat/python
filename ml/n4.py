def neural_network(inp, weights):
    
    prediction = [0] * len(weights) 
    
    for i in range(len(weights)):
        ws = 0
        for j  in range(len(inp)):
            ws += inp[j] * weights[i] [j]
        prediction[i] = ws 
    return prediction

inp = [50, 165, 10]             

weights_1 = [0.2, 0.1, 0.05]
weights_2 = [0.3, 0.1, 0.05]    
weights_3 = [0.3, 0.1, 0.05]

weights = [weights_1, weights_2, weights_3]
print(neural_network(inp, weights))