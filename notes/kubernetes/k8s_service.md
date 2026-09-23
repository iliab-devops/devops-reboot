## Service

I Pod muoiono/vengono ricreati di continuo e **ogni volta cambiano IP**. 
Il Service è un punto di accesso stabile (nome/IP fisso) che indirizza il 
traffico verso i Pod giusti, indipendentemente da quali Pod specifici 
sono attivi in quel momento.

Il collegamento avviene tramite `selector`/label, non IP diretti. 
Il load balancing tra le repliche è incluso automaticamente.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mia-app-service
spec:
  selector:
    app: mia-app       # stesso label del Deployment
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

### Tipi di Service

| Tipo | Raggiungibile da | Caso d'uso | Note |
|---|---|---|---|
| **ClusterIP** (default) | solo dall'interno del cluster | comunicazione tra microservizi | se non specifichi `type:`, è questo di default |
| **NodePort** | `<IP-del-Node>:<porta>` (range 30000-32767) | test/sviluppo | raramente in produzione: espone le porte dei Node, meno sicuro |
| **LoadBalancer** | Internet, IP pubblico dedicato | esporre un servizio in produzione | richiede un cloud provider (AWS/Azure/GCP) che lo fornisca; ha un costo; in cluster on-premise serve un controller extra come MetalLB |
| **ExternalName** | fa da alias verso un servizio esterno al cluster (via DNS) | integrazione con risorse esterne (es. DB gestito) | non instrada verso Pod |