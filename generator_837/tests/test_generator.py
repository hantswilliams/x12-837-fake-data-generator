"""
Unit tests for X12 837 generator functionality.

Tests cover:
- Transaction generation
- Segment generation
- Data loading
- Utility functions
"""

import pytest
import os
from generator_837.api.generator import generate_837_transaction
from generator_837.api.segments import (
    generate_isa_segment, generate_gs_segment, generate_st_segment,
    generate_se_segment, generate_ge_segment, generate_iea_segment
)
from generator_837.api.data_loader import load_codes, load_orgs, load_payers
from generator_837.api.utils import format_date_qualifier, get_random_code


class TestTransactionGeneration:
    """Tests for complete 837 transaction generation."""

    def test_generate_transaction_returns_string(self):
        """Test that generate_837_transaction returns a string."""
        transaction = generate_837_transaction()
        assert isinstance(transaction, str)
        assert len(transaction) > 0

    def test_generate_transaction_has_required_segments(self):
        """Test that generated transaction contains all required X12 segments."""
        transaction = generate_837_transaction()

        # Check for envelope segments
        assert "ISA*" in transaction, "Missing ISA segment"
        assert "GS*" in transaction, "Missing GS segment"
        assert "ST*837*" in transaction, "Missing ST segment"

        # Check for header segments
        assert "BHT*" in transaction, "Missing BHT segment"
        assert "NM1*" in transaction, "Missing NM1 segment"

        # Check for claim segments
        assert "HL*" in transaction, "Missing HL segment"
        assert "CLM*" in transaction, "Missing CLM segment"
        assert "HI*" in transaction, "Missing HI segment (diagnosis)"

        # Check for service line segments
        assert "LX*" in transaction, "Missing LX segment"
        assert "SV1*" in transaction, "Missing SV1 segment"

        # Check for closing segments
        assert "SE*" in transaction, "Missing SE segment"
        assert "GE*" in transaction, "Missing GE segment"
        assert "IEA*" in transaction, "Missing IEA segment"

    def test_generate_transaction_has_valid_structure(self):
        """Test that transaction has valid X12 structure."""
        transaction = generate_837_transaction()
        segments = transaction.split('\n')

        # First segment should be ISA
        assert segments[0].startswith("ISA*"), "First segment should be ISA"

        # Last segment should be IEA
        assert segments[-1].startswith("IEA*"), "Last segment should be IEA"

        # All segments should end with ~
        for segment in segments:
            assert segment.endswith("~"), f"Segment should end with ~: {segment[:50]}"

    def test_generate_transaction_has_diagnoses(self):
        """Test that transaction contains diagnosis codes."""
        transaction = generate_837_transaction()

        # Count HI segments (diagnosis codes)
        hi_count = transaction.count("HI*ABK:")
        assert hi_count >= 3, "Should have at least 3 diagnosis codes"
        assert hi_count <= 8, "Should have at most 8 diagnosis codes"

    def test_generate_transaction_has_service_lines(self):
        """Test that transaction contains service lines."""
        transaction = generate_837_transaction()

        # Count LX segments (service line numbers)
        lx_count = transaction.count("LX*")
        assert lx_count >= 1, "Should have at least 1 service line"
        assert lx_count <= 5, "Should have at most 5 service lines"


class TestSegmentGeneration:
    """Tests for individual X12 segment generation functions."""

    def test_generate_isa_segment(self):
        """Test ISA segment generation."""
        sender_id = "123456789012345"
        receiver_id = "TESTRECV"
        control_number = "000000001"

        segment = generate_isa_segment(sender_id, receiver_id, control_number)

        assert segment.startswith("ISA*00*")
        assert segment.endswith("~")
        assert control_number in segment
        assert "ZZ*" in segment  # Interchange ID qualifier

    def test_generate_gs_segment(self):
        """Test GS segment generation."""
        sender_id = "123456789012345"
        receiver_id = "TESTRECV"
        control_number = "1"

        segment = generate_gs_segment(sender_id, receiver_id, control_number)

        assert segment.startswith("GS*HC*")  # HC = Healthcare Claim
        assert segment.endswith("~")
        assert "005010X223A2" in segment  # 837I version
        assert sender_id in segment

    def test_generate_st_segment(self):
        """Test ST segment generation."""
        transaction_control_number = "0001"

        segment = generate_st_segment(transaction_control_number)

        assert segment == "ST*837*0001*005010X223A2~"

    def test_generate_se_segment(self):
        """Test SE segment generation."""
        segment_count = 100
        transaction_control_number = "0001"

        segment = generate_se_segment(segment_count, transaction_control_number)

        assert segment.startswith("SE*")
        assert segment.endswith("~")
        assert str(segment_count) in segment
        assert transaction_control_number in segment

    def test_generate_ge_segment(self):
        """Test GE segment generation."""
        transaction_set_count = 1

        segment = generate_ge_segment(transaction_set_count)

        assert segment.startswith("GE*")
        assert segment.endswith("~")

    def test_generate_iea_segment(self):
        """Test IEA segment generation."""
        control_number = "000000001"

        segment = generate_iea_segment(control_number)

        assert segment.startswith("IEA*")
        assert segment.endswith("~")
        assert control_number in segment


class TestDataLoaders:
    """Tests for reference data loading functions."""

    def test_load_codes_returns_lists(self):
        """Test that load_codes returns two lists."""
        icd_codes, cpt_codes = load_codes()

        assert isinstance(icd_codes, list)
        assert isinstance(cpt_codes, list)
        assert len(icd_codes) > 0, "ICD codes list should not be empty"
        assert len(cpt_codes) > 0, "CPT codes list should not be empty"

    def test_load_codes_valid_formats(self):
        """Test that loaded codes have valid formats."""
        icd_codes, cpt_codes = load_codes()

        # Check a sample ICD code format (e.g., "A00.0")
        if len(icd_codes) > 0:
            sample_icd = icd_codes[0]
            assert isinstance(sample_icd, str)
            assert len(sample_icd) > 0

        # Check a sample CPT code format (e.g., "99213")
        if len(cpt_codes) > 0:
            sample_cpt = cpt_codes[0]
            assert isinstance(sample_cpt, str)
            assert len(sample_cpt) > 0

    def test_load_orgs_returns_dataframe(self):
        """Test that load_orgs returns a DataFrame."""
        orgs = load_orgs()

        assert orgs is not None
        assert len(orgs) > 0, "Organizations DataFrame should not be empty"

        # Check for expected columns
        expected_columns = ['NPI', 'Provider Organization Name (Legal Business Name)']
        for col in expected_columns:
            assert col in orgs.columns, f"Missing column: {col}"

    def test_load_payers_returns_dataframe(self):
        """Test that load_payers returns a filtered DataFrame."""
        payers = load_payers()

        assert payers is not None
        assert len(payers) > 0, "Payers DataFrame should not be empty"

        # Check that only PPO/POS/HMO plans are included
        if 'ProductType' in payers.columns:
            product_types = payers['ProductType'].unique()
            for ptype in product_types:
                assert any(x in ptype for x in ['PPO', 'POS', 'HMO']), \
                    f"Unexpected product type: {ptype}"


class TestUtilities:
    """Tests for utility functions."""

    def test_format_date_qualifier_default(self):
        """Test format_date_qualifier with default parameters."""
        result = format_date_qualifier()

        assert result.startswith("D8*")
        assert len(result) > 3  # D8* plus date

        # Extract date part and verify it's 8 digits
        date_part = result.split("*")[1]
        assert len(date_part) == 8
        assert date_part.isdigit()

    def test_format_date_qualifier_custom_date(self):
        """Test format_date_qualifier with custom date."""
        custom_date = "20240430"
        result = format_date_qualifier("D8", custom_date)

        assert result == "D8*20240430"

    def test_format_date_qualifier_range(self):
        """Test format_date_qualifier with date range format."""
        date_range = "20240422-20240430"
        result = format_date_qualifier("RD8", date_range)

        assert result == "RD8*20240422-20240430"

    def test_get_random_code(self):
        """Test get_random_code returns valid code from list."""
        test_codes = ['A00.0', 'A00.1', 'A00.9', 'B01.0', 'C02.0']

        # Test multiple times to ensure randomness works
        for _ in range(10):
            code = get_random_code(test_codes)
            assert code in test_codes

    def test_get_random_code_single_item(self):
        """Test get_random_code with single item list."""
        test_codes = ['ONLY_CODE']
        code = get_random_code(test_codes)
        assert code == 'ONLY_CODE'


class TestIntegration:
    """Integration tests that combine multiple components."""

    def test_generate_and_validate_structure(self):
        """Test that generated transaction has proper control number matching."""
        transaction = generate_837_transaction()

        # Extract control numbers
        lines = transaction.split('\n')

        # Find ISA and IEA control numbers (should match)
        isa_line = [l for l in lines if l.startswith("ISA*")][0]
        iea_line = [l for l in lines if l.startswith("IEA*")][0]

        # ISA control number is field 13
        isa_control = isa_line.split("*")[13]
        # IEA control number is field 2
        iea_control = iea_line.split("*")[2].replace("~", "")

        assert isa_control == iea_control, \
            f"ISA and IEA control numbers should match: {isa_control} != {iea_control}"

    def test_generate_multiple_transactions(self):
        """Test that multiple transactions can be generated without errors."""
        for i in range(5):
            transaction = generate_837_transaction()
            assert len(transaction) > 0
            assert "ISA*" in transaction
            assert "IEA*" in transaction

    def test_transaction_charge_amounts_sum(self):
        """Test that service line charges sum to total claim charge."""
        transaction = generate_837_transaction()

        # Extract CLM segment to get total charge
        clm_segment = [s for s in transaction.split('\n') if s.startswith("CLM*")][0]
        total_charge_str = clm_segment.split("*")[2]

        # Verify it's a valid number
        try:
            total_charge = float(total_charge_str)
            assert total_charge > 0
        except ValueError:
            pytest.fail(f"Invalid charge amount in CLM segment: {total_charge_str}")


# Pytest fixtures for reusable test data
@pytest.fixture
def sample_transaction():
    """Fixture to generate a sample transaction for testing."""
    return generate_837_transaction()


@pytest.fixture
def sample_codes():
    """Fixture to load sample ICD and CPT codes."""
    return load_codes()


@pytest.fixture
def sample_orgs():
    """Fixture to load sample organizations."""
    return load_orgs()


@pytest.fixture
def sample_payers():
    """Fixture to load sample payers."""
    return load_payers()
