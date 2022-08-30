import pulp
import pandas as pd
from pandas.api.types import CategoricalDtype
    
data_file = 'jackProj.csv'

df = pd.read_csv(data_file, index_col=['Name', 'Pos'], skipinitialspace=True)

totalMoney = 0
totalPoints = 0

legal_assignments = df.index   
name_set = df.index.unique(0)  

#costs = df['Salary'].to_dict()
values = df['FPTs'].to_dict()

# set up LP
draft = pulp.LpVariable.dicts('selected', legal_assignments, cat='Binary')

prob = pulp.LpProblem('Draft_Kings_Showdown', pulp.LpMaximize)

# obj
prob += pulp.lpSum([draft[n, p]*values[n,p] for (n, p) in legal_assignments])

'''
# salary cap
prob += pulp.lpSum([draft[n, p]*costs[n,p] for (n, p) in legal_assignments]) <= 50000
'''



# pick 1 RB
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'RB']) == 2

# pick 2 WR
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'WR']) == 2

# pick 1 QB
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'QB']) == 1

# pick 1 TE
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'TE']) == 1

# pick 1 DEF
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'DEF']) == 1

# pick 1 FLEX
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'FLEX']) == 1

# pick 1 K
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'K']) == 1


removeNames = [] #Add names that were already picked from the draft that aren't on your team.

for names in removeNames:
    prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if n == names]) == 0


addedNames = [] #Add names that are currently on your team.
for names in addedNames:
    prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if n == names]) == 1

prob += pulp.lpSum([draft[n, p]*values[n,p] for (n, p) in legal_assignments]) <= 50000

for name in name_set:
    prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if n == name]) <=1
    

prob.solve()

lineup = []

for idx in draft:
    if draft[idx].varValue:
        lineup.append({
                        'Name': idx[0],
                        'Pos': idx[1],
                        'FPTs': values[idx]
                })
        
lineups = pd.DataFrame(lineup)
totalPoints = lineups['FPTs'].sum()
positions = ['QB', 'RB', 'WE', 'TE', 'FLEX', 'DEF', 'K']
cat_size_order = CategoricalDtype(
    ['QB', 'RB', 'WR', 'TE', 'FLEX', 'DEF', 'K'], 
    ordered=True
)
lineups = lineups.reset_index(drop=True)
lineups['Pos'] = lineups['Pos'].astype(cat_size_order)
lineups['FPTs'] = lineups['FPTs'].astype(float)
lineups = lineups.sort_values(by=['Pos'])
print(lineups)
        
#print("Total used amount of salary cap:", totalMoney, "Amount remaining: ", 50000 - totalMoney)

totalWR = lineups.loc[lineups['Pos'] == 'WR', 'FPTs'].sum()
totalRB = lineups.loc[lineups['Pos'] == 'RB', 'FPTs'].sum()
totalFlex = lineups.loc[lineups['Pos'] == 'FLEX', 'FPTs'].sum()
print()
print("Running Back point total: ", totalRB)
print("Wide Receiver point total: ", totalWR)
print("Running Back point total with flex: ", totalRB + totalFlex)
print("Wide Receiver point total with flex: ", totalWR + totalFlex)
print("Projected points for the season: ", round(totalPoints, 2))

