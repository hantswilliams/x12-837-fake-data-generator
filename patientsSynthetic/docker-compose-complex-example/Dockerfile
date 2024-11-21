# Use an official OpenJDK image as the base
FROM openjdk:11-jre-slim

# Set working directory
WORKDIR /synthea

# Download the Synthea JAR file
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Echo the contents of the current working directoy
RUN echo "Contents of the current working directory:" && ls -l

    # Copy synthea.properties file to the container and overwrite the default one in synthea/src/main/resources
COPY synthea.properties /synthea/src/main/resources/

# Debug: Print the contents of synthea.properties to verify the correct file
RUN echo "Printing synthea.properties for verification:" && cat /synthea/src/main/resources/synthea.properties

# Create a volume for output data
VOLUME ["/synthea/output"]

# Set the default command to run Synthea with arguments passed at runtime
ENTRYPOINT ["java", "-jar", "synthea-with-dependencies.jar"]

