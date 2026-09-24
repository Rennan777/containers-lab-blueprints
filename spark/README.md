# Spark Standalone Local

Ambiente local de Apache Spark 3.5.0 em modo standalone (master + 1 worker) com Docker Compose.

## Requisitos

- Docker
- Docker Compose
- Portas `8081` e `7077` livres na máquina

## Primeira execução

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `spark-master`
- container `spark-worker`
- rede `spark_default`

## Acesso

Interface web do master:

```text
http://localhost:8081
```

Endpoint do cluster (para submissão de jobs):

```text
spark://localhost:7077
```

## Comandos úteis

Subir:

```bash
docker compose up -d
```

Parar e remover containers/rede:

```bash
docker compose down
```

Ver logs:

```bash
docker logs -f spark-master
docker logs -f spark-worker
```

Submeter um job de exemplo:

```bash
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/work-dir/bitcoin_job.py
```

## Persistência

Este stack usa bind mounts (não volumes nomeados):

- `./jars/postgresql-42.7.3.jar` -> `/opt/spark/jars/postgresql.jar` (driver JDBC do Postgres, disponível para os jobs)
- `./spark_jobs/` -> `/opt/spark/work-dir` (scripts de job, ex.: `bitcoin_job.py`)

## Reset Completo

```bash
docker compose down
docker rm -f spark-master spark-worker 2>/dev/null || true
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
