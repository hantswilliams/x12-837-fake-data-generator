import pandas as pd 
import os 
import sys

directory_837 = 'parser_837_output'
diagnoses_file_ending = '_diagnoses.csv'
procedures_file_ending = '_service_lines.csv'
header_file_ending = '_header.csv'

### loop through diagnoses files
diagnoses_files = []
for filename in os.listdir(directory_837):
    if filename.endswith(diagnoses_file_ending):
        print(filename)
        df = pd.read_csv(os.path.join(directory_837, filename))
        print(df.head())
        diagnoses_files.append(df)

### loop through procedures files
procedures_files = []
for filename in os.listdir(directory_837):
    if filename.endswith(procedures_file_ending):
        print(filename)
        df = pd.read_csv(os.path.join(directory_837, filename))
        print(df.head())
        procedures_files.append(df)

### loop through header files
header_files = []
for filename in os.listdir(directory_837):
    if filename.endswith(header_file_ending):
        print(filename)
        df = pd.read_csv(os.path.join(directory_837, filename))
        print(df.head())
        header_files.append(df)


## concatenate all the dataframes
diagnoses = pd.concat(diagnoses_files)
procedures = pd.concat(procedures_files)
header = pd.concat(header_files)

## example analyses 

### count the number of unique patients
num_patients = len(header['Subscriber ID (NM109)'].unique())
print('Number of unique patients: ', num_patients)

### count the number of unique diagnoses
num_diagnoses = len(diagnoses['Diagnosis Code'].unique())
print('Number of unique diagnoses: ', num_diagnoses)

### count the number of unique procedures
num_procedures = len(procedures['Product or Service ID (SV101)'].unique())
print('Number of unique procedures: ', num_procedures)

