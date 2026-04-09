from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Calculo

app = FastAPI(
    title="Calculadora API",
    description="API de Calculadora para Sistemas Distribuidos",
    version="1.0.0"
)

app.mount("/frontend", StaticFiles(directory="calculadora-api"), name="frontend")

Base.metadata.create_all(bind=engine)

class OperacaoRequest(BaseModel):
    numero1: float
    numero2: float

class ResultadoResponse(BaseModel):
    operacao: str
    numero1: float
    numero2: float
    resultado: float


def salvar_calculo(db: Session, numero1: float, numero2: float, operacao: str, resultado: float):
    registro = Calculo(
        numero1=numero1,
        numero2=numero2,
        operacao=operacao,
        resultado=resultado
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro

@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à Calculadora API!", "docs": "/docs"}

@app.get("/app")
def app_ui():
    return RedirectResponse(url="/frontend/index.html")

@app.post("/somar", response_model=ResultadoResponse)
def somar(dados: OperacaoRequest, db: Session = Depends(get_db)):
    resultado = dados.numero1 + dados.numero2
    salvar_calculo(db, dados.numero1, dados.numero2, "soma", resultado)
    return ResultadoResponse(
        operacao="soma",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado
    )

@app.post("/subtrair", response_model=ResultadoResponse)
def subtrair(dados: OperacaoRequest, db: Session = Depends(get_db)):
    resultado = dados.numero1 - dados.numero2
    salvar_calculo(db, dados.numero1, dados.numero2, "subtracao", resultado)
    return ResultadoResponse(
        operacao="subtracao",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado
    )

@app.post("/multiplicar", response_model=ResultadoResponse)
def multiplicar(dados: OperacaoRequest, db: Session = Depends(get_db)):
    resultado = dados.numero1 * dados.numero2
    salvar_calculo(db, dados.numero1, dados.numero2, "multiplicacao", resultado)
    return ResultadoResponse(
        operacao="multiplicacao",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado
    )

@app.post("/dividir", response_model=ResultadoResponse)
def dividir(dados: OperacaoRequest, db: Session = Depends(get_db)):
    if dados.numero2 == 0:
        raise HTTPException(
            status_code=400,
            detail="Divisao por zero nao e permitida!"
        )
    resultado = dados.numero1 / dados.numero2
    salvar_calculo(db, dados.numero1, dados.numero2, "divisao", resultado)
    return ResultadoResponse(
        operacao="divisao",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado
    )


@app.get("/calcular")
def calcular_query(numero1: float, numero2: float, operacao: str, db: Session = Depends(get_db)):
    operacoes = {
        "soma": lambda a, b: a + b,
        "subtracao": lambda a, b: a - b,
        "multiplicacao": lambda a, b: a * b,
        "divisao": lambda a, b: a / b,
    }
    if operacao not in operacoes:
        raise HTTPException(
            status_code=400,
            detail=f"Operacao invalida. Use: {list(operacoes.keys())}"
        )
    if operacao == "divisao" and numero2 == 0:
        raise HTTPException(
            status_code=400,
            detail="Divisao por zero!"
        )
    resultado = operacoes[operacao](numero1, numero2)
    salvar_calculo(db, numero1, numero2, operacao, resultado)
    return {
        "operacao": operacao,
        "numero1": numero1,
        "numero2": numero2,
        "resultado": resultado
    }

@app.get("/historico")
def historico(db: Session = Depends(get_db)):
    calculos = db.query(Calculo).all()
    return calculos

@app.put("/calculo/{id}")
def atualizar_calculo(id: int, resultado: float, db: Session = Depends(get_db)):
    calculo = db.query(Calculo).filter(Calculo.id == id).first()

    if not calculo:
        return {"erro": "Cálculo não encontrado"}

    calculo.resultado = resultado
    db.commit()

    return {"mensagem": "Atualizado com sucesso"}

@app.delete("/calculo/{id}")
def deletar_calculo(id: int, db: Session = Depends(get_db)):
    calculo = db.query(Calculo).filter(Calculo.id == id).first()

    if not calculo:
        return {"erro": "Cálculo não encontrado"}

    db.delete(calculo)
    db.commit()

    return {"mensagem": "Deletado com sucesso"}