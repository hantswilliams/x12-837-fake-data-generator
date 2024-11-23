from flask import Flask, request, jsonify, send_file, render_template
import sys
import os
import io
import zipfile

# Add the root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Import API routes from api.py
from api import api  # Import the api instance from the api.py file

# Import the generator and parser logic
from generator_837.api.generator import generate_837_transaction
from parser_837.api.parser import parser_main

app = Flask(__name__)

# Web Routes
@app.route("/", methods=["GET"])
def index_home():
    return render_template("combined.html")

@app.route("/generate", methods=["POST"])
def web_generate():
    """
    Web interface for generating X12 837 files.
    """
    try:
        num_files = int(request.form.get("number", 1))

        if not (1 <= num_files <= 25):
            return jsonify({"error": "Number must be between 1 and 25."}), 400

        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for i in range(num_files):
                output = generate_837_transaction()
                zf.writestr(f"837_example_{i + 1}.txt", output)

        memory_file.seek(0)
        return send_file(memory_file, mimetype="application/zip", as_attachment=True, download_name="837_files.zip")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/parse", methods=["POST"])
def web_parse():
    """
    Web interface for parsing a single X12 837 file.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded."}), 400

        uploaded_file = request.files["file"]
        if not uploaded_file.filename.endswith(".txt"):
            return jsonify({"error": "Only .txt files are allowed."}), 400

        filename_base = uploaded_file.filename.replace(".txt", "")
        content = uploaded_file.read().decode("utf-8")

        input_file = io.StringIO(content)
        services, diagnoses, header = parser_main(input_file)

        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, "w") as zf:
            zf.writestr(f"{filename_base}_claim_service_lines.csv", services.getvalue())
            zf.writestr(f"{filename_base}_claim_diagnoses.csv", diagnoses.getvalue())
            zf.writestr(f"{filename_base}_header.csv", header.getvalue())

        memory_zip.seek(0)
        return send_file(memory_zip, mimetype="application/zip", as_attachment=True, download_name="parsed_837_files.zip")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Register the API with the Flask app
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5007, host="0.0.0.0")
