import json
from pathlib import Path

CONFIG = Path.home() / '.config/skoob_cli'
if not CONFIG.exists():
    Path.mkdir(CONFIG)

CONFFILE = CONFIG / 'config.json'


class ConfigError(Exception):
    def __init__(self, mensagem='Erro no arquivo de configuração'):
        self.mensagem = mensagem
        super().__init__(self.mensagem)


def cria_config(id):
    CONFFILE.touch()
    with CONFFILE.open('w') as arquivo:
        config = {}
        config['id'] = id
        json.dump(config, arquivo)


def confere_config(caminho):
    if caminho.exists():
        with caminho.open() as arquivo:
            arq = json.load(arquivo)

        return arq
    raise ConfigError
