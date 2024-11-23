from flask import Flask, request, jsonify, send_file, render_template
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
def index():
    return render_template("combined.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Get parameters from the request
        num_files = int(request.form.get("number", 1))

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
        return jsonify({"error": str(e)}), 500

@app.route("/parse", methods=["POST"])
def parse_files():
    try:
        # Ensure files are uploaded
        if "files" not in request.files:
            return jsonify({"error": "No files uploaded."}), 400

        # Get uploaded files
        uploaded_files = request.files.getlist("files")
        if not uploaded_files:
            return jsonify({"error": "No valid files found."}), 400

        # In-memory ZIP file to store output CSVs
        memory_zip = io.BytesIO()

        # Parse each file and add outputs to the ZIP
        with zipfile.ZipFile(memory_zip, "w") as zf:
            for file in uploaded_files:
                if not file.filename.endswith(".txt"):
                    continue

                filename_base = file.filename.replace(".txt", "")
                content = file.read().decode("utf-8")

                # Use parser_main to parse the content
                input_file = io.StringIO(content)
                services, diagnoses, header = parser_main(input_file)

                # Extract content from StringIO and add to the ZIP
                zf.writestr(f"{filename_base}_claim_service_lines.csv", services.getvalue())
                zf.writestr(f"{filename_base}_claim_diagnoses.csv", diagnoses.getvalue())
                zf.writestr(f"{filename_base}_header.csv", header.getvalue())

        memory_zip.seek(0)

        # Return ZIP file for download
        return send_file(memory_zip, mimetype="application/zip", as_attachment=True, download_name="parsed_837_files.zip")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5007, host="0.0.0.0")
