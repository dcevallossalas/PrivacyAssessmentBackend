# A GPT-based Assessment of Privacy Legal Frameworks under ISO/IEC 27701:2025: A Latin American Case Study

This repository provides all the files and elements required for experiments reproducibility of the backend component of the research project: "A GPT-based Assessment of Privacy Legal Frameworks under ISO/IEC 27701:2025: A Latin American Case Study".

This research is part of the project "PRIVIA: Identificación Automatizada de Brechas de Privacidad en Ecuador usando Inteligencia Artificial Generativa y LLMs" conducted by Escuela Politécnica Nacional.

## Research information

- **Main project:** "PRIVIA: Identificación Automatizada de Brechas de Privacidad en Ecuador usando Inteligencia Artificial Generativa y LLMs" conducted by Escuela Politécnica Nacional.
- **Main project reference:** PIGR-24-06.
- **Date:** 2026-02-01.

## How to use this repository?

First, clone the repositoty in a local folder, Then, run the script dataBase.sql in your MySQL database engine. The database and analysis results will be loaded within a new schema.

Next, build a docker image using the Docker file and an image name (e.g., assessment).

```{r}
sudo docker build -t assessment .
```

Configure the configuration file config.json according to the following criteria:

- host: IP address or domain name to reach the database. 
- user: User with enough privileges
- password: Password of the database.
- database1: Name of the schema.

Run a new container of the built image mapping a local port to port 80 (e.g., port 8080 of local host to port 80 of docker) and the folder where the .py files are located with the home of docker alpine (e.g., folder /home/privacy/PrivacyAssessmentBackend of local host to folder /home/alpine of docker):

```{r}
sudo docker run -p 8090:80 -v /home/privacy/PrivacyAssessmentBackend:/home/alpine assessment
```

Or if you prefer, use the docker compose file localted in the docker-compose folder.


```{r}
cd /home/privacy/PrivacyAssessmentBackend/docker-compose
sudo docker compose up
```
