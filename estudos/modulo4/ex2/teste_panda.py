import pandas as pd

linhas = []
linhas.append({'Nome': 'Ana', 'Idade': 30})
linhas.append({'Nome': 'Bruno', 'Idade': 25, 'Cidade': 'POA'})

df = pd.DataFrame(linhas)
print(df)
df.to_excel('teste.xlsx', index=False)