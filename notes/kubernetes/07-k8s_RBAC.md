## RBAC (Role-Based Access Control)

Decide **chi può fare cosa** nel cluster (utenti umani, ServiceAccount, 
pipeline CI/CD) — sempre 2 pezzi in coppia.

### 1. Role / ClusterRole — definisce i permessi (verbi su risorse)

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
- `ClusterRole` → vale su **tutto il cluster** (o per risorse non-namespaced, 
  es. i Node).

### 2. RoleBinding / ClusterRoleBinding — assegna il Role a un soggetto

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

Senza il Binding, il Role esiste ma non è assegnato a nessuno.

**Chi può essere il `subject`**: non solo `User` umani, ma anche 
**`ServiceAccount`** — l'identità pensata per processi automatizzati 
(pipeline CI/CD, applicazioni dentro il cluster). Best practice: dare a 
una pipeline un ServiceAccount con permessi mirati (es. solo `deploy` 
su un namespace), invece di usare credenziali umane troppo ampie 
(principio del *least privilege*).

**Pattern comune**: un `ClusterRole` (definito una volta, riutilizzabile) 
può essere collegato con un `RoleBinding` namespaced — così i permessi 
valgono solo in quel namespace specifico, pur riusando la stessa 
definizione di Role ovunque serva.