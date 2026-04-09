# Trabalho Glaydes - Sistemas Distribuídos

Projeto avaliativo da disciplina de Programação de Sistemas Distribuídos da UNILAGO, desenvolvido com FastAPI. A aplicação oferece uma API de calculadora com operações básicas, armazenamento de histórico em SQLite e uma interface web simples para interação.

## Funcionalidades

- Operações de soma, subtração, multiplicação e divisão
- Persistência dos cálculos em banco SQLite
- Consulta de histórico
- Atualização e remoção de registros
- Interface web servida pela própria aplicação
- Documentação automática com Swagger em `/docs`

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- HTML, CSS e JavaScript

## Estrutura do projeto

```text
.
|-- calculadora-api/
|   |-- app.js
|   |-- index.html
|   `-- styles.css
|-- docs/
|   `-- Documentação.tex
|-- database.py
|-- main.py
|-- models.py
|-- requirements.txt
`-- test_client.py
```

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/diegomlima14/Trabalho-Glaydes---Sistemas-Distribuidos.git
cd Trabalho-Glaydes---Sistemas-Distribuidos
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
pip install sqlalchemy
```

4. Execute a aplicação:

```bash
uvicorn main:app --reload
```

5. Acesse no navegador:

- API: `http://127.0.0.1:8000`
- Documentação interativa: `http://127.0.0.1:8000/docs`
- Interface web: `http://127.0.0.1:8000/app`

## Endpoints principais

### POST `/somar`

```json
{
  "numero1": 10,
  "numero2": 5
}
```

### POST `/subtrair`

```json
{
  "numero1": 10,
  "numero2": 3
}
```

### POST `/multiplicar`

```json
{
  "numero1": 4,
  "numero2": 5
}
```

### POST `/dividir`

```json
{
  "numero1": 10,
  "numero2": 2
}
```

### GET `/calcular`

Exemplo:

```text
/calcular?numero1=8&numero2=2&operacao=divisao
```

### GET `/historico`

Retorna todos os cálculos registrados no banco.

### PUT `/calculo/{id}`

Atualiza o resultado de um cálculo existente.

### DELETE `/calculo/{id}`

Remove um cálculo do histórico.

## Teste rápido

O arquivo `test_client.py` faz requisições para os endpoints principais e pode ser usado para validar a API com o servidor em execução:

```bash
python test_client.py
```

## Observações

- O banco local utilizado pela aplicação é o arquivo `banco.db`
- O diretório `venv/` não é versionado no GitHub
- A aplicação cria a tabela automaticamente ao iniciar

## Autor

Diego Lima
