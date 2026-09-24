# MinIO Local

Ambiente local de MinIO (armazenamento de objetos compativel com S3) em Docker Compose, usando volume nomeado do Docker para facilitar persistencia, identificacao e reaproveitamento em qualquer maquina.

## Requisitos

- Docker
- Docker Compose
- Portas `9000` e `9001` livres na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `minio01`
- rede `minio_default`
- volume `minio01_data`

## Acesso

Console web:

```text
http://localhost:9001
```

Endpoint S3 (API):

```text
http://localhost:9000
```

Credenciais:

```text
usuario: minio
senha: minio123
```

## Comandos uteis

Subir:

```bash
docker compose up -d
```

Parar e remover container/rede:

```bash
docker compose down
```

Ver logs:

```bash
docker logs -f minio01
```

Listar volumes do projeto:

```bash
docker volume ls | grep minio01_
```

## Persistencia

Os dados ficam no volume nomeado do Docker, nao na pasta do projeto.

Volume montado no container:

- `minio01_data` -> `/data`

## Integrando com outros stacks

Para outro stack (ex.: `hive-metastore/`, `trino/`) acessar este MinIO pelo nome de servico Docker (`minio`) em vez de `localhost`, conecte o container dele nesta rede:

```bash
docker network connect minio_default <container-do-outro-stack>
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f minio01 2>/dev/null || true
docker volume rm minio01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
