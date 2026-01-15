from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas
from .crud import register_all_buying


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
@app.post("/buying_list/", response_model=schemas.BuyingListCreate)
def create_buying_list(buying_itens: schemas.BuyingListCreate, db: Session = Depends(get_db)):
    # 1. Transforma a resposta em dados para installments e purchase itens
    """
    Endpoint que recebe a descrição da compra, o banco e a lista de itens.
    A lógica de soma e atribuição de FK acontece no crud.py.
    """
    try:
        # Chamamos a função do CRUD que vai orquestrar a transação
        nova_compra = register_all_buying(db=db, bundle=buying_itens)
        return nova_compra
    
    except Exception as e:
        # Se algo falhar na transformação (ex: banco não existe), 
        # retornamos um erro claro para o Streamlit
        raise HTTPException(status_code=400, detail=str(e))

# (GET)
@app.get("/buying_installments/", response_model=list[schemas.BuyingInstallmentsResponse])
def list_buying_installments(db: Session = Depends(get_db)):
    return db.query(models.purchases_installments).all()



## Reads
#print(read_month_input_hist(date="2025-05-01", cur=cur))
#print(read_input_permanent(cur=cur))
#print(read_month_output_hist(date="2025-05-01", cur=cur))
#print(read_output_permanent(cur=cur))
#print(read_purchase_itens(fk_purch_inst=1,cur=cur))
#print(read_month_bank_purchase_installments(date="2025-05-01", bank="Itau Black", cur=cur))
