from fastapi import FastAPI

app = FastAPI(title="Navegador de Carreira API")

@app.get("/")
def read_root():
    return {"mensagem": "API do Navegador de Carreira rodando com sucesso! 🚀"}
