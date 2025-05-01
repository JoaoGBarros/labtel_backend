
from datetime import datetime
import enum
from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import MappedColumn, mapped_column, Mapped
from sqlalchemy.orm import relationship

from app.settings.database import Base

class TipoMovimentacao(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Movimentacao(Base):
    __tablename__ = "movimentacao"
    
    id: MappedColumn[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    
    tipo: MappedColumn[str] = mapped_column(
        Enum(TipoMovimentacao),
        nullable=False,
    )
      
    quantidade: MappedColumn[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    data: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    produto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("produto.id"),
        nullable=False,
    )

    produto: Mapped["Produto"] = relationship(
        "Produto",
        back_populates="movimentacoes"
    )
