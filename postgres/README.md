# PostgreSQL Local

Ambiente local de PostgreSQL com Docker Compose, usando volume nomeado do Docker para facilitar persistencia, identificacao e reaproveitamento em qualquer maquina.

## Requisitos

- Docker
- Docker Compose
- Porta `5432` livre na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `postgres01`
- rede `postgres_default`
- volume `postgres01_data`

## Acesso

Conexao local:

```text
host: localhost
porta: 5432
database: pgdb
usuario: pguser
senha: pgpass
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

Reiniciar so o container:

```bash
docker restart postgres01
```

Ver logs:

```bash
docker logs -f postgres01
```

Testar conexao dentro do container:

```bash
docker exec -it postgres01 psql -U pguser -d pgdb
```

Listar volumes do projeto:

```bash
docker volume ls | grep postgres01_
```

## Persistencia

Os dados do PostgreSQL ficam no volume nomeado do Docker, nao na pasta do projeto.

Volume montado no container:

- `postgres01_data` -> `/var/lib/postgresql/data`

Para inspecionar o caminho fisico do volume:

```bash
docker volume inspect postgres01_data
```

Se quiser mostrar so nome e caminho:

```bash
docker volume inspect postgres01_data --format '{{ .Name }} -> {{ .Mountpoint }}'
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f postgres01 2>/dev/null || true
docker volume rm postgres01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
