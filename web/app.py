from flask import Flask, request, jsonify, send_file, render_template
from flask_restx import Api, Resource, fields
import os
import io
import zipfile
import sys

# Add the root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from generator_837.api.generator import generate_837_transaction
from parser_837.api.parser import parser_main

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index_home():
    return render_template("combined.html")

# Set up Flask-RESTx for API and docs, move docs to a custom path
api = Api(
    app,
    title="X12 837 Generator and Parser",
    version="1.0",
    description="API for generating and parsing X12 837 files",
    doc="/api-docs"  # Custom documentation route
)

# Define API namespaces
generator_ns = api.namespace('generator', description='Generate X12 837 files')
parser_ns = api.namespace('parser', description='Parse X12 837 files')

# Generator endpoint model
generate_model = api.model('GenerateRequest', {
    'number': fields.Integer(required=True, description='Number of files to generate (1-25)', min=1, max=25)
})

# Parser endpoint model
parse_model = api.model('ParseResponse', {
    'message': fields.String(description='Status message'),
    'error': fields.String(description='Error message, if any')
})

@generator_ns.route("/generate")
class GenerateAPI(Resource):
    @api.expect(generate_model)
    @api.response(200, "Files generated successfully")
    @api.response(400, "Invalid input")
    @api.response(500, "Internal server error")
    def post(self):
        """
        Generate X12 837 files.
        Accepts a `number` parameter and returns a ZIP file with the generated files.
        """
        try:
            # Get parameters from the request
            data = request.json
            num_files = data.get("number", 1)

            if not (1 <= num_files <= 25):
                return {"error": "Number must be between 1 and 25."}, 400

            # Use an in-memory zip file
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                for i in range(num_files):
                    output = generate_837_transaction()
                    # Add each file to the zip archive in memory
                    zf.writestr(f"837_example_{i + 1}.txt", output)

            memory_file.seek(0)

            # Send the zip file for download
            return send_file(
                memory_file,
                mimetype="application/zip",
                as_attachment=True,
                download_name="837_files.zip"
            )

        except Exception as e:
            return {"error": str(e)}, 500

@parser_ns.route("/parse")
class ParseAPI(Resource):
    @api.response(200, "File parsed successfully")
    @api.response(400, "Invalid input")
    @api.response(500, "Internal server error")
    def post(self):
        """
        Parse a single X12 837 file into CSVs.
        Accepts a file upload and returns a ZIP file with the parsed CSVs.
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

            # Use parser_main to parse the content
            input_file = io.StringIO(content)
            services, diagnoses, header = parser_main(input_file)

            # In-memory ZIP file to store output CSVs
            memory_zip = io.BytesIO()
            with zipfile.ZipFile(memory_zip, "w") as zf:
                zf.writestr(f"{filename_base}_claim_service_lines.csv", services.getvalue())
                zf.writestr(f"{filename_base}_claim_diagnoses.csv", diagnoses.getvalue())
                zf.writestr(f"{filename_base}_header.csv", header.getvalue())

            memory_zip.seek(0)

            # Return ZIP file for download
            return send_file(memory_zip, mimetype="application/zip", as_attachment=True, download_name="parsed_837_files.zip")

        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, port=5007, host="0.0.0.0")
