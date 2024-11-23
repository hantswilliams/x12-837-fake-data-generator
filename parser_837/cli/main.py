import argparse
import os
from ..api.parser import parser_main


def parse_837_file(input_file, output_dir):
    """
    Parse a single 837 file and save the results as CSV files.

    Args:
        input_file (str): Path to input 837 file.
        output_dir (str): Directory to save the parsed CSV files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_filename = os.path.basename(input_file).replace(".txt", "")
    service_csv = os.path.join(output_dir, f"{base_filename}_claim_service_lines.csv")
    diagnosis_csv = os.path.join(output_dir, f"{base_filename}_claim_diagnoses.csv")
    header_csv = os.path.join(output_dir, f"{base_filename}_header.csv")

    print(f"Parsing file {input_file}...")

    # Use parser_main to parse the file
    services, diagnoses, header = parser_main(input_file)

    # Extract content from StringIO and write to files
    with open(service_csv, "w") as f:
        f.write(services.getvalue())
    with open(diagnosis_csv, "w") as f:
        f.write(diagnoses.getvalue())
    with open(header_csv, "w") as f:
        f.write(header.getvalue())

    print(f"Parsed and exported: {service_csv}, {diagnosis_csv}, {header_csv}")


def main():
    parser = argparse.ArgumentParser(description="Parse 837 file(s) into CSVs.")
    parser.add_argument(
        "-i", "--input", required=True, help="Path to input file or directory containing 837 files."
    )
    parser.add_argument(
        "-o", 
        "--output", 
        required=True, 
        help="Directory to save the parsed CSV files. If unsure, you can use the current directory (e.g., '.')"
    )

    args = parser.parse_args()
    input_path = args.input
    output_dir = args.output

    if output_dir == ".":
        output_dir = os.getcwd()
        print(f"Output directory set to current working directory: {output_dir}")

    if os.path.isdir(input_path):
        # Parse all files in the directory
        for file in os.listdir(input_path):
            if file.endswith(".txt"):
                input_file = os.path.join(input_path, file)
                parse_837_file(input_file, output_dir)
    elif os.path.isfile(input_path) and input_path.endswith(".txt"):
        # Parse a single file
        parse_837_file(input_path, output_dir)
    else:
        print("Invalid input path. Please provide a valid .txt file or directory.")
        exit(1)


if __name__ == "__main__":
    main()
