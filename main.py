import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # necessário para comandos funcionarem

bot = commands.Bot(command_prefix=".", intents=intents)

WELCOME_CHANNEL_ID = 1385081350545211483

@bot.event
async def on_ready():
    print(f'✅ Bot está online como {bot.user}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        print("Canal de boas-vindas não encontrado.")
        return

    embed = discord.Embed(
        title="Bem-vindo(a) ao servidor!",
        description=f"Estamos muito felizes em te receber, {member.mention}!\nAproveite e sinta-se em casa!",
        color=discord.Color.pink()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Agora somos {len(member.guild.members)} membros!")

    await channel.send(embed=embed)

# Função para tocar som no canal de voz
async def tocar_som(vc, arquivo="alarm.mp3"):
    vc.play(discord.FFmpegPCMAudio(arquivo))
    while vc.is_playing():
        await asyncio.sleep(0.5)

# Comando para iniciar o ciclo de estudo e descanso
# Dicionário para guardar as tasks de foco
focus_tasks = {}

@bot.command(name="focus")
async def focus(ctx, estudo: int, descanso: int):
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.reply("❗ Você precisa estar em um canal de voz para iniciar o foco.")

    canal = ctx.author.voice.channel

    try:
        vc = await canal.connect()
        await ctx.send("🔊 Bot entrou no canal de voz e iniciou o ciclo de foco.")
    except Exception as e:
        await ctx.send(f"❌ Erro ao conectar ao canal de voz: `{e}`")
        return

    await ctx.send(f"🕒 Iniciando: **{estudo} minutos de estudo** seguidos de **{descanso} minutos de descanso**")

    async def ciclo():
        ciclo_atual = "estudo"
        tempo = estudo * 60
        try:
            while True:
                print(f"⏳ Esperando {tempo} segundos ({ciclo_atual})")
                await asyncio.sleep(tempo)
                await tocar_som(vc)

                if ciclo_atual == "estudo":
                    ciclo_atual = "descanso"
                    tempo = descanso * 60
                    await ctx.send("✅ Estudo encerrado! Iniciando descanso.")
                else:
                    ciclo_atual = "estudo"
                    tempo = estudo * 60
                    await ctx.send("✅ Descanso encerrado! Iniciando novo ciclo de estudo.")

                await tocar_som(vc)
        except asyncio.CancelledError:
            pass
        finally:
            await vc.disconnect()
            await ctx.send("⏹️ Bot desconectado.")

    # Salva a task do canal para depois poder cancelar
    task = asyncio.create_task(ciclo())
    focus_tasks[ctx.guild.id] = task


@bot.command(name="stopfocus")
async def stopfocus(ctx):
    task = focus_tasks.get(ctx.guild.id)
    if task:
        task.cancel()
        await ctx.reply("🛑 Ciclo interrompido!")
        del focus_tasks[ctx.guild.id]
    else:
        await ctx.reply("ℹ️ Nenhum ciclo de foco está ativo no momento.")


@focus.error
async def focus_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Você precisa usar o comando assim: `.focus <minutos_de_estudo> <minutos_de_descanso>`\nExemplo: `.focus 25 5`")
    
# Comando de ajuda personalizada
@bot.command(name="commands")
async def help_command(ctx):
    embed = discord.Embed(
        title="🆘 Comandos disponíveis",
        description="Aqui estão os comandos que você pode usar:",
        color=discord.Color.blurple()
    )
    embed.add_field(name=".focus <estudo> <descanso>", value="Inicia um ciclo de estudo e descanso. Ex: `.focus 25 5`", inline=False)
    embed.add_field(name=".stopfocus", value="Interrompe o ciclo atual de foco.", inline=False)
    await ctx.send(embed=embed)

# Aviso quando o comando não existir
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando não reconhecido. Use `.help` para ver os comandos disponíveis.")
    else:
        raise error  # mantém outros erros funcionando normalmente

bot.run(os.getenv("DISCORD_TOKEN"))
