import typer
from typing import List
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# from dotenv import load_dotenv
from supabase import create_client, Client

# load_dotenv()

# Carregar as variáveis de ambiente (como a URL do Supabase e a API key)
SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")  # URL do Supabase
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")  # Chave da API do Supabase


# Criar o cliente do Supabase
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_API_KEY)


# Criar uma instância do cliente do Supabase que pode ser reutilizada em todo o projeto
supabase = get_supabase_client()


# Instância do app CLI
app = typer.Typer()


def parse_list(value: str) -> List[int]:
    return [int(i) for i in value.split(",")]


#########################################################
###################### EMPRESA ##########################
#########################################################


@app.command()
def criar_empresa(
    name: str = typer.Option(..., help="Nome da empresa"),
    descricao: str = typer.Option(..., help="Descrição da empresa"),
    faixas_salariais: str = typer.Option(
        ..., help="Faixas salariais da empresa (lista de inteiros, ex: 0,10,20)"
    ),
    renda_por_faixa: str = typer.Option(
        ..., help="Renda por faixa da empresa (lista de inteiros, ex: 100,200,300)"
    ),
):
    """
    Comando para criar uma empresa no sistema e enviar ao Supabase.
    """
    # Convertendo as faixas salariais e renda por faixa de string para listas de inteiros
    faixas_salariais_lista = [int(x) for x in faixas_salariais.split(",")]
    renda_por_faixa_lista = [int(x) for x in renda_por_faixa.split(",")]

    # Dados a serem inseridos no Supabase
    data = {
        "name": name,
        "descricao": descricao,
        "faixas_salariais": faixas_salariais_lista,
        "renda_por_faixa": renda_por_faixa_lista,
    }
    try:
        # Enviando os dados para o Supabase
        response = supabase.table("companies").insert(data).execute()

        # Verificando se houve erro na resposta
        if response is not None:
            typer.echo(f"Empresa {name} criada com sucesso!")
    except:
        typer.echo(
            f"Erro ao criar a empresa: {response.data}"
        )  # Usando response.data para exibir o erro


@app.command()
def listar_empresas():
    """
    Comando para listar todas as empresas registradas no sistema.
    """
    try:
        # Enviando a consulta para o Supabase
        response = supabase.table("companies").select("*").execute()

        # Verificando se a resposta retornou dados
        if not response.data:
            typer.echo("Nenhuma empresa encontrada.")
            return

        # Exibindo as empresas
        typer.echo("Lista de empresas:")
        for empresa in response.data:
            typer.echo(
                f"ID: {empresa['id']} | Nome: {empresa['name']} | Descrição: {empresa['descricao']}"
            )
    except Exception as e:
        typer.echo(f"Erro ao listar empresas: {str(e)}")


#########################################################
###################### TAREFA ###########################
#########################################################


@app.command()
def criar_tarefa(
    name: str = typer.Option(..., help="Nome da tarefa"),
    descricao: str = typer.Option(..., help="Descrição da tarefa"),
    horario_de_inicio: int = typer.Option(None, help="Duração da tarefa em horas"),
    horario_de_finalizacao: int = typer.Option(None, help="Faixa salarial da tarefa"),
    company_id: int = typer.Option(..., help="ID da empresa à qual a tarefa pertence"),
):
    """
    Comando para criar uma empresa no sistema e enviar ao Supabase.
    """
    # show_data = supabase.table("tasks").select("*").execute()
    # print(show_data)

    if not horario_de_inicio:
        sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
        horario_de_inicio = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d %H:%M:%S")

    # Dados a serem inseridos no Supabase
    data = {
        "name": name,
        "descricao": descricao,
        "horario_de_inicio": horario_de_inicio,
        "horario_de_finalizacao": horario_de_finalizacao,
        "company_id": company_id,
    }
    try:
        # Enviando os dados para o Supabase
        response = supabase.table("tasks").insert(data).execute()

        # Verificando se houve erro na resposta
        if response is not None:
            typer.echo(f"Tarefa {name} criada com sucesso!")
    except Exception as e:
        typer.echo(
            f"Erro ao criar a empresa: {str(e)}"
        )  # Usando response.data para exibir o erro


# Função para listar tarefas
@app.command()
def listar_tarefas():
    """
    Comando para listar todas as empresas registradas no sistema.
    """
    try:
        # Enviando a consulta para o Supabase
        response = supabase.table("tasks").select("*").execute()

        # Verificando se a resposta retornou dados
        if not response.data:
            typer.echo("Nenhuma tarefa encontrada.")
            return

        # Exibindo as empresas
        typer.echo("Lista de tarefas:")
        for task in response.data:
            typer.echo(
                f"ID: {task['id']} | Nome: {task['name']} | Descrição: {task['descricao']} | "
                f"Horário de Início: {task['horario_de_inicio']} | Horário de Fim: {task['horario_de_finalizacao']}"
            )
    except Exception as e:
        typer.echo(f"Erro ao listar empresas: {str(e)}")


@app.command()
def terminar_tarefa(
    task_id: int = typer.Option(..., help="ID da tarefa que será finalizada"),
):
    """
    Comando para marcar uma tarefa como concluída, definindo o horário de finalização.
    """

    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    horario_de_finalizacao = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Atualizando a tarefa no Supabase para definir o horário de finalização
        response = (
            supabase.table("tasks")
            .update({"horario_de_finalizacao": horario_de_finalizacao, "ativo": False})
            .eq("id", task_id)
            .execute()
        )

        # Verifica se há resposta (se houver, deu certo, se for nulo, não)
        if response:
            typer.echo(f"Tarefa {task_id} finalizada com sucesso!")

    except Exception as e:
        typer.echo(f"Erro ao finalizar a tarefa {task_id}: {str(e)}")


# Função para deletar uma tarefa
@app.command()
def deletar_tarefa(
    task_id: int = typer.Argument(..., help="ID da tarefa a ser deletada")
):
    """
    Comando para deletar uma tarefa do sistema.
    """
    # Buscar a tarefa pelo ID para garantir que ela existe antes de deletar
    response = supabase.table("empresa.tasks").select("*").eq("id", task_id).execute()

    if response.error:
        typer.echo(f"Erro ao buscar a tarefa: {response.error.message}")
        return

    if not response.data:
        typer.echo(f"Tarefa com ID {task_id} não encontrada.")
        return

    # Deletando a tarefa
    response_delete = (
        supabase.table("empresa.tasks").delete().eq("id", task_id).execute()
    )

    if response_delete.error:
        typer.echo(f"Erro ao deletar a tarefa: {response_delete.error.message}")
        return

    # Confirmar que a tarefa foi deletada
    typer.echo(f"Tarefa {task_id} deletada com sucesso!")


if __name__ == "__main__":
    app()
