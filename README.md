# Containers Lab Blueprints

Coleção de ambientes Docker Compose autocontidos para subir serviços de laboratório rapidamente. Cada pasta é um stack independente, pronto para `docker compose up -d`.

## Stacks disponíveis

| Stack | Serviço(s) | Porta principal | README |
|---|---|---|---|
| [`nifi/`](nifi/README.md) | Apache NiFi 1.26.0 | `8443` | [nifi/README.md](nifi/README.md) |
| [`postgres/`](postgres/README.md) | PostgreSQL 15 | `5432` | [postgres/README.md](postgres/README.md) |
| [`sqlserver/`](sqlserver/README.md) | SQL Server 2022 | `1433` | [sqlserver/README.md](sqlserver/README.md) |
| [`jasper/`](jasper/README.md) | JasperReports Server + MariaDB | `15080` | [jasper/README.md](jasper/README.md) |
| [`spark/`](spark/README.md) | Spark standalone (master + worker) | `8081` / `7077` | [spark/README.md](spark/README.md) |
| [`cassandra/`](cassandra/README.md) | Apache Cassandra 5.0 | `9042` | [cassandra/README.md](cassandra/README.md) |
| [`monitoring/`](monitoring/README.md) | Prometheus + Node Exporter + cAdvisor + Grafana | `9095` / `3000` | [monitoring/README.md](monitoring/README.md) |
| [`kafka/`](kafka/README.md) | Kafka (KRaft) + Kafka UI | `9092` / `7071` | [kafka/README.md](kafka/README.md) |
| [`minio/`](minio/README.md) | MinIO (S3 compatível) | `9000` / `9001` | [minio/README.md](minio/README.md) |
| [`hive-metastore/`](hive-metastore/README.md) | Hive Metastore + MariaDB | `9083` | [hive-metastore/README.md](hive-metastore/README.md) |
| [`trino/`](trino/README.md) | Trino (coordinator + worker) | `8080` | [trino/README.md](trino/README.md) |

## Uso rápido

```bash
cd <stack>
docker compose up -d
docker compose config   # valida o compose antes de subir
docker compose down     # para e remove containers/rede
```

Cada stack é isolado: não há dependência entre pastas, e cada um usa seus próprios volumes/rede nomeados. Exceção: dentro de um stack, um serviço pode depender de outro do mesmo stack quando isso é inerente ao serviço (ex.: `jasper/` com sua MariaDB, `hive-metastore/` com sua MariaDB) — nesses casos os dois ficam juntos no mesmo `docker-compose.yml` porque não fazem sentido separados. Stacks que normalmente se integram na prática (ex.: `trino/` consultando `kafka/`, `hive-metastore/` ou `minio/`) ficam desacoplados aqui; o README de cada um documenta como conectá-los via `docker network connect` quando precisar.

## Convenções

- Nome de container: `<serviço>01` (ex.: `postgres01`).
- Nome de volume: `<container>_<propósito>` (ex.: `postgres01_data`).
- Volumes nomeados do Docker em vez de bind mounts, para portabilidade entre máquinas.
- Cada stack documenta em seu próprio `README.md`: quick-start, acesso, persistência e reset completo.

## Segurança

As credenciais nos `docker-compose.yml` são de demonstração, propositalmente simples e visíveis, para uso local de laboratório. Não use estes stacks como estão em produção.
