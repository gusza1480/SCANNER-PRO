import argparse

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
