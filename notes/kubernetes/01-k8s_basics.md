# Kubernetes — Basi

## Cos'è e perché

Docker gestisce bene **un container su una macchina**. Ma con decine di 
microservizi distribuiti su tante macchine servono risposte a: chi decide 
dove girano? Cosa succede se una macchina muore? Come li scalo? Come li 
aggiorno senza downtime? Kubernetes (k8s) è il sistema di **orchestrazione** 
che risponde a queste domande a livello di cluster.

## Pod, Node, Cluster

- **Pod**: unità minima gestita da k8s. Di solito contiene **un container** 
  (a volte più container strettamente collegati, pattern *sidecar*: l'app 
  principale + un "aiutante" accanto).
- **Node**: macchina (fisica o virtuale) dove i pod girano davvero. Ha 
  CPU/RAM limitate. Ogni Node ha un agente, il **kubelet**, che comunica 
  costantemente col control plane (heartbeat) e fa effettivamente partire 
  i container su quel Node.
- **Cluster**: insieme di node gestiti insieme, con un **control plane** 
  centrale che decide dove piazzare ogni pod e i **worker node** dove 
  girano i pod.

Analogia: il cluster è un magazzino, i node sono gli scaffali, i pod sono 
le scatole. Se una scatola si rompe (pod crasha), il magazziniere (k8s) 
ne rimette subito un'altra.

## Modello dichiarativo e self-healing

Kubernetes funziona in modo **dichiarativo**:
1. Tu dichiari lo **stato desiderato** (es. "voglio sempre 3 repliche di 
   questa app").
2. Un **controller** confronta continuamente stato desiderato vs 
   **stato attuale**.
3. Se c'è una differenza (node morto, pod crashato), il controller agisce 
   per riallinearli — senza intervento manuale.

Questo loop si chiama **reconciliation loop**. Stesso identico principio 
usato poi da **ArgoCD** in ottica GitOps (confronta "cosa dice Git" con 
"cosa c'è nel cluster").

Nota: il Deployment non gestisce i Pod direttamente — crea e gestisce un 
**ReplicaSet**, che è il vero responsabile di mantenere il numero di 
repliche desiderato. Il Deployment si occupa in più di orchestrare gli 
aggiornamenti (rolling update/rollback), creando un nuovo ReplicaSet a 
ogni cambio di versione.

Se un intero **node** si guasta, il control plane se ne accorge perché 
il kubelet smette di mandare heartbeat: dopo un timeout, il Node viene 
marcato `NotReady` e i suoi Pod vengono considerati "morti" e ricreati 
su altri Node con capacità disponibile. Il rilevamento non è istantaneo 
— dipende dai timeout configurati.