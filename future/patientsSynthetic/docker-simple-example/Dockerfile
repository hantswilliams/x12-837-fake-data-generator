# Use an official OpenJDK image as the base
FROM openjdk:11-jre-slim

# Set working directory
WORKDIR /synthea

# Install required tools
RUN apt-get update && apt-get install -y wget unzip zip && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the Synthea JAR file
RUN wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

# Extract the JAR file
RUN mkdir extracted && cd extracted && unzip ../synthea-with-dependencies.jar && ls -R

# Debug: List files to confirm where synthea.properties is located
RUN cd extracted && find . -name "synthea.properties"

# Modify the properties file
RUN sed -i 's/exporter.csv.export = false/exporter.csv.export = true/' extracted/synthea.properties

# Turn off fhir export
RUN sed -i 's/exporter.fhir.export = true/exporter.fhir.export = false/' extracted/synthea.properties

# Repackage the JAR file
RUN cd extracted && zip -r ../synthea-with-dependencies.jar *

# Clean up extracted files
RUN rm -rf extracted

# Define entrypoint for running Synthea
ENTRYPOINT ["java", "-jar", "synthea-with-dependencies.jar"]

# Default command to generate 100 patients
CMD ["-p", "10"]
