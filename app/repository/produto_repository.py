from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload 
from app.models.produto import Produto
from app.schemas.produto import ProdutoRequest


class ProdutoRepository:

    def get_produto(self, produto_nome: str, session: Session) -> bool:
        query = select(Produto).where(Produto.nome == produto_nome)
        return session.scalars(query).first()
    
    def get_todos_produtos_e_movimentacoes(self, session: Session):
        query = select(Produto).options(joinedload(Produto.movimentacoes))
        result = session.execute(query).unique()
        return result.scalars().all()
    
    def get_produto_e_movimentacoes(self, produto_nome: str, session: Session) -> Produto:
        query = select(Produto).options(joinedload(Produto.movimentacoes)).where(Produto.nome == produto_nome)
        return session.scalars(query).first()

    def produto_exists(self, produto_nome: str, session: Session) -> bool:
        result = self.get_produto(produto_nome, session)
        return result is not None

    def add_produto(self, produto_dict, session: Session) -> Produto:
        produto = Produto(**produto_dict)
        session.add(produto)
        session.commit()
        return produto

    def update_produto(self, produto : Produto, session: Session) -> Produto:
        session.add(produto)
        session.commit()
        return produto
    