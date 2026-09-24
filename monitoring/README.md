# Monitoring Local

Stack de observabilidade local com Prometheus, Node Exporter, cAdvisor e Grafana, em Docker Compose.

## Requisitos

- Docker
- Docker Compose
- Portas `9095`, `9100`, `8082` e `3000` livres na maquina

> Nota: a porta padrao do Prometheus (`9090`) foi remapeada para `9095` no host para evitar conflito com outros containers comuns (ex.: apps que ja usam 9090/9091 na maquina). O container continua ouvindo na `9090` internamente.

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `prometheus01`
- container `node-exporter01`
- container `cadvisor01`
- container `grafana01`
- rede `monitoring_default`
- volume `grafana01_data`

## Acesso

Prometheus:

```text
http://localhost:9095
```

cAdvisor:

```text
http://localhost:8082
```

Node Exporter (metricas cruas):

```text
http://localhost:9100/metrics
```

Grafana:

```text
http://localhost:3000
```

Credenciais padrao do Grafana:

```text
usuario: admin
senha: admin
```

## Configurando o Grafana

1. Acesse `http://localhost:3000` e faca login.
2. Va em **Connections** > **Data sources** > **Add data source** > **Prometheus**.
3. URL: `http://prometheus:9090` (nome do servico Docker, nao `localhost`, pois o Grafana acessa pela rede interna do Compose).
4. **Save & test**.

Consultas PromQL uteis para dashboards de containers:

```promql
# Uso de CPU por container
rate(container_cpu_usage_seconds_total{image!=""}[1m])

# Uso de memoria por container
container_memory_usage_bytes{image!=""}

# Quantidade de containers
count(container_memory_usage_bytes{image!=""})

# Uso de CPU do host
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Uso de memoria do host
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
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
docker logs -f prometheus01
docker logs -f grafana01
```

Ver os targets do Prometheus:

```bash
curl -s http://localhost:9095/api/v1/targets | jq
```

## Persistencia

Apenas o Grafana persiste dados (dashboards, data sources) em volume nomeado:

- `grafana01_data` -> `/var/lib/grafana`

Prometheus, Node Exporter e cAdvisor sao stateless neste stack (sem volume de dados de series temporais).

## Reset Completo

```bash
docker compose down
docker rm -f prometheus01 node-exporter01 cadvisor01 grafana01 2>/dev/null || true
docker volume rm grafana01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
