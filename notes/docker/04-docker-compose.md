# Docker Compose

Docker Compose permette di definire e gestire un'applicazione composta da più container utilizzando un unico file YAML.

Invece di eseguire molti comandi `docker run`, è possibile descrivere tutti i servizi in un file `compose.yaml` ed avviarli con un solo comando.

## Perché usare Docker Compose

Senza Docker Compose, un'applicazione con più servizi richiede diversi comandi:

```bash
docker network create devops-net

docker run -d \
  --name database \
  --network devops-net \
  postgres

docker run -d \
  --name backend \
  --network devops-net \
  my-backend
```

Con Docker Compose basta un file di configurazione:

```yaml
services:
  database:
    image: postgres

  backend:
    image: my-backend
```

ed un solo comando:

```bash
docker compose up
```

Docker creerà automaticamente:

- i container;
- la rete;
- il DNS interno;
- i collegamenti tra i servizi.

---

# Il file compose.yaml

Un file Compose è composto principalmente dalla sezione `services`.

Ogni servizio rappresenta un container (o un gruppo di container) che fa parte dell'applicazione.

Esempio:

```yaml
services:
  app:
    image: python:3.12
```

---

# Proprietà principali

## image

Specifica quale immagine utilizzare.

```yaml
image: python:3.12
```

---

## build

Invece di utilizzare un'immagine già esistente, Docker può costruirla partendo da un Dockerfile.

```yaml
build: .
```

oppure

```yaml
build:
  context: .
```

---

## ports

Espone una porta del container verso l'host.

```yaml
ports:
  - "8080:80"
```

Formato:

```
porta_host:porta_container
```

---

## volumes

Permette di montare un volume o un bind mount.

Bind mount:

```yaml
volumes:
  - .:/app
```

Volume Docker:

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

---

## working_dir

Imposta la cartella di lavoro all'interno del container.

```yaml
working_dir: /app
```

Equivale ad eseguire:

```bash
cd /app
```

prima del comando principale.

---

## command

Specifica il comando eseguito all'avvio del container.

```yaml
command: python app.py
```

---

# Networking

Tutti i servizi definiti nello stesso file Compose vengono collegati automaticamente alla stessa rete.

Questo permette ai servizi di comunicare usando il nome del servizio.

Esempio:

```python
host = "database"
```

Docker utilizza il DNS interno per risolvere automaticamente il nome nell'indirizzo IP corretto.

---

# Comandi principali

Avviare l'applicazione:

```bash
docker compose up
```

Avviare in background:

```bash
docker compose up -d
```

Arrestare i servizi:

```bash
docker compose down
```

Visualizzare i container:

```bash
docker compose ps
```

Visualizzare i log:

```bash
docker compose logs
```