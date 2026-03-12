import math

def update_ability(ability, difficulty, correct):

    predicted = 1 / (1 + math.exp(difficulty - ability))

    actual = 1 if correct else 0

    learning_rate = 0.1

    ability = ability + learning_rate * (actual - predicted)

    ability = max(0.1, min(1.0, ability))

    return ability