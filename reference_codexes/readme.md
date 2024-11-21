# Data Sources

- Start with: 
    - Location (house):
        - National Address Database 
        - [National Address Database](https://www.transportation.gov/gis/national-address-database) 
    - Based on the house, find a hospital that would make sense 
        - CMS - Medicare only 
        - [CMS Hospitals](https://data.cms.gov/provider-data/dataset/xubh-q36u) 
    - Based on the hospital, find a health insurance company that would make sense
        - ACA Plan Finder 
        - [CMS Finder API](https://developer.cms.gov/finder-api/)
    - Then based on the location (zip), use synthea to generate a patient profile that would make sense for that location 
        - Synthea 

## Details 

### Hospitals 
- Hospital General Information
    - https://data.cms.gov/provider-data/dataset/xubh-q36u 

### NPIs - Orgs 
- https://download.cms.gov/nppes/NPI_Files.html 
- then only kept the rows where the NPI was that of a organization 

### Health Insurance Companies 
- https://www.cms.gov/marketplace/resources/data/healthcaregov-plan-finder-data 
    - Data being used: Quarter 2 2023 HIOS and RBIS Data: 
        - https://downloads.cms.gov/files/2023Q2-HIOS.zip 
- https://www.cms.gov/marketplace/resources/data/public-use-files

### Addresses (subscriber)
- Read addresses: https://github.com/uva-bi-sdad/national_address_database/blob/main/README.md 