# Kubernetes — Basi 

## Cos'è e perché

Docker gestisce bene **un container su una macchina**. Ma con decine di microservizi distribuiti su tante macchine servono risposte a: chi decide dove girano? Cosa succede se una macchina muore? Come li scalo? Come li aggiorno senza downtime? Kubernetes (k8s) è il sistema di **orchestrazione** che risponde a queste domande a livello di cluster.

## Pod, Node, Cluster

- **Pod**: unità minima gestita da k8s. Di solito contiene **un container** (a volte più container strettamente collegati, pattern *sidecar*: l'app principale + un "aiutante" accanto).
- **Node**: macchina (fisica o virtuale) dove i pod girano davvero. Ha CPU/RAM limitate.
- **Cluster**: insieme di node gestiti insieme, con un control plane centrale che decide dove piazzare ogni pod.

Analogia: il cluster è un magazzino, i node sono gli scaffali, i pod sono le scatole. Se una scatola si rompe (pod crasha), il magazziniere (k8s) ne rimette subito un'altra.

## Modello dichiarativo e self-healing

Kubernetes funziona in modo **dichiarativo**:
1. Tu dichiari lo **stato desiderato** (es. "voglio sempre 3 repliche di questa app").
2. Un **controller** confronta continuamente stato desiderato vs **stato attuale**.
3. Se c'è una differenza (node morto, pod crashato), il controller agisce per riallinearli — senza intervento manuale.

Questo loop si chiama **reconciliation loop**. Stesso identico principio usato poi da **ArgoCD** in ottica GitOps (confronta "cosa dice Git" con "cosa c'è nel cluster").

Se un intero **node** si guasta, k8s considera i suoi pod "morti" e li **ricrea su altri node disponibili** con capacità libera.

## Deployment

Oggetto che dichiara "voglio N copie di questa app sempre attive" — è il responsabile diretto del self-healing.

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

- `replicas` → stato desiderato.
- `template` → stampo per creare ogni pod (immagine, porte...).
- Gestisce anche **rolling update** (aggiorna un pod alla volta, senza downtime) e **rollback** in caso di problemi con la nuova versione.

## Service

Problema che risolve: i pod muoiono/vengono ricreati di continuo e **ogni volta cambiano IP**. Il Service dà un **indirizzo stabile** (IP fisso + DNS interno) che punta sempre ai pod corretti.

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

Collegamento tramite `selector`/label, non IP diretti. Load balancing tra le repliche incluso. `ClusterIP` (default) → raggiungibile solo da **dentro** il cluster.

## Ingress

Per raggiungere i Service da **fuori** (internet):

- **Ingress**: regole di routing HTTP/HTTPS verso i Service interni (per path/dominio, es. `/api` → `api-service`, `/web` → `web-service`), gestisce anche TLS/certificati in un punto centrale.
- Serve un **Ingress Controller** installato nel cluster (es. NGINX Ingress, o quello nativo GKE).
- Alternativa più semplice ma meno flessibile: `type: LoadBalancer` sul Service → su GKE crea automaticamente un load balancer esterno GCP.

## ConfigMap e Secret

Stesso principio di `variable` in Terraform: non hardcodare config nell'immagine Docker, iniettarla dall'esterno.

**ConfigMap** — dati non sensibili:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
```

**Secret** — dati sensibili, valori in **base64** (⚠️ base64 non è crittografia, solo codifica — chiunque acceda al cluster può decodificarlo. Per segreti critici in produzione: Vault, AWS/GCP Secret Manager).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=
```

Si collegano al Deployment come **variabili d'ambiente** o **file montati**:
```yaml
containers:
  - name: mia-app
    envFrom:
      - configMapRef:
          name: app-config
      - secretRef:
          name: app-secret
```

Vantaggio: cambi la config senza ricostruire l'immagine Docker.

## Namespace

Compartimenti logici dentro lo stesso cluster.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: staging
```

A cosa serve:
- Separazione tra **ambienti** (dev/staging/prod) nello stesso cluster.
- Separazione tra **team/progetti**, con permessi (RBAC) diversi.
- Evitare conflitti di nomi (stesso nome risorsa, namespace diversi).
- **Quote di risorse** per namespace.

Nota: alcune risorse sono *namespaced* (Pod, Deployment, Service, ConfigMap...), altre sono *cluster-wide* (Node, alcune config di sicurezza globali).

## RBAC (Role-Based Access Control)

Decide **chi può fare cosa** nel cluster (utenti umani, service account, pipeline CI/CD) — sempre 2 pezzi in coppia:

**1. Role / ClusterRole** — definisce i permessi (verbi su risorse):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: staging
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```
- `Role` → vale solo in **un namespace**.
- `ClusterRole` → vale su **tutto il cluster** (o per risorse non-namespaced).

**2. RoleBinding / ClusterRoleBinding** — assegna quel Role a un utente/service account:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: leggi-pod-per-mario
  namespace: staging
subjects:
  - kind: User
    name: mario.rossi@azienda.com
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

Senza il Binding, il Role esiste ma non è assegnato a nessuno. Usato anche per dare permessi mirati a una pipeline CI/CD tramite service account, invece di usare credenziali umane troppo ampie.

---

## Domande tipiche da colloquio su questi argomenti

- Cosa succede se un node si guasta? (self-healing, reconciliation loop)
- Differenza tra Deployment e Pod creato "a mano"?
- Perché serve un Service se i pod hanno già un IP proprio?
- Differenza tra Service e Ingress, quando serve l'uno o l'altro?
- ConfigMap vs Secret: differenza reale (non solo "uno è sensibile")?
- Perché usare i Namespace invece di cluster separati per ogni ambiente?
- Come funziona RBAC, differenza tra Role e ClusterRole?
- Collegamento concettuale tra reconciliation loop di k8s e GitOps/ArgoCD.
