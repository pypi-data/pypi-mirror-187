# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Certifik8',
 'Certifik8.constants',
 'Certifik8.examples',
 'Certifik8.modules',
 'Certifik8.modules.converter',
 'Certifik8.modules.generator',
 'Certifik8.modules.handler',
 'Certifik8.tests']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==9.3.0',
 'PyPDF2==2.11.1',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas==1.5.2',
 'pdfkit==1.0.0',
 'setuptools==65.6.3',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['certifik8 = Certifik8.main:run']}

setup_kwargs = {
    'name': 'certifik8',
    'version': '0.2.2',
    'description': 'Certifik8 é um gerador de certificados automático criado em Python. O projeto busca facilitar a geração massiva de documentos a serem emitidos após algum evento.',
    'long_description': '# 2022-2-Certifik8\n\n<a name="readme-top"></a>\n\n<div align="center">\n\n[![Contributors](https://img.shields.io/github/contributors/fga-eps-mds/2022-2-Certifik8.svg?style=for-the-badge&color=e703f7)](https://github.com/fga-eps-mds/2022-2-Certifik8/graphs/contributors)\n[![Issues](https://img.shields.io/github/issues/fga-eps-mds/2022-2-Certifik8.svg?style=for-the-badge&color=e703f7)](https://github.com/fga-eps-mds/2022-2-Certifik8/issues)\n[![MIT License](https://img.shields.io/github/license/fga-eps-mds/2022-2-Certifik8.svg?style=for-the-badge&color=e703f7)](https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/LICENSE)\n\n</div>\n\n<br />\n<div align="center">\n  <a href="https://github.com/fga-eps-mds/2022-2-Certifik8">\n    <img src="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/imagens/logo.png" width="300" height="300">\n  </a>\n  \n  <h3 align="center">Certifik8</h3>\n\n  <p align="center">\n   Gerador Automatico de Certificados \n    <br />\n    <a href="docs">Documentos</a>\n    -\n    <a href="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/SECURITY.md#pol%C3%ADtica-de-seguran%C3%A7a">Reportar Bug</a>\n    -\n    <a href="https://github.com/fga-eps-mds/2022-2-Certifik8/issues">Recomendar Feature</a>\n  </p>\n</div>\n\n<!-- TABLE OF CONTENTS -->\n<details>\n  <summary>Conteúdo</summary>\n  <ol>\n    <li>\n      <a href="#-sobre-o-projeto">📝 Sobre o projeto</a>\n      <ul>\n        <li><a href="#-tecnologias">💻 Tecnologias</a></li>\n      </ul>\n    </li>\n    <li><a href="#-funcionalidade">🤖 Funcionalidade</a></li>\n    <li><a href="#-requisitos">❗ Requisitos</a></li>\n    <li><a href="#-como-rodar">\U0001f6de Como executar</a>\n\t<ul>\n        <li><a href="#---usuário">👩\u200d🦰 Usuário</a></li>\n        </ul>\n\t<ul>\n        <li><a href="#--%EF%B8%8F-desenvolvimento-local">🧙🏼\u200d♀️ Desenvolvimento local</a></li>\n        </ul>  \n    </li>\n    <li><a href="#-desenvolvedores">👨\u200d💻 Desenvolvedores</a></li>\n  </ol>\n</details>\n\n## 📝 Sobre o projeto\n\nCertifik8 é um gerador de certificados automático criado em Python. O projeto busca facilitar a geração massiva de documentos a serem emitidos após algum evento. \n\n## 💻 Tecnologias\n\n#### Tecnologias utilizadas neste projeto:\n\n<p align="center">\n\t<a href="https://skillicons.dev">\n\t\t<img src="https://skillicons.dev/icons?i=python,html,css"/>\n\t</a>\n</p>\n\n## 🤖 Funcionalidade\nO Certifik8 necessita de duas entradas de dados, uma tabela (Excel) no formato XLSX, e dados gerais sobre o evento. Para cada conjunto de informações passadas, um documento com um modelo já preestabelecido é gerado. Os certificados em formato PDF são salvos diretamente na pasta Downloads do computador do usuário.\n\n<div align="center">\n  <a href="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/exemplo/Melissa%20Ribeiro%20Araujo.png">\n    <img src="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/exemplo/Melissa%20Ribeiro%20Araujo.png" width="413" height="291">\n  </a>\n</div>\n\n## ❗ Requisitos\nO Certifik8 só funciona em sistemas operacionais Linux. \n\nTestado no:\n- Linux Mint 21\n- Ubuntu 22.04.01\n\n<div align="center">\n\n![LinuxMint](https://img.shields.io/badge/Linux_Mint-87CF3E?style=for-the-badge&logo=linux-mint&logoColor=black)\n\n![Ubuntu](https://img.shields.io/static/v1?style=for-the-badge&message=Ubuntu&color=E95420&logo=Ubuntu&logoColor=FFFFFF&label=)\n\n</div>\n\n\n**Para conseguir executá-lo, o usuário precisa instalar:**\n  - **Python3 e Pip**\n    ```\n    sudo apt install python3 && sudo apt install python3-pip\n    ```\n\n  - **Instalar a ferramenta wkhtmltopdf**\n    ```\n    sudo apt install wkhtmltopdf\n    ```\n\n## \U0001f6de Como executar/rodar\n### **- 👩\u200d🦰 Usuário**\n1. **Instalando o Certifik8:**\n```\npip install -i https://test.pypi.org/simple/ Certifik8==0.0.2\n```\n\n2. **Digite o comando para obter o endereço da biblioteca:**\n ```\n pip show Certifik8 \n ```\n<div align="center">\n<img src="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/imagens/pip-show.png" width="500" height="300">\n\nCopie o endereço após a "Location", marcado de vermelho na imagem.\n</div>\n\n3. **Executando a aplicação:**\n ```\n python3 {endereço_biblioteca}/Certifik8/main.py\n ```\n<div align="center">\n<img src="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/imagens/path-image.png" width="762" height="95">\n\nSubstitua a chave {endereço_biblioteca} pelo endereço copiado no passo 2.\n</div>\n\n4. **Insira os dados conforme pedido:**\n\n* O endereço da tabela deve ser absoluto.\n\n* Estrutura da tabela Excel ([Exemplo](docs/exemplo/exemplo.xlsx)): \n  - Obs: a tabela deve seguir essa estrutura obrigatoriamente.\n    | 1  | Nome | cpf | Função | Frequência |\n    |---|------|-----|--------|------------|\n    | 2 | Samuel Barbosa Alves | 729.334.326-41 | PARTICIPANTE | 100 |\n    | 3 | Melissa Ribeiro Araujo | 201.544.482-30 | MONITOR | 97 |\n    | 4 | Gabrielly Rodrigues Castro | 451.016.912-40 | PARTICIPANTE | 80 |\n    | ... | ... | ... | ... | ... |\n  \n\n<div align="center">\n\n*Demonstração de funcionalidade.*\n\n<img src="https://github.com/fga-eps-mds/2022-2-Certifik8/blob/main/docs/imagens/demonstracao.png" width="500" height="300">\n\n</div>\n\n### **- 🧙🏼\u200d♀️ Desenvolvimento local**\n1. **Clone o repositório**\n```\ngit clone https://github.com/fga-eps-mds/2022-2-Certifik8.git\n```\n\n2. **Rode os comandos:**\n\n```\nsudo docker build -t squad08\n```\n\n```\ndocker run --name cont_squad08 -it squad08\n```\n\n\n## 👨\u200d💻 Desenvolvedores\n\n<center>\n<table style="margin-left: auto; margin-right: auto;">\n    <tr>\n        <td align="center">\n            <a href="https://github.com/PedroSampaioDias">\n                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/90795603?v=4" width="150px;"/>\n                <h5 class="text-center">Pedro Sampaio</h5>\n            </a>\n        </td>\n        <td align="center">\n            <a href="https://github.com/phmelosilva">\n                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/88786258?v=4" width="150px;"/>\n                <h5 class="text-center">Pedro Henrique</h5>\n            </a>\n        </td>\n        <td align="center">\n            <a href="https://github.com/Victor-oss">\n                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/55855365?v=4" width="150px;"/>\n                <h5 class="text-center">Victório Lazaro</h5>\n            </a>\n        </td>\n        <td align="center">\n            <a href="https://github.com/daniel-de-sousa">\n                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/95941136?v=4" width="150px;"/>\n                <h5 class="text-center">Daniel Sousa</h5>\n            </a>\n        </td>\n        <td align="center">\n            <a href="https://github.com/Leanddro13">\n                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/86811628?v=4" width="150px;"/>\n                <h5 class="text-center">Leandro Silva</h5>\n            </a>\n        </td>\n        <td align="center">\n            <a href="https://github.com/BlimblimCFT">\n                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/12275797?v=4" width="150px;"/>\n                <h5 class="text-center">Geovane Freitas</h5>\n            </a>\n        </td>\n</table>\n</center>\n',
    'author': 'Victorio',
    'author_email': 'victorio.lazaro15@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fga-eps-mds/Certifik8',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
