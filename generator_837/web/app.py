from flask import Flask, request, jsonify, render_template, send_file
import os
import io
import zipfile
import sys

# Add the root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from generator_837.api.generator import generate_837_transaction

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True, port=5005, host="0.0.0.0")
