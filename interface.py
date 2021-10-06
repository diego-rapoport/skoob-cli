from pathlib import Path
import click
from config import cria_config, confere_config, CONFFILE
from base_dataclass import Estante, prateleira
from busca import buscar, pega_info_livros


@click.group(invoke_without_command=True)
def base():
    ...


@base.command()
@click.option('--config',
              '-c',
              help='Caminho para arquivo de configuração não default.',
              type=click.Path(),
              required=False)
@click.option('--id', '-i', help='ID do Usuário', required=False, type=int)
@click.argument('estante')
def livros(estante, config, id):
    """
        Livros da estante: Lido, Lendo, Quero...
    """
    if not CONFFILE.exists() and not config:
        if click.confirm(
                'Você não possui um arquivo de configuração. Deseja gerar um?',
                default=True,
                show_default=True):

            id = click.prompt('Qual o seu ID do Skoob?')
            cria_config(id)
        else:
            click.secho(
                'Você precisa usar um arquivo de configuração! Saindo...',
                fg='red',
                bold=True)
            return 1

    if id:
        conf = {'id': id}
    elif not config:
        conf = confere_config(CONFFILE)
    else:
        conf = confere_config(Path(config))

    if estante.upper() not in prateleira.keys():
        sep = '\n'
        click.secho(f'"{estante}" não encontrada como estante válida.\n',
                    fg='red',
                    bold=True)
        click.echo(
            f'Tente uma das opções abaixo:\n{sep.join(prateleira.keys()).lower()}'
        )
        return 1
    shelf = prateleira.get(estante.upper())
    estante = Estante(**conf, shelf_id=shelf)
    while estante.mais_livros:
        estante.pega_mais_livros()
    click.echo(f'Total de livros: {len(estante.livros)}')
    for indice, livro in enumerate(estante.livros, start=1):
        click.echo(f'{indice} - {livro}')


@click.group()
def procura():
    ...


@procura.command('pesquisar')
@click.option('--pagina',
              '-p',
              help='Procura em outra página, se existir',
              default=1)
@click.argument('nome', required=True)
def procurar(pagina, nome):
    """
        Você pode pesquisar por nome do livro, autor, isbn e etc...
    """
    resposta = buscar(nome, pagina)
    lista_livros = pega_info_livros(resposta)
    for livro in lista_livros:
        click.echo(livro[0])


cli = click.CommandCollection(sources=[base, procura])

if __name__ == '__main__':
    cli()
