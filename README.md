# x12-837-fake-data-generator
Fake generator for X12 837 form 

## Required Loops and Segments:

### Heading Section:
- ST: Transaction Set Header (mandatory)
- BHT: Beginning of Hierarchical Transaction (mandatory)
- NM1 Loop 1000 for Submitter and Receiver, with optional N3 (address), N4 (geographic location), and PER (contact information).

### Detail Section:
- HL (Hierarchical Level) in Loop 2000 (mandatory) to represent different levels (e.g., billing provider, subscriber).
- NM1 Loop 2010 for individual providers (billing, pay-to provider, etc.), with optional N3 (address), N4 (geographic), DMG (demographic), and PER segments.

### Claim Level:
- CLM Loop 2300 contains the main CLM segment and can contain additional data such as DTP (Date or Time Period), HI (Health Care Diagnosis Codes), and REF (reference identifiers).

### Service Line Level (Loop 2400):
- Each service line must contain LX (Line Number) and SV1 (Professional Service) or SV2 (Institutional Service).
- May contain DTP, QTY, and REF segments.

## Common Missing Segments:
### Loop 1000:
- Ensure that NM1-40 (Receiver) and NM1-41 (Submitter) both include necessary segments.
### Loop 2010 for Billing Provider:
- REF segment after NM1-85 with the Tax ID (qualifier EI).
- Optional N3 and N4 segments for billing provider address details.
### Loop 2000 
- With HL for defining hierarchical levels (this might be required if not already included).

# PARSING: 
- https://github.com/databricks-industry-solutions/x12-edi-parser 

# API PARSING: 
- https://datainsight.health/clinsight/swagger-ui/index.html#/File/fetchFiles 