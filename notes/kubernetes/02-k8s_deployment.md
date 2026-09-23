## Deployment

Definisce **come** un'applicazione deve girare: quante repliche (copie 
identiche) del Pod vuoi, quale immagine Docker usare, come aggiornarla. 
È il responsabile diretto del **self-healing**: se un Pod crasha, il 
Deployment ne crea automaticamente un altro per sostituirlo.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mia-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mia-app
  template:
    metadata:
      labels:
        app: mia-app
    spec:
      containers:
        - name: mia-app
          image: mia-registry/mia-app:1.0
          ports:
            - containerPort: 8080
```

- `replicas` → stato desiderato (K8s lavora sempre per "far combaciare" 
  lo stato reale con quello desiderato)
- `selector` → dice al Deployment **quali** Pod deve gestire (in base al 
  label `app: mia-app`)
- `template` → lo "stampo" per creare ogni Pod (immagine, porte, label...)

### Rolling update (aggiornamento senza downtime)

Quando cambi l'immagine (es. `1.0` → `1.1`) e fai `kubectl apply`, il 
Deployment non spegne tutti i Pod insieme: ne crea di nuovi con la 
versione aggiornata **gradualmente**, mentre spegne quelli vecchi solo 
dopo che i nuovi sono pronti (`readiness check`). Comportamento 
regolabile con `strategy.rollingUpdate` (es. `maxUnavailable`, 
`maxSurge` — quanti Pod vecchi puoi fermare/quanti nuovi puoi aggiungere 
in parallelo durante l'update).

### Rollback (in caso di problemi con la nuova versione)

```bash
kubectl rollout status deployment mia-app     # segui l'avanzamento
kubectl rollout history deployment mia-app    # storico delle revisioni
kubectl rollout undo deployment mia-app       # torna alla versione precedente
```

Questo è un dettaglio molto concreto e "da troubleshooting reale": se 
un deploy introduce un bug, non devi rifare manualmente il deploy della 
versione vecchia — `kubectl rollout undo` lo fa automaticamente, 
sfruttando lo storico delle revisioni che K8s mantiene di default.

Nota: il Deployment non gestisce i Pod direttamente — crea e gestisce un 
**ReplicaSet**, che è il vero responsabile di mantenere il numero di 
repliche desiderato. Il Deployment si occupa in più di orchestrare gli 
aggiornamenti (rolling update/rollback), creando un nuovo ReplicaSet a 
ogni cambio di versione.