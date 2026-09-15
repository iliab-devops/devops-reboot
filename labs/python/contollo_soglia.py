import subprocess

def disco_quasi_pieno(soglia = 80):
    result = subprocess.run(["df"], capture_output=True, text=True)
    righe = result.stdout.split("\n")
    righe = righe[1:]
    for r in righe:
        if not r.strip():
            continue
        colonna = r.split()
        uso = colonna[4].replace("%","")
        uso = int(uso)
        if uso > soglia:
            return True
    return False

