# Emulador do Sistema CHIP-8

Esse projeto tem como objetivo emular a maquina virtual antiga CHIP-8, uma maquina virtual criada em 1976 por Joseph Weisbecker, esse sistema foi projetado para rodar jogos simples em PC'S antigos, como os COSMAC VIP. Nesse caso, este será um emulador que rodará o jogo `pong` feito para esse sistema, de forma totalmente funcional.


**ESPECIFICAÇÕES TÉCNICAS**
- MEMORIA: 4KB
- GRAFICOS: tela monocromatica de 64x32 pixels 
- REGISTRADORES: 16 registradores de uso geral 
- INSTRUÇÕES: 35 instruções simples de 16 bits 
- TIMERS: 2 temporizadores de 8 bits que decrementam a 60hz 

**INSTALAÇÃO**

Esse projeto usa a biblioteca `pygame`. No Windows, use Python 3.12 ou 3.13 x64.

Passos recomendados (como desenvolvedor):

1. Instale Python 3.13 x64.
2. Crie e ative uma virtualenv:
	- `py -3.13 -m venv .venv`
	- `.venv\Scripts\Activate.ps1`
3. Atualize o instalador de pacotes:
	- `python -m pip install --upgrade pip setuptools wheel`
4. Instale as dependências:
	- `pip install -r requirements.txt`
5. No VS Code, selecione o interpretador da `.venv`.

Para executar o emulador, basta abrir o arquivo executável dentro da pasta "dist"

