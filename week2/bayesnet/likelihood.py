from model import model

# Calculate probability for a given observation
probability = model.probability([["light", "yes", "on time", "attend"]])

print(probability)
