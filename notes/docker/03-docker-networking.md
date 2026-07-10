## Docker Networking

Tutti i container creati senza specificare una rete vengono collegati automaticamente alla rete bridge predefinita.

Sulla rete bridge predefinita:
- i container possono comunicare tramite IP;
- la risoluzione automatica tramite nome del container non è disponibile.

Le reti bridge create manualmente invece forniscono un DNS interno:
- i container possono comunicare usando il nome del container;
- gli IP possono cambiare senza rompere la comunicazione.

## Docker Network e DNS

I container collegati alla stessa rete Docker personalizzata possono comunicare usando il nome del container.

Docker fornisce un DNS interno (127.0.0.11) che risolve:

nome container → indirizzo IP

Esempio:

backend → database

non serve conoscere l'IP del database.