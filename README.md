<div align="justify">

## Descrição

Este CLI foi criado com o intuito de facilitar o registro de informações sobre atividades feitas para uma empresa e a escolha de ser um CLI é que eu precisaria utilizá-lo em diferentes projetos, de uma forma fácil e que garantisse uma uniformidade nas entradas das informações.

## Objetivos

WIP

## Diretórios do projeto

WIP

## Pré-requisitos

- Python version
> Python 3.11.9

## Setup de Ambiente

1. Realize o clone do repositório:
  > git clone [https://github.com/VictorJSSantos/Atualizador-de-Pedidos.git](https://github.com/VictorJSSantos/Atualizador-de-Pedidos.git)

2. Recomendado:: Crie o ambiente virtual: 
  > python -m venv venv

3. Ativando o ambiente virtual: 
No Windows:
  > venv\Scripts\activate
No Linux:
  > source venv/bin/activate

4. Atualize o pip para garantir a instalação devida das dependências:
  > python -m pip install --upgrade pip

5. Instale as dependências:
  > pip install -r requirements.txt

## O que vai ser necessário para rodar este CLI normalmente?

Será necessário adicionar duas variáveis de ambiente no seu arquivo .env do projeto que utilizará este CLI, que são:
* SUPABASE_PROJECT_URL
* SUPABASE_API_KEY

Além disso, para que funcione conforme o planejado, basta fazer a criação das tabelas da seguinte forma:
```
 CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    descricao TEXT,
    faixas_salariais JSONB,
    renda_por_faixa JSONB
 ); 

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    descricao TEXT,
    horario_de_inicio TIMESTAMP,
    horario_de_finalizacao TIMESTAMP,
    ativo BOOLEAN,
    company_id INT REFERENCES companies (id),
    duracao INTERVAL GENERATED ALWAYS AS (horario_de_finalizacao - horario_de_inicio) STORED,
    projeto TEXT
);
```
</div>
