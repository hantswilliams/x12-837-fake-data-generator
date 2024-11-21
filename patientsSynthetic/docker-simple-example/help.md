docker build -t synthea-custom .

docker run --rm -v $(pwd)/output:/synthea/output synthea-custom
