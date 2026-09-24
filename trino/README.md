# Trino Local

Cluster local de Trino (coordinator + worker), em Docker Compose. Standalone por padrao — sem catalogs pre-conectados a outros stacks deste repo, so o catalog `tpch` (dados sinteticos, sem dependencia externa) para validar que o cluster esta de pe.

## Requisitos

- Docker
- Docker Compose
- Porta `8080` livre na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `trino-coordinator01`
- container `trino-worker01`
- rede `trino_default`

O worker so sobe depois que o coordinator reporta `healthy`. Depois de alguns segundos os dois nodes aparecem registrados no cluster.

## Acesso

Interface web:

```text
http://localhost:8080
```

CLI dentro do proprio container:

```bash
docker exec -it trino-coordinator01 trino
```

Testar o cluster (catalog `tpch`, sem dependencias externas):

```sql
SELECT count(*) FROM tpch.tiny.nation;
```

Ver os nodes do cluster:

```sql
SELECT * FROM system.runtime.nodes;
```

## Conectando a outros stacks

Por padrao este Trino nao enxerga os outros stacks do repo (`kafka/`, `hive-metastore/`, `minio/`, `cassandra/`) porque cada um roda isolado na sua propria rede Docker. Ha exemplos prontos em `catalog/*.properties.example` para Kafka e Hive/MinIO.

Para ativar um catalog:

1. Copie o exemplo sem o sufixo `.example` (ex.: `catalog/kafka.properties.example` -> `catalog/kafka.properties`).
2. Suba o stack alvo (ex.: `kafka/`, `hive-metastore/`, `minio/`).
3. Conecte este Trino a rede do stack alvo:

```bash
docker network connect kafka_default trino-coordinator01
docker network connect kafka_default trino-worker01
```

4. Reinicie o Trino:

```bash
docker compose restart
```

Repita para cada stack que quiser conectar (`hive-metastore_default`, `minio_default`, etc).

## Comandos uteis

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
docker logs -f trino-coordinator01
docker logs -f trino-worker01
```

## Configuracao

- `etc-coordinator/` -> config do coordinator, montado em `/etc/trino` no container `trino-coordinator01`.
- `etc-worker/` -> config do worker, montado em `/etc/trino` no container `trino-worker01`.
- `catalog/` -> compartilhado entre os dois nodes, montado em `/etc/trino/catalog`.

## Reset Completo

```bash
docker compose down
docker rm -f trino-coordinator01 trino-worker01 2>/dev/null || true
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
