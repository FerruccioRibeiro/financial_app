from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Localização do Banco de Dados
# O ./data/ garante que ele salve na pasta que mapeamos no Docker
SQLALCHEMY_DATABASE_URL = "sqlite:///../data/financeiro.db"

# 2. Criar o Engine
# O check_same_thread=False é necessário apenas para o SQLite no FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Criar a Sessão
# Cada requisição terá sua própria sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Classe Base para os Modelos
# É daqui que seus modelos (Tabela de Transações, etc) vão herdar
Base = declarative_base()

# 5. Dependência (O "pulo do gato" do FastAPI)
# Isso garante que a conexão abra e feche corretamente a cada chamada da API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
