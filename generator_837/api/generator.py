import regex
from random import randint, sample
from faker import Faker

from .segments import (
    generate_isa_segment, generate_gs_segment, generate_st_segment,
    generate_bht_segment, generate_nm1_segment, generate_nm1_segment_subscriber, generate_per_segment,
    generate_hl_segment, generate_clm_segment, generate_dtp_segment,
    generate_hi_segment, generate_sv1_segment, generate_se_segment,
    generate_ge_segment, generate_iea_segment
)
from .data_loader import load_codes, load_orgs, load_payers
from .utils import get_random_code

def generate_837_transaction():

    # Load ICD and CPT codes, orgs, and payers
    icd_codes, cpt_codes = load_codes()
    orgs = load_orgs()
    payers = load_payers()

    ## select a random row from payers 
    payer = payers.sample(1)
    payer_name = payer['ProductName'].values[0]
    payer_name = regex.sub(r'[^\w\s]', '', payer_name).replace(" ", "")[:60]
    payer_hios_product_id = payer['HIOSProductID'].values[0]
    payer_faker_firstname = Faker().first_name()
    payer_faker_lastname = Faker().last_name()
    payer_telephone_10digits = "".join([str(randint(0, 9)) for _ in range(10)])

    # create random sender_id, receiver_id, control_number, transaction_control_number
    sender_id_generated = "".join([str(randint(0, 9)) for _ in range(15)])
    receiver_id_generated = payer_name + "".join([str(randint(0, 9)) for _ in range(12)]) + "001"
    receiver_id_generated = receiver_id_generated[:15]
    control_number_generated = "".join([str(randint(0, 9)) for _ in range(9)])
    transaction_control_number_generated = "".join([str(randint(0, 9)) for _ in range(randint(4, 9))])

    sender_id = sender_id_generated
    receiver_id = receiver_id_generated
    control_number = control_number_generated
    transaction_control_number = transaction_control_number_generated

    # Select a random row from orgs df
    random_org = orgs.sample(1)
    ## get the random orgs NPI, and business name, Authorized Official Last Name, Authorized Official First Name, and Authorized Official Telephone Number
    random_org_npi = random_org['NPI'].values[0]
    random_org_name = random_org['Provider Organization Name (Legal Business Name)'].values[0][:60]
    random_org_official_firstname = random_org['Authorized Official First Name'].values[0]
    random_org_official_lastname = random_org['Authorized Official Last Name'].values[0]
    random_org_official_telephone = random_org['Authorized Official Telephone Number'].values[0].astype(str)[:10]
    random_org_business_address = random_org['Provider First Line Business Mailing Address'].values[0]
    random_org_business_cityname = random_org['Provider Business Mailing Address City Name'].values[0]
    random_org_business_state = random_org['Provider Business Mailing Address State Name'].values[0]
    random_org_business_postal = random_org['Provider Business Mailing Address Postal Code'].values[0].astype(str)[:5]
    random_org_ein = "".join([str(randint(0, 9)) for _ in range(9)])
    random_org_ein = f"{random_org_ein[:2]}-{random_org_ein[2:]}"


    ### subscriber information
    ## create random combination of letters and characters, between 5-10 in length
    subscriber_reference_id = "".join([str(randint(0, 9)) for _ in range(9)])
    subscriber_faker_firstname = Faker().first_name()
    subscriber_faker_lastname = Faker().last_name()
    subscriber_faker_middle_initial = Faker().random_uppercase_letter()
    subscriber_member_identification_id = "".join([str(randint(0, 9)) for _ in range(12)])
    subscriber_faker_stress_address = Faker().street_address()
    subscriber_faker_city = Faker().city()
    subscriber_faker_state = Faker().state_abbr()
    subscriber_faker_zipcode = Faker().zipcode_in_state()


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
        generate_nm1_segment("41", random_org_name, random_org_npi),
        ## submitter
        generate_per_segment(f'{random_org_official_firstname} {random_org_official_lastname}', random_org_official_telephone),
        ## receiver !!!!! ideally this should match the receiver_id_selections organization along with the NPI
        generate_nm1_segment("40", payer_name, payer_hios_product_id),
        ## receiver contact
        generate_per_segment(f'{payer_faker_firstname} {payer_faker_lastname}', payer_telephone_10digits),
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
    segments.append(generate_nm1_segment("85", random_org_name, random_org_npi))
    segments.append(f'N3*{random_org_business_address}~')
    segments.append(f'N4*{random_org_business_cityname}*{random_org_business_state}*{random_org_business_postal}~')
    segments.append(f'REF*EI*{random_org_ein}~')
    segments.append(generate_per_segment(f'{random_org_official_firstname} {random_org_official_lastname}', random_org_official_telephone))


    # HL Segment for Subscriber (e.g., Patient)
    ## Loop 2000B - Subscriber (SBR)
    ## https://knowledge.therabill.com/hc/en-us/articles/360006851231-Loop-2000B-Subscriber
    hierarchical_id_subscriber = 2
    # Example: HL*2*1*22*0~
    segments.append(generate_hl_segment(hierarchical_id_subscriber, hierarchical_id_billing, 22, 0))
    segments.append(f'SBR*P*18*{subscriber_reference_id}******CI~')
    ## Loop 2010BA - Subscriber (SBR) Name
    segments.append(generate_nm1_segment_subscriber("IL", subscriber_faker_firstname, subscriber_faker_lastname, subscriber_faker_middle_initial, subscriber_member_identification_id))
    segments.append(f'N3*{subscriber_faker_stress_address}~')
    segments.append(f'N4*{subscriber_faker_city}*{subscriber_faker_state}*{subscriber_faker_zipcode}~')


    # Claim Information
    ## 2300 Loop Claim Information
    ## https://knowledge.therabill.com/hc/en-us/articles/360006563852-Loop-2300-Claim-Information
    ## Segment CLM - Claim; Example: CLM*18434718T0*150.00***11:B:1*Y*A*Y*Y~
    ## https://www.stedi.com/edi/x12/transaction-set/837?segment=CLM&position=1300&area=detail
    ## Segment DTP - Date; Example: DTP*431*D8*20170720~
    claim_id = "4742333269"
    charge_amount = randint(100, 1000)
    segments.append(generate_clm_segment(claim_id, charge_amount, "11"))  # Claim segment
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


    ## create a number that is a random number of diagnoses between 3-8
    number_of_diagnoses = randint(3, 8)

    print(f"number of diagnoses to incorporate: {number_of_diagnoses}")

    for i in range(number_of_diagnoses):
        segments.append(generate_hi_segment(get_random_code(icd_codes)))

    # segments.append(generate_hi_segment(get_random_code(icd_codes)))  # Diagnosis code 1
    # segments.append(generate_hi_segment(get_random_code(icd_codes)))  # Diagnosis code 2
    # segments.append(generate_hi_segment(get_random_code(icd_codes)))  # Diagnosis code 3



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
    
    ### create a random number of services between 1-5
    number_of_services = randint(1, 5)

    print(f"number of services to incorporate: {number_of_services}")

    service_count = 0

    ## based on charge_amount and the number of servies, create {X} number of services charges that add up to the total charge amount
    breakpoints = sorted(sample(range(1, charge_amount), number_of_services - 1))
    # Add 0 and total_charges to the breakpoints
    breakpoints = [0] + breakpoints + [charge_amount]
    # Calculate the differences between consecutive breakpoints
    parts = [breakpoints[i + 1] - breakpoints[i] for i in range(len(breakpoints) - 1)]
    # Verify that the sum of parts equals the total charges
    assert sum(parts) == charge_amount, "The sum of parts does not match total charges"
    # Output
    print(f"Total Charges: {charge_amount}")
    print(f"Number of Parts: {number_of_services}")
    print(f"Parts: {parts}")

    for i in range(number_of_services):
        service_count += 1
        part_cost = parts[i]
        segments.append(f"LX*{service_count}~")
        ## based on the number of diagnoses, randomly select between either one or multipl diagnoses separated by a colon
        if number_of_diagnoses > 1:
            # Assuming 'number_of_diagnoses' is the total number of diagnoses
            diagnosis_pointers = ":".join(
                str(code) for code in sample(range(1, number_of_diagnoses + 1), randint(1, number_of_diagnoses))
            )
            segments.append(generate_sv1_segment(get_random_code(cpt_codes), part_cost, "UN", "1", diagnosis_pointers))
        else:
            segments.append(generate_sv1_segment(get_random_code(cpt_codes), part_cost, "UN", "1", "1"))
        segments.append(generate_dtp_segment("472", "D8", "20180428"))
        segments.append("REF*6R*142671~")

    

    # ### service 1 
    # segments.append("LX*1~")  # Line number
    # segments.append(generate_sv1_segment(get_random_code(cpt_codes), "20", "UN", "1", "1:2"))  # Service line, the last number is the associated diagnosis code 1 and 2
    # segments.append(generate_dtp_segment("472", "D8", "20180428"))  # Date for the procedure
    # segments.append("REF*6R*142671~")  # Reference identification
    
    # #### service 2
    # segments.append("LX*2~")  # Line number
    # segments.append(generate_sv1_segment(get_random_code(cpt_codes), "40", "UN", "1", "2"))  # Service line, the last number is the associated diagnosis code
    # segments.append(generate_dtp_segment("472", "D8", "20180428"))  # Date for the procedure
    # segments.append("REF*6R*142671~")  # Reference identification

    
    
    
    # Ending segments
    segment_count = len(segments) - 1  # Exclude SE from count
    segments.append(generate_se_segment(segment_count, transaction_control_number))
    segments.append(generate_ge_segment(1))
    segments.append(generate_iea_segment(control_number))
    
    return "\n".join(segments)

# # Usage Example
# if __name__ == "__main__":
#     number_of_files = 10 # number of files to generate
#     for i in range(number_of_files):
#         example_output = generate_837_transaction()
#         with open(f"generator_837_output/837_example_{i}.txt", "w") as file:
#             file.write(example_output)
#         print(f"837 Example {i} has been generated successfully!")
#     print("All 837 Examples have been generated successfully!")



