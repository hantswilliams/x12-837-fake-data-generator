import datetime
import pandas as pd
import random

# Load ICD-10 and CPT codes from CSV files with specified columns
icd_df = pd.read_csv('codexes/icd10.csv', usecols=['A00', 'A000'])
cpt_df = pd.read_csv('codexes/cpt4.csv', usecols=['com.medigy.persist.reference.type.clincial.CPT.code'])

# Convert ICD and CPT codes to lists for random selection
ICD_CODES = icd_df['A000'].dropna().tolist()
CPT_CODES = cpt_df['com.medigy.persist.reference.type.clincial.CPT.code'].dropna().tolist()


def generate_isa_segment(sender_id, receiver_id, control_number):
    sender_id_padded = sender_id.ljust(15)
    receiver_id_padded = receiver_id.ljust(15)
    return (
        f"ISA*00*          *00*          *ZZ*{sender_id_padded}*ZZ*{receiver_id_padded}*"
        f"{datetime.datetime.now():%y%m%d}*{datetime.datetime.now():%H%M}*U*00401*{control_number}*0*P*:~"
    )

def generate_gs_segment(sender_id, receiver_id, control_number):
    return (
        f"GS*HC*{sender_id}*{receiver_id}*{datetime.datetime.now():%Y%m%d}*{datetime.datetime.now():%H%M}*{control_number}*X*005010X223A2~"
    )

def generate_st_segment(transaction_control_number):
    return f"ST*837*{transaction_control_number}*005010X223A2~"

def generate_bht_segment():
    return f"BHT*0019*00*{datetime.datetime.now().strftime('%y%m%d%H%M%S')}*{datetime.datetime.now():%Y%m%d}*{datetime.datetime.now():%H%M}*CH~"

def generate_nm1_segment(identifier_code, name, entity_id):
    return f"NM1*{identifier_code}*2*{name}*****XX*{entity_id}~"

def generate_per_segment(contact_name, phone_number):
    return f"PER*IC*{contact_name}*TE*{phone_number}~"

def generate_hl_segment(hierarchical_id, parent_id, level_code, child_code):
    return f"HL*{hierarchical_id}*{parent_id}*{level_code}*{child_code}~"

def generate_clm_segment(claim_id, amount, place_of_service):
    return f"CLM*{claim_id}*{amount}***{place_of_service}:B:1*Y*A*Y*I~"

def generate_dtp_segment(date_qualifier, date_format, date_value):
    return f"DTP*{date_qualifier}*{date_format}*{date_value}~"

def generate_hi_segment(code):
    return f"HI*ABK:{code}~"

def generate_sv1_segment(procedure_code, amount, unit, quantity, modifier=""):
    return f"SV1*HC:{procedure_code}*{amount}*{unit}*{quantity}***{modifier}~"

def generate_se_segment(segment_count, transaction_control_number):
    return f"SE*{segment_count}*{transaction_control_number}~"

def generate_ge_segment(group_control_number):
    return f"GE*1*{group_control_number}~"

def generate_iea_segment(interchange_control_number):
    return f"IEA*1*{interchange_control_number}~"

# Generate a single 837 transaction example
def generate_837_example(control_number, transaction_control_number):
    sender_id = "FAKE837SEND"
    receiver_id = "FAKE837RECV"
    
    segments = []
    segments.append(generate_isa_segment(sender_id, receiver_id, control_number))
    segments.append(generate_gs_segment(sender_id, receiver_id, 1))
    segments.append(generate_st_segment(transaction_control_number))
    segments.append(generate_bht_segment())
    segments.append(generate_nm1_segment("41", "Submitter Organization", "4675433976"))
    segments.append(generate_per_segment("Adam Velasquez", "2492742731"))
    segments.append(generate_nm1_segment("40", "Receiver Organization", "0238660013"))
    
    # HL Loop for Billing Provider
    hierarchical_id_billing = 1
    segments.append(generate_hl_segment(hierarchical_id_billing, "", 20, 1))
    segments.append(generate_nm1_segment("85", "Garcia Ltd", "5709867528"))
    segments.append("N3*5921 Lisa Inlet~")
    segments.append("N4*East Jeffery*TN*34498~")
    segments.append("REF*EI*628740805~")
    segments.append(generate_per_segment("Juan Ramirez", "228.701.4467x569"))
    
    # HL Loop for Subscriber
    hierarchical_id_subscriber = 22  # Use 22 as per example specification
    segments.append(generate_hl_segment(hierarchical_id_subscriber, hierarchical_id_billing, 22, 0))
    segments.append(generate_nm1_segment("IL", "Kristin Phillips", "7932682729"))
    segments.append("N3*83816 Maria Estate Suite 225~")
    segments.append("N4*East Nicholas*WV*09804~")
    
    # Claim information
    segments.append(generate_clm_segment("4742333269", "711", "11"))
    segments.append(generate_dtp_segment("434", "RD8", "20240422-20240430"))
    segments.append(generate_dtp_segment("435", "D8", "20240809"))
    segments.append(generate_dtp_segment("096", "TM", "2337"))
    segments.append(generate_hi_segment(random.choice(ICD_CODES)))
    segments.append(generate_hi_segment(random.choice(ICD_CODES)))
    
    # Adding a service line with SV1 for a random CPT code
    segments.append("LX*1~")  # Line number segment
    cptcode = random.choice(CPT_CODES)
    segments.append(generate_sv1_segment(cptcode, "20", "UN", "1"))
    segments.append(generate_dtp_segment("472", "D8", "20180428"))
    segments.append("REF*6R*142671~")
    
    # Calculate SE segment count more accurately
    segment_count = len(segments) - 1  # Subtract 1 since SE should not be counted yet
    segments.append(generate_se_segment(segment_count, transaction_control_number))

    segments.append(generate_ge_segment(1))
    segments.append(generate_iea_segment(control_number))
    
    # Join segments with newlines for readability
    return "\n".join(segments)

# Generate multiple 837 examples and save each to a unique file
for i in range(5):
    control_number = f"{748158818 + i}"  # Increment control number for uniqueness
    transaction_control_number = f"{521718582 + i}"  # Unique transaction control number
    
    example_output = generate_837_example(control_number, transaction_control_number)
    
    # Save each file with a unique name
    filename = f"generated_837_institutional_files/837_example_{i + 1}.txt"
    with open(filename, "w") as file:
        file.write(example_output)
    
    print(f"File {filename} generated successfully.")
