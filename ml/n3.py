def neural_network(inp, weights):
    prediction = 0
    for i in range(len(inp)):
        prediction += inp[i] * weights[i]
    return prediction 
out_1 = neural_network( inp= [150, 40], weights= [0.2, 0.3])
out_2 = neural_network( inp= [160, 70], weights= [0.2, 0.3])

print(out_1)
print(out_2)

