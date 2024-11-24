from flask_restx import Api, Resource, fields
from flask import request, send_file
import io
import zipfile
from generator_837.api.generator import generate_837_transaction
from parser_837.api.parser import parser_main

# Set up Flask-RESTx for API and docs
api = Api(
    title="X12 837 Generator and Parser",
    version="1.0",
    description="API for generating and parsing X12 837 files",
    doc="/api"  # Set the documentation to a non-root path
)

# Define API namespaces
generator_ns = api.namespace('api/generate', description='Generate X12 837 files programmatically')
parser_ns = api.namespace('api/parse', description='Parse X12 837 files programmatically')

# Generator endpoint model
generate_model = api.model('GenerateRequest', {
    'number': fields.Integer(required=True, description='Number of files to generate (1-25)', min=1, max=25)
})

# Parser endpoint model
parse_model = api.model('ParseResponse', {
    'message': fields.String(description='Status message'),
    'error': fields.String(description='Error message, if any')
})

# REST API Routes
@generator_ns.route("/", defaults={'count': None}, methods=["GET", "POST"])
@generator_ns.route("/<int:count>", methods=["GET"])
class GenerateAPI(Resource):
    @api.expect(generate_model, validate=True)
    @api.response(200, "Files generated successfully")
    @api.response(400, "Invalid input")
    @api.response(500, "Internal server error")
    def post(self):
        """
        RESTful API for generating X12 837 files.
        Generates the requested number of 837 files and returns them as a ZIP.
        """
        try:
            data = request.json
            num_files = data.get("number", 1)

            if not (1 <= num_files <= 25):
                return {"error": "Number must be between 1 and 25."}, 400

            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                for i in range(num_files):
                    output = generate_837_transaction()
                    zf.writestr(f"837_example_{i + 1}.txt", output)

            memory_file.seek(0)
            return send_file(
                memory_file,
                mimetype="application/zip",
                as_attachment=True,
                download_name="837_files.zip"
            )

        except Exception as e:
            return {"error": str(e)}, 500

    @api.response(200, "Fake claim generated successfully")
    @api.response(400, "Invalid input")
    @api.response(500, "Internal server error")
    @api.doc(params={'count': 'Number of fake claims to generate (default is 1, max is 25)'})
    def get(self, count=None):
        """
        RESTful API for generating a single or multiple X12 837 files.
        Generates the requested number of claims (default 1) and returns them as text files.
        """
        try:
            # Use `count` from the route or default to 1
            num_claims = int(count) if count else 1
            if not (1 <= num_claims <= 25):
                return {"error": "Number must be between 1 and 25."}, 400

            # Generate the requested number of fake claims
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                for i in range(num_claims):
                    fake_claim = generate_837_transaction()
                    zf.writestr(f"fake_claim_{i + 1}.txt", fake_claim)

            memory_file.seek(0)
            return send_file(
                memory_file,
                mimetype="application/zip",
                as_attachment=True,
                download_name=f"{num_claims}_fake_claims.zip"
            )

        except Exception as e:
            print(f"Error during fake claim generation: {str(e)}")
            return {"error": str(e)}, 500




@parser_ns.route("/")
class ParseAPI(Resource):
    @api.response(200, "File parsed successfully")
    @api.response(400, "Invalid input")
    @api.response(500, "Internal server error")
    def post(self):
        """
        RESTful API for parsing a single X12 837 file.
        Parses an uploaded 837 text file and returns the parsed data as a ZIP file.
        """
        try:
            # Ensure a file is uploaded
            if "file" not in request.files:
                return {"error": "No file uploaded."}, 400

            uploaded_file = request.files["file"]
            if not uploaded_file.filename.endswith(".txt"):
                return {"error": "Only .txt files are allowed."}, 400

            filename_base = uploaded_file.filename.replace(".txt", "")
            content = uploaded_file.read().decode("utf-8")

            # Use parser_main to parse the file content
            input_file = io.StringIO(content)
            services, diagnoses, header = parser_main(input_file)

            # Create an in-memory ZIP file
            memory_zip = io.BytesIO()
            with zipfile.ZipFile(memory_zip, "w") as zf:
                zf.writestr(f"{filename_base}_claim_service_lines.csv", services.getvalue())
                zf.writestr(f"{filename_base}_claim_diagnoses.csv", diagnoses.getvalue())
                zf.writestr(f"{filename_base}_header.csv", header.getvalue())

            memory_zip.seek(0)
            return send_file(memory_zip, mimetype="application/zip", as_attachment=True, download_name="parsed_837_files.zip")

        except Exception as e:
            # Log the error and return it
            print(f"Error during parsing: {str(e)}")
            return {"error": str(e)}, 500

    # @api.response(200, "Parser is available and ready.")
    # def get(self):
    #     """
    #     Test the parser API.
    #     Returns a success message to confirm that the endpoint is reachable.
    #     """
    #     try:
    #         return {"message": "Parser API is up and running."}, 200
    #     except Exception as e:
    #         print(f"Error during parser testing: {str(e)}")
    #         return {"error": str(e)}, 500
