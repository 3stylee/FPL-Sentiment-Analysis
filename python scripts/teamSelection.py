import pulp
import pandas as pd

# Load player data (assuming a CSV file with columns: Name, Team, Position, Price, ExpectedPoints)
df = pd.read_csv("players.csv")

# Define the problem
problem = pulp.LpProblem("FPL_Team_Selection", pulp.LpMaximize)

# Decision variables (1 if player is selected, 0 otherwise)
players = df["Name"].tolist()
x = pulp.LpVariable.dicts("x", players, cat="Binary")

# Objective: Maximize total expected points
problem += pulp.lpSum(df.loc[df["Name"] == p, "ExpectedPoints"].values[0] * x[p] for p in players)

# Constraints
## Budget Constraint
problem += pulp.lpSum(df.loc[df["Name"] == p, "Price"].values[0] * x[p] for p in players) <= 100.0

## Squad Size Constraint
problem += pulp.lpSum(x[p] for p in players) == 15

## Positional Constraints
positions = {"GK": 2, "DEF": 5, "MID": 5, "FWD": 3}
for pos, count in positions.items():
    problem += pulp.lpSum(x[p] for p in players if df.loc[df["Name"] == p, "Position"].values[0] == pos) == count

## Team Constraints (max 3 players per club)
teams = df["Team"].unique()
for team in teams:
    problem += pulp.lpSum(x[p] for p in players if df.loc[df["Name"] == p, "Team"].values[0] == team) <= 3

# Solve the problem
problem.solve()

# Extract selected players
selected_players = [p for p in players if pulp.value(x[p]) == 1]

# Print results
print("Optimal Team Selection:")
print(df[df["Name"].isin(selected_players)][["Name", "Team", "Position", "Price", "ExpectedPoints"]])