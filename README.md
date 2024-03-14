# Medical Bot Discord

Este projeto consiste em um bot para o Discord que tem como objetivo auxiliar os usuários a encontrar informações sobre remédios, buscando o menor custo em uma farmácia online. O bot foi desenvolvido em Python e utiliza bibliotecas como Discord.py e Selenium para interagir com o Discord e realizar a automação de processos de web scraping, respectivamente.

## Bot Discord

### Funcionalidades:

- **Mensagem de Boas-Vindas:** Quando o bot é iniciado, ele envia uma mensagem de boas-vindas em um canal específico do servidor Discord, informando aos usuários sobre sua disponibilidade para buscar informações sobre remédios.

- **Recepção de Novos Membros:** O bot também recebe e saúda novos membros que entram no servidor Discord, fornecendo informações sobre como usar o comando de busca de remédios.

- **Busca de Remédios:** Os usuários podem usar o comando `.buscar_remedio nomedoremedio` para solicitar informações sobre um remédio específico. O bot realiza uma busca na farmácia online especificada e retorna informações sobre o remédio, incluindo nome, fabricante, preço e disponibilidade.

### Pré-requisitos:

- Python 3.x
- Discord.py
- Selenium

### Instalação:

1. Clone o repositório para sua máquina local.
2. Instale as dependências `pip install discord selenium webdriver_manager`.
3. Configure o token do bot Discord gerado através do Discord Developer Portal.

### Como Usar:

1. Execute o bot usando o comando `python bot.py`.
2. Conecte o bot ao seu servidor Discord.
3. Use o comando `.buscar_remedio nomedoremedio` para buscar informações sobre um remédio específico.

## Serviço de Farmácia (PharmacyService)

Este serviço é responsável por realizar a busca e a coleta de informações sobre os remédios em uma farmácia online. Ele utiliza o Selenium para automatizar a navegação na web e o web scraping para extrair os dados relevantes.

### Funcionalidades:

- **Busca de Produtos:** O serviço recebe o nome de um remédio como entrada e realiza uma busca na farmácia online especificada, coletando informações sobre os produtos encontrados.

### Uso:

- O serviço pode ser utilizado como uma classe independente para realizar buscas de produtos em uma farmácia online. Basta instanciar a classe `PharmacyService` e chamar o método `get_products`.
