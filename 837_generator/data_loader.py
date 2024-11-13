import pandas as pd

def load_codes(icd_path='codexes/icd10.csv', cpt_path='codexes/cpt4.csv'):
    icd_df = pd.read_csv(icd_path, usecols=['A00', 'A000'])
    cpt_df = pd.read_csv(cpt_path, usecols=['com.medigy.persist.reference.type.clincial.CPT.code'])
    icd_codes = icd_df['A000'].dropna().tolist()
    cpt_codes = cpt_df['com.medigy.persist.reference.type.clincial.CPT.code'].dropna().tolist()
    return icd_codes, cpt_codes
