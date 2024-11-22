# Addresses 
## https://github.com/uva-bi-sdad/national_address_database/blob/main/README.md

import pandas as pd

## function to select random row from df_fips, then select a random county from that row
def random_location():
    ## read txt file from URL on github: https://raw.githubusercontent.com/uva-bi-sdad/national_address_database/refs/heads/main/data/counties.txt
    url = "https://raw.githubusercontent.com/uva-bi-sdad/national_address_database/refs/heads/main/data/counties.txt"
    df_fips = pd.read_csv(url, sep="\t", header=None)
    row = df_fips.sample(1)
    county = row.iloc[0, 0]
    ## read csv file from URL on github:
    df = pd.read_csv(f'https://github.com/uva-bi-sdad/national_address_database/raw/main/data/address/{county}', dtype={'GEOI20':object})
    output = df.sample(1)
    ## if df['address'] is empty or NaN, then select another random row and keep doing it until df['address'] is not empty
    while output['address'].empty or pd.isnull(output['address'].values[0]):
        row = df_fips.sample(1)
        county = row.iloc[0, 0]
        df = pd.read_csv(f'https://github.com/uva-bi-sdad/national_address_database/raw/main/data/address/{county}', dtype={'GEOI20':object})
        output = df.sample(1)
    ## return the output
    return output




