import pandas as pd
import matplotlib.pyplot as plt

data = {
    "player": ["Beginner", "Intermediate", "Advanced"],
    # number of wins
    "RandAI": [3,0,0],
    "ABPrun": [5,3,2]
}


df = pd.DataFrame(data)         # create data flame
plt.plot(df['player'], df['RandAI'], label='Random AI', color='blue', marker='o')
plt.plot(df['player'], df['ABPrun'], label='Alpha-Beta Pruning', color='green', marker='o')

# title and shaft label
plt.title("Comparing AI")
plt.xlabel('player')
plt.ylabel('Win times')

plt.legend()

plt.show()