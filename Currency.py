import pandas as pd

file = '/Users/alexrives/Downloads/FRB_H10.csv'
df = pd.read_csv(file)

# Renaming the columns:
def columnNames(columnName):
    # Notice that most countries are seperated by a double hyphen
    if '--' in columnName:
        splitName = columnName.split('--')
        return splitName[0].strip().upper()
    if '-' in columnName:
        splitName = columnName.split('-')
        return splitName[1].strip().upper()
    
    splitName = columnName.split(' ')
    return splitName[0].strip().upper()

def rowUnit(rows):
    return rows.split('_Per_')[-1]

df.rename(columns=columnNames, inplace=True)

df = df.transpose()

df[0] = df[0].apply(rowUnit)

df = df.transpose()

Final = df.loc[[0,2,df.index[-1]]]
Final.drop(columns = 'SERIES',inplace=True)
Final = Final.transpose()

Final = Final.astype({14: float})

for index in Final.index:
    if Final.loc[index][0] != 'USD':
        
        currentCountry = Final.loc[index][0]
        newvalue = 1/Final.loc[index][14]
        
        Final.loc[index,0] = 'USD' 
        Final.loc[index,2] = currentCountry
        Final.loc[index,14] = newvalue

print(Final)