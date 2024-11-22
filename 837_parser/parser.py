from claim_services.cpt_hcpcs import parse_service_lines
from claim_diagnoses.icd_diagnoses import parse_clm_diagnosis_segments
from transaction_header.header import parse_header_data

import os 
import random

## Get list of files in the directory 837_generator_output
files = os.listdir('837_generator_output')

## randomly select a file from the list
file = random.choice(files)

print(f'Parsing file {file}')

if not os.path.exists(f'837_parser_output/{file}'):
    os.makedirs(f'837_parser_output/{file}')

parse_service_lines(
    f'837_generator_output/{file}', 
    f'837_parser_output/{file}/{file}_claim_service_lines.csv'
    )

parse_clm_diagnosis_segments(
    f'837_generator_output/{file}', 
    f'837_parser_output/{file}/{file}_claim_diagnoses.csv'
    )

parse_header_data(
    f'837_generator_output/{file}', 
    f'837_parser_output/{file}/{file}_header.csv'
    )



