import pandas as pd

def load_codes(icd_path='generator_837/api/reference_data/icd10.csv', cpt_path='generator_837/api/reference_data/cpt4.csv'):
    icd_df = pd.read_csv(icd_path, usecols=['A00', 'A000'])
    cpt_df = pd.read_csv(cpt_path, usecols=['com.medigy.persist.reference.type.clincial.CPT.code'])
    icd_codes = icd_df['A000'].dropna().tolist()
    cpt_codes = cpt_df['com.medigy.persist.reference.type.clincial.CPT.code'].dropna().tolist()
    return icd_codes, cpt_codes

def load_orgs(org_path='generator_837/api/reference_data/npi_orgs.csv'):
    ## load and silence the warnings 
    orgs_df = pd.read_csv(org_path, low_memory=False)
    return orgs_df

def load_payers(payer_path='generator_837/api/reference_data/payers.csv'):
    payers_df = pd.read_csv(payer_path, low_memory=False)
    payers_df = payers_df[payers_df['ProductType'].str.contains('PPO|POS|HMO')]
    payers_df = payers_df[payers_df['ProductName'].str.len() > 5]
    return payers_df




# ##### FUTURE SECTION NOT YET INCORPORATED ######
# def synthea_data_loader(data_path='patientsSynthetic/docker-simple-example/output/csv/'):
#     patients = pd.read_csv(data_path + 'patients.csv', low_memory=False)
#     conditions = pd.read_csv(data_path + 'conditions.csv', low_memory=False)
#     procedures = pd.read_csv(data_path + 'procedures.csv', low_memory=False)
#     claims = pd.read_csv(data_path + 'claims.csv', low_memory=False)
#     claims_transactions = pd.read_csv(data_path + 'claims_transactions.csv', low_memory=False)
#     return patients, conditions, procedures, claims, claims_transactions

# patients, conditions, procedures, claims, claims_transactions = synthea_data_loader()

# ## print where conditions has a description that contains disorder
# conditions_disorders = conditions[conditions['DESCRIPTION'].str.contains('disorder')]
# conditions_disorders['DESCRIPTION'].value_counts()

# #### the claims_transactions.csv contains the procedure (HCPCS/CPT in snowmed format), and then 
# #### references the claim 
# #### the claims_transactions has a column called 'claim_id' that references the 'id' column in the claims.csv

# ## lets test that
# ## select a random row from claims_transactions
# claim_transaction = claims_transactions.sample(1)
# claim_transaction.columns
# claim_id = claim_transaction['CLAIMID'].values[0]
# claim = claims[claims['Id'] == claim_id]