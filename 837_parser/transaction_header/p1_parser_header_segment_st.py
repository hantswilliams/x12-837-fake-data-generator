# import csv

# ##### NOTE THIS IS CURRNETLY WRONGG!!!!!
# ##### It looks like this is accidently bring over the submitter
# ##### code instead of the ST code is simple and should look like this:
# """
# Transaction Set Identifier Code,Transaction Set Control Number,Implementation Convention Reference
# 837,521718582,005010X223A2
# """

# def parse_submitter_segment(filepath, output_csv):
#     # Open and read the file content
#     with open(filepath, 'r') as file:
#         content = file.read()

#     print(f"File loaded: {filepath}")
    
#     # Split the content into segments using '~' as the delimiter
#     segments = content.split('~')
    
#     # List to store parsed NM1*41 and PER segment data
#     submitter_data = []
#     capture_next_per = False
    
#     # Loop through each segment and parse the submitter info
#     for segment in segments:
#         # Remove any leading/trailing whitespace
#         segment = segment.strip()

#         # Check if the segment is NM1*41 (submitter)
#         if segment.startswith('NM1*41'):
#             # Split by '*' to get each element within the NM1*41 segment
#             elements = segment.split('*')
#             print("NM1*41 segment found:", elements)
            
#             # Collect the general values for NM1*41 fields
#             nm1_data = {
#                 "Identifier Code (NM101)": elements[1].strip() if len(elements) > 1 else "",
#                 "Entity Type Qualifier (NM102)": elements[2].strip() if len(elements) > 2 else "",
#                 "Submitter Organization Name (NM103)": elements[3].strip() if len(elements) > 3 else ""
#             }
            
#             # Locate the last two non-empty elements for NM108 and NM109
#             non_empty_elements = [el.strip() for el in elements if el.strip()]
#             if len(non_empty_elements) >= 9:
#                 nm1_data["Identification Code Qualifier (NM108)"] = non_empty_elements[-2]  # Second last non-empty field
#                 nm1_data["Entity ID (NM109)"] = non_empty_elements[-1]  # Last non-empty field
            
#             submitter_data.append(nm1_data)
#             print("Parsed NM1*41 data:", nm1_data)
            
#             # Set flag to capture the next PER segment
#             capture_next_per = True

#         # Check if the segment is PER and capture contact details after NM1*41
#         elif capture_next_per and segment.startswith('PER*'):
#             # Split by '*' to get each element within the PER segment
#             elements = segment.split('*')
#             print("PER segment found:", elements)
            
#             # Update the last added entry in submitter_data with PER details
#             submitter_data[-1].update({
#                 "Contact Name (PER02)": elements[2].strip() if len(elements) > 2 else "",
#                 "Communication Number Qualifier (PER03)": elements[3].strip() if len(elements) > 3 else "",
#                 "Phone Number (PER04)": elements[4].strip() if len(elements) > 4 else ""
#             })
#             print("Parsed PER data added to submitter data:", submitter_data[-1])
            
#             # Reset flag to avoid capturing subsequent PER segments
#             capture_next_per = False

#     # Check if any submitter segments were collected
#     if not submitter_data:
#         print("No NM1*41 (submitter) segments found. CSV file will not be created.")
#         return
    
#     # Define the CSV fieldnames
#     fieldnames = [
#         "Identifier Code (NM101)",
#         "Entity Type Qualifier (NM102)",
#         "Submitter Organization Name (NM103)",
#         "Identification Code Qualifier (NM108)",
#         "Entity ID (NM109)",
#         "Contact Name (PER02)",
#         "Communication Number Qualifier (PER03)",
#         "Phone Number (PER04)"
#     ]
    
#     # Write the parsed data to a CSV file
#     with open(output_csv, 'w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(submitter_data)

#     print(f"Submitter segment data written to {output_csv}")

# # Example usage
# parse_submitter_segment('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/header_submitter.csv')


import csv
from io import StringIO

def parse_st_segment(filepath):
    """
    Parses the ST segment in the 837 file.

    Args:
        filepath (str): Path to the input 837 file.

    Returns:
        str: CSV-formatted string of the parsed ST segment.
    """
    # Open and read the file content
    with open(filepath, 'r') as file:
        content = file.read()

    print(f"File loaded: {filepath}")
    
    # Split the content into segments using '~' as the delimiter
    segments = content.split('~')
    
    # List to store parsed ST segment data
    st_segments = []
    
    # Loop through each segment and parse if it starts with 'ST*'
    for segment in segments:
        # Remove any leading/trailing whitespace and check for 'ST*' at the start
        segment = segment.strip()
        if segment.startswith('ST*'):
            # Split by '*' to get each element within the ST segment
            elements = segment.split('*')
            print("ST segment found:", elements)
            
            # Extract the required values
            st_segment_data = {
                "Transaction Set Identifier Code": elements[1].strip() if len(elements) > 1 else "",
                "Transaction Set Control Number": elements[2].strip() if len(elements) > 2 else "",
                "Implementation Convention Reference": elements[3].strip() if len(elements) > 3 else ""
            }
            st_segments.append(st_segment_data)
            break  # Stop after the first ST segment is found
    
    # Check if any ST segments were collected
    if not st_segments:
        print("No ST segments found. CSV file will not be created.")
        return
    
    # Define the CSV fieldnames
    fieldnames = [
        "Transaction Set Identifier Code",
        "Transaction Set Control Number",
        "Implementation Convention Reference"
    ]

    # Create in-memory file that gets returned
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(st_segments)
    return output.getvalue()

# Example usage
# parse_st_segment('path/to/837_file.txt')
