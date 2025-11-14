"""
Unit tests for X12 837 parser functionality.

Tests cover:
- Main parser function
- Service line parsing
- Diagnosis parsing
- Header parsing
"""

import pytest
import io
import tempfile
import os
from parser_837.api.parser import parser_main
from parser_837.api.claim_services.cpt_hcpcs import parse_service_lines
from parser_837.api.claim_diagnoses.icd_diagnoses import parse_clm_diagnosis_segments
from parser_837.api.transaction_header.header import parse_header_data


# Sample 837 transaction for testing
SAMPLE_837_TRANSACTION = """ISA*00*          *00*          *ZZ*123456789012345*ZZ*TESTRECV       *250110*1234*U*00401*000000001*0*P*:~
GS*HC*123456789012345*TESTRECV*20250110*1234*1*X*005010X223A2~
ST*837*0001*005010X223A2~
BHT*0019*00*0001*20250110*1234*CH~
NM1*41*2*TEST HOSPITAL*****XX*1234567890~
PER*IC*John Doe*TE*5551234567~
NM1*40*2*TEST INSURANCE*****46*TESTINS001~
PER*IC*Jane Smith*TE*5559876543~
HL*1**20*1~
NM1*85*2*TEST HOSPITAL*****XX*1234567890~
N3*123 MAIN ST~
N4*TESTCITY*NY*12345~
REF*EI*12-3456789~
PER*IC*John Doe*TE*5551234567~
HL*2*1*22*0~
SBR*P*18*REF123******CI~
NM1*IL*1*PATIENT*TEST*M***MI*MEM123456~
N3*456 ELM ST~
N4*TESTCITY*NY*12345~
CLM*CLAIM123*500.00***11:B:1*Y*A*Y*Y~
DTP*434*RD8*20240422-20240430~
DTP*435*D8*20240809~
DTP*096*TM*2337~
HI*ABK:A000~
HI*ABK:B010~
HI*ABK:C020~
LX*1~
SV1*HC:99213*200.00*UN*1***1~
DTP*472*D8*20240428~
REF*6R*142671~
LX*2~
SV1*HC:99214*300.00*UN*1***2~
DTP*472*D8*20240428~
REF*6R*142672~
SE*35*0001~
GE*1*1~
IEA*1*000000001~"""


class TestParserMain:
    """Tests for main parser_main function."""

    def test_parser_main_with_string_path(self):
        """Test parser_main with file path string."""
        # Create temporary file with sample transaction
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(SAMPLE_837_TRANSACTION)
            temp_path = f.name

        try:
            services, diagnoses, header = parser_main(temp_path)

            # Verify all three outputs are returned
            assert services is not None
            assert diagnoses is not None
            assert header is not None

            # Verify they are StringIO objects or similar
            assert hasattr(services, 'getvalue')
            assert hasattr(diagnoses, 'getvalue')
            assert hasattr(header, 'getvalue')

        finally:
            os.unlink(temp_path)

    def test_parser_main_with_file_object(self):
        """Test parser_main with file object."""
        file_obj = io.StringIO(SAMPLE_837_TRANSACTION)

        services, diagnoses, header = parser_main(file_obj)

        assert services is not None
        assert diagnoses is not None
        assert header is not None

    def test_parser_main_invalid_input(self):
        """Test parser_main with invalid input type."""
        with pytest.raises(ValueError, match="Invalid input"):
            parser_main(12345)  # Invalid type

    def test_parser_main_returns_csv_data(self):
        """Test that parser_main returns CSV-formatted data."""
        file_obj = io.StringIO(SAMPLE_837_TRANSACTION)

        services, diagnoses, header = parser_main(file_obj)

        # Get the CSV content
        services_content = services.getvalue()
        diagnoses_content = diagnoses.getvalue()
        header_content = header.getvalue()

        # Verify they contain data (not empty)
        assert len(services_content) > 0, "Services CSV should not be empty"
        assert len(diagnoses_content) > 0, "Diagnoses CSV should not be empty"
        assert len(header_content) > 0, "Header CSV should not be empty"

        # Verify they look like CSV (contain commas or newlines)
        assert '\n' in services_content or ',' in services_content
        assert '\n' in diagnoses_content or ',' in diagnoses_content
        assert '\n' in header_content or ',' in header_content


class TestServiceLineParsing:
    """Tests for service line parsing functionality."""

    def test_parse_service_lines_basic(self):
        """Test basic service line parsing."""
        result = parse_service_lines(SAMPLE_837_TRANSACTION)

        assert result is not None
        assert hasattr(result, 'getvalue')

        content = result.getvalue()
        assert len(content) > 0

    def test_parse_service_lines_contains_cpt_codes(self):
        """Test that parsed service lines contain CPT codes."""
        result = parse_service_lines(SAMPLE_837_TRANSACTION)
        content = result.getvalue()

        # Our sample has CPT codes 99213 and 99214
        # The parser should extract these
        assert '99213' in content or '213' in content, "Should contain first CPT code"

    def test_parse_service_lines_with_no_services(self):
        """Test parsing transaction with no service lines."""
        minimal_transaction = """ISA*00*          *00*          *ZZ*TEST~
GS*HC*TEST~
ST*837*0001~
SE*3*0001~
GE*1*1~
IEA*1*000000001~"""

        result = parse_service_lines(minimal_transaction)
        assert result is not None


class TestDiagnosisParsing:
    """Tests for diagnosis code parsing functionality."""

    def test_parse_diagnoses_basic(self):
        """Test basic diagnosis parsing."""
        result = parse_clm_diagnosis_segments(SAMPLE_837_TRANSACTION)

        assert result is not None
        assert hasattr(result, 'getvalue')

        content = result.getvalue()
        assert len(content) > 0

    def test_parse_diagnoses_contains_codes(self):
        """Test that parsed diagnoses contain ICD codes."""
        result = parse_clm_diagnosis_segments(SAMPLE_837_TRANSACTION)
        content = result.getvalue()

        # Our sample has diagnosis codes A000, B010, C020
        # Check if at least one is present
        has_diagnosis = any(code in content for code in ['A000', 'B010', 'C020', 'A00', 'B01', 'C02'])
        assert has_diagnosis, "Should contain at least one diagnosis code"

    def test_parse_diagnoses_with_no_diagnoses(self):
        """Test parsing transaction with no diagnoses."""
        minimal_transaction = """ISA*00*          *00*          *ZZ*TEST~
GS*HC*TEST~
ST*837*0001~
SE*3*0001~
GE*1*1~
IEA*1*000000001~"""

        result = parse_clm_diagnosis_segments(minimal_transaction)
        assert result is not None


class TestHeaderParsing:
    """Tests for header data parsing functionality."""

    def test_parse_header_basic(self):
        """Test basic header parsing."""
        result = parse_header_data(SAMPLE_837_TRANSACTION)

        assert result is not None
        assert hasattr(result, 'getvalue')

        content = result.getvalue()
        assert len(content) > 0

    def test_parse_header_contains_transaction_info(self):
        """Test that parsed header contains transaction information."""
        result = parse_header_data(SAMPLE_837_TRANSACTION)
        content = result.getvalue()

        # Should contain some transaction identifiers
        # Check for ST segment transaction control number
        assert '0001' in content or 'ST' in content or '837' in content

    def test_parse_header_with_minimal_transaction(self):
        """Test header parsing with minimal transaction."""
        minimal_transaction = """ISA*00*          *00*          *ZZ*TEST~
GS*HC*TEST~
ST*837*0001~
BHT*0019*00*0001~
SE*4*0001~
GE*1*1~
IEA*1*000000001~"""

        result = parse_header_data(minimal_transaction)
        assert result is not None


class TestIntegration:
    """Integration tests for complete parsing workflow."""

    def test_generate_and_parse_roundtrip(self):
        """Test generating a transaction and parsing it back."""
        # This test requires generator - import only if available
        try:
            from generator_837.api.generator import generate_837_transaction

            # Generate a transaction
            transaction = generate_837_transaction()

            # Parse it
            services, diagnoses, header = parser_main(io.StringIO(transaction))

            # Verify all outputs have content
            assert len(services.getvalue()) > 0
            assert len(diagnoses.getvalue()) > 0
            assert len(header.getvalue()) > 0

        except ImportError:
            pytest.skip("Generator module not available for integration test")

    def test_parse_file_to_csvs(self):
        """Test complete workflow of parsing file to CSV outputs."""
        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(SAMPLE_837_TRANSACTION)
            temp_input = f.name

        try:
            # Parse the file
            services, diagnoses, header = parser_main(temp_input)

            # Write to temporary CSV files
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
                f.write(services.getvalue())
                temp_services = f.name

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
                f.write(diagnoses.getvalue())
                temp_diagnoses = f.name

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
                f.write(header.getvalue())
                temp_header = f.name

            # Verify files were created and have content
            try:
                assert os.path.exists(temp_services)
                assert os.path.exists(temp_diagnoses)
                assert os.path.exists(temp_header)

                assert os.path.getsize(temp_services) > 0
                assert os.path.getsize(temp_diagnoses) > 0
                assert os.path.getsize(temp_header) > 0

            finally:
                # Cleanup CSV files
                for temp_file in [temp_services, temp_diagnoses, temp_header]:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)

        finally:
            # Cleanup input file
            os.unlink(temp_input)


# Pytest fixtures
@pytest.fixture
def sample_transaction_string():
    """Fixture providing sample 837 transaction as string."""
    return SAMPLE_837_TRANSACTION


@pytest.fixture
def sample_transaction_file():
    """Fixture providing sample 837 transaction as temporary file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(SAMPLE_837_TRANSACTION)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def parsed_sample():
    """Fixture providing parsed sample transaction."""
    return parser_main(io.StringIO(SAMPLE_837_TRANSACTION))
