class NaoEUrlErro(Exception):
    def __init__(
            self,
            mensagem='A url está incorreta e faltando https ou skoob.com.br'):
        self.mensagem = mensagem
        super().__init__(self.mensagem)


class NaoDeu200Erro(Exception):
    def __init__(self, mensagem='Problema com a resposta do servidor.'):
        self.mensagem = mensagem
        super().__init__(self.mensagem)
