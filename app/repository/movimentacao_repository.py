from sqlalchemy.orm import Session
from sqlalchemy import and_, select, update
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao
from app.schemas.produto import ProdutoRequest


class MovimentacaoRepository:

    def get_todas_movimentacoes(self, session: Session) -> list[Movimentacao]:
        query = select(Movimentacao).order_by(Movimentacao.data.desc())
        return session.scalars(query).fetchall()

    def get_todas_movimentacao_by_produto(self, produto_id: int, session: Session) -> list[Movimentacao]:
        query = select(Movimentacao).where(Movimentacao.produto_id == produto_id)
        return session.scalars(query).fetchall()
    
    def get_movimentacao_entrada_by_produto(self, produto_id: int, session: Session) -> list[Movimentacao]:
        query = select(Movimentacao).where(and_(Movimentacao.produto_id == produto_id, Movimentacao.tipo == "ENTRADA"))
        return session.scalars(query).fetchall()
    
    def get_movimentacao_saida_by_produto(self, produto_id: int, session: Session) -> list[Movimentacao]:
        query = select(Movimentacao).where(and_(Movimentacao.produto_id == produto_id, Movimentacao.tipo == "SAIDA"))
        return session.scalars(query).fetchall()

    def add_movimentacao(self, movimentacao : Movimentacao, session: Session) -> Movimentacao:
        session.add(movimentacao)
        session.commit()
        return movimentacao