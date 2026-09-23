import socket
import argparse
import threading
import json

parser = argparse.ArgumentParser(description="Scanner de portas simples")
parser.add_argument("-t", "--target", help="Endereço IP ou host do alvo", required=True)
parser.add_argument("-p", "--ports", default="1-1000", help="Faixa de portas (ex: 1-1000)")

args = parser.parse_args()
partes = args.ports.split("-")

porta_inicial = int(partes[0])
porta_final = int(partes[1])

print(f"Alvo: {args.target}")
print(f"Portas: {args.ports}")
print(f"Porta inicial: {porta_inicial}")
print(f"Porta final: {porta_final}")

def escanear_porta(porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1)
        s.connect((args.target, porta))
    except Exception:
        pass
    else:
        print(f"Porta {porta} está aberta")
        banner = "N/A"
        try:
            banner = s.recv(1024).decode()
            print(f"Banner da porta {porta}: {banner}")
        except Exception:
            print(f"Não foi possível obter o banner da porta {porta}")

        info = {"porta": porta, "banner": banner}
        with lock:
            resultados.append(info)

resultados = []
lock = threading.Lock()

threads = []
    
for porta in range(porta_inicial, porta_final + 1):
    thread = threading.Thread(target=escanear_porta, args=(porta,))
    thread.start()
    threads.append(thread)

# Esperar todas as threads terminarem
for thread in threads:
    thread.join()

with open("resultados.json", "w") as arquivo:
    json.dump(resultados, arquivo, indent=4)
