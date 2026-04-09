
import urllib . request , json
BASE_URL = "http://localhost:8000"

def post(endpoint, dados):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(dados).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Testar todas as operações

r = post("/somar", {"numero1": 10, "numero2": 5})
print(f"Soma: {r['resultado']}")  # 15.0

r = post("/subtrair", {"numero1": 10, "numero2": 3})
print(f"Subtração: {r['resultado']}")  # 7.0

r = post("/multiplicar", {"numero1": 4, "numero2": 5})
print(f"Multiplicação: {r['resultado']}")  # 20.0

r = post("/dividir", {"numero1": 10, "numero2": 2})
print(f"Divisão: {r['resultado']}")  # 5.0
