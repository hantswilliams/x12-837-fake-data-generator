import datetime

## https://www.hcmhrsb.org/wp-content/uploads/2017/10/SHARES-837P-Companion-Guide-HAMI.pdf
## https://www.in.gov/health/cshcs/files/ISDH_Companion_Guide_837P_V2_5__2_.pdf
## https://www.bcbsnm.com/pdf/837_prof_compguide.pdf
## https://www.stedi.com/edi/x12/segment/PER



## ISA Interchange Control Header
## The Interchange Control Header starts and identifies an electronic interchange of functional groups.
def generate_isa_segment(sender_id, receiver_id, control_number):
    ## ## https://providers.bcbsla.com/-/media/Files/Providers/5010_Institutional_Claims_Companion_Guide%20pdf.pdf
    ## ISA has 16 fields
        ## ISA01 - Authorization Information Qualifier (2 characters): value: 00
        ## ISA02 - Authorization Information (10 characters): value: 1234567890
        ## ISA03 - Security Information Qualifier (2 characters): value: 00
        ## ISA04 - Security Information (10 characters): value: 1234567890
        ## ISA05 - Interchange ID Qualifier (2 characters): value: ZZ
        ## ISA06 - Interchange Sender ID (15 characters): 998877665544333
            ## id will be assigned by the health plan
            ## fixed length of 15 characters
            ## !!!!!!!gs02 must contain the same value as isa06
        ## ISA07 - Interchange ID Qualifier (2 characters): value: ZZ
        ## ISA08 - Interchange Receiver ID (15 characters): value: BCBSLA001
            ## id will be assigned by the health plan
        ## ISA09 - Interchange Date (6 characters): value: YYMMDD
            ## Use YYMMDD format
        ## ISA10 - Interchange Time (4 characters): value: HHMM
            ## Use HHMM format
        ## ISA11 - Interchange Control Standards Identifier (1 character): value: ^
            ## Use ^ (carat)
        ## ISA12 - Interchange Control Version Number (5 characters): value: 00501 
            ## Must use 00501
        ## ISA13 - Interchange Control Number (9 characters): value: XXXX
            ## Must be identical to value in IEA02
        ## ISA14 - Acknowledgment Requested (1 character): value: 1
            ## Can be 0 or 1
        ## ISA15 - Usage Indicator (1 character): value: T
            ## Must be T for test or P for production
        ## ISA16 - Component Element Separator (1 character): value: :
            ## Use : (colon)
    sender_id_padded = sender_id.ljust(15)
    receiver_id_padded = receiver_id.ljust(15)
    return (
        f"ISA*00*          *00*          *ZZ*{sender_id_padded}*ZZ*{receiver_id_padded}*"
        f"{datetime.datetime.now():%y%m%d}*{datetime.datetime.now():%H%M}*U*00401*{control_number}*0*P*:~"
    )




## GS Segment
## indicates the beginning of a functional group and provides
## control information. The GS segment has 8 fields.
def generate_gs_segment(sender_id, receiver_id, control_number):
    ## https://providers.bcbsla.com/-/media/Files/Providers/5010_Institutional_Claims_Companion_Guide%20pdf.pdf
    ## Functional Group GS (header) has 8 fields
        ## GS01 - Functional Identifier Code (2 characters): value: HC
            ## 837 Institutional = HC
            ## HC = Healthcare Claim
        ## GS02 - Application Sender's Code (15 characters): value: 998877665544333
            ## !!!!!!!!Must use Submitter ID number assigned by BCBSLA. Must contain same value as ISA06.
        ## GS03 - Application Receiver's Code (15 characters): value: BCBSLA001
            ## Will be provided by health plan
        ## GS04 - Date (8 characters): value: CCYYMMDD
            ## Creation Date in CCYYMMDD format
        ## GS05 - Time (4 characters): value: HHMM
            ## Creation Time in HHMM format
        ## GS06 - Group Control Number (9 characters): value: 998877665544333
            ## !!!!!!!!!!Same as GS02
        ## GS07 - Responsible Agency Code (2 characters): value: X
            ## Must be X Accredited Standards Committee X12
        ## GS08 - Version/Release/Industry Identifier Code (12 characters)
            ## For 837I must be: 005010X223A2
    return (
        f"GS*HC*{sender_id}*{receiver_id}*{datetime.datetime.now():%Y%m%d}*{datetime.datetime.now():%H%M}*{control_number}*X*005010X223A2~"
    )



## ST Segment
def generate_st_segment(transaction_control_number):
    ## To indicate the start of a transaction set and to assign a control number
    ## https://providers.bcbsla.com/-/media/Files/Providers/5010_Institutional_Claims_Companion_Guide%20pdf.pdf
    ## Transaction Set Header ST (header) has 3 fields
        ## ST02 - Transaction Set Identifier Code (3 characters): value: 837
            ## Assigned by the sender (ST02 must be identical to SE02). Field must contain 4 – 9 positions and cannot contain more
            ## than 3 leading zeros.
        ## SE02 - Transaction Set Identifier Code (3 characters): value: 837
            ## Assigned by the sender (ST02 must be identical to SE02). Field must contain 4 – 9 positions and cannot contain more
            ## than 3 leading zeros.
        ## ST03 - Implementation Convention Reference (5-6 characters): value: 005010X223A2
            ## For 837 Institutional must use: 005010X223A2
    return f"ST*837*{transaction_control_number}*005010X223A2~"





##### BHT Segment
def generate_bht_segment():
    ## https://www.stedi.com/edi/x12/segment/BHT  - for values
    ## To define the business hierarchical structure of the transaction set and identify the business application purpose and reference data, i.e., number, date, and time
    ## Contains 6 fields
        ## BHT01 - Hierarchical Structure Code (4 characters): value:  [manditory]
            ## 0060	Hospital, ancillary facility or department
	        ## 0061 Health Industry Business Communications Council (HIBCC) Health Industry Number (HIN) database, facility record, location record 
        ## BHT02 - Transaction Set Purpose Code (2 characters): value:  [manditory]
            ## Code identifying purpose of transaction set
            ## 00   Original
            ## 02	Add
        ## BHT03 - Reference Identification (2-30 characters): value:  [optional]
            ## NOT INCLUDED 
        ## BHT04 - Date (8 characters): value: CCYYMMDD
            ## Date in CCYYMMDD format
        ## BHT05 - Time (4 characters): value: HHMM
            ## Time in HHMM format
        ## BHT06 - Transaction Type Code (2-2 characters): value: CH
            ## CH	Chargeable  ? 
    return f"BHT*0019*00*{datetime.datetime.now().strftime('%y%m%d%H%M%S')}*{datetime.datetime.now():%Y%m%d}*{datetime.datetime.now():%H%M}*CH~"




### Loop 1000A - Submitter Name
#### The Submitter Name Loop 1000A supplies the full name of the organization creating and formatting the
#### transaction. Has segments NM1 and PER. 
def generate_nm1_segment(identifier_code, name, entity_id):
    ## https://www.stedi.com/edi/x12/transaction-set/837?segment=NM1&position=0200&area=heading
    ## https://www.stedi.com/edi/x12/segment/NM1
    ## https://www.hcmhrsb.org/wp-content/uploads/2017/10/SHARES-837P-Companion-Guide-HAMI.pdf 
    ## NM1 Segment has 8 fields
    ## NM101 - Entity Identifier Code (2 characters): value: 41
        ## 1O	Acute Care Hospital
        ## 41 = Submitting Provider
        ## 80	Hospital An institution where the ill or injured may receive medical treatment
    ## NM102 - Entity Type Qualifier (1 character): value: 2
        ## 1 = Person
        ## 2 = Non-Person Entity
    ## NM103 - Submitter Last or Organization Name
        ## Submitter Last or Organization Name, 1-35 characters
    ## NM104 - Name First (1-35 characters): value: [optional]
    ## NM105 - Name Middle (1-25 characters): value: [optional]
    ## NM106 - Name Prefix (1-10 characters): value: [optional]
    ## NM107 - Name Suffix (1-10 characters): value: [optional]
    ## NM108 - Identification Code Qualifier (2 characters): value: XX
        ## XX = Health Care Financing Administration National Provider Identifier
    ## NM109 - Identification Code (2-80 characters): value: 1952465171
        ## Health Care Financing Administration National Provider Identifier (NPI) assigned to the provider
    ## NM110 - Entity Relationship Code (2 characters): value: [optional]
    ## NM111 - Entity Identifier Code (2 characters): value: [optional]
    ## NM112 - Name Last or Organization Name (1-60 characters): value: [optional]
    return f"NM1*{identifier_code}*2*{name}*****XX*{entity_id}~"

#### generate NM1 segment for subscriber
def generate_nm1_segment_subscriber(identifier_code, firstname, lastname, middlename, subscriber_id):
    ## NM1*IL*1*ABCDEFGH*IJKLMNOP*B***MI*111111100~
    position1 = identifier_code
    position2 = "1"
    position3 = firstname
    position4 = lastname
    position5 = middlename
    position6 = "MI"
    position7 = subscriber_id
    return f"NM1*{position1}*{position2}*{position3}*{position4}*{position5}***{position6}*{position7}~"

    

def generate_per_segment(contact_name, phone_number):
    ## https://www.stedi.com/edi/x12/segment/PER
    ## PER Segment has 9 fields
    ## PER01 - Contact Function Code (2 characters): value: IC
        ## 1C = 1C	Health Maintenance Organization (HMO) Contact
    ## PER02 - Name (1-60 characters): value: Adam Velasquez
    ## PER03 - Communication Number Qualifier (2 characters): value: TE
        ## TE = Telephone
    ## PER04 - Communication Number (1-256 characters): value: 2492742731
    ## PER05 - Communication Number Qualifier (2 characters): value: [optional]
        ## Code identifying the type of communication number
    ## PER06 - Communication Number (1-256 characters): value: [optional]
        ## Complete communications number including country or area code when applicable
    ## PER07 - Communication Number Qualifier (2 characters): value: [optional]
        ## Code identifying the type of communication number
    ## PER08 - Communication Number (1-256 characters): value: [optional]
        ## Complete communications number including country or area code when applicable
    ## PER09 - Contact Inquiry Reference (1-20 characters): value: [optional]
        ## Free-form description of a reference number or identification assigned to the contact
    return f"PER*IC*{contact_name}*TE*{phone_number}~"
########

### HL Segment can be for Billing Provider (e.g., Organization) or Subscriber (e.g., Patient)
## so loop 2000A and loop 2000B
def generate_hl_segment(hierarchical_id, parent_id, level_code, child_code):
    parent_id_value = parent_id if parent_id else ""
    return f"HL*{hierarchical_id}*{parent_id_value}*{level_code}*{child_code}~"


##### CLM Segment for claim information
def generate_clm_segment(claim_id, amount, place_of_service):
    ## 2300 Loop Claim Information
        ## https://knowledge.therabill.com/hc/en-us/articles/360006563852-Loop-2300-Claim-Information
        ## Segment CLM - Claim; Example: CLM*18434718T0*150.00***11:B:1*Y*A*Y*Y~
    return f"CLM*{claim_id}*{amount}***{place_of_service}:B:1*Y*A*Y*I~"

### DTP can be for Date of Service, Admission, Discharge, etc.
### can be used to specify any or all of a date, a time, or a time period
def generate_dtp_segment(date_qualifier, date_format, date_value):
    ## To specify any or all of a date, a time, or a time period, use the DTP segment.
        ## A dtp contains 3 fields: 1) Date/Time Qualifier, 2) Date, 3) Time
        ## Field 1: https://www.stedi.com/edi/x12/element/374; 
        ## Field 2: https://www.stedi.com/edi/x12/element/1250;
        ## Field 3: https://www.stedi.com/edi/x12/element/1251; 
    return f"DTP*{date_qualifier}*{date_format}*{date_value}~"

def generate_hi_segment(code):
    ## https://www.stedi.com/edi/x12/transaction-set/837?segment=HI&position=2310&area=detail   
    ## HI*ABK:{code}~"
        ## Value 1: https://www.stedi.com/edi/x12/element/1270 
            ## ABK: International Classification of Diseases Clinical Modification (ICD-10-CM) Principal Diagnosis
        ## Value 2 : Code: will then be a valid ICD-10-CM code
    return f"HI*ABK:{code}~"

def generate_sv1_segment(procedure_code, amount, unit, quantity, modifier="", diagnosis_code_pointer=""):
    #### 2400 Loop Service Line (Procedure) Information
    ## https://www.stedi.com/edi/x12/transaction-set/837?segment=SV1&position=3700&area=detail
    ## sv1 = professional service
    ## value1: Product/Service ID Qualifier - https://www.stedi.com/edi/x12/element/235 - HC = Healthcare Common Procedure Coding System (HCPCS)
    ## value2: Product/Service ID - the CPT/HCPCS code
    ## value3: amount - https://www.stedi.com/edi/x12/element/782 - monetary amount
    ## value4: unit - https://www.stedi.com/edi/x12/element/355 - unit or basis for measurement
    ## value5: quantity - https://www.stedi.com/edi/x12/element/380 - quantity
    ## value6: modifier section - https://www.stedi.com/edi/x12/element/128 - modifier
    ## example: SV1*HC:00902:AA::::46705*1230*MJ*65***2~
        ## HC: Healthcare Common Procedure Coding System (HCPCS)
        ## 00902:AA: the CPT/HCPCS code
        ## AA: modifier
        ## ::::46705: descipriton which is optional, can be left blank
        ## 1230: amount (https://www.stedi.com/edi/x12/element/782) 
        ## MJ: unit (https://www.stedi.com/edi/x12/element/355) 
        ## 65: quantity (https://www.stedi.com/edi/x12/element/380) 
        ## ***2: diagnosis code pointer 
            ## in this example the ***2 means that this service is associated with the 2nd diagnosis code
    modifier_section = f"***{modifier}" if modifier else ""
    return f"SV1*HC:{procedure_code}*{amount}*{unit}*{quantity}{modifier_section}***{diagnosis_code_pointer}~"

def generate_se_segment(segment_count, transaction_control_number):
    return f"SE*{segment_count}*{transaction_control_number}~"

def generate_ge_segment(group_control_number):
    return f"GE*1*{group_control_number}~"

def generate_iea_segment(interchange_control_number):
    return f"IEA*1*{interchange_control_number}~"
