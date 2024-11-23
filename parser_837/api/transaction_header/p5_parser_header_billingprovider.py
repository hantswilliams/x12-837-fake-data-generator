import csv
from io import StringIO

##### Loop 2000A for Billing Provider; HL*1, NM1*85, N3, N4, REF, PER segments ####
##### Loop 2000A for Billing Provider; HL*1, NM1*85, N3, N4, REF, PER segments ####
##### Loop 2000A for Billing Provider; HL*1, NM1*85, N3, N4, REF, PER segments ####
##### Loop 2000A for Billing Provider; HL*1, NM1*85, N3, N4, REF, PER segments ####

# 85 = Billing Provider

def parse_billing_provider_segment(file_content):
    # # Open and read the file content
    # with open(filepath, 'r') as file:
    #     content = file.read()

    # print(f"File loaded: {filepath}")
    
    # Split the content into segments using '~' as the delimiter
    segments = file_content.split('~')
    
    # List to store parsed billing provider data
    billing_provider_data = []
    capture_section = False
    
    # Loop through each segment and parse the billing provider info
    billing_provider_record = {}
    for segment in segments:
        # Remove any leading/trailing whitespace
        segment = segment.strip()
        
        # Start of the billing provider section
        if segment.startswith('HL*1**20*1'):
            capture_section = True
            # print("Billing provider section start found:", segment)
            # Initialize a new record for billing provider data
            billing_provider_record = {"HL Segment": segment}

        # Check if a new HL section starts, ending the current billing provider loop
        elif segment.startswith('HL*') and capture_section:
            # print("New HL section found. Ending billing provider section capture.")
            billing_provider_data.append(billing_provider_record)
            break  # Exit as we have reached the end of the billing provider section

        # Capture and parse segments within the billing provider section
        elif capture_section:
            elements = segment.split('*')
            
            # Parse the NM1*85 segment for the billing provider's name and ID
            if segment.startswith('NM1*85'):
                billing_provider_record.update({
                    "Entity Identifier Code (NM101)": elements[1].strip() if len(elements) > 1 else "",
                    "Entity Type Qualifier (NM102)": elements[2].strip() if len(elements) > 2 else "",
                    "Billing Provider Last or Organization Name (NM103)": elements[3].strip() if len(elements) > 3 else "",
                    "Identification Code Qualifier (NM108)": elements[8].strip() if len(elements) > 8 else "",
                    "Entity ID (NM109)": elements[9].strip() if len(elements) > 9 else ""
                })
                print("Parsed NM1*85 data:", billing_provider_record)

            # Parse N3 segment for billing provider's address
            elif segment.startswith('N3'):
                billing_provider_record.update({
                    "Billing Provider Address Line (N301)": elements[1].strip() if len(elements) > 1 else ""
                })
                # print("Parsed N3 data:", billing_provider_record)

            # Parse N4 segment for city, state, and zip
            elif segment.startswith('N4'):
                billing_provider_record.update({
                    "Billing Provider City Name (N401)": elements[1].strip() if len(elements) > 1 else "",
                    "Billing Provider State Code (N402)": elements[2].strip() if len(elements) > 2 else "",
                    "Billing Provider Postal Code (N403)": elements[3].strip() if len(elements) > 3 else ""
                })
                # print("Parsed N4 data:", billing_provider_record)

            # Parse REF segment for billing provider tax ID
            elif segment.startswith('REF*EI'):
                billing_provider_record.update({
                    "Reference Identification Qualifier (REF01)": elements[1].strip() if len(elements) > 1 else "",
                    "Billing Provider Tax Identification Number (REF02)": elements[2].strip() if len(elements) > 2 else ""
                })
                # print("Parsed REF data:", billing_provider_record)

            # Parse PER segment for billing provider contact information
            elif segment.startswith('PER*IC'):
                billing_provider_record.update({
                    "Contact Function Code (PER01)": elements[1].strip() if len(elements) > 1 else "",
                    "Contact Name (PER02)": elements[2].strip() if len(elements) > 2 else "",
                    "Communication Number Qualifier (PER03)": elements[3].strip() if len(elements) > 3 else "",
                    "Communication Number (PER04)": elements[4].strip() if len(elements) > 4 else ""
                })
                # print("Parsed PER data:", billing_provider_record)
    
    # Write to CSV
    if billing_provider_data:
        fieldnames = [
            "HL Segment",
            "Entity Identifier Code (NM101)",
            "Entity Type Qualifier (NM102)",
            "Billing Provider Last or Organization Name (NM103)",
            "Identification Code Qualifier (NM108)",
            "Entity ID (NM109)",
            "Billing Provider Address Line (N301)",
            "Billing Provider City Name (N401)",
            "Billing Provider State Code (N402)",
            "Billing Provider Postal Code (N403)",
            "Reference Identification Qualifier (REF01)",
            "Billing Provider Tax Identification Number (REF02)",
            "Contact Function Code (PER01)",
            "Contact Name (PER02)",
            "Communication Number Qualifier (PER03)",
            "Communication Number (PER04)"
        ]

        # create in memory file that gets returned
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(billing_provider_data)
        return output.getvalue()
        
        # with open(output_csv, 'w', newline='') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     writer.writerows(billing_provider_data)
        
        # print(f"Billing provider section data written to {output_csv}")

# Example usage
# parse_billing_provider_segment('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/header_billing_provider.csv')
