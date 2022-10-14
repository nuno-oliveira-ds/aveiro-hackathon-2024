# Aveiro Tech City Hackathon

This repository hosts the code of **Continental_AA&AI_2** team for **Challenge 5) City Data**.

# Data Source

All files provided by the organization were compressed to `.parquet` and uploaded into a S3 Buckett (`s3://datalake-eu-central-1/ugiO-atchackathon`) in order to address the volume of data.

# Suggested Setup

## Development 

Using virtualenv, in the repository root:

```bash
python3 -m venv atcenv
```

Note that default environment name, `/atcenv`, was already added to `.gitignore`. If using a different one, please add it yourself.

Activate/Deactivate virtualenv:

```bash
source atcenv/bin/activate
```

```bash
deactivate
```

Install default dependencies:

```bash
pip install -r requirements.txt
```

Add new dependencies, within an active environment:

```bash
pip install <dependency>
```

```bash
pip freeze > requirements.txt
```

### Run dashboard

```bash
streamlit run src/1_Mobility_Monitoring.py --server.port 8089 --browser.serverAddress 0.0.0.0
```

## Deployment (Docker)

### Build docker container

```bash
docker build -t mobility .
```

### Run docker

```bash
docker run mobility
```

