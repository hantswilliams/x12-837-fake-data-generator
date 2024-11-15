import pandas as pd 

# og file 
df = pd.read_csv('reference_codexes/npis_complete.csv')

## keep only where Entity Type Code is 2.0 
df = df[df['Entity Type Code'] == 2.0]

## keep only rows that contain '282N00000X' for 'Healthcare Provider Taxonomy Code_1' column 
df = df[df['Healthcare Provider Taxonomy Code_1'].str.contains('282N00000X')]

## save 
df.to_csv('reference_codexes/npi_orgs.csv', index=False)