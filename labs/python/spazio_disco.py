import subprocess

def spazio_disco():
    result = subprocess.run(["df","-h"],capture_output= True, text= True)
    return result.stdout