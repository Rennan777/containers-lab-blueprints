# Kafka Local

Ambiente local de Apache Kafka (modo KRaft, sem Zookeeper) com Kafka UI, em Docker Compose.

## Requisitos

- Docker
- Docker Compose
- Portas `9092`, `29092` e `7071` livres na maquina

> Nota: as imagens atuais do Confluent Platform (`cp-kafka:latest`) removeram o suporte a Zookeeper e exigem modo KRaft. Este stack usa um broker unico atuando como broker+controller (`KAFKA_PROCESS_ROLES: broker,controller`), que e o modelo recomendado hoje para uso local/lab.

## Primeira execucao

Na pasta do projeto:

```bash
docker compose up -d
```

Esse comando cria automaticamente:

- container `kafka01`
- container `kafka-ui01`
- rede `kafka_default`
- volume `kafka01_data`

## Acesso

Kafka UI:

```text
http://localhost:7071
```

Bootstrap servers:

```text
- de dentro da rede Docker do stack: kafka:29092
- do host (fora do Docker):          localhost:9092
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
docker logs -f kafka01
docker logs -f kafka-ui01
```

Criar um topico:

```bash
docker exec kafka01 kafka-topics --bootstrap-server localhost:9092 \
  --create --topic meu-topico --partitions 1 --replication-factor 1
```

Listar topicos:

```bash
docker exec kafka01 kafka-topics --bootstrap-server localhost:9092 --list
```

Produzir mensagens (linha a linha, Ctrl+D para sair):

```bash
docker exec -it kafka01 kafka-console-producer --bootstrap-server localhost:9092 --topic meu-topico
```

Consumir mensagens desde o inicio:

```bash
docker exec -it kafka01 kafka-console-consumer --bootstrap-server localhost:9092 --topic meu-topico --from-beginning
```

## Persistencia

Os dados do broker ficam em volume nomeado do Docker, nao na pasta do projeto.

> `docker compose down` remove containers e rede, mas **nao** remove o volume nomeado — os dados continuam no disco ate um `docker volume rm` explicito (ver Reset Completo abaixo).

Volume montado no container:

- `kafka01_data` -> `/var/lib/kafka/data`

## Reset Completo

Para apagar tudo e voltar ao estado de primeira execucao:

```bash
docker compose down
docker rm -f kafka01 kafka-ui01 2>/dev/null || true
docker volume rm kafka01_data
```

Depois, para recriar do zero:

```bash
docker compose up -d
```
