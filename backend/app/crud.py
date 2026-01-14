from sqlalchemy.orm import Session
from . import models, schemas

def registrar_compra_completa(db: Session, compra_in: schemas.CompraCreate):
    # 1. Lógica de Transformação (Data Engineering)
    total = sum(item.valor_unitario for item in compra_in.itens)
    vlr_parcela = total / compra_in.qtd_parcelas

    # 2. Criar o Cabeçalho (Parcelas)
    db_compra = models.CompraParcelada(
        valor_total=total,
        qtd_parcelas=compra_in.qtd_parcelas,
        valor_parcela=vlr_parcela,
        data_compra=compra_in.data_compra
    )
    db.add(db_compra)
    db.flush() # Gera o ID

    # 3. Criar os Detalhes (Itens)
    for item_data in compra_in.itens:
        db_item = models.ItemComprado(
            nome=item_data.nome,
            valor_unitario=item_data.valor_unitario,
            fk_compra=db_compra.id
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_compra)
    return db_compra