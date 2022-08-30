import pandas as pd
    
data_file = 'ProjStats.csv'

df = pd.read_csv(data_file, skipinitialspace=True,  encoding= 'unicode_escape')

df["Pos"] = df["PLAYER"].str.split().str[-2:-1].str.join(sep=" ")

positions = ['QB', 'RB', 'WR', 'TE', 'K', 'FB']
df.loc[~df['Pos'].isin(positions), 'Pos'] = 'DEF' 
df["PLAYER"] = df["PLAYER"].str.split().str[0:2].str.join(sep=" ")

df.loc[df['PLAYER'] == "Kyle Juszczyk", 'Pos'] = 'RB'
df.loc[df['PLAYER'] == "Tory Carter", 'Pos'] = 'RB'
df.loc[df['PLAYER'] == "Patrick Ricard", 'Pos'] = 'RB'
df.loc[df['PLAYER'] == "Paul Quessenberry", 'Pos'] = 'TE'

df.rename(columns = {'PLAYER':'Name', 'FPTS':'FPTs'}, inplace = True)

df.loc[df['Pos'] != 'QB', 'Pos'] = df['Pos'].astype(str) + '/FLEX'
df = df.drop('Pos', axis=1).join(df['Pos'].str.split('/', expand=True).stack().reset_index(level=1, drop=True).rename('Pos')).reset_index(drop=True)

df.to_csv("jackProj.csv")
