from parsel import Selector
import re
import requests
# from typing import


def buscar(busca: str, pagina: int) -> str:
    endpoint = f'https://www.skoob.com.br/livro/lista/busca:{busca}/tipo:geral/mpage:{pagina}'
    resposta = requests.get(endpoint)
    return resposta.text


def pega_info_livros(resposta: str) -> list:
    seletor = Selector(resposta)
    nomes_links = list(
        zip(
            seletor.css('.box_lista_busca_vertical_capa').xpath(
                './a/img/@title').getall(),
            seletor.css('.box_lista_busca_vertical_capa').xpath(
                './a/@href').getall()))
    return nomes_links


def pega_id_livro(link: str) -> str:
    regex = re.compile(r'\d+\w+\.html')
    encontrado = re.findall(regex, link)
    return encontrado[0][:-5]


def pega_ed_livro(link: str) -> str:
    regex = re.compile(r'ed\d+\.')
    encontrado = re.findall(regex, link)
    return encontrado[0][2:-1]
