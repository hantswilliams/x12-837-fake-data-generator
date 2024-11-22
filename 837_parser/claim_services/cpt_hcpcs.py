import csv

def parse_service_lines(filepath, output_csv):
    # Open and read the file content
    with open(filepath, 'r') as file:
        content = file.read()

    print(f"File loaded: {filepath}")
    
    # Split the content into segments using '~' as the delimiter
    segments = content.split('~')
    
    # List to store parsed service line data
    service_line_data = []
    current_clm_id = None

    # Step 1: Identify the indices of all LX segments
    lx_indices = []
    for i, segment in enumerate(segments):
        segment = segment.strip()
        if segment.startswith('LX'):
            lx_indices.append(i)

    print(f"LX segments found at indices: {lx_indices}")

    # Step 2: Process each LX segment by index
    for lx_index in lx_indices:
        service_record = {}
        
        # Move backwards to find the closest CLM segment for current_clm_id
        for j in range(lx_index - 1, -1, -1):
            if segments[j].strip().startswith('CLM'):
                elements = segments[j].strip().split('*')
                current_clm_id = elements[1].strip() if len(elements) > 1 else ""
                print("CLM section found. CLM ID:", current_clm_id)
                break
        
        # Initialize the service line number and start parsing the LX segment
        segment = segments[lx_index].strip()
        elements = segment.split('*')
        service_line_num = int(elements[1]) if len(elements) > 1 and elements[1].isdigit() else 1
        service_record = {
            "CLM ID": current_clm_id,
            "Service Line Number": service_line_num,
        }
        print("Processing service line:", service_record)

        # Step 3: Parse following segments for SV1, DTP, and REF details
        for k in range(lx_index + 1, len(segments)):
            sub_segment = segments[k].strip()
            
            if sub_segment.startswith('SV1'):
                elements = sub_segment.split('*')

                diagnosis_code_pointer = elements[7].strip() if len(elements) > 7 else ""
                diagnosis_code_pointer = diagnosis_code_pointer.replace(':', ',')
                diagnosis_code_pointer = diagnosis_code_pointer.split(',')
                diagnosis_code_pointer = [code.strip() for code in diagnosis_code_pointer if code.strip()]
                diagnosis_code_pointer = [int(code) for code in diagnosis_code_pointer if code.isdigit()]
                diagnosis_code_pointer.sort()

                service_record.update({
                    "Product or Service ID (SV101)": elements[1].strip() if len(elements) > 1 else "",
                    "Monetary Amount (SV102)": elements[2].strip() if len(elements) > 2 else "",
                    "Unit or Basis for Measurement Code (SV103)": elements[3].strip() if len(elements) > 3 else "",
                    "Quantity (SV104)": elements[4].strip() if len(elements) > 4 else "",
                    "Diagnosis Code Pointer": diagnosis_code_pointer
                })
                print("Parsed SV1 data:", service_record)
            
            elif sub_segment.startswith('DTP'):
                elements = sub_segment.split('*')
                if len(elements) > 2:
                    service_record.update({
                        "Date Time Qualifier (DTP01)": elements[1].strip(),
                        "Service Date (DTP03)": elements[3].strip()
                    })
                print("Parsed DTP data:", service_record)
            
            elif sub_segment.startswith('REF'):
                elements = sub_segment.split('*')
                service_record.update({
                    "Reference Identification Qualifier (REF01)": elements[1].strip() if len(elements) > 1 else "",
                    "Reference Identification (REF02)": elements[2].strip() if len(elements) > 2 else ""
                })
                print("Parsed REF data:", service_record)
            
            # Stop parsing when reaching another LX, CLM, or HL segment
            if sub_segment.startswith('LX') or sub_segment.startswith('CLM') or sub_segment.startswith('HL'):
                break

        # Append the completed service record to the list
        service_line_data.append(service_record)

    # Step 4: Write to CSV
    if service_line_data:
        fieldnames = [
            "CLM ID",
            "Service Line Number",
            "Product or Service ID (SV101)",
            "Monetary Amount (SV102)",
            "Unit or Basis for Measurement Code (SV103)",
            "Quantity (SV104)",
            "Diagnosis Code Pointer",
            "Date Time Qualifier (DTP01)",
            "Service Date (DTP03)",
            "Reference Identification Qualifier (REF01)",
            "Reference Identification (REF02)"
        ]
        
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(service_line_data)
        
        print(f"Service line data written to {output_csv}")

# Example usage
# parse_service_lines('837_generator_output/837_example_0.txt', '837_parser_output/837_example_0_claim_service_lines.csv')
