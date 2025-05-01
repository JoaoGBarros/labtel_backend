from pydantic import BaseModel

class ProdutoRequest(BaseModel):
	nome: str
	estoque: int