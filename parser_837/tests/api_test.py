from parser_837.api.parser import parser_main

services, diagnoses, header = parser_main('generator_837_output/837_example_1.txt')

# Write the parsed data to CSV files
with open('parser_837_output/TESTB_837_example_1_claim_service_lines.csv', 'w') as f:
    f.write(services.getvalue())

with open('parser_837_output/TESTB_837_example_1_claim_diagnoses.csv', 'w') as f:
    f.write(diagnoses.getvalue())

with open('parser_837_output/TESTB_837_example_1_transaction_header.csv', 'w') as f:
    f.write(header.getvalue())
