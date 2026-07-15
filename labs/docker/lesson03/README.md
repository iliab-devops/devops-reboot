# Docker Networking

## Obiettivo

Imparare a:

- creare una rete Docker;
- collegare container alla stessa rete;
- verificare il DNS interno;
- ispezionare una rete.

---

## 1. Creare una rete

```bash
docker network create devops-net
```

Verificare:

```bash
docker network ls
```

---

## 2. Creare due container

```bash
docker run -dit \
--name ubuntu1 \
--network devops-net \
ubuntu bash
```

```bash
docker run -dit \
--name ubuntu2 \
--network devops-net \
ubuntu bash
```

---

## 3. Entrare nel primo container

```bash
docker exec -it ubuntu1 bash
```

---

## 4. Verificare l'IP

```bash
hostname -i
```

---

## 5. Verificare la risoluzione DNS

```bash
ping ubuntu2
```

---

## 6. Ispezionare la rete

```bash
docker network inspect devops-net
```

---

## Domande

## Domande

### Perché è meglio usare il nome del container invece dell'IP?

Perché l'indirizzo IP è dinamico e può cambiare quando il container viene ricreato.

### Cosa succede se un container viene eliminato e ricreato?

Può ricevere un nuovo indirizzo IP, ma continua a essere raggiungibile tramite il suo nome (se è collegato alla stessa rete Docker).

### Un container può appartenere a più reti?

Sì, un container può essere collegato contemporaneamente a più reti Docker.