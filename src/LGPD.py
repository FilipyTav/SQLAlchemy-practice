from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime
from env import DB_NAME, DB_PWD, DB_HOST, DB_USER
import csv
from pathlib import Path
import logging
from config import LOG_PATH, DATA_DIR, ALL_USERS_CSV, DATA_YEARS_DIR

import time
from functools import wraps

logging.basicConfig(
    filename=LOG_PATH, 
    filemode='w',
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        logging.info(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:5432/{DB_NAME}", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo
def LGPD(row):
    return censor_user(row)

# ATV. 1
def censor_user(user):
    # Cause user is immutable
    # return (
    #     user.id, censor_name(user), censor_cpf(user), censor_email(user),
    #     censor_phone(user), user.data_nascimento, user.created_on
    # )

    return {
        "id": user.id,
        "nome": censor_name(user),
        "cpf": censor_cpf(user),
        "email": censor_email(user),
        "telefone": censor_phone(user),
        "data_nascimento": user.data_nascimento,
        "created_on": user.created_on,
        "updated_on": user.updated_on,
    }

def censor_name(user) -> str :
    name: list[str] = user.nome.split(" ")
    newn: str = name[0]
    newn: str = newn[0] + "*" * (len(newn) - 1)
    return newn

def censor_cpf(user) -> str:
    cpf: list[str] = user.cpf.split(".")
    return f"{cpf[0]}.***.***-**"

def censor_email(user) -> str:
    email: list[str] = user.email.split("@")
    newem: str = email[0]
    newem: str = newem[0] + "*" * (len(newem) - 1)
    return f"{newem}@{email[1]}"

def censor_phone(user) -> str:
    if not user.telefone:
            return "****"
    phone: list[str] = user.telefone
    return phone[-4:]

@medir_tempo
def save_to_csv(data: list[dict], filepath: Path, fieldnames: list[str] = []) -> None:
    if not data:
        return

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as file:
        fieldnames: list[str] = fieldnames if fieldnames else data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)

users_uncensored: list = []
users: list = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        users_uncensored.append(row)

        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)

# ATV.2
def users_by_yob(users: list, year: int) -> list:
    return [u for u in users if u["data_nascimento"].year == year]

year: int = 2006
save_to_csv(users_by_yob(users, year), DATA_YEARS_DIR / f"{year}.csv")

# ATV. 3
all: list[dict] = [{"Nome": u.nome, "CPF": u.cpf} for u in users_uncensored]
save_to_csv(all, ALL_USERS_CSV)
