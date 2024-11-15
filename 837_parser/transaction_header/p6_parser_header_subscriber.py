import csv

##### Loop 2000B for Subscriber; HL*2, SBR, NM1*IL, N3, N4 segments ####
##### Loop 2000B for Subscriber; HL*2, SBR, NM1*IL, N3, N4 segments ####
##### Loop 2000B for Subscriber; HL*2, SBR, NM1*IL, N3, N4 segments ####
##### Loop 2000B for Subscriber; HL*2, SBR, NM1*IL, N3, N4 segments ####


def parse_subscriber_segment(filepath, output_csv):
    # Open and read the file content
    with open(filepath, 'r') as file:
        content = file.read()

    print(f"File loaded: {filepath}")
    
    # Split the content into segments using '~' as the delimiter
    segments = content.split('~')
    
    # List to store parsed subscriber data
    subscriber_data = []
    capture_section = False
    
    # Loop through each segment to capture the subscriber information
    subscriber_record = {}
    for segment in segments:
        # Remove any leading/trailing whitespace
        segment = segment.strip()
        
        # Start of the subscriber section
        if segment.startswith('HL*2*1*22*0'):
            capture_section = True
            print("Subscriber section start found:", segment)
            # Initialize a new record for subscriber data
            subscriber_record = {"HL Segment": segment}

        # Stop capturing when we encounter the CLM segment
        elif segment.startswith('CLM') and capture_section:
            print("CLM segment found. Ending subscriber section capture.")
            subscriber_data.append(subscriber_record)
            break  # Exit as we have reached the end of the subscriber section

        # Capture and parse segments within the subscriber section
        elif capture_section:
            elements = segment.split('*')
            
            # Parse the SBR segment for subscriber relationship and insurance info
            if segment.startswith('SBR'):
                subscriber_record.update({
                    "Payer Responsibility Sequence Number Code (SBR01)": elements[1].strip() if len(elements) > 1 else "",
                    "Individual Relationship Code (SBR02)": elements[2].strip() if len(elements) > 2 else "",
                    "Subscriber Group or Policy Number (SBR03)": elements[3].strip() if len(elements) > 3 else "",
                    "Claim Filing Indicator Code (SBR09)": elements[9].strip() if len(elements) > 9 else ""
                })
                print("Parsed SBR data:", subscriber_record)

            # Parse NM1 segment for subscriber name and ID
            elif segment.startswith('NM1*IL'):
                subscriber_record.update({
                    "Entity Identifier Code (NM101)": elements[1].strip() if len(elements) > 1 else "",
                    "Entity Type Qualifier (NM102)": elements[2].strip() if len(elements) > 2 else "",
                    "Subscriber Last or Organization Name (NM103)": elements[3].strip() if len(elements) > 3 else "",
                    "Subscriber First Name (NM104)": elements[4].strip() if len(elements) > 4 else "",
                    "Identification Code Qualifier (NM108)": elements[8].strip() if len(elements) > 8 else "",
                    "Subscriber ID (NM109)": elements[9].strip() if len(elements) > 9 else ""
                })
                print("Parsed NM1 data:", subscriber_record)

            # Parse N3 segment for subscriber address
            elif segment.startswith('N3'):
                subscriber_record.update({
                    "Subscriber Address Line (N301)": elements[1].strip() if len(elements) > 1 else ""
                })
                print("Parsed N3 data:", subscriber_record)

            # Parse N4 segment for subscriber city, state, and zip
            elif segment.startswith('N4'):
                subscriber_record.update({
                    "Subscriber City Name (N401)": elements[1].strip() if len(elements) > 1 else "",
                    "Subscriber State Code (N402)": elements[2].strip() if len(elements) > 2 else "",
                    "Subscriber Postal Code (N403)": elements[3].strip() if len(elements) > 3 else ""
                })
                print("Parsed N4 data:", subscriber_record)
    
    # Write to CSV
    if subscriber_data:
        fieldnames = [
            "HL Segment",
            "Payer Responsibility Sequence Number Code (SBR01)",
            "Individual Relationship Code (SBR02)",
            "Subscriber Group or Policy Number (SBR03)",
            "Claim Filing Indicator Code (SBR09)",
            "Entity Identifier Code (NM101)",
            "Entity Type Qualifier (NM102)",
            "Subscriber Last or Organization Name (NM103)",
            "Subscriber First Name (NM104)",
            "Identification Code Qualifier (NM108)",
            "Subscriber ID (NM109)",
            "Subscriber Address Line (N301)",
            "Subscriber City Name (N401)",
            "Subscriber State Code (N402)",
            "Subscriber Postal Code (N403)"
        ]
        
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(subscriber_data)
        
        print(f"Subscriber section data written to {output_csv}")

# Example usage
parse_subscriber_segment('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/header_subscriber.csv')
