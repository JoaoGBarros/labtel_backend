from pydantic import BaseModel

class MovimentacaoRequest(BaseModel):
	produto: str # Idealmente seria o id, mas para generalizar e deixar parecido com o get, será usado o nome
	quantidade: int
	tipo: str
	