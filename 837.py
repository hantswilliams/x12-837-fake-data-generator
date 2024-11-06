import random
import datetime
from faker import Faker
import os
import pandas as pd

# Initialize Faker
fake = Faker()

# Load ICD-10 and CPT codes from CSV files
icd_df = pd.read_csv('codexes/icd10.csv', usecols=['A00', 'A000'])
cpt_df = pd.read_csv('codexes/cpt4.csv', usecols=['com.medigy.persist.reference.type.clincial.CPT.code'])

# Convert ICD and CPT codes to lists for random selection
ICD_CODES = icd_df['A000'].dropna().tolist()
CPT_CODES = cpt_df['com.medigy.persist.reference.type.clincial.CPT.code'].dropna().tolist()

# Function to generate random digits with a fixed length
def random_digits(length):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# Generate the ISA Header
def generate_isa():
    return f"ISA*00*          *00*          *ZZ*FAKE837SEND *ZZ*FAKE837RECV *{datetime.datetime.now().strftime('%y%m%d')}*{datetime.datetime.now().strftime('%H%M')}*U*00401*{random_digits(9)}*0*P*:~"

# Generate the GS Segment
def generate_gs():
    return f"GS*HC*FAKE837SEND*FAKE837RECV*{datetime.datetime.now().strftime('%Y%m%d')}*{datetime.datetime.now().strftime('%H%M')}*1*X*005010X222A1~"

# Generate the ST Segment (Transaction Set Header)
def generate_st():
    return f"ST*837*{random_digits(9)}*005010X222A1~"

# Generate the BHT Segment
def generate_bht():
    return f"BHT*0019*00*{random_digits(9)}*{datetime.datetime.now().strftime('%Y%m%d')}*{datetime.datetime.now().strftime('%H%M')}*CH~"

# Generate the NM1 Segment (for example, Billing Provider or Patient)
def generate_nm1(entity_id, entity_type, name, npi):
    return f"NM1*{entity_id}*{entity_type}*{name}*****XX*{npi}~"

# Generate the CLM Segment (Claim Information) with POS Code and claim amount
def generate_clm():
    pos_code = random.choice(["11", "21", "22"])  # Office, Inpatient, Outpatient
    claim_amount = random.randint(200, 1000)
    return f"CLM*{random_digits(10)}*{claim_amount}***{pos_code}:B:1*Y*A*Y*I~"

# Generate the HI Segment (Health Care Diagnosis Codes) with multiple ICD codes
def generate_hi():
    icd_codes = random.sample(ICD_CODES, random.randint(1, 3))  # 1 to 3 ICD codes
    hi_segments = [f"HI*ABK:{code}~" for code in icd_codes]
    return hi_segments

# Generate the SV1 Segment (Professional Service) with CPT codes, Modifiers, and Service Date
def generate_sv1():
    cpt_code = random.choice(CPT_CODES)
    modifier = random.choice(["", "LT", "RT"])  # Left, Right, or no modifier
    charge_amount = random.randint(100, 500)
    date_of_service = fake.date_this_year().strftime("%Y%m%d")
    return f"SV1*HC:{cpt_code}{modifier}*{charge_amount}*UN*1***{date_of_service}~"

# Generate multiple service lines for a claim
def generate_service_lines():
    return [generate_sv1() for _ in range(random.randint(1, 15))]  # 1 to 15 service lines

# Generate the PAT Segment (Patient Information)
def generate_pat():
    relationship_code = random.choice(["19", "01", "18"])  # Self, Spouse, Child
    return f"PAT*{relationship_code}~"

# Generate the SE Segment (Transaction Set Trailer)
def generate_se(segment_count):
    return f"SE*{segment_count}*{random_digits(9)}~"

# Generate the GE and IEA Trailers
def generate_ge():
    return "GE*1*1~"

def generate_iea():
    return f"IEA*1*{random_digits(9)}~"

# Main function to assemble the 837 file
def generate_837():
    provider_name = fake.company()
    provider_npi = random_digits(10)
    patient_name = fake.name()
    patient_npi = random_digits(10)
    
    segments = []
    segments.append(generate_isa())
    segments.append(generate_gs())
    segments.append(generate_st())
    segments.append(generate_bht())
    segments.append(generate_nm1("85", "2", provider_name, provider_npi))  # Billing Provider
    segments.append(generate_nm1("IL", "1", patient_name, patient_npi))  # Patient
    segments.append(generate_clm())
    
    # Add multiple HI segments for diagnoses
    hi_segments = generate_hi()
    segments.extend(hi_segments)
    
    # Add service lines
    segments.extend(generate_service_lines())
    
    segments.append(generate_pat())
    segments.append(generate_se(len(segments) + 2))
    segments.append(generate_ge())
    segments.append(generate_iea())
    
    return '\n'.join(segments)

# Directory to save the generated files
output_dir = "generated_837_files"
os.makedirs(output_dir, exist_ok=True)

# Generate 25 files
for i in range(25):
    file_content = generate_837()
    filename = os.path.join(output_dir, f"fake_837_{i+1}.txt")
    with open(filename, "w") as file:
        file.write(file_content)

print(f"25 Dummy 837 files with variations generated in the '{output_dir}' directory.")
