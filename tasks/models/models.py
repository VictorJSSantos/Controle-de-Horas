from datetime import datetime


class Company:
    def __init__(self, name, descricao, renda_por_faixa, faixas_salariais):
        self.name = name
        self.descricao = descricao
        self.renda_por_faixa = renda_por_faixa
        self.faixas_salariais = faixas_salariais
        self._horas_trabalhadas = 0
        self.tarefas = []

    def __str__(self):
        faixas_e_rendas = "\n".join(
            f"Faixa salarial: {faixa}, Renda: {renda}"
            for faixa, renda in zip(self.faixas_salariais, self.renda_por_faixa)
        )
        return (
            f"A empresa {self.name} tem a descrição: \n{self.descricao}\n\n"
            "Além disso, a renda por faixa é a seguinte:\n"
            f"{faixas_e_rendas}"
        )

    def adicionar_tarefa(self, tarefa):
        """Adiciona uma tarefa à lista de tarefas da empresa."""
        self.tarefas.append(tarefa)

    def adicionar_horas_trabalhadas(self, quantidade):
        """Adiciona horas trabalhadas e recalcula faixa salarial."""
        if quantidade > 0:
            self._horas_trabalhadas += quantidade

    def reduzir_horas_trabalhadas(self, quantidade):
        """Reduz horas trabalhadas, se aplicável."""
        if quantidade > 0 and self._horas_trabalhadas >= quantidade:
            self._horas_trabalhadas -= quantidade

    def calcular_faixa_atual(self):
        """Determina a faixa salarial com base nas horas trabalhadas."""
        for faixa, renda in zip(self.faixas_salariais, self.renda_por_faixa):
            if self._horas_trabalhadas < faixa:
                return faixa
        return self.faixas_salariais[-1]  # Última faixa, caso ultrapasse todas

    def calcular_remuneracao_total(self):
        """Calcula a remuneração total de acordo com as faixas salariais e horas trabalhadas."""
        total = 0
        horas_restantes = self._horas_trabalhadas
        for faixa, renda in zip(self.faixas_salariais, self.renda_por_faixa):
            if horas_restantes > faixa:
                total += faixa * renda
                horas_restantes -= faixa
            else:
                total += horas_restantes * renda
                break
        return total


class Task:
    def __init__(
        self,
        name,
        descricao,
        duracao,
        faixa_salarial,
        status="ativo",
        horario_inicio=None,
        horario_fim=None,
    ):
        self.name = name
        self.descricao = descricao
        self.duracao = duracao  # Duração em horas
        self.faixa_salarial = faixa_salarial
        self.status = status
        self.horario_inicio = horario_inicio or datetime.now()
        self.horario_fim = horario_fim

    def __str__(self):
        return (
            f"Tarefa: {self.name}\n"
            f"Descrição: {self.descricao}\n"
            f"Duração: {self.duracao} horas\n"
            f"Faixa Salarial: {self.faixa_salarial}\n"
            f"Status: {self.status}\n"
            f"Horário de Início: {self.horario_inicio}\n"
            f"Horário de Finalização: {self.horario_fim or 'Ainda não finalizada'}"
        )

    def finalizar_tarefa(self):
        """Finaliza a tarefa e define o horário de finalização."""
        self.status = "finalizado"
        self.horario_fim = datetime.now()
