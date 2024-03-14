import discord
from discord.ext import commands
import json

# Definindo as permissões do bot Discord
permisions = discord.Intents.default()
permisions.message_content = True
permisions.members = True

# Inicializando o bot com o prefixo de comando e as permissões definidas
bot = commands.Bot(command_prefix=".", intents=permisions)

# Função acionada quando o bot está pronto e online
@bot.event
async def on_ready():
    print('bot online')
    canal_id = 'id_do_canal_do_servidor'
    canal = bot.get_channel(canal_id)

    # Verificando se o canal está disponível
    if canal:
        # Criando um embed para enviar uma mensagem de boas-vindas no canal
        meu_embed = discord.Embed(title='Olá pessoal!', description='Estou disponível para fazer buscas por remédios!')
        author_file = discord.File('imagembot.jpeg', 'imagembot.jpeg')
        meu_embed.set_author(name='Medical Bot', icon_url='attachment://imagembot.jpeg', url='https://www.linkedin.com/in/thiago-ferreirapy/')    

        meu_embed.color = discord.Color.dark_green()
        meu_embed.add_field(name='Sou um bot criado para ajudá-los a encontrar remédios de forma autônoma, para isso basta informar o comando com o nome do remédio', value='.buscar_remedio nomedoremedio', inline=False)
        
        # Enviando a mensagem com o embed
        await canal.send(file=author_file, embed=meu_embed)
    else:
        # Caso o canal não seja encontrado
        print(f"Canal com ID {canal_id} não encontrado.")

# Função acionada quando um novo membro entra no servidor do Discord
@bot.event
async def on_member_join(membro:discord.Member):
    canal = bot.get_channel('id_do_canal_do_servidor')
    # Criando um embed para enviar uma mensagem de boas-vindas para o novo membro
    meu_embed = discord.Embed(title=f'Olá {str(membro.display_name).upper()}, seja bem vindo(a) ao servidor!', description="Aproveite o nosso servidor!")

    author_file = discord.File('imagembot.jpeg', 'imagembot.jpeg')
    meu_embed.set_author(name='Bot Python', icon_url='attachment://imagembot.jpeg', url='https://www.linkedin.com/in/thiago-ferreirapy/')    
    meu_embed.set_thumbnail(url=membro.avatar)
    
    meu_embed.color = discord.Color.dark_green()
    meu_embed.add_field(name='Comando aceito:', value='.buscar_remedio nomedoremedio', inline=False)
    
    # Enviando a mensagem com o embed
    await canal.send(file=author_file, embed=meu_embed)

# Comando acionado quando um usuário solicita informações sobre um remédio
@bot.command()
async def buscar_remedio(ctx:commands.Context, remedio:str):
    # Respondendo ao usuário que a busca pelo remédio está em andamento
    await ctx.reply(f"Estou buscando informações sobre {remedio.title()} . Aguarde um momento...")
    from scraping.pharmacy_scraping import PharmacyService
    
    # Obtendo informações sobre o remédio do serviço de scraping
    produto = PharmacyService().get_products(remedio)
    
    # Verificando se o produto foi encontrado
    if produto:
        # Processando e exibindo as informações do produto em um embed
        produto_json = json.loads(produto)
        title_product = produto_json['title_product'][0]
        name_manufacturer = produto_json['name_manufacturer'][0]
        porcent = produto_json['porcent'][0]
        price_from = produto_json['price_from'][0]
        price_final = produto_json['price_final'][0]
        url_image = produto_json['url_image'][0]
        url_product = produto_json['url_product'][0]

        meu_embed = discord.Embed(title=f'Seu produto {remedio.upper()}', description=f"Encontrei seu produto: {title_product}", url=url_product)

        author_file = discord.File('logostoly3.jpg', 'logostoly3.jpg')
        meu_embed.set_author(name='Medical Bot', icon_url='attachment://logostoly3.jpg')
        meu_embed.set_image(url=url_image)

        meu_embed.set_footer(text=f'Fabricante: {name_manufacturer}' )
        meu_embed.color = discord.Color.dark_green()
        meu_embed.add_field(name='Compre no site da farmácia:', value=url_product, inline=False)
        meu_embed.url = url_product

        if porcent != 'N/F':
            meu_embed.add_field(name='Produto em promoção:', value=porcent, inline=False)
            meu_embed.add_field(name='valor sem promoção:', value=price_from, inline=False)
            meu_embed.add_field(name='valor com promoção:', value=price_final, inline=False)
        else:
            meu_embed.add_field(name='valor do produto:', value=price_final, inline=False)

        # Enviando o embed com as informações do produto
        await ctx.send(files=[author_file], embed=meu_embed)
    elif produto == 404:
        # Resposta ao usuário caso o produto não seja encontrado no site da farmácia
        await ctx.reply(f'O produto {remedio.title()} não foi encontrado no site da farmácia')
    else:
        # Resposta ao usuário caso ocorra algum erro na busca pelo produto
        await ctx.reply(f'Desculpa não foi possível encontrar seu produto')

# Execução do bot
if __name__ == "__main__":
    bot.run('codigo_gerado_pelo_auth_do_discord')