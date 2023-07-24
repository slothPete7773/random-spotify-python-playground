# Process automation

## Setup

1. Airflow

Create required directories

```sh
# /workflow-process/.
$ mkdir -p dags logs plugins test
```

Spining up Airflow service.

```sh
# /workflow-process/.
$ docker compose up
```

## Plan

### TODO

- Fetch top tracks monthly to GCS
- Fetch top artists monthly to GCS