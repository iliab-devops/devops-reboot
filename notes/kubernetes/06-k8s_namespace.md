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
- **Quote di risorse** (CPU/memoria) assegnabili per namespace.

**Nota**: alcune risorse sono *namespaced* (Pod, Deployment, Service, 
ConfigMap...), altre sono *cluster-wide* (Node, PersistentVolume, alcune 
config di sicurezza globali) — queste ultime non appartengono a nessun 
namespace specifico.

### Nella pratica con kubectl

Se non specifichi nulla, i comandi agiscono sul namespace **`default`**:

```bash
kubectl get pods                      # solo namespace default
kubectl get pods -n staging           # namespace specifico
kubectl get pods --all-namespaces     # tutti i namespace insieme
```

Errore comune da principianti (e domanda trabocchetto da colloquio): 
"perché non vedo il mio Pod con `kubectl get pods`?" — spesso è perché 
il Pod è stato creato in un namespace diverso da `default` e ci si 
dimentica il flag `-n`.