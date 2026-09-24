# SQL Server Local

Ambiente local de SQL Server com Docker Compose, usando volume nomeado do Docker para facilitar persistencia, identificacao e reaproveitamento em qualquer maquina.

## Requisitos

- Docker
- Docker Compose
- Porta `1433` livre na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `sqlserver01`
- rede `sqlserver_default`
- volume `sqlserver01_data`

## Acesso

Conexao local:

```text
host: localhost
porta: 1433
usuario: sa
senha: YourStrong!Passw0rd
edition: Developer
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
docker restart sqlserver01
```

Ver logs:

```bash
docker logs -f sqlserver01
```

Listar volumes do projeto:

```bash
docker volume ls | grep sqlserver01_
```

## Persistencia

Os dados do SQL Server ficam no volume nomeado do Docker, nao na pasta do projeto.

Volume montado no container:

- `sqlserver01_data` -> `/var/opt/mssql`

Para inspecionar o caminho fisico do volume:

```bash
docker volume inspect sqlserver01_data
```

Se quiser mostrar so nome e caminho:

```bash
docker volume inspect sqlserver01_data --format '{{ .Name }} -> {{ .Mountpoint }}'
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f sqlserver01 2>/dev/null || true
docker volume rm sqlserver01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
