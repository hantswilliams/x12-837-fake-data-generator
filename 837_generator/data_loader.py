import pandas as pd

def load_codes(icd_path='reference_codexes/icd10.csv', cpt_path='reference_codexes/cpt4.csv'):
    icd_df = pd.read_csv(icd_path, usecols=['A00', 'A000'])
    cpt_df = pd.read_csv(cpt_path, usecols=['com.medigy.persist.reference.type.clincial.CPT.code'])
    icd_codes = icd_df['A000'].dropna().tolist()
    cpt_codes = cpt_df['com.medigy.persist.reference.type.clincial.CPT.code'].dropna().tolist()
    return icd_codes, cpt_codes

def load_orgs(org_path='reference_codexes/npi_orgs.csv'):
    ## load and silence the warnings 
    orgs_df = pd.read_csv(org_path, low_memory=False)
    return orgs_df


def load_payers(payer_path='reference_codexes/payers.csv'):
    payers_df = pd.read_csv(payer_path, low_memory=False)
    payers_df = payers_df[payers_df['ProductType'].str.contains('PPO|POS|HMO')]
    payers_df = payers_df[payers_df['ProductName'].str.len() > 5]
    return payers_df