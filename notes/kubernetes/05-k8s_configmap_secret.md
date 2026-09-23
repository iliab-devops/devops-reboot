## ConfigMap e Secret

Stesso principio delle `variable` in Terraform: non hardcodare config 
nell'immagine Docker, iniettarla dall'esterno.

### ConfigMap — dati non sensibili

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
```

### Secret — dati sensibili

Valori codificati in **base64**.
⚠️ base64 non è crittografia, solo codifica — chiunque abbia accesso al 
cluster può decodificarlo in un attimo. Per segreti critici in produzione: 
Vault, AWS/GCP Secret Manager, o Sealed Secrets.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=
```

### Come si collegano al Deployment

Come **variabili d'ambiente** (tutte insieme, con `envFrom`):
```yaml
containers:
  - name: mia-app
    envFrom:
      - configMapRef:
          name: app-config
      - secretRef:
          name: app-secret
```

Oppure come **file montati** (utile se l'app legge da file invece che da 
env var, o se il Secret è grande):
```yaml
containers:
  - name: mia-app
    volumeMounts:
      - name: config-volume
        mountPath: /etc/config
volumes:
  - name: config-volume
    configMap:
      name: app-config
```

**Vantaggio**: cambi la config senza ricostruire l'immagine Docker.

**⚠️ Attenzione**: aggiornare un ConfigMap/Secret già in uso **non riavvia 
automaticamente** i Pod esistenti (specialmente se iniettato come env var). 
Serve un riavvio manuale (`kubectl rollout restart deployment nome`) o uno 
strumento come Reloader per farlo automaticamente.