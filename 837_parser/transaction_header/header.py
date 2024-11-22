from transaction_header.p1_parser_header_segment_st import parse_st_segment
from transaction_header.p2_parser_header_segment_bht import parse_bht_segment
from transaction_header.p3_parser_header_segment_submitter_nm1_per import parse_submitter_segment
from transaction_header.p4_parser_header_segment_receiver_nm1_per import parse_receiver_segment
from transaction_header.p5_parser_header_billingprovider import parse_billing_provider_segment
from transaction_header.p6_parser_header_subscriber import parse_subscriber_segment
from io import StringIO
import csv

def parse_header_data(file, output_csv):
    segment_st = StringIO(parse_st_segment(file))
    segment_bht = StringIO(parse_bht_segment(file))
    segment_submitter = StringIO(parse_submitter_segment(file))
    segment_receiver = StringIO(parse_receiver_segment(file))
    segment_billing_provider = StringIO(parse_billing_provider_segment(file))
    segment_subscriber = StringIO(parse_subscriber_segment(file))

    # Read data from each segment
    segments = [segment_st, segment_bht, segment_submitter, segment_receiver, segment_billing_provider, segment_subscriber]
    combined_header = []
    combined_row = []

    for segment in segments:
        reader = csv.DictReader(segment)
        for row in reader:  # Assuming each segment has only one row
            combined_header.extend(row.keys())  # Collect all column names
            combined_row.extend(row.values())  # Collect all values
            break  # Stop after the first row

    # Write the combined data to the output CSV file
    with open(output_csv, mode='w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(combined_header)  # Write the header
        writer.writerow(combined_row)    # Write the combined row

    return 'Header data written to {output_csv}'