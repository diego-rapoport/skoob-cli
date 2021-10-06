from parsel import Selector
import re
import requests

# https://www.skoob.com.br/livro/lista/busca:Asimov/tipo:geral/mpage:1


# seletor.css('.detalhes').xpath('./a/text()').getall()
def buscar(busca, pagina):
    endpoint = f'https://www.skoob.com.br/livro/lista/busca:{busca}/tipo:geral/mpage:{pagina}'
    resposta = requests.get(endpoint)
    return resposta.text


def pega_info_livros(resposta):
    seletor = Selector(resposta)
    nomes_links = list(
        zip(
            seletor.css('.box_lista_busca_vertical_capa').xpath(
                './a/img/@title').getall(),
            seletor.css('.box_lista_busca_vertical_capa').xpath(
                './a/@href').getall()))
    return nomes_links


def pega_id_livro(link):
    regex = re.compile('\d+\w+\.html')
    encontrado = re.findall(regex, link)
    return encontrado[0][:-5]


def pega_ed_livro(link):
    regex = re.compile('ed\d+\.')
    encontrado = re.findall(regex, link)
    return encontrado[0][2:-1]
