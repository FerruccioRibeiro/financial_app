#from datetime import datetime
#from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas


# Cria as tabelas no SQLite assim que a API sobe
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## Banks
# (POST)
@app.post("/banks/", response_model=schemas.BankResponse)
def create_bank(bank: schemas.BankCreate, db: Session = Depends(get_db)):
    # 1. Converte o Schema em Model
    db_bank = models.bank(name=bank.name, due_date=bank.due_date)
    
    # 2. Salva no Banco
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    
    # 3. Retorna o Model (O FastAPI vai usar o BancoResponse para limpar o dado)
    return db_bank

# (GET)
@app.get("/banks/", response_model=list[schemas.BankResponse])
def list_bancos(db: Session = Depends(get_db)):
    return db.query(models.bank).all()


## Buying itens
# (POST)
@app.post("/buying_installments/", response_model=schemas.BuyingInstallmentsResponse)
def create_bbuying_installments(buying_installments: schemas.BuyingInstallmentsCreate, db: Session = Depends(get_db)):
    # 1. Transforma a resposta em dados para installments e purchase itens
    """
    Endpoint que recebe a descrição da compra, o banco e a lista de itens.
    A lógica de soma e atribuição de FK acontece no crud.py.
    """
    try:
        # Chamamos a função do CRUD que vai orquestrar a transação
        nova_compra = crud.register_all_buying(db=db, bundle=bundle)
        return nova_compra
    
    except Exception as e:
        # Se algo falhar na transformação (ex: banco não existe), 
        # retornamos um erro claro para o Streamlit
        raise HTTPException(status_code=400, detail=str(e))

# (GET)
@app.get("/buying_installments/", response_model=list[schemas.BuyingInstallmentsResponse])
def list_buying_installments(db: Session = Depends(get_db)):
    return db.query(models.purchases_installments).all()











## Inserts
# #Metodo de pagamento
# payment_m = "Credito"

# # Parcelas
# installments = 2
# if payment_m == "Debito":
#     installments = 0

# # Itens
# itens = [
#     ("gasolina", 10)
# ]

# # Categoria
# categoria = "Locomocao"

# # Data - Pegara automatico
# date = "2025-05-01"

# # Somatorio do valor
# total_value = round(sum(x[1] for x in itens),2)

# # Descricao
# desc = "Gasolina"

# # Banco
# bank = "Itau Black"

# # Localizacao - Pegara automatico
# location = "Belo Horizonte"

# # Transforma em datetime pra extrair o dia
# date_date = datetime.strptime(date, "%Y-%m-%d")

# # Primeiro banco
# insert_bank(name="Itau Black", due_date="4", cur=cur, conn=conn)

# # Consulta pra ver o dia de virada da fatura
# cur.execute(f"""
#         SELECT 
#             due_day 
#         FROM bank
#         WHERE 
#             is_delete = 0 
#             AND name = '{bank}'  
# """)
# day_bank = cur.fetchall()[0][0]

# # Inicio do mes
# begin_month = date_date.replace(day=1) if date_date.day < day_bank else date_date.replace(day=1) + relativedelta(months=1)
# formated_begin_month = begin_month.strftime("%Y-%m-%d")

# fk_oh = insert_or_update_output_hist(category=categoria, init_month=formated_begin_month, sum_value=total_value, cur=cur, conn=conn)
# fk_purch_inst = insert_purchase_installments(fk_oh=fk_oh, category=categoria, sum_value=total_value, description=desc, payment_m=payment_m, 
#                                              installments=installments, date=date, init_month=formated_begin_month, bank=bank, 
#                                              location=location, cur=cur, conn=conn)
# insert_purchase_itens(fk_purch_inst=fk_purch_inst, itens=itens, cur=cur, conn=conn)

# insert_input_permanent(description="salario", value=8000, bank="Itau", cur=cur, conn=conn)

# insert_input_hist(description="salario", value=8000, bank="Itau", init_month=formated_begin_month, cur=cur, conn=conn)

# insert_output_permanent(description="aluguel", category="moradia", value=1500, bank="Itau", init_date="2025-05-01", end_date="2026-05-01", rate=0.0147, cur=cur, conn=conn)

## Reads
#print(read_month_input_hist(date="2025-05-01", cur=cur))
#print(read_input_permanent(cur=cur))
#print(read_month_output_hist(date="2025-05-01", cur=cur))
#print(read_output_permanent(cur=cur))
#print(read_purchase_itens(fk_purch_inst=1,cur=cur))
#print(read_month_bank_purchase_installments(date="2025-05-01", bank="Itau Black", cur=cur))
