## kubectl — comandi essenziali

`kubectl` è il CLI per interagire con un cluster Kubernetes. Sintassi 
generale: `kubectl <verbo> <risorsa> <nome> [flag]`.

### Vedere lo stato delle risorse (`get`)

```bash
kubectl get pods                      # pod nel namespace default
kubectl get pods -n staging           # pod in un namespace specifico
kubectl get pods --all-namespaces     # pod in tutti i namespace
kubectl get pods -o wide              # info extra: IP, node, ecc.
kubectl get deployments
kubectl get services
kubectl get nodes
```

`-o wide` e `-o yaml`/`-o json` sono utili per vedere più dettagli senza 
fare `describe`.

### Investigare un problema (`describe`, `logs`) — i più usati per troubleshooting

```bash
kubectl describe pod nome-pod         # eventi, stato, motivo di eventuali errori
kubectl logs nome-pod                 # log del container nel pod
kubectl logs nome-pod -f              # segui i log in tempo reale (come tail -f)
kubectl logs nome-pod -c nome-container   # se il pod ha più container
kubectl logs nome-pod --previous      # log del container PRIMA del suo ultimo restart (utile se è crashato)
```

`describe` mostra anche la sezione **Events**, spesso la prima cosa da 
guardare per capire *perché* un pod non parte (es. immagine non trovata, 
risorse insufficienti, problemi di permessi).

### Entrare/eseguire comandi dentro un pod

```bash
kubectl exec -it nome-pod -- /bin/bash   # apri una shell interattiva nel pod
kubectl exec nome-pod -- ls /app         # esegui un comando singolo senza entrare
```

### Applicare/modificare configurazioni

```bash
kubectl apply -f file.yaml            # crea o aggiorna una risorsa da YAML
kubectl delete -f file.yaml           # elimina la risorsa definita nel YAML
kubectl delete pod nome-pod           # elimina un pod specifico (verrà ricreato se gestito da un Deployment!)
```

### Scalare manualmente

```bash
kubectl scale deployment mia-app --replicas=5
```

### Rollout (aggiornamenti e rollback, visti col Deployment)

```bash
kubectl rollout status deployment mia-app
kubectl rollout history deployment mia-app
kubectl rollout undo deployment mia-app
kubectl rollout restart deployment mia-app   # utile dopo aver aggiornato un ConfigMap
```

### Debug rapido: stato generale del cluster

```bash
kubectl get events --sort-by=.metadata.creationTimestamp   # eventi recenti, utile per capire cosa è successo di recente
kubectl top pods                      # uso CPU/memoria per pod (serve metrics-server installato)
kubectl top nodes                     # uso CPU/memoria per node
```

### Un flusso di troubleshooting tipico (utile da avere a mente per un colloquio)

1. `kubectl get pods` → noti un pod in stato `CrashLoopBackOff` o `Pending`
2. `kubectl describe pod nome-pod` → guardi la sezione Events per capire il motivo
3. `kubectl logs nome-pod` (o `--previous` se è già ricrashato) → guardi l'errore applicativo
4. Se serve indagare più a fondo: `kubectl exec -it nome-pod -- /bin/bash`