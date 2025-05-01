echo "Iniciando a aplicação"
# Inicializar a aplicação FastAPI com logs detalhados
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug