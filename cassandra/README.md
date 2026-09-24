# Cassandra Local

Ambiente local de Apache Cassandra em Docker Compose, usando volume nomeado do Docker para facilitar persistencia, identificacao e reaproveitamento em qualquer maquina.

## Requisitos

- Docker
- Docker Compose
- Porta `9042` livre na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `cassandra01`
- rede `cassandra_default`
- volume `cassandra01_data`

O container pode levar cerca de 1 minuto para ficar `healthy` (inicializacao do node).

## Acesso

Via `cqlsh` dentro do proprio container:

```bash
docker exec -it cassandra01 cqlsh
```

Conexao externa (driver/cliente CQL):

```text
host: localhost
porta: 9042
cluster: MyCluster
```

Sem autenticacao habilitada (uso local de laboratorio).

## Comandos uteis

Subir:

```bash
docker compose up -d
```

Parar e remover container/rede:

```bash
docker compose down
```

Reiniciar so o container:

```bash
docker restart cassandra01
```

Ver logs:

```bash
docker logs -f cassandra01
```

Verificar status do node:

```bash
docker exec -it cassandra01 nodetool status
```

Listar volumes do projeto:

```bash
docker volume ls | grep cassandra01_
```

## Persistencia

Os dados ficam no volume nomeado do Docker, nao na pasta do projeto.

Volume montado no container:

- `cassandra01_data` -> `/var/lib/cassandra`

Para inspecionar o caminho fisico do volume:

```bash
docker volume inspect cassandra01_data --format '{{ .Name }} -> {{ .Mountpoint }}'
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f cassandra01 2>/dev/null || true
docker volume rm cassandra01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
