let pyodide;
let generatorLoaded = false;
let parserLoaded = false;

// Initialize Pyodide
async function initPyodide() {
    try {
        pyodide = await loadPyodide();

        // Load required packages
        await pyodide.loadPackage(['micropip', 'pandas']);

        // Install faker
        await pyodide.runPythonAsync(`
            import micropip
            await micropip.install('faker')
        `);

        // Load the generator and parser code
        await loadGeneratorCode();
        await loadParserCode();

        // Hide loading, show app
        document.getElementById('loading').style.display = 'none';
        document.getElementById('app').style.display = 'block';

        console.log('Pyodide initialized successfully!');
    } catch (error) {
        console.error('Error initializing Pyodide:', error);
        document.getElementById('loading').innerHTML = `
            <div style="color: red;">
                <h2>❌ Error loading Python environment</h2>
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Load generator Python code
async function loadGeneratorCode() {
    const generatorCode = `
import io
from faker import Faker
import random
from datetime import datetime

fake = Faker()

def generate_837_transaction():
    """Generate a simple X12 837 transaction for demonstration"""

    # Generate random claim data
    claim_id = f"CLM{random.randint(100000, 999999)}"
    patient_name = fake.name()
    patient_dob = fake.date_of_birth(minimum_age=1, maximum_age=90).strftime("%Y%m%d")
    service_date = fake.date_this_year().strftime("%Y%m%d")
    charge_amount = f"{random.randint(100, 5000)}.00"

    # Simple 837 structure
    transaction = f"""ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*^*00501*{random.randint(100000000, 999999999)}*0*P*:~
GS*HC*SENDER*RECEIVER*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*{random.randint(1, 9999)}*X*005010X222A1~
ST*837*{random.randint(1000, 9999)}*005010X222A1~
BHT*0019*00*{random.randint(1, 9999)}*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*CH~
NM1*41*2*{fake.company()}*****46*{random.randint(1000000000, 9999999999)}~
NM1*40*2*{fake.company()}*****46*{random.randint(1000000000, 9999999999)}~
HL*1**20*1~
NM1*85*2*{fake.company()}*****XX*{random.randint(1000000000, 9999999999)}~
HL*2*1*22*0~
SBR*P*18*******CI~
NM1*IL*1*{patient_name.split()[-1]}*{patient_name.split()[0]}****MI*{random.randint(100000000, 999999999)}~
DMG*D8*{patient_dob}*{random.choice(['M', 'F'])}~
NM1*PR*2*{fake.company()}*****PI*{random.randint(10000, 99999)}~
CLM*{claim_id}*{charge_amount}***11:B:1*Y*A*Y*Y~
DTP*472*D8*{service_date}~
LX*1~
SV1*HC:99213*{charge_amount}*UN*1***1~
DTP*472*D8*{service_date}~
SE*{random.randint(20, 40)}*{random.randint(1000, 9999)}~
GE*1*{random.randint(1, 9999)}~
IEA*1*{random.randint(100000000, 999999999)}~"""

    return transaction

generatorLoaded = True
    `;

    await pyodide.runPythonAsync(generatorCode);
    generatorLoaded = true;
}

// Load parser Python code
async function loadParserCode() {
    const parserCode = `
import io
import csv

def parse_837_simple(content):
    """Simple parser to extract basic claim information"""
    segments = content.split('~')

    claims = []
    services = []
    headers = []

    # Track header info
    header_info = {}

    for segment in segments:
        segment = segment.strip()
        elements = segment.split('*')

        # ISA - Interchange Control Header
        if segment.startswith('ISA'):
            header_info['ISA_Sender'] = elements[6] if len(elements) > 6 else ''
            header_info['ISA_Receiver'] = elements[8] if len(elements) > 8 else ''
            header_info['ISA_Date'] = elements[9] if len(elements) > 9 else ''
            header_info['ISA_Time'] = elements[10] if len(elements) > 10 else ''
            header_info['ISA_Control_Number'] = elements[13] if len(elements) > 13 else ''

        # GS - Functional Group Header
        elif segment.startswith('GS'):
            header_info['GS_Sender'] = elements[2] if len(elements) > 2 else ''
            header_info['GS_Receiver'] = elements[3] if len(elements) > 3 else ''
            header_info['GS_Date'] = elements[4] if len(elements) > 4 else ''
            header_info['GS_Time'] = elements[5] if len(elements) > 5 else ''
            header_info['GS_Control_Number'] = elements[6] if len(elements) > 6 else ''

        # ST - Transaction Set Header
        elif segment.startswith('ST'):
            header_info['ST_Transaction_Type'] = elements[1] if len(elements) > 1 else ''
            header_info['ST_Control_Number'] = elements[2] if len(elements) > 2 else ''

        # BHT - Beginning of Hierarchical Transaction
        elif segment.startswith('BHT'):
            header_info['BHT_Purpose'] = elements[2] if len(elements) > 2 else ''
            header_info['BHT_Reference'] = elements[3] if len(elements) > 3 else ''
            header_info['BHT_Date'] = elements[4] if len(elements) > 4 else ''
            header_info['BHT_Time'] = elements[5] if len(elements) > 5 else ''

        # CLM - Claim Information
        elif segment.startswith('CLM'):
            claim = {
                'Claim_ID': elements[1] if len(elements) > 1 else '',
                'Claim_Amount': elements[2] if len(elements) > 2 else ''
            }
            claims.append(claim)

        # SV1 - Service Line
        elif segment.startswith('SV1'):
            service = {
                'Service_Code': elements[1] if len(elements) > 1 else '',
                'Service_Amount': elements[2] if len(elements) > 2 else ''
            }
            services.append(service)

    # Add header info to list
    if header_info:
        headers.append(header_info)

    # Convert to CSV
    claims_csv = io.StringIO()
    if claims:
        writer = csv.DictWriter(claims_csv, fieldnames=['Claim_ID', 'Claim_Amount'])
        writer.writeheader()
        writer.writerows(claims)

    services_csv = io.StringIO()
    if services:
        writer = csv.DictWriter(services_csv, fieldnames=['Service_Code', 'Service_Amount'])
        writer.writeheader()
        writer.writerows(services)

    headers_csv = io.StringIO()
    if headers:
        fieldnames = ['ISA_Sender', 'ISA_Receiver', 'ISA_Date', 'ISA_Time', 'ISA_Control_Number',
                     'GS_Sender', 'GS_Receiver', 'GS_Date', 'GS_Time', 'GS_Control_Number',
                     'ST_Transaction_Type', 'ST_Control_Number',
                     'BHT_Purpose', 'BHT_Reference', 'BHT_Date', 'BHT_Time']
        writer = csv.DictWriter(headers_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(headers)

    return {
        'claims': claims_csv.getvalue(),
        'services': services_csv.getvalue(),
        'headers': headers_csv.getvalue()
    }

parserLoaded = True
    `;

    await pyodide.runPythonAsync(parserCode);
    parserLoaded = true;
}

// Switch between tabs
function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Generate X12 files
async function generateFiles() {
    const numFiles = parseInt(document.getElementById('num-files').value);
    const statusDiv = document.getElementById('generator-status');
    const outputDiv = document.getElementById('generator-output');

    if (numFiles < 1 || numFiles > 25) {
        statusDiv.className = 'status error';
        statusDiv.textContent = 'Please enter a number between 1 and 25';
        return;
    }

    try {
        statusDiv.className = 'status info';
        statusDiv.textContent = `Generating ${numFiles} file(s)...`;
        outputDiv.innerHTML = '';

        const files = [];

        for (let i = 0; i < numFiles; i++) {
            const result = await pyodide.runPythonAsync('generate_837_transaction()');
            files.push({
                name: `claim_${String(i + 1).padStart(3, '0')}.txt`,
                content: result
            });
        }

        // Create download links
        outputDiv.innerHTML = '<h3>Generated Files:</h3>';
        files.forEach(file => {
            const blob = new Blob([file.content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = file.name;
            link.className = 'file-download';
            link.textContent = `📄 ${file.name}`;
            outputDiv.appendChild(link);
        });

        statusDiv.className = 'status success';
        statusDiv.textContent = `✅ Successfully generated ${numFiles} file(s)!`;

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = `❌ Error: ${error.message}`;
        console.error(error);
    }
}

// Parse X12 file
async function parseFile() {
    const fileInput = document.getElementById('file-upload');
    const statusDiv = document.getElementById('parser-status');
    const outputDiv = document.getElementById('parser-output');

    if (!fileInput.files.length) {
        statusDiv.className = 'status error';
        statusDiv.textContent = 'Please select a file first';
        return;
    }

    try {
        statusDiv.className = 'status info';
        statusDiv.textContent = 'Parsing file...';
        outputDiv.innerHTML = '';

        const file = fileInput.files[0];
        const content = await file.text();

        // Parse the file
        pyodide.globals.set('file_content', content);
        const result = await pyodide.runPythonAsync(`
            parse_837_simple(file_content)
        `);

        const parsed = result.toJs();
        const claims = parsed.get('claims');
        const services = parsed.get('services');
        const headers = parsed.get('headers');

        // Create download links
        outputDiv.innerHTML = '<h3>Parsed Data:</h3>';

        if (headers) {
            const blob0 = new Blob([headers], { type: 'text/csv' });
            const url0 = URL.createObjectURL(blob0);
            const link0 = document.createElement('a');
            link0.href = url0;
            link0.download = 'header.csv';
            link0.className = 'file-download';
            link0.textContent = '📊 header.csv';
            outputDiv.appendChild(link0);
        }

        if (claims) {
            const blob1 = new Blob([claims], { type: 'text/csv' });
            const url1 = URL.createObjectURL(blob1);
            const link1 = document.createElement('a');
            link1.href = url1;
            link1.download = 'claims.csv';
            link1.className = 'file-download';
            link1.textContent = '📊 claims.csv';
            outputDiv.appendChild(link1);
        }

        if (services) {
            const blob2 = new Blob([services], { type: 'text/csv' });
            const url2 = URL.createObjectURL(blob2);
            const link2 = document.createElement('a');
            link2.href = url2;
            link2.download = 'services.csv';
            link2.className = 'file-download';
            link2.textContent = '📊 services.csv';
            outputDiv.appendChild(link2);
        }

        statusDiv.className = 'status success';
        statusDiv.textContent = '✅ Successfully parsed file!';

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = `❌ Error: ${error.message}`;
        console.error(error);
    }
}

// Initialize when page loads
window.addEventListener('DOMContentLoaded', initPyodide);
