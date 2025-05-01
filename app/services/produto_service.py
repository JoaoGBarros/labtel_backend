from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.produto import Produto
from app.repository.produto_repository import ProdutoRepository
from app.schemas.produto import ProdutoRequest


class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()

    def produto_get(self, produto_nome: str, session: Session) -> Produto:
        return self.repository.get_produto(produto_nome, session)
    
    def get_todos_produtos(self, session: Session):
        return self.repository.get_todos_produtos_e_movimentacoes(session)

    def produto_exists(self, produto_nome: str, session: Session) -> bool:
        return self.repository.get_produto(produto_nome, session) is not None

    def adicionar_produto(self, produto: ProdutoRequest, session: Session) -> Produto:
        produto_dict = produto.model_dump()
        return self.repository.add_produto(produto_dict, session)
    
    def atualizar_produto(self, produto: Produto, session: Session):
        return self.repository.update_produto(produto, session)
    
    def get_produto_info(self, produto_nome: str, session: Session) -> Produto:
        return self.repository.get_produto_e_movimentacoes(produto_nome, session)
    
    def gerar_estatisticas(self, session: Session) -> list[dict]:
        produtos = self.get_todos_produtos(session)
        if not produtos:
            raise ValueError("Nenhum produto encontrado no banco de dados.")

        estatisticas = []
        for produto in produtos:
            quantidade_entrada = 0
            quantidade_saida = 0
            quantidade_registros_entrada = 0
            quantidade_registros_saida = 0

            for mov in produto.movimentacoes:
                if mov.tipo == "ENTRADA":
                    quantidade_entrada += mov.quantidade
                    quantidade_registros_entrada += 1
                elif mov.tipo == "SAIDA":
                    quantidade_saida += mov.quantidade
                    quantidade_registros_saida += 1

            estoque_atual = produto.estoque

            if quantidade_registros_entrada > quantidade_registros_saida:
                relacao_entrada_saida = "ENTRA MAIS"
            elif quantidade_registros_saida > quantidade_registros_entrada:
                relacao_entrada_saida = "SAI MAIS"
            else:
                relacao_entrada_saida = "IGUAL"

            estatisticas.append({
                "produto": produto.nome,
                "quantidade_reistros_entrada": quantidade_registros_entrada,
                "quantidade_reistros_saida": quantidade_registros_saida,
                "quantidade_entrada": quantidade_entrada,
                "quantidade_saida": quantidade_saida,
                "relacao_entrada_saida": relacao_entrada_saida,
                "estoque_atual": estoque_atual
            })

        return estatisticas