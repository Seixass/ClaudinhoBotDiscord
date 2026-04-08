# 🤖 Claudinho Bot — Discord

Bot para Discord desenvolvido em Python com a biblioteca `discord.py`. O Claudinho tem como objetivo melhorar a experiência do servidor com boas-vindas personalizadas e um sistema de foco estilo **Pomodoro** direto no canal de voz.

---

## ✨ Funcionalidades

- 👋 **Boas-vindas automáticas** — envia uma mensagem embed personalizada sempre que um novo membro entra no servidor
- ⏱️ **Ciclo de Foco (Pomodoro)** — entra no canal de voz e alterna entre períodos de estudo e descanso com alertas sonoros
- 🛑 **Parar ciclo** — interrompe o ciclo de foco a qualquer momento
- 📋 **Lista de comandos** — exibe todos os comandos disponíveis via embed

---

## 🚀 Comandos

| Comando | Descrição | Exemplo |
|---|---|---|
| `.focus <estudo> <descanso>` | Inicia um ciclo Pomodoro no canal de voz | `.focus 25 5` |
| `.stopfocus` | Interrompe o ciclo de foco ativo | `.stopfocus` |
| `.commands` | Lista todos os comandos disponíveis | `.commands` |

> **Prefixo padrão:** `.`

---

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [FFmpeg](https://ffmpeg.org/) *(para áudio no canal de voz)*

---

## ⚙️ Como Rodar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/Seixass/ClaudinhoBotDiscord.git
cd ClaudinhoBotDiscord
```

### 2. Instale as dependências

```bash
pip install discord.py python-dotenv PyNaCl
```

> Certifique-se de ter o **FFmpeg** instalado e disponível no PATH do sistema.

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN=seu_token_aqui
```

> ⚠️ **Nunca compartilhe seu token!** O arquivo `.env` já está no `.gitignore`.

### 4. Execute o bot

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
ClaudinhoBotDiscord/
├── main.py        # Código principal do bot
├── alarm.mp3      # Áudio tocado ao fim de cada ciclo
├── .env           # Variáveis de ambiente (não versionado)
├── .gitignore
└── README.md
```

---

## 👤 Autor

Feito com 💜 por **Victor Seixas**  
[GitHub](https://github.com/Seixass)
