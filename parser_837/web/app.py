from flask import Flask, request, jsonify, send_file, render_template
import os
import io
import zipfile
import sys

# Add the root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from parser_837.api.parser import parser_main

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Simple form for file upload

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
    app.run(debug=True, port=5005, host="0.0.0.0")
