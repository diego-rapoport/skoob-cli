from pathlib import Path
import click
from config import cria_config, confere_config, CONFFILE
from base_dataclass import Estante, Livro, Capa


@click.command()
@click.option('--config',
              help='Caminho para arquivo de configuração não default.')
def main(config):
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
    elif config:
        id = confere_config(Path(config))
        cria_config(id)

    else:
        click.echo('Algo aconteceu')


if __name__ == '__main__':
    main()
