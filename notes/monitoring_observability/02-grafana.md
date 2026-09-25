# Grafana

## Cos'è

Strumento di **visualizzazione e dashboard**. Da solo **non raccoglie 
alcun dato** — si collega a fonti dati esterne (data source) e le mostra 
in grafici, tabelle, mappe di calore, gauge, ecc.

## Data source

Grafana può collegarsi a tante fonti diverse contemporaneamente:
- **Prometheus** (la combinazione più comune in ambienti Kubernetes/microservizi)
- Elasticsearch (log, dallo stack ELK)
- Database SQL (PostgreSQL, MySQL...)
- CloudWatch, Azure Monitor, e molti altri

**Punto chiave da ricordare**: Prometheus conserva e ti fa interrogare 
i numeri (con PromQL), Grafana li **rende leggibili** — è la coppia 
standard, non sono in competizione, sono complementari.

**Node Exporter** → **Prometheus** (raccoglie/conserva/query) → **Grafana** (visualizza)


## Dashboard

Una dashboard è un insieme di **pannelli** (grafici), ciascuno basato 
su una query verso il data source. Esempio: un pannello che mostra 
`rate(http_requests_total[5m])` come grafico a linee nel tempo.

Vantaggio pratico: dashboard **pronte e condivisibili** — esistono 
dashboard già fatte per strumenti comuni (es. dashboard ufficiale per 
Node Exporter, per Kubernetes) importabili con un ID, senza doverle 
costruire da zero.

## Alert

Grafana permette di definire **alert** direttamente sui pannelli (es. 
"avvisami se questa metrica supera una soglia per un certo periodo"), 
con notifiche verso email, Slack, ecc. — in alcuni setup questa parte 
viene delegata invece ad **Alertmanager** di Prometheus, per centralizzare 
tutta la logica di alerting in un unico posto.

## In sintesi (per un colloquio)

- **Node Exporter**: raccoglie i dati grezzi dal sistema operativo
- **Prometheus**: li scrape, li conserva come serie temporali, li rende 
  interrogabili (PromQL), gestisce alert
- **Grafana**: li visualizza in dashboard leggibili, per persone umane

Sapere descrivere questa catena in una frase ("Node Exporter raccoglie, 
Prometheus scrape e conserva, Grafana visualizza") è probabilmente la 
risposta più efficace se ti chiedono "spiegami come monitoreresti un 
cluster Kubernetes".