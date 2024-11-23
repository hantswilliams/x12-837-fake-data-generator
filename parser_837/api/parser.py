from .claim_services.cpt_hcpcs import parse_service_lines
from .claim_diagnoses.icd_diagnoses import parse_clm_diagnosis_segments
from .transaction_header.header import parse_header_data

def parser_main(file):
    """
    Parse the content of an 837 file.

    Args:
        file (str or TextIOWrapper): Path to the file or file content.

    Returns:
        tuple: Services CSV, Diagnoses CSV, Header CSV
    """
    # Ensure the input is file content, not a file object
    if hasattr(file, "read"):
        file_content = file.read()  # Read content from the file object
    elif isinstance(file, str):
        # Read file content from the given path
        with open(file, "r") as f:
            file_content = f.read()
    else:
        raise ValueError("Invalid input. Must be a file object or filepath string.")

    print(f"Parsing file {file}")
    
    # Pass the content instead of filepath
    services = parse_service_lines(file_content)
    diagnoses = parse_clm_diagnosis_segments(file_content)
    header = parse_header_data(file_content)

    return services, diagnoses, header