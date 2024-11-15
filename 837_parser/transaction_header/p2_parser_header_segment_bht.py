import csv

def parse_bht_segment(filepath, output_csv):
    # Open and read the file content
    with open(filepath, 'r') as file:
        content = file.read()

    print(f"File loaded: {filepath}")
    
    # Split the content into segments using '~' as the delimiter
    segments = content.split('~')
    
    # List to store parsed BHT segment data
    bht_segments = []
    
    # Loop through each segment and parse if it starts with 'BHT*'
    for segment in segments:
        # Remove any leading/trailing whitespace and check for 'BHT*' at the start
        segment = segment.strip()
        if segment.startswith('BHT*'):
            # Split by '*' to get each element within the BHT segment
            elements = segment.split('*')
            print("BHT segment found:", elements)
            
            # Collect the six expected values, ensuring elements exist
            bht_segment_data = {
                "Hierarchical Structure Code (BHT01)": elements[1].strip() if len(elements) > 1 else "",
                "Transaction Set Purpose Code (BHT02)": elements[2].strip() if len(elements) > 2 else "",
                "Reference Identification (BHT03)": elements[3].strip() if len(elements) > 3 else "",
                "Date (BHT04)": elements[4].strip() if len(elements) > 4 else "",
                "Time (BHT05)": elements[5].strip() if len(elements) > 5 else "",
                "Transaction Type Code (BHT06)": elements[6].strip() if len(elements) > 6 else ""
            }
            bht_segments.append(bht_segment_data)
            print("Parsed BHT segment data:", bht_segment_data)
            break  # Stop after the first BHT segment is found
    
    # Check if any BHT segments were collected
    if not bht_segments:
        print("No BHT segments found. CSV file will not be created.")
        return
    
    # Define the CSV fieldnames
    fieldnames = [
        "Hierarchical Structure Code (BHT01)",
        "Transaction Set Purpose Code (BHT02)",
        "Reference Identification (BHT03)",
        "Date (BHT04)",
        "Time (BHT05)",
        "Transaction Type Code (BHT06)"
    ]
    
    # Write the parsed data to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bht_segments)

    print(f"BHT segment data written to {output_csv}")

# Example usage
parse_bht_segment('generated_837_institutional_files/837_example_3.txt', 'generated_837_institutional_files/header_bht.csv')

