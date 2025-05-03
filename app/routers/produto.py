from app.models.movimentacao import Movimentacao
from app.services.movimentacao_service import MovimentacaoService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.produto import ProdutoRequest
from app.schemas.movimentacao import MovimentacaoRequest
from app.models.produto import Produto
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produto", tags=["Produto"])

produtoService = ProdutoService()
movimentacaoService = MovimentacaoService()

@router.post("/addProduto", status_code=status.HTTP_201_CREATED)
async def adicionar_produto(
    produto: ProdutoRequest,
    session: Session = Depends(get_session),
):
    
    try:
        if produtoService.produto_exists(produto.nome, session):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Produto já cadastrado.",
            )
        produtoService.adicionar_produto(produto, session)
        return {"message": "Produto adicionado com sucesso."}
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.__str__(),
        )

@router.get("/info/{produto_nome}")
async def get_produto(
	produto_nome: str,
	session: Session = Depends(get_session),
):
    try:
        produto = produtoService.get_produto_info(produto_nome, session)
        if not produto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Produto não encontrado.",
            )
        return produto
    
    except Exception as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            e.__str__(),
        )

@router.post("/registrarMovimentacao", status_code=status.HTTP_201_CREATED)
async def registrar_movimentacao(
    movimentacao: MovimentacaoRequest,
    session: Session = Depends(get_session),
):
    try:
        produto = produtoService.produto_get(movimentacao.produto, session)
        if not produto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Produto não encontrado.",
            )
        movimentacaoService.registrar_movimentacao(movimentacao, produto, session)
        return {"message": "Movimentação registrada com sucesso."}
    except Exception as e:
          raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                e.__str__(),
            )

@router.get("/{produto_nome}/movimentacoes")
async def retornar_todas_movimentacoes(
    produto_nome: str,
    session: Session = Depends(get_session),
):
    try:
        produto = produtoService.produto_get(produto_nome, session)
        if not produto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Produto não encontrado.",
            )
        
        movimentacoes = movimentacaoService.get_todas_movimentacoes_do_produto(produto.id, session)
        return {"produto": produto.nome, "estoque": produto.estoque, "movimentacoes": movimentacoes}

    except Exception as e:
          raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                e.__str__(),
            )
    
@router.get("/{produto_nome}/movimentacoesSaida")
async def retornar_todas_movimentacoes(
    produto_nome: str,
    session: Session = Depends(get_session),
):
    try:
        produto = produtoService.produto_get(produto_nome, session)
        if not produto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Produto não encontrado.",
            )
        return movimentacaoService.get_movimentacao_saida_do_produto(produto.id, session)
    except Exception as e:
          raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                e.__str__(),
            )
    
@router.get("/{produto_nome}/movimentacoesEntrada")
async def retornar_todas_movimentacoes(
    produto_nome: str,
    session: Session = Depends(get_session),
):
    try:
        produto = produtoService.produto_get(produto_nome, session)
        if not produto:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Produto não encontrado.",
            )
        return movimentacaoService.get_movimentacao_entrada_do_produto(produto.id, session)
    except Exception as e:
          raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                e.__str__(),
            )
    
@router.get("/estatisticas")
async def retornar_estatisticas(
    session: Session = Depends(get_session),
):
    try:
        estatisticas = produtoService.gerar_estatisticas(session)
        return estatisticas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/todosProdutos")
async def retornar_estatisticas(
    session: Session = Depends(get_session),
):
    try:
        produtos = produtoService.get_todos_produtos(session)
        return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))