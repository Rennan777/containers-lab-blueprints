# Hive Metastore Local

Ambiente local de Hive Metastore (standalone) com seu proprio banco MariaDB, em Docker Compose. Segue o mesmo padrao do stack `jasper/` (app + banco dedicado): sao dois containers, mas interdependentes, entao ficam juntos no mesmo compose.

## Requisitos

- Docker
- Docker Compose
- Porta `9083` livre na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `hive-metastore-db01` (MariaDB)
- container `hive-metastore01`
- rede `hive-metastore_default`
- volume `hive-metastore-db01_data`

O `hive-metastore01` so sobe depois que o banco reporta `healthy`, e ao subir pela primeira vez roda o `schemaTool` automaticamente para criar o schema do metastore (Hive release 3.0.0).

## Acesso

Thrift endpoint (usado por Trino, Spark, etc.):

```text
thrift://localhost:9083
```

Banco (uso interno do metastore, nao pensado para acesso direto):

```text
host: hive-metastore-db01 (dentro do compose) / localhost (fora, se expuser a porta)
usuario: admin
senha: admin
database: metastore_db
```

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
docker logs -f hive-metastore01
docker logs -f hive-metastore-db01
```

## Persistencia

Volume montado no container do banco:

- `hive-metastore-db01_data` -> `/var/lib/mysql`

> `docker compose down` remove containers e rede, mas **nao** remove o volume nomeado — os dados continuam no disco ate um `docker volume rm` explicito (ver Reset Completo abaixo).

O container `hive-metastore01` em si nao tem estado proprio (tudo fica no banco).

## Integrando com o MinIO (tabelas externas em S3)

O arquivo `config_hive/metastore-site.xml` ja vem com as propriedades `fs.s3a.*` apontando para um host chamado `minio` (usuario `minio` / senha `minio123`, compativel com o stack `minio/` deste repo). Sem isso configurado na rede, o metastore sobe e funciona normalmente, so nao consegue gravar/ler tabelas externas em S3.

Para conectar ao stack `minio/` (que precisa estar rodando):

```bash
docker network connect minio_default hive-metastore01
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f hive-metastore01 hive-metastore-db01 2>/dev/null || true
docker volume rm hive-metastore-db01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
