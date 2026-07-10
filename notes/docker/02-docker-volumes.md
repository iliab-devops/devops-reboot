# Volumes

Un **Docker Volume** è un'area di storage persistente gestita da Docker e indipendente dal ciclo di vita dei container.

I dati salvati in un volume rimangono disponibili anche se il container viene arrestato o eliminato.

## Creare un container con un volume

```bash
docker run -it \
-v prova-volume:/app \
ubuntu /bin/bash
```

In questo comando:

- `prova-volume` è un **volume Docker**.
- `/app` è una directory **all'interno del container**.
- Docker collega (monta) il volume `prova-volume` alla directory `/app`.

Qualunque file creato in `/app` verrà salvato nel volume e sarà disponibile anche per altri container che monteranno lo stesso volume.

## Quando usare un volume

I volumi sono utilizzati per conservare dati persistenti, ad esempio:

- database;
- file caricati dagli utenti;
- log;
- configurazioni.

---

# Bind Mount

Un **bind mount** permette di collegare una directory reale del computer host a una directory del container.

A differenza dei volumi, Docker **non gestisce lo storage**: viene utilizzata direttamente una cartella del sistema host.

Esempio:

```bash
docker run -it \
-v /home/ilia/progetto:/app \
ubuntu
```

In questo caso:

- `/home/ilia/progetto` è una cartella reale del computer host;
- `/app` è una directory del container.

Qualsiasi modifica ai file nella cartella host è immediatamente visibile anche dal container.

## Esempio durante lo sviluppo

Supponiamo di avere:

```text
lesson02/
├── Dockerfile
├── app.py
└── README.md
```

Dopo aver costruito l'immagine:

```bash
docker build -t python-bind .
```

possiamo eseguire:

```bash
docker run --rm \
-v $(pwd):/app \
python-bind
```

`$(pwd)` rappresenta la directory corrente.

Il bind mount collega la cartella del progetto alla directory `/app` del container.

Se modifico `app.py` in VS Code e rilancio il container, le modifiche vengono viste immediatamente **senza ricostruire l'immagine**, perché il container sta leggendo direttamente i file presenti sul computer host.

## Quando usare un bind mount

Il bind mount viene utilizzato principalmente durante lo sviluppo, perché permette di modificare il codice senza dover ricostruire l'immagine Docker ad ogni cambiamento.

---

# Differenze

| Volume | Bind Mount |
|---------|------------|
| Gestito da Docker | Gestito dall'utente |
| Docker decide dove salvare i dati | L'utente sceglie la cartella host |
| Ideale per dati persistenti | Ideale per lo sviluppo |
| Indipendente dal filesystem host | Dipende dal filesystem host |