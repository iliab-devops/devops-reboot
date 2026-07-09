# What is Docker?

## Definition
Docker is a platform used to create, deploy and run applications inside containers.

## Why Docker exists
- Avoid "it works on my machine"
- Ensure reproducibility
- Simplify deployment

## Main concepts
- Image: blueprint
- Container: running instance
- Registry: image storage (e.g. Docker Hub)

## Image vs Container

- An image is an immutable template (è indipendente dal container, se elimino container l'immagine esiste).
- A container is a running instance of an image.
- Containers share the host operating system kernel.

## Tag dell'immagine
Un tag è un riferimento (alias) a una specifica immagine Docker. Viene comunemente utilizzato per identificare una versione dell'immagine (ad esempio 1.0, 2.0 o latest).
Un'immagine è immutabile: se il contenuto cambia, Docker crea una nuova immagine con un nuovo Image ID. Successivamente è possibile assegnare uno o più tag a quella nuova immagine.
Una stessa immagine può avere più tag (e quindi più nomi), ma tutti puntano allo stesso Image ID. Il tag non è una copia dell'immagine, è semplicemente un riferimento ad essa.

## VM vs Container
Un container non è una macchina virtuale. È un processo isolato. Se il processo principale termina, il container termina. I container condividono il kernel dell'host (più leggero di VM).

## Kernel e container

Un container Docker **non contiene un kernel**.

Contiene il filesystem, le librerie e i programmi necessari per eseguire un'applicazione.

Tutti i container condividono il kernel del sistema operativo host.

Per questo motivo i container sono molto più leggeri e veloci da avviare rispetto alle macchine virtuali.


## My understanding
Docker is a platform used to build, ship and run applications inside containers.
A container is a lightweight and isolated runtime process created from a Docker image.
Images can be downloaded from a registry (like Docker Hub) or built locally using a Dockerfile.
Docker helps ensure that applications run consistently across different environments.