# Docker Instructions

- Build the docker-compose file
```bash
docker-compose build
```

- Run the docker-compose file, 5 records of persons between 25 and 65 years old will be generated
```bash
docker-compose run synthea -p 5 -a 25-65
```

- Run the docker-compose file, 5 records of persons between 35-45 years old from the state of New York will be generated
```bash
docker-compose run synthea -p 5 -a 35-45 "New York"
```





