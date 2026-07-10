### Volumes
Un Docker Volume è un'area di storage persistente gestita da Docker e indipendente dal ciclo di vita dei container.


## Creiamo un container con Volume
docker run -it \
-v prova-volume:/app \
ubuntu /bin/bash

Creo un container, /app è una cartella dentro al container dove si troveranno i dati del volume "prova-volume".

### Bind Mount

