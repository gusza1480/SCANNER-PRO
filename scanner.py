import socket
import argparse
import threading
import json

# Configuração dos argumentos de linha de comando 
parser = argparse.ArgumentParser(description="Scanner de portas simples")
parser.add_argument("-t", "--target", help="Endereço IP ou host do alvo", required=True)
parser.add_argument("-p", "--ports", default="1-1000", help="Faixa de portas (ex: 1-1000)")

args = parser.parse_args()

# Separa a faixa de portas recebida (ex: "1-1000") em início e fim
partes = args.ports.split("-")    

porta_inicial = int(partes[0])
porta_final = int(partes[1])

print(f"Alvo: {args.target}")
print(f"Portas: {args.ports}")

resultados = []                    # Lista compartilhada que vai guardar os resultados de todas as threads
lock = threading.Lock()            # Lock evita que duas threads escrevam em 'resultados' ao mesmo tempo

# Função que tenta conectar a uma porta específica e capturar o banner do serviço
def escanear_porta(porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1)
        s.connect((args.target, porta))
    except Exception:
        pass                        # Porta fechada ou inacessível — ignora silenciosamente

    else:
        print(f"Porta {porta} está aberta")

        banner = "N/A"              # Tenta capturar o banner enviado pelo serviço (se houver) 
        try:
            banner = s.recv(1024).decode()
            print(f"Banner da porta {porta}: {banner}")
        except Exception:
            print(f"Não foi possível obter o banner da porta {porta}")

        # Registra o resultado de forma segura entre threads
        info = {"porta": porta, "banner": banner}
        with lock:
            resultados.append(info)


# Dispara uma thread para cada porta da faixa, permitindo scan paralelo 
threads = []

for porta in range(porta_inicial, porta_final + 1):
    thread = threading.Thread(target=escanear_porta, args=(porta,))
    thread.start()
    threads.append(thread)

# Aguarda todas as threads finalizarem antes de exportar o resultado
for thread in threads:
    thread.join()

# Exporta os resultados coletados em formato JSON 
with open("resultados.json", "w") as arquivo:
    json.dump(resultados, arquivo, indent=4)
