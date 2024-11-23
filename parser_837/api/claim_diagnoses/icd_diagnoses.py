import csv
from io import StringIO

#### Loop 2300 for CLM: Specifically HI segments for diagnosis codes ####
#### Loop 2300 for CLM: Specifically HI segments for diagnosis codes ####
#### Loop 2300 for CLM: Specifically HI segments for diagnosis codes ####
#### Loop 2300 for CLM: Specifically HI segments for diagnosis codes ####

def parse_clm_diagnosis_segments(file_content):    
    # Split the content into segments using '~' as the delimiter
    segments = file_content.split('~')
    
    # List of accepted diagnosis type codes (ICD9 and ICD10)
    accepted_diagnosis_types = {"AAU", "AAV", "AAX", "ABF", "ABJ", "ABK", "ABN"}
    
    # List to store parsed diagnosis data
    diagnosis_data = []
    current_clm_id = None
    capture_diagnosis = False
    diagnosis_pointer = 1  # Initialize diagnosis code pointer
    
    # Loop through each segment and parse the diagnosis info
    for segment in segments:
        # Remove any leading/trailing whitespace
        segment = segment.strip()
        
        # Start of a CLM section
        if segment.startswith('CLM'):
            # Split by '*' to get each element within the CLM segment
            elements = segment.split('*')
            current_clm_id = elements[1].strip() if len(elements) > 1 else ""
            print("CLM section found. CLM ID:", current_clm_id)
            capture_diagnosis = True  # Start capturing HI segments after this CLM segment
            diagnosis_pointer = 1  # Reset diagnosis code pointer for each new CLM segment
        
        # Capture HI segments for specified diagnosis types after CLM
        elif capture_diagnosis and segment.startswith('HI'):
            # Split by '*' to get each element within the HI segment
            elements = segment.split('*')
            # The first element is "HI", so we start parsing from the second element
            for code in elements[1:]:
                # Extract the diagnosis type code and principal diagnosis code
                if ':' in code:
                    diagnosis_type_code, principal_diagnosis_code = code.split(':')
                    # Only capture diagnosis codes that match accepted types
                    if diagnosis_type_code in accepted_diagnosis_types:
                        diagnosis_data.append({
                            "CLM ID": current_clm_id,
                            "HI": "HI",
                            "Diagnosis Type Code": diagnosis_type_code,
                            "Diagnosis Code": principal_diagnosis_code,
                            "Diagnosis Code Pointer": diagnosis_pointer
                        })
                        print("Parsed HI data:", diagnosis_data[-1])
                        diagnosis_pointer += 1  # Increment the pointer for each diagnosis code
        
        # Stop capturing HI segments once we reach another CLM or HL segment
        elif segment.startswith('CLM') or segment.startswith('HL'):
            capture_diagnosis = False
    
    # Write to CSV
    if diagnosis_data:
        fieldnames = [
            "CLM ID",
            "HI",
            "Diagnosis Type Code",
            "Diagnosis Code",
            "Diagnosis Code Pointer"
        ]

        ## using io.StringIO to write to csv
        output_csv = StringIO()

        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        for diagnosis in diagnosis_data:
            writer.writerow(diagnosis)

        # Reset the cursor to the beginning of the StringIO object
        output_csv.seek(0)
        
        return output_csv

# Example usage
# parse_clm_diagnosis_segments('837_generator_output/837_example_0.txt', '837_parser_output/837_example_0_claim_diagnoses.csv')
