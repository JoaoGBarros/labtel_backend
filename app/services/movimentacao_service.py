from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import DateTime, select
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.repository.movimentacao_repository import MovimentacaoRepository
from app.schemas.movimentacao import MovimentacaoRequest


class MovimentacaoService:
    def __init__(self):
        self.repository = MovimentacaoRepository()

    def get_todas_movimentacoes_do_produto(self, produto_id: int, session: Session) -> list[Movimentacao]:
        return self.repository.get_todas_movimentacao_by_produto(produto_id, session)
    
    def get_todas_movimentacoes(self, session: Session) -> list[Movimentacao]:
        return self.repository.get_todas_movimentacoes(session)
    
    def get_movimentacao_entrada_do_produto(self, produto_id: int, session: Session) -> list[Movimentacao]:
        return self.repository.get_movimentacao_entrada_by_produto(produto_id, session)
    
    def get_movimentacao_saida_do_produto(self, produto_id: int, session: Session) -> list[Movimentacao]:
        return self.repository.get_movimentacao_saida_by_produto(produto_id, session)

    def registrar_movimentacao(self, movimentacao_req: MovimentacaoRequest, produto: Produto, session: Session) -> dict:
        print(movimentacao_req.tipo.upper())
        if movimentacao_req.tipo.upper() == "ENTRADA":
                produto.estoque += movimentacao_req.quantidade
        elif movimentacao_req.tipo.upper() == "SAIDA":
            if produto.estoque < movimentacao_req.quantidade:
                raise ValueError("Estoque insuficiente.")
            produto.estoque -= movimentacao_req.quantidade
        else:
            raise ValueError("Tipo de movimentação inválido.")
        
        movimentacao = Movimentacao(
            produto = produto,
            tipo = movimentacao_req.tipo,
            quantidade = movimentacao_req.quantidade,
            data = datetime.now()
        )

        produto.movimentacoes.append(movimentacao)

        self.repository.update_movimentacao(
            produto.id, {"estoque": produto.estoque}, session
        )

        return {"message": "Movimentação registrada com sucesso."}

    def gerar_estatisticas(self, session: Session) -> dict:
        movimentacoes = self.get_todas_movimentacoes(session)
        total_entrada = sum(mov.quantidade for mov in movimentacoes if mov.tipo == "ENTRADA")
        total_saida = sum(mov.quantidade for mov in movimentacoes if mov.tipo == "SAIDA")
        saldo_atual = total_entrada - total_saida

        return {
            "total_entrada": total_entrada,
            "total_saida": total_saida,
            "saldo_atual": saldo_atual
        }