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

## Uso rápido

```bash
cd <stack>
docker compose up -d
docker compose config   # valida o compose antes de subir
docker compose down     # para e remove containers/rede
```

Cada stack é isolado: não há dependência entre pastas, e cada um usa seus próprios volumes/rede nomeados.

## Convenções

- Nome de container: `<serviço>01` (ex.: `postgres01`).
- Nome de volume: `<container>_<propósito>` (ex.: `postgres01_data`).
- Volumes nomeados do Docker em vez de bind mounts, para portabilidade entre máquinas.
- Cada stack documenta em seu próprio `README.md`: quick-start, acesso, persistência e reset completo.

## Segurança

As credenciais nos `docker-compose.yml` são de demonstração, propositalmente simples e visíveis, para uso local de laboratório. Não use estes stacks como estão em produção.
