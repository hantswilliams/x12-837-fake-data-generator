import argparse
import os
from api.generator import generate_837_transaction

def list_available_functions():
    """
    Returns a list of available functions in the api.generator module.
    """
    return [
        "generate_837_transaction: Generate a complete 837 transaction file.",
        # Add more function references here as needed
    ]

def main():
    parser = argparse.ArgumentParser(
        description="Generate X12 837 transactions with options for customization.",
        epilog="Use --functions to list available functions in the module."
    )
    parser.add_argument(
        "-n", "--number", type=int, default=1,
        help="Number of 837 files to generate. Default is 1."
    )
    parser.add_argument(
        "-o", "--output", type=str, default="837_generator_output",
        help="Directory to save the generated 837 files. Default is '837_generator_output'."
    )
    parser.add_argument(
        "--functions", action="store_true",
        help="List available functions in the api.generator module and their descriptions."
    )
    args = parser.parse_args()

    # Display available functions if --functions is used
    if args.functions:
        print("Available Functions in api.generator:")
        for func in list_available_functions():
            print(f" - {func}")
        return

    # Ensure the output directory exists or create it
    try:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
            print(f"Output directory '{args.output}' created.")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        return

    # Generate files
    for i in range(args.number):
        try:
            example_output = generate_837_transaction()
            file_path = os.path.join(args.output, f"837_example_{i + 1}.txt")
            with open(file_path, "w") as file:
                file.write(example_output)
            print(f"837 Example {i + 1} generated successfully: {file_path}")
        except Exception as e:
            print(f"Error generating 837 file {i + 1}: {e}")

    print("All files have been generated successfully!")

if __name__ == "__main__":
    main()


## python {X}/837.py --help

