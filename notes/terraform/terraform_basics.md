# Terraform — Basi 

## Cos'è e perché

Terraform è uno strumento di **Infrastructure as Code (IaC)**: descrivi l'infrastruttura desiderata in file di testo (`.tf`, linguaggio HCL) e Terraform la crea/modifica per te, chiamando le API dei provider.

Perché usare IaC invece di creare risorse a mano dalla console:
- **Ripetibilità**: rigeneri lo stesso ambiente in modo identico.
- **Versionamento**: il codice sta in Git → storia, review, rollback.
- **Riduzione errore umano**.
- **Disaster recovery più veloce**: ricrei l'infrastruttura da zero con `apply`.

## Provider

Il **provider** è un plugin che sa parlare con una qualsiasi API. Esistono provider per AWS, GCP, Azure, ma anche per Kubernetes, DNS (Cloudflare), monitoring (Datadog), GitHub, ecc.

Un'unica architettura reale può avere pezzi che vivono su sistemi diversi ma che devono lavorare insieme (i.e. app che gira su una VM AWS e che deve scrivere i suoi log su uno storage bucket GCP), in questo caso si utilizzano **più provider nello stesso progetto**:

```hcl
provider "google" {
  project = "il-tuo-progetto"
  region  = "europe-west1"
}

provider "aws" {
  region = "eu-west-1"
}
```

**Punto chiave sul provider Kubernetes**: un cluster è di per sé un sistema con una sua API. Distinzione importante:
- Per **creare il cluster** (es. GKE) → provider `google` (parli con l'API GCP).
- Per **gestire cosa gira dentro il cluster** già esistente (deployment, service, configmap) → provider `kubernetes` (parli con l'API di Kubernetes).

Nella pratica reale, spesso Terraform gestisce solo l'infrastruttura (il cluster), mentre le applicazioni dentro il cluster si gestiscono con Helm/ArgoCD (GitOps) — cicli di vita diversi (l'infrastruttura cambia raramente, i deploy delle app sono frequenti).

## Resource

```hcl
resource "aws_instance" "web_server" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  tags = {
    Name = "prod-web-01"
  }
}
```

Due nomi distinti nel blocco `resource`:
- **`"aws_instance"`** → tipo di risorsa, **fisso**, definito dal provider (documentazione ufficiale). Non si inventa.
- **`"web_server"`** → nome **logico Terraform**, lo scegli tu, deve solo essere unico nel file/modulo. Usato per riferirsi alla risorsa altrove nel codice (es. `aws_instance.web_server.id`).
- Il tag `Name` è invece il nome **reale** che vedi nella console cloud — cosa diversa dal nome logico.

### Creare più risorse simili

- **`count`**: crea N copie identiche, indicizzate (`count.index` parte da 0). Attenzione: se rimuovi un elemento in mezzo, gli indici si "spostano" a cascata → rischio di ricreare risorse per sbaglio.
- **`for_each`**: alternativa più moderna, usa mappa/set con chiavi leggibili invece di indici numerici — preferita quando le risorse non sono identiche tra loro (es. regioni diverse). 

## Variable

Valori parametrizzabili, per non avere nulla hardcoded nel codice.

```hcl
variable "region" {
  type    = string
  default = "europe-west1"
}
```

Uso: `var.region`. Permette di riusare lo stesso file `.tf` per ambienti diversi (dev/staging/prod) cambiando solo i valori. I valori si passano con `default`, file `.tfvars`, o `-var` da riga di comando. Utile anche per non mettere segreti nel codice versionato.

## Output

Valore che Terraform "restituisce" dopo l'`apply`, preso da una risorsa appena creata.

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
}

output "public_ip" {
  value = aws_instance.web.public_ip
}
```

Due usi principali:
1. **Debug/visibilità**: vedi subito un dato (es. IP) senza andare a cercarlo in console.
2. **Collegare moduli tra loro**: l'output di un modulo (es. ID subnet dal modulo "rete") diventa l'input/`variable` di un altro modulo (es. modulo "VM" che deve sapere in quale subnet nascere).

In sintesi: **variable = dati in ingresso, output = dati in uscita.**

## Module

Blocco di risorse riutilizzabile, per non copiare-incollare lo stesso codice più volte (es. stessa configurazione di rete + cluster GKE + bucket per dev/staging/prod).

```hcl
module "gke_cluster" {
  source        = "./modules/gke"
  cluster_name  = "staging-cluster"
  region        = "europe-west1"
}
```

È come "chiamare una funzione": passi parametri (`variable` del modulo), ricevi eventualmente `output`. 

Vantaggi: coerenza tra ambienti, manutenzione centralizzata (fix in un posto solo), riuso tra progetti. Può venire da un registry pubblico o da un repo Git interno aziendale.

## Workspace

Stesso codice, **state separati** per ambiente:

```bash
terraform workspace new dev
terraform workspace select dev
terraform apply   # tocca solo le risorse di "dev"
```

Dentro al codice puoi referenziare `terraform.workspace` per variare configurazioni (es. istanza più grande in prod).

**Nota da colloquio**: i workspace nativi vanno bene per differenze *piccole* (dimensioni, conteggi). Per differenze *strutturali* grandi tra ambienti, molti team preferiscono cartelle separate (`envs/dev`, `envs/prod`) che richiamano gli stessi moduli — più esplicito, meno rischio di applicare per sbaglio in prod.

## State file e remote backend

Il **state file** (`terraform.tfstate`) è la "mappa" di cosa esiste davvero nel cloud secondo Terraform.

- **Mai locale in un contesto di team** → si usa un **remote backend** (es. bucket S3 o GCS).
- Il remote backend abilita anche lo **state locking**: evita che due persone facciano `apply` in conflitto contemporaneamente.

## Autenticazione (come Terraform accede ai provider)

Terraform non ha credenziali proprie — usa quelle trovate nell'ambiente, come farebbe la CLI ufficiale del provider.

**AWS**:
- Variabili d'ambiente `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`
- Profilo da `aws configure` (`~/.aws/credentials`)
- **IAM Role** assegnato alla macchina/pipeline (metodo preferito in produzione — nessuna chiave scritta da nessuna parte)

**GCP**:
- Service Account con chiave JSON (`GOOGLE_APPLICATION_CREDENTIALS`)
- Application Default Credentials se già dentro GCP (es. pipeline su Cloud Build)

**Kubernetes** (provider `kubernetes`):
- Stesso `kubeconfig` usato da `kubectl` (endpoint cluster + certificati/token)

**Regola d'oro da colloquio**: mai credenziali hardcoded nel codice `.tf`, specialmente se il codice sta su Git — sempre variabili d'ambiente, service account o ruoli IAM legati alla pipeline.

---

## Domande tipiche da colloquio su questi argomenti

- Perché usare Terraform invece di creare risorse a mano?
- Differenza tra `count` e `for_each`, quando usare l'uno o l'altro?
- Perché il state file deve stare su un backend remoto in team?
- Come struttureresti un progetto Terraform con più ambienti (dev/staging/prod)?
- Come gestisci le credenziali in una pipeline CI/CD che esegue Terraform?
- Differenza tra gestire il cluster GKE (provider `google`) e gestire risorse dentro il cluster (provider `kubernetes`)?
