import pandas as pd

# Importação dos dados originais
data = pd.read_csv('./Data/Raw/Occupancy.csv')

# Deletando valores NaN
data = data.dropna()

# Deletando colunas que não serão usadas
data.drop(['HumidityRatio'], axis=1, inplace=True)

data.to_csv("Data/Processed/Ocuppancy_processed.csv")