# Docker Networking

Per impostazione predefinita, tutti i container creati senza specificare una rete vengono collegati alla rete `bridge` predefinita di Docker.

Sulla rete `bridge` predefinita:
- i container possono comunicare tramite indirizzo IP;
- la risoluzione automatica dei nomi dei container non è disponibile.

Creando invece una rete bridge personalizzata:

```bash
docker network create devops-net
```

Docker crea anche un DNS interno.

Su una rete personalizzata:
- i container possono comunicare usando il nome del container;
- non è necessario conoscere l'indirizzo IP;
- gli indirizzi IP possono cambiare senza modificare la configurazione dell'applicazione.

## DNS interno di Docker

Docker utilizza un DNS interno (`127.0.0.11`)[^bignote] per risolvere:

[^bignote] : Questo indirizzo appartiene alla rete di loopback `127.0.0.0/8` (rete virtuale che permette a un dispositivo di inviare pacchetti di dati a se stesso). Docker utilizza un altro indirizzo della stessa rete (127.0.0.11) per far girare il suo piccolo server DNS dentro ogni container.
```
nome container → indirizzo IP
```

Esempio:

```
backend
    |
    | host = "database"
    ▼
Docker DNS
    ▼
database → 172.19.0.3
```

In questo modo, se il container `database` viene eliminato e ricreato con un nuovo indirizzo IP, il backend continua a funzionare perché utilizza il nome del container e non l'IP.

## Ispezionare una rete

Per visualizzare le informazioni di una rete Docker:

```bash
docker network inspect devops-net
```

Tra le informazioni mostrate è possibile vedere:
- i container collegati alla rete;
- l'indirizzo IP assegnato a ciascun container;
- il MAC Address;
- altre informazioni sulla configurazione della rete.

## Un container può appartenere a più reti

Un container può essere collegato a più reti Docker contemporaneamente.

Esempio:

```text
frontend-net
       │
     nginx
       │
backend-net
       │
    database
```

Questo permette, ad esempio, a un container di comunicare sia con l'esterno sia con altri servizi interni.