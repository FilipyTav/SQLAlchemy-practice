# Prática SQL Alchemy

Projeto para acessar uma base de dados e aplicar a LGPD em dados de usuários, censurando-os.

## Estrutura do Projeto

| Diretório / Arquivo | Descrição |
| :--- | :--- |
| | Ponto de entrada da aplicação. |

## Como Executar

### 1. Pré-requisitos
* **Python 3.10** ou superior.

### 2. Instalação
1. Clone o repositório para sua máquina:
```bash
git clone https://github.com/FilipyTav/SQLAlchemy-practice.git
cd SQLAlchemy-practice
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

- Windows:
```bash
venv\Scripts\activate
```

- Linux:
```bash
source venv/bin/activate
```

3. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

4. Conexão com base de dados:

- Crie o arquivo `src/env.py` e defina as seguintes variáveis:
```py
DB_NAME = ...
DB_PWD = ...
DB_HOST = ...
DB_USER = ...
```

### 3. Execução
Execute o arquivo principal:
```bash
python src/main.py
```
