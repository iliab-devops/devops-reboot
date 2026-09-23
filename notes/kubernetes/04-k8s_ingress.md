## Ingress

Per raggiungere i Service da **fuori** (Internet), specialmente quando hai 
molti microservizi, `LoadBalancer` su ogni singolo Service non è pratico 
(un IP pubblico/costo per ciascuno). L'Ingress risolve questo: un unico 
punto di ingresso che smista il traffico a più Service interni.

- **Ingress**: regole di routing HTTP/HTTPS verso i Service interni 
  (per path/dominio, es. `/api` → `api-service`, `/web` → `web-service`), 
  gestisce anche TLS/certificati in un punto centrale.
- Serve un **Ingress Controller** installato nel cluster (es. NGINX 
  Ingress, o quello nativo GKE).
- L'Ingress Controller stesso viene tipicamente esposto tramite un 
  Service `type: LoadBalancer` — quindi non è un'alternativa a 
  LoadBalancer, ma un modo per usarne **uno solo** invece di uno per 
  ogni microservizio.

Flusso tipico in produzione:
Internet → LoadBalancer (espone l'Ingress Controller) → Ingress 
(routing per path/dominio) → Service (ClusterIP) → Pod