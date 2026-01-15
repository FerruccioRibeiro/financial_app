from sqlalchemy.orm import Session
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import models, schemas

def register_all_buying(db, buying_itens):
    #Metodo de pagamento
    if buying_itens.installments != None:
        payment_m = "Credito"
    else:
        payment_m = "Debito"

    # Somatorio do valor
    total_value = round(sum(x[1] for x in buying_itens.itens),2)

    # Transforma em datetime pra extrair o dia
    date_date = datetime.strptime(datetime.today(), "%Y-%m-%d")

    # 1. CONSULTA AO BANCO DE BANCOS
    # Buscamos o banco pelo ID para pegar o dia de vencimento (due_date)
    banco = db.query(models.bank).filter(models.bank.name == buying_itens.bank).first()
    dia_vencimento = banco.due_date

    # Inicio do mes
    begin_month = date_date.replace(day=1) if date_date.day < dia_vencimento else date_date.replace(day=1) + relativedelta(months=1)
    formated_begin_month = begin_month.strftime("%Y-%m-%d")


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


print(datetime.today())






# fk_oh = insert_or_update_output_hist(category=categoria, init_month=formated_begin_month, sum_value=total_value, cur=cur, conn=conn)
# fk_purch_inst = insert_purchase_installments(fk_oh=fk_oh, category=categoria, sum_value=total_value, description=desc, payment_m=payment_m, 
#                                              installments=installments, date=date, init_month=formated_begin_month, bank=bank, 
#                                              location=location, cur=cur, conn=conn)
# insert_purchase_itens(fk_purch_inst=fk_purch_inst, itens=itens, cur=cur, conn=conn)

# insert_input_permanent(description="salario", value=8000, bank="Itau", cur=cur, conn=conn)

# insert_input_hist(description="salario", value=8000, bank="Itau", init_month=formated_begin_month, cur=cur, conn=conn)

# insert_output_permanent(description="aluguel", category="moradia", value=1500, bank="Itau", init_date="2025-05-01", end_date="2026-05-01", rate=0.0147, cur=cur, conn=conn)

