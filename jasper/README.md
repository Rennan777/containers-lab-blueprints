# JasperReports Local

Ambiente local de JasperReports Server com MariaDB em Docker Compose, usando volumes nomeados do Docker para facilitar persistencia, identificacao e reaproveitamento em qualquer maquina.

## Requisitos

- Docker
- Docker Compose
- Porta `15080` livre na maquina

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `mariadb01`
- container `jasperreports01`
- rede `jasper_default`
- volumes `mariadb01_data` e `jasperreports01_data`

Ambos os containers têm healthcheck. O `jasperreports01` só sobe depois que o `mariadb01` reporta `healthy`, e o próprio `jasperreports01` pode levar alguns minutos até ficar `healthy` (aplicação Java inicializando). Acompanhe com:

```bash
docker compose ps
```

## Acesso

Interface web:

```text
http://localhost:15080/jasperserver
```

Credenciais padrao da aplicacao:

```text
usuario: jasperadmin
senha: bitnami
```

Banco configurado no compose:

```text
host: localhost
porta: 3306
database: jasperreports
usuario: jasperreports
senha: jasperpass
root: rootpass
```

Observacao: a porta `3306` do MariaDB nao esta publicada no host. O acesso acima vale para conexao interna entre os containers; se quiser acessar pelo host, adicione o mapeamento de porta no compose.

## Comandos uteis

Subir:

```bash
docker compose up -d
```

Parar e remover containers/rede:

```bash
docker compose down
```

Reiniciar containers:

```bash
docker restart mariadb01 jasperreports01
```

Ver logs da aplicacao:

```bash
docker logs -f jasperreports01
```

Ver logs do banco:

```bash
docker logs -f mariadb01
```

Listar volumes do projeto:

```bash
docker volume ls | grep -E 'mariadb01_|jasperreports01_'
```

## Persistencia

Os dados ficam em volumes nomeados do Docker, nao na pasta do projeto.

> `docker compose down` remove containers e rede, mas **nao** remove os volumes nomeados — os dados continuam no disco ate um `docker volume rm` explicito (ver Reset Completo abaixo).

Volumes montados nos containers:

- `mariadb01_data` -> `/var/lib/mysql`
- `jasperreports01_data` -> `/bitnami/jasperreports`

Para inspecionar o caminho fisico dos volumes:

```bash
docker volume inspect mariadb01_data jasperreports01_data
```

Se quiser mostrar so nome e caminho:

```bash
for v in mariadb01_data jasperreports01_data
do
  docker volume inspect "$v" --format '{{ .Name }} -> {{ .Mountpoint }}'
done
```

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f mariadb01 jasperreports01 2>/dev/null || true
docker volume rm mariadb01_data jasperreports01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
