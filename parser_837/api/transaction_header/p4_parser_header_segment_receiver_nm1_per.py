import csv
from io import StringIO

#### LOOP 1000B for Receiver Name; NM1*40 and PER segments ####
#### LOOP 1000B for Receiver Name; NM1*40 and PER segments ####
#### LOOP 1000B for Receiver Name; NM1*40 and PER segments ####
#### LOOP 1000B for Receiver Name; NM1*40 and PER segments ####

# 40 = Receiver

def parse_receiver_segment(file_content):
    # # Open and read the file content
    # with open(filepath, 'r') as file:
    #     content = file.read()

    # print(f"File loaded: {filepath}")
    
    # Split the content into segments using '~' as the delimiter
    segments = file_content.split('~')
    
    # List to store parsed NM1*41 and PER segment data
    submitter_data = []
    capture_next_per = False
    
    # Loop through each segment and parse the receiver info
    for segment in segments:
        # Remove any leading/trailing whitespace
        segment = segment.strip()
        
        # Check if the segment is NM1*40 (received)
        if segment.startswith('NM1*40'):
            # Split by '*' to get each element within the NM1*41 segment
            elements = segment.split('*')
            # print("NM1*40 segment found:", elements)

            # ## print what will be stripped NM101, NM102, NM103, NM108, NM109
            # print('Element1: ', elements[1].strip()) ## NM101
            # print('Element2: ', elements[2].strip()) ## NM102
            # print('Element3: ', elements[3].strip()) ## NM103
            # print('Element4: ', elements[4].strip())
            # print('Element5: ', elements[5].strip())
            # print('Element6: ', elements[6].strip())
            # print('Element7: ', elements[7].strip())
            # print('Element8: ', elements[8].strip()) ## NM108
            # print('Element9: ', elements[9].strip()) ## NM109
            
            # Collect values for NM1*40
            nm1_data = {
                "Entity Identifier Code (NM101)": elements[1].strip(),
                "Entity Type Qualifier (NM102)": elements[2].strip(),
                "Receiver Name (NM103)": elements[3].strip(),
                "Identification Code Qualifier (NM108)": elements[8].strip(),
                "Entity ID (NM109)": elements[9].strip()
            }
            submitter_data.append(nm1_data)
            print("Parsed NM1*40 data:", nm1_data)
            
            # Set flag to capture the next PER segment
            capture_next_per = True

        # Check if the segment is PER and capture contact details after NM1*41
        elif capture_next_per and segment.startswith('PER*'):
            # Split by '*' to get each element within the PER segment
            elements = segment.split('*')
            # print("PER segment found:", elements)
            
            # Update the last added entry in submitter_data with PER details
            submitter_data[-1].update({
                "Contact Name (PER02)": elements[2].strip() if len(elements) > 2 else "",
                "Communication Number Qualifier (PER03)": elements[3].strip() if len(elements) > 3 else "",
                "Phone Number (PER04)": elements[4].strip() if len(elements) > 4 else ""
            })
            print("Parsed PER data added to submitter data:", submitter_data[-1])
            
            # Reset flag to avoid capturing subsequent PER segments
            capture_next_per = False

    # Check if any submitter segments were collected
    if not submitter_data:
        print("No NM1*40 (receover) segments found. CSV file will not be created.")
        return
    
    # Define the CSV fieldnames
    fieldnames = [
        "Entity Identifier Code (NM101)",
        "Entity Type Qualifier (NM102)",
        "Receiver Name (NM103)",
        "Identification Code Qualifier (NM108)",
        "Entity ID (NM109)",
        "Contact Name (PER02)",
        "Communication Number Qualifier (PER03)",
        "Phone Number (PER04)"
    ]

    # create in memory file that gets returned
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(submitter_data)
    return output.getvalue()
    
    # # Write the parsed data to a CSV file
    # with open(output_csv, 'w', newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerows(submitter_data)

    # print(f"Receiver segment data written to {output_csv}")

# Example usage
# parse_receiver_segment('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/header_receiver.csv')

