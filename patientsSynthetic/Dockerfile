# Use an official OpenJDK image as the base
FROM openjdk:11-jre-slim

# Set working directory
WORKDIR /synthea

# Download the Synthea JAR file
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a volume for output data
VOLUME ["/synthea/output"]

# Set the default command to run Synthea with arguments passed at runtime
ENTRYPOINT ["java", "-jar", "synthea-with-dependencies.jar"]

