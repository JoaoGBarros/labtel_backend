from typing import List, Optional
from sqlalchemy import VARCHAR, BigInteger, String
from sqlalchemy.orm import MappedColumn, mapped_column, Mapped
from app.models.movimentacao import Movimentacao
from sqlalchemy.orm import relationship

from app.settings.database import Base

class Produto(Base):
	__tablename__ = "produto"
	
	id: MappedColumn[BigInteger] = mapped_column(
		BigInteger,
		primary_key=True,
		autoincrement=True,
		
	)
	
	nome: MappedColumn[str] = mapped_column(
		String(255),
		unique=True,
		nullable=False,
	)
	
	estoque: MappedColumn[int] = mapped_column(
		BigInteger,
		nullable=False,
	)

	movimentacoes: Mapped[List["Movimentacao"]] = relationship(
        "Movimentacao",
        back_populates="produto",
        cascade="all, delete-orphan"
    )
	

	
	
    