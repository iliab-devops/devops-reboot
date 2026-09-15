def conta_errori(percorso_file):
    contatore = 0
    try:
        with open(percorso_file,'r') as file:
            for riga in file:
                if "ERROR" in riga:
                    contatore += 1
                    if contatore <= 3:
                        print(f"{riga}")
        return contatore
    except FileNotFoundError:
        print("Il file non esiste")
        return 0
