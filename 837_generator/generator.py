import os

from segments import (
    generate_isa_segment, generate_gs_segment, generate_st_segment,
    generate_bht_segment, generate_nm1_segment, generate_nm1_segment_subscriber, generate_per_segment,
    generate_hl_segment, generate_clm_segment, generate_dtp_segment,
    generate_hi_segment, generate_sv1_segment, generate_se_segment,
    generate_ge_segment, generate_iea_segment
)
from data_loader import load_codes
from utils import get_random_code

def generate_837_transaction():
    # Load ICD and CPT codes
    icd_codes, cpt_codes = load_codes()
    sender_id = "FAKE837SEND"
    receiver_id = "FAKE837RECV"
    control_number = "748158818"
    transaction_control_number = "521718582"

    # Start creating segments list
    segments = [
        ## key info / isa : loop 0000
        generate_isa_segment(sender_id, receiver_id, control_number),
        ## functional group header : loop 0000
        generate_gs_segment(sender_id, receiver_id, 1),
        ## general stuff 
        generate_st_segment(transaction_control_number),
        generate_bht_segment(),
        ## 
        generate_nm1_segment("41", "Submitter Organization Hospital A", "4675433976"),
        ## submitter
        generate_per_segment("Adam Velasquez Submitter Person", "2492742731"),
        ## receiver
        generate_nm1_segment("40", "Receiver Organization United Health", "0238660013"),
        ## receiver contact
        generate_per_segment("Jorge Mccarthy Receiver Person ", "2287014467"),
    ]
    

    # HL Segment for Billing Provider (e.g., Organization)
    ## https://knowledge.therabill.com/hc/en-us/articles/360006856311-Loop-2000A-Billing-Provider
    ## 2000A: Billing Provider: Contains 2010AA and 2010AB
    ## https://knowledge.therabill.com/hc/en-us/articles/360006856311-Loop-2000A-Billing-Provider
    ## Segment NM1 - Name: Example: NM1*85*2*WEBPTTHERABILL CLINIC*****XX*1952465171~
    ## Segment N3 - Street Address N3*123 STREET~
    ## Segment N4 - City, State, and ZIP: Example: N4*PHOENIX*AZ*850044461~
    ## Segment REF - Reference - Example: REF*EI*365421684~
    
    # Loop 2000A - Billing/Pay-To Provider
    hierarchical_id_billing = 1
    segments.append(generate_hl_segment(hierarchical_id_billing, "", 20, 1))
    # Loop 2010AA - Billing Provider (BP) Name
    segments.append(generate_nm1_segment("85", "Garcia Ltd", "5709867528"))
    segments.append("N3*5921 Lisa Inlet~")
    segments.append("N4*East Jeffery*TN*34498~")
    segments.append("REF*EI*628740805~")
    segments.append(generate_per_segment("Juan Ramirez", "2287014467"))


    # HL Segment for Subscriber (e.g., Patient)
    ## Loop 2000B - Subscriber (SBR)
    ## https://knowledge.therabill.com/hc/en-us/articles/360006851231-Loop-2000B-Subscriber
    hierarchical_id_subscriber = 2
    # Example: HL*2*1*22*0~
    segments.append(generate_hl_segment(hierarchical_id_subscriber, hierarchical_id_billing, 22, 0))
    segments.append('SBR*P*18*ABCDE01234******CI~')
    ## Loop 2010BA - Subscriber (SBR) Name
    segments.append(generate_nm1_segment_subscriber("IL", "Kristin", "Phillips", "7932682729"))
    segments.append("N3*83816 Maria Estate Suite 225~")
    segments.append("N4*East Nicholas*WV*09804~")


    # Claim Information
    ## 2300 Loop Claim Information
    ## https://knowledge.therabill.com/hc/en-us/articles/360006563852-Loop-2300-Claim-Information
    ## Segment CLM - Claim; Example: CLM*18434718T0*150.00***11:B:1*Y*A*Y*Y~
    ## https://www.stedi.com/edi/x12/transaction-set/837?segment=CLM&position=1300&area=detail
    ## Segment DTP - Date; Example: DTP*431*D8*20170720~
    claim_id = "4742333269"
    segments.append(generate_clm_segment(claim_id, "711", "11"))  # Claim segment
        # Field 1 - Claim Submitter's Identifier
        # Field 2 - Monetary Amount
        # Field 3 - Claim Filing Indicator Code: https://www.stedi.com/edi/x12/element/1032
    ## To specify any or all of a date, a time, or a time period, use the DTP segment.
    ## A dtp contains 3 fields: 1) Date/Time Qualifier, 2) Date, 3) Time
    ## Field 1: https://www.stedi.com/edi/x12/element/374; 
    ## Field 2: https://www.stedi.com/edi/x12/element/1250;
    ## Field 3: https://www.stedi.com/edi/x12/element/1251; 
    segments.append(generate_dtp_segment("434", "RD8", "20240422-20240430"))  # Date of service
    segments.append(generate_dtp_segment("435", "D8", "20240809"))  # Date of admission
    segments.append(generate_dtp_segment("096", "TM", "2337"))  # Time of admission
    ## appear to have up to 12 diagnosis codes https://soapware.screenstepslive.com/s/documentation/m/5138/l/47803-segment-hi
    ## https://www.stedi.com/edi/x12/transaction-set/837?segment=HI&position=2310&area=detail   
    ## HI*ABK:{code}~"
        ## Value 1: https://www.stedi.com/edi/x12/element/1270 
            ## ABK: International Classification of Diseases Clinical Modification (ICD-10-CM) Principal Diagnosis
        ## Value 2 : Code: will then be a valid ICD-10-CM code
    segments.append(generate_hi_segment(get_random_code(icd_codes)))  # Diagnosis code 1
    segments.append(generate_hi_segment(get_random_code(icd_codes)))  # Diagnosis code 2
    segments.append(generate_hi_segment(get_random_code(icd_codes)))  # Diagnosis code 3



    # Service Line (Procedure) Information
    ## https://knowledge.therabill.com/hc/en-us/articles/360006563912-Loop-2400-Service-Line-Information
    ## Segment LX - Line; Example: LX*1~
        ## https://www.stedi.com/edi/x12/transaction-set/837?segment=LX&position=3650&area=detail
        ## the value of the LX segment is the line number of the service line
        ## and can be between a number between 1 to 9
    ## https://www.stedi.com/edi/x12/element/554
    ## Segment SV1 (SV5 for DME) - Service; Example: SV1*HC:97010:GP::::LINE NOTE*150.00*UN*1***1:2~
        ### Professional Service Line (SV1) 
        ### Institutional Service Line (SV2). 
        ## Example: "HC : 99213 * 40 * UN * 1 *** 1 ~"
        ## Example: https://datainsight.health/edi/segments/codes-hi/ 
    ## Segment DTP - Date; Example: DTP*472*D8*20180629~
    ### service 1 
    segments.append("LX*1~")  # Line number
    segments.append(generate_sv1_segment(get_random_code(cpt_codes), "20", "UN", "1", "1"))  # Service line, the last number is the associated diagnosis code
    segments.append(generate_dtp_segment("472", "D8", "20180428"))  # Date for the procedure
    segments.append("REF*6R*142671~")  # Reference identification
    #### service 2
    segments.append("LX*2~")  # Line number
    segments.append(generate_sv1_segment(get_random_code(cpt_codes), "40", "UN", "1", "2"))  # Service line, the last number is the associated diagnosis code
    segments.append(generate_dtp_segment("472", "D8", "20180428"))  # Date for the procedure
    segments.append("REF*6R*142671~")  # Reference identification

    # Ending segments
    segment_count = len(segments) - 1  # Exclude SE from count
    segments.append(generate_se_segment(segment_count, transaction_control_number))
    segments.append(generate_ge_segment(1))
    segments.append(generate_iea_segment(control_number))
    
    return "\n".join(segments)

# Usage Example
if __name__ == "__main__":
    example_output = generate_837_transaction()    
    with open("generated_837_institutional_files/837_example_3.txt", "w") as file:
        file.write(example_output)

