from parser_837.api.parser import parser_main

services, diagnoses, header = parser_main("generator_837_output/837_example_7.txt")

print(services.getvalue())
print(diagnoses.getvalue())
print(header.getvalue())