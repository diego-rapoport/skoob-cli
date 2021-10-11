from dataclasses import dataclass, field
from .erros import NaoDeu200Erro
from pathlib import Path
import requests
from time import sleep
from typing import Optional, NoReturn

HOME = Path.home()
CACHE = HOME / '.cache/skoob-cli'

if not CACHE.exists():
    Path.mkdir(CACHE)

estantes = 'TODOS LIDO LENDO QUERO RELENDO ABANDONEI TENHO EBOOK FAVORITO DESEJADO TROCO EMPRESTEI META AVALIADO RESENHADO AUDIOBOOK'
prateleira = {k: v for v, k in enumerate(estantes.split())}


@dataclass
class Estante:
    """
        Classe Estante do usuário do skoob dado sua ID.
        Cada tipo de estante possui um número com um limite de livros baixados por vez e uma paginação.

        id: Número do id do usuário do skoob
        limite: Número limite de livros baixados de uma vez
        pagina: Número da paginação da estante do skoob
        shelf_id: Tipo da estante

        shelf_ids:
            0 - Todos
            1 - Lido
            2 - Lendo
            3 - Quero Ler
            4 - Relendo
            5 - Abandonei
            6 - Tenho
            7 - Ebook/Digital
            8 - Favorito
            9 - Desejado
            10 - Troco
            11 - Emprestei
            12 - Meta de Leitura
            13 - Avaliado
            14 - Resenhado
            15 - AudioBook

    """
    id: int
    limite: int = field(default=36, compare=False, repr=False)
    pagina: int = field(default=1, compare=False, repr=False)
    shelf_id: int = field(default=0, compare=False)
    mais_livros: bool = field(default=False)

    def __post_init__(self) -> None:
        self.livros = []
        self.atualiza_dados()

    def atualiza_dados(self) -> Optional[str]:
        """
            Função que pega as informações principais do usuário.
        """
        self.url = f'https://www.skoob.com.br/v1/bookcase/books/{self.id}/shelf_id:{self.shelf_id}/page:{self.pagina}/limit:{self.limite}/'
        try:
            self.lista_livros_cru = self.confere_resposta(self.url)
        except NaoDeu200Erro:
            self.livros.append(f'Erro ao pegar livros página: {self.pagina}')
        else:
            # Pega o valor total de livros da estante no skoob
            if not self.lista_livros_cru.get('response'):
                return f'Nenhum livro enontrado na estante {self.shelf_id}'
            self.mais_livros = self.lista_livros_cru.get('paging').get(
                'next_page')
            # Pega só os primeiros 36 livros(default)
            self.pega_livros()
            self.total_livros = self.lista_livros_cru.get('paging').get(
                'total')

    def pega_livros(self) -> None:
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
            Função que chama o erro para operações ternárias e f-strings.
        """
        raise tipo

    def confere_resposta(self, url: str) -> Optional[NoReturn]:
        """
            Verifica se o status da url parâmetro é 200.
            Caso não seja, retorna um erro.
        """
        raw = requests.get(url)
        return raw.json() if raw.status_code == 200 else self.deu_erro(
            NaoDeu200Erro)

    def pega_mais_livros(self) -> None:
        """
            Função que confere se existem mais livros a serem coletados no skoob.
            Caso existam, salva no Usuário.
        """
        if not self.mais_livros:
            return
        self.pagina += 1
        self.atualiza_dados()


@dataclass
class Capa:
    """
        Classe da Capa do livro. Responsável pelas imagens da capa.
        Recebe a url de onde baixa o livro.
    """
    link: str
    titulo: str

    # TODO: Fazer de forma async
    def baixa_capa(self) -> requests.models.Response:
        sleep(1)  # Pra não sobrecarregar o servidor
        download = requests.get(self.link)
        return download

    def cache_capa(self) -> None:
        """
            Salva a imagem da capa do livro em cache.
        """
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
        return f'{self.titulo_br if self.titulo_br else self.titulo} - {self.autor} ({self.ano})'
