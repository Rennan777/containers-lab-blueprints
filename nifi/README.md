# NiFi Local

Ambiente local do Apache NiFi com Docker Compose, usando volumes nomeados do Docker para facilitar identificação, inspeção e persistência.

## Requisitos

- Docker
- Docker Compose
- Porta `8443` livre na máquina

## Primeira execução

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `nifi01`
- rede `nifi_default`
- volumes `nifi01_*`

Volumes criados:

- `nifi01_conf`
- `nifi01_state`
- `nifi01_logs`
- `nifi01_flowfile_repository`
- `nifi01_provenance_repository`
- `nifi01_content_repository`
- `nifi01_database_repository`

## Acesso

Interface web:

```text
http://localhost:8443/nifi
```

Credenciais padrão:

```text
usuario: admin
senha: nifiadmin123456
```

## Comandos úteis

Subir:

```bash
docker compose up -d
```

Parar e remover container/rede:

```bash
docker compose down
```

Reiniciar só o container:

```bash
docker restart nifi01
```

Ver logs:

```bash
docker logs -f nifi01
```

Listar volumes do projeto:

```bash
docker volume ls | grep nifi01_
```

## Persistência

Os dados do NiFi ficam nos volumes nomeados do Docker, não na pasta do projeto.

> `docker compose down` remove containers e rede, mas **não** remove os volumes nomeados — os dados continuam no disco até um `docker volume rm` explícito (ver Reset Completo abaixo).

Volumes montados no container:

- `nifi01_conf` -> `/opt/nifi/nifi-current/conf`
- `nifi01_state` -> `/opt/nifi/nifi-current/state`
- `nifi01_logs` -> `/opt/nifi/nifi-current/logs`
- `nifi01_flowfile_repository` -> `/opt/nifi/nifi-current/flowfile_repository`
- `nifi01_provenance_repository` -> `/opt/nifi/nifi-current/provenance_repository`
- `nifi01_content_repository` -> `/opt/nifi/nifi-current/content_repository`
- `nifi01_database_repository` -> `/opt/nifi/nifi-current/database_repository`

Para inspecionar o caminho físico de um volume:

```bash
docker volume inspect nifi01_conf
```

Para listar o caminho físico de todos os volumes do projeto:

```bash
docker volume inspect \
  nifi01_conf \
  nifi01_state \
  nifi01_logs \
  nifi01_flowfile_repository \
  nifi01_provenance_repository \
  nifi01_content_repository \
  nifi01_database_repository
```

Cada volume terá um campo parecido com este:

```text
Mountpoint: /var/lib/docker/volumes/nifi01_conf/_data
```

Se quiser mostrar só nome e caminho:

```bash
for v in \
  nifi01_conf \
  nifi01_state \
  nifi01_logs \
  nifi01_flowfile_repository \
  nifi01_provenance_repository \
  nifi01_content_repository \
  nifi01_database_repository
do
  docker volume inspect "$v" --format '{{ .Name }} -> {{ .Mountpoint }}'
done
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execução:

```bash
docker compose down
docker rm -f nifi01 2>/dev/null || true
docker volume rm \
  nifi01_conf \
  nifi01_state \
  nifi01_logs \
  nifi01_flowfile_repository \
  nifi01_provenance_repository \
  nifi01_content_repository \
  nifi01_database_repository
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
