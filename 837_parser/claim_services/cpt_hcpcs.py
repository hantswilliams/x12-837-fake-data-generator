# # import csv

# # def parse_service_lines(filepath, output_csv):
# #     # Open and read the file content
# #     with open(filepath, 'r') as file:
# #         content = file.read()

# #     print(f"File loaded: {filepath}")
    
# #     # Split the content into segments using '~' as the delimiter
# #     segments = content.split('~')
    
# #     # List to store parsed service line data
# #     service_line_data = []
# #     current_clm_id = None
# #     capture_service = False
# #     service_line_num = 1  # Initialize service line number
# #     service_record = {}  # Initialize service_record to avoid unbound errors

# #     print("Parsing service lines...")
    
# #     # Loop through each segment and parse service line info
# #     for segment in segments:

# #         # Remove any leading/trailing whitespace
# #         segment = segment.strip()
        
# #         # Start of a CLM section
# #         if segment.startswith('CLM'):
# #             # Split by '*' to get each element within the CLM segment
# #             elements = segment.split('*')
# #             current_clm_id = elements[1].strip() if len(elements) > 1 else ""
# #             print("CLM section found. CLM ID:", current_clm_id)
# #             capture_service = False  # Reset capture state for service lines
# #             service_line_num = 1  # Reset service line number for each new CLM segment
        
# #         # Count the number of LX segments that exist 
# #         elif segment.startswith('LX'):
# #             elements = segment.split('*')
# #             service_line_num = int(elements[1]) if len(elements) > 1 and elements[1].isdigit() else service_line_num
# #             print("Service line number found:", service_line_num)

# #         # Start of a service line within the CLM segment
# #         elif segment.startswith('LX'):
# #             capture_service = True
# #             elements = segment.split('*')
# #             service_line_num = int(elements[1]) if len(elements) > 1 and elements[1].isdigit() else service_line_num
# #             # Create a new service record for each LX segment
# #             service_record = {
# #                 "CLM ID": current_clm_id,
# #                 "Service Line Number": service_line_num,
# #             }
# #             # print("Service line start found:", segment)
        
# #         # Capture and parse the SV1 segment
# #         elif capture_service and segment.startswith('SV1'):
# #             elements = segment.split('*')
# #             # Capture the diagnosis code pointer, which is the last value in SV1
# #             diagnosis_code_pointer = elements[7].strip() if len(elements) > 7 else ""
# #             service_record.update({
# #                 "Product or Service ID (SV101)": elements[1].strip() if len(elements) > 1 else "",
# #                 "Monetary Amount (SV102)": elements[2].strip() if len(elements) > 2 else "",
# #                 "Unit or Basis for Measurement Code (SV103)": elements[3].strip() if len(elements) > 3 else "",
# #                 "Quantity (SV104)": elements[4].strip() if len(elements) > 4 else "",
# #                 "Diagnosis Code Pointer": diagnosis_code_pointer  # Add the diagnosis code pointer
# #             })
# #             # print("Parsed SV1 data:", service_record)
        
# #         # Capture and parse the DTP segment for service date
# #         elif capture_service and segment.startswith('DTP'):
# #             elements = segment.split('*')
# #             if len(elements) > 2:
# #                 service_record.update({
# #                     "Date Time Qualifier (DTP01)": elements[1].strip(),
# #                     "Service Date (DTP03)": elements[3].strip()
# #                 })
# #             # print("Parsed DTP data:", service_record)
        
# #         # Capture and parse the REF segment for reference information
# #         elif capture_service and segment.startswith('REF'):
# #             elements = segment.split('*')
# #             service_record.update({
# #                 "Reference Identification Qualifier (REF01)": elements[1].strip() if len(elements) > 1 else "",
# #                 "Reference Identification (REF02)": elements[2].strip() if len(elements) > 2 else ""
# #             })
# #             # print("Parsed REF data:", service_record)
        
# #         # Append the completed service record at the end of each service line
# #         elif capture_service and (segment.startswith('LX') or segment.startswith('CLM') or segment.startswith('HL')):
# #             # Only append if service_record has content
# #             if service_record:
# #                 service_line_data.append(service_record)
# #                 service_record = {}  # Reset for the next service line
# #             capture_service = False  # Reset service capture for the new segment

# #     # Print the service_record data
# #     print("Final service record data:", service_record)

# #     # Append any remaining service record if the file ends without another CLM or HL
# #     if service_record:
# #         service_line_data.append(service_record)

# #     # Write to CSV
# #     if service_line_data:
# #         fieldnames = [
# #             "CLM ID",
# #             "Service Line Number",
# #             "Product or Service ID (SV101)",
# #             "Monetary Amount (SV102)",
# #             "Unit or Basis for Measurement Code (SV103)",
# #             "Quantity (SV104)",
# #             "Diagnosis Code Pointer",
# #             "Date Time Qualifier (DTP01)",
# #             "Service Date (DTP03)",
# #             "Reference Identification Qualifier (REF01)",
# #             "Reference Identification (REF02)"
# #         ]
        
# #         with open(output_csv, 'w', newline='') as csvfile:
# #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# #             writer.writeheader()
# #             writer.writerows(service_line_data)
        
# #         # print(f"Service line data written to {output_csv}")

# # # Example usage
# # parse_service_lines('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/claim_service_lines.csv')



# import csv

# def parse_service_lines(filepath, output_csv):
#     # Open and read the file content
#     with open(filepath, 'r') as file:
#         content = file.read()

#     print(f"File loaded: {filepath}")
    
#     # Split the content into segments using '~' as the delimiter
#     segments = content.split('~')
    
#     # List to store parsed service line data
#     service_line_data = []
#     current_clm_id = None
#     capture_service = False

#     print("Parsing service lines...")

#     # Loop through each segment and parse service line info
#     i = 0
#     while i < len(segments):
#         segment = segments[i].strip()
        
#         # Start of a CLM section
#         if segment.startswith('CLM'):
#             elements = segment.split('*')
#             current_clm_id = elements[1].strip() if len(elements) > 1 else ""
#             print("CLM section found. CLM ID:", current_clm_id)
#             capture_service = False  # Reset capture state for service lines
        
#         # Start of a service line within the CLM segment
#         elif segment.startswith('LX'):

#             capture_service = True
#             elements = segment.split('*')
#             service_line_num = int(elements[1]) if len(elements) > 1 and elements[1].isdigit() else 1
#             # Create a new service record for each LX segment
#             service_record = {
#                 "CLM ID": current_clm_id,
#                 "Service Line Number": service_line_num,
#             }
#             print("Service line start found:", segment)
#             i += 1

#             # Continue parsing within this LX segment until a new LX, CLM, or HL segment
#             while i < len(segments):
#                 sub_segment = segments[i].strip()
                
#                 if sub_segment.startswith('SV1'):
#                     elements = sub_segment.split('*')
#                     diagnosis_code_pointer = elements[7].strip() if len(elements) > 7 else ""
#                     service_record.update({
#                         "Product or Service ID (SV101)": elements[1].strip() if len(elements) > 1 else "",
#                         "Monetary Amount (SV102)": elements[2].strip() if len(elements) > 2 else "",
#                         "Unit or Basis for Measurement Code (SV103)": elements[3].strip() if len(elements) > 3 else "",
#                         "Quantity (SV104)": elements[4].strip() if len(elements) > 4 else "",
#                         "Diagnosis Code Pointer": diagnosis_code_pointer
#                     })
#                     print("Parsed SV1 data:", service_record)
                
#                 elif sub_segment.startswith('DTP'):
#                     elements = sub_segment.split('*')
#                     if len(elements) > 2:
#                         service_record.update({
#                             "Date Time Qualifier (DTP01)": elements[1].strip(),
#                             "Service Date (DTP03)": elements[3].strip()
#                         })
#                     print("Parsed DTP data:", service_record)
                
#                 elif sub_segment.startswith('REF'):
#                     elements = sub_segment.split('*')
#                     service_record.update({
#                         "Reference Identification Qualifier (REF01)": elements[1].strip() if len(elements) > 1 else "",
#                         "Reference Identification (REF02)": elements[2].strip() if len(elements) > 2 else ""
#                     })
#                     print("Parsed REF data:", service_record)
                
#                 # Break the loop if another LX, CLM, or HL segment is encountered
#                 if sub_segment.startswith('LX') or sub_segment.startswith('CLM') or sub_segment.startswith('HL'):
#                     break
                
#                 # Move to the next segment
#                 i += 1

#             # Append the completed service record to the list
#             service_line_data.append(service_record)
#             capture_service = False  # Reset service capture for the next segment
        
#         # Move to the next segment if not in an LX
#         i += 1

#     # Write to CSV
#     if service_line_data:
#         fieldnames = [
#             "CLM ID",
#             "Service Line Number",
#             "Product or Service ID (SV101)",
#             "Monetary Amount (SV102)",
#             "Unit or Basis for Measurement Code (SV103)",
#             "Quantity (SV104)",
#             "Diagnosis Code Pointer",
#             "Date Time Qualifier (DTP01)",
#             "Service Date (DTP03)",
#             "Reference Identification Qualifier (REF01)",
#             "Reference Identification (REF02)"
#         ]
        
#         with open(output_csv, 'w', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(service_line_data)
        
#         print(f"Service line data written to {output_csv}")

# # Example usage
# parse_service_lines('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/claim_service_lines.csv')


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
parse_service_lines('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/claim_service_lines.csv')
