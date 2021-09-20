from pathlib import Path
import requests
from dataclasses import dataclass, field
from time import sleep
from erros import NaoDeu200Erro

HOME = Path.home()
CACHE = HOME / '.cache/skoob-cli'

if not CACHE.exists():
    Path.mkdir(CACHE)


@dataclass
class Estante:
    """
        Classe Estante com ID do usuário, limite de páginas pra baixar de uma vez do skoob, pagina atual de pesquisa na lista do skoob e livros salvos em formato de lista de dicionários.
    """
    id: int
    limite: int = field(default=36, compare=False, repr=False)
    pagina: int = field(default=1, compare=False, repr=False)

    def __post_init__(self):
        self.livros = []
        self.atualiza_dados()
        self.total_livros = self.lista_livros_cru.get('paging').get('total')

    def atualiza_dados(self):
        """
            Função que pega as informações principais do usuário.
        """
        self.url = f'https://www.skoob.com.br/v1/bookcase/books/{self.id}/shelf_id:0/page:{self.pagina}/limit:{self.limite}/'
        try:
            self.lista_livros_cru = self.confere_resposta(self.url)
        except NaoDeu200Erro:
            self.livros = ['Erro na busca pelos livros.']
        else:
            # Pega o valor total de livros da estante no skoob
            self.mais_livros = True if self.lista_livros_cru.get('paging').get(
                'next_page') else False
            # Pega só os primeiros 36 livros(default)
            self.pega_livros()

    def pega_livros(self):
        for livro in self.lista_livros_cru.get('response'):
            edicao = livro.get('edicao')
            id = edicao.get('livro_id')
            titulo = edicao.get('titulo')
            titulo_br = edicao.get('nome_portugues')
            autor = edicao.get('autor')
            ano = edicao.get('ano')
            capa_media = edicao.get('capa_media')
            capa = Capa(capa_media, titulo_br)
            novo_livro = Livro(id, titulo, titulo_br, autor, ano, capa)
            self.livros.append(novo_livro)

        self.pagina = self.lista_livros_cru.get('paging').get('page')

    def deu_erro(self, tipo):
        """
            Função que chama o erro para operações ternárias.
        """
        raise tipo

    def confere_resposta(self, url):
        """
            Verifica se o status da url parâmetro é 200.
            Caso não seja, retorna um erro.
        """
        raw = requests.get(url)
        return raw.json() if raw.status_code == 200 else self.deu_erro(
            NaoDeu200Erro)

    def pega_mais_livros(self):
        """
            Função que confere se existem mais livros a serem coletados no skoob.
            Caso existam, salva no Usuário.
        """
        if not self.mais_livros:
            return
        self.pagina += 1
        self.pega_livros()


@dataclass
class Capa:
    """
        Classe da Capa do livro. Responsável pelas imagens da capa.
        Recebe a url de onde baixa o livro.
    """
    link: str
    titulo: str

    # TODO: Fazer de forma async
    def baixa_capa(self):
        sleep(1)  # Pra não sobrecarregar o servidor
        download = requests.get(self.link)
        return download

    def cache_capa(self):
        '''
            Salva a imagem da capa do livro em cache.
        '''
        imagem = self.baixa_capa()
        with open(f'{CACHE}/{self.titulo}.jpg', 'wb') as arq:
            arq.write(imagem.content)


@dataclass
class Livro:
    """
        Classe Livro com as informações básicas sobre o mesmo.
    """
    id: int
    titulo: str
    titulo_br: str
    autor: str
    ano: int
    capa: Capa

    def __str__(self):
        return f'{self.titulo_br if self.titulo_br else self.titulo} de {self.autor} - {self.ano}'
