# Prometheus

## Cos'è

Sistema di monitoring che raccoglie **metriche numeriche** nel tempo (serie temporali: valore + timestamp). Risponde alla domanda "*quanto*" — CPU al 85%, 200 richieste/sec, 3 errori negli ultimi 5 minuti.

## Come funziona: modello PULL

A differenza di molti sistemi di logging (che ricevono dati "spinti" dalle app), Prometheus funziona al contrario: **è lui che va a raccogliere i dati**, a intervalli regolari (di default ogni 15s), da un endpoint HTTP che ogni applicazione/servizio espone — di solito `/metrics`.

```
Prometheus ---(scrape ogni 15s)---> App (espone /metrics)
```

Questa operazione si chiama **scraping**.

Esempio di cosa espone un endpoint `/metrics` (testo semplice, formato standard):
```
http_requests_total{method="GET", status="200"} 1523
cpu_usage_percent 42.3
```

## Perché il modello pull (vantaggi pratici)

- Prometheus sa sempre **chi dovrebbe rispondere** — se un target non risponde allo scrape, è già di per sé un segnale che qualcosa non va (target down)
- Centralizza la configurazione: decidi tu, da Prometheus, cosa e ogni quanto raccogliere, senza dover configurare ogni singola app per "spedire" dati altrove
- Eccezione: per processi di breve durata (es. job batch che finiscono in pochi secondi, troppo veloci per essere "scrapati"), si usa il **Pushgateway** — un componente intermedio a cui *quei* job possono effettivamente "pushare" un valore, che Prometheus poi scrapa da lì

## Node Exporter

Il problema: Prometheus sa leggere solo endpoint `/metrics` — ma un sistema operativo (CPU, RAM, disco, rete di un Node) non espone nativamente un endpoint del genere. Serve un "traduttore".

**Node Exporter** è esattamente questo: un piccolo programma che gira su ogni macchina (Node) e **espone le metriche di sistema** (CPU, memoria, spazio disco, I/O di rete, ecc.) in formato `/metrics`, pronto per essere scrapato da Prometheus.

```
Node Exporter (gira sul Node) → espone /metrics con dati OS
                ↑
        Prometheus fa scrape
```

In un cluster Kubernetes, Node Exporter gira tipicamente come **DaemonSet** (un Pod su *ogni* Node del cluster, automaticamente), proprio perché serve un'istanza per ogni macchina fisica/virtuale da monitorare.

Metriche tipiche esposte da Node Exporter:
```
node_cpu_seconds_total
node_memory_MemAvailable_bytes
node_filesystem_avail_bytes
node_network_receive_bytes_total
```

**Da ricordare per un colloquio**: esistono "exporter" analoghi per tante altre tecnologie (non solo il sistema operativo) — es. **postgres_exporter** per un database Postgres, **redis_exporter** per Redis. Il pattern è sempre lo stesso: un piccolo processo che traduce le metriche interne di uno strumento in formato compatibile Prometheus.

## PromQL — il linguaggio di query

```promql
rate(http_requests_total[5m])
```
Tasso di richieste negli ultimi 5 minuti — utile per vedere un **trend**, non solo un numero istantaneo (che da solo dice poco).

```promql
node_filesystem_avail_bytes{mountpoint="/"} < 10000000000
```
Esempio di condizione — spazio disco disponibile sotto una soglia, la base logica per un **alert**.

## Alerting

Prometheus ha un componente separato, **Alertmanager**, che riceve le regole di alert definite (es. "CPU > 90% per più di 5 minuti") e si occupa di instradare le notifiche (email, Slack, PagerDuty...), con funzioni utili come raggruppare alert simili o evitare di spammare notifiche ripetute per lo stesso problema.

## In sintesi (catena completa di monitoring)

```
Node Exporter (raccoglie dati grezzi dal sistema operativo)
        ↓
Prometheus (scrape, conserva come serie temporali, interrogabile via PromQL, gestisce alert)
        ↓
Grafana (visualizza in dashboard leggibili)
```

Sapere descrivere questa catena in una frase ("Node Exporter raccoglie, Prometheus scrape e conserva, Grafana visualizza") è probabilmente la risposta più efficace se in un colloquio chiedono "spiegami come monitoreresti un cluster Kubernetes".
