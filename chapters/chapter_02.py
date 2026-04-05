#!/usr/bin/env python3
"""
CHAPTER_02.PY - "O Vazio entre os Bits"
Três semanas depois. O apartamento está um caos. Garrafas vazias, tela do laptop a única luz.
A depressão consome, mas o código... o código faz sentido.

Foco: Autoaprendizado, primeiros fóruns underground
Habilidades: Criptografia básica, anonimato digital, navegação na dark web
Objetivos: 6 missões principais + exploração livre
"""

import os
import sys
import time
import random
import json
import shutil
from datetime import datetime
from pathlib import Path

# Importar dependências
try:
    from utils.terminal_kali import C, digitar as _digitar_padrao
except ImportError:
    class C:
        VERDE = '\033[92m'
        VERMELHO = '\033[91m'
        BRANCO = '\033[97m'
        CINZA = '\033[90m'
        CIANO = '\033[96m'
        AMARELO = '\033[93m'
        ROXO = '\033[95m'
        NEGRITO = '\033[1m'
        RESET = '\033[0m'

    def _digitar_padrao(texto, delay=0.01, cor=C.BRANCO, fim="\n"):
        """Fallback para função de digitação"""
        for char in texto:
            print(f"{cor}{char}{C.RESET}", end='', flush=True)
            time.sleep(delay)
        print(fim, end='')


# ========== GERENCIADOR DE ESTADO DO JOGO ==========

class GameState:
    """Gerencia o estado durante o capítulo"""

    def __init__(self, dados_jogador):
        # Dados originais do jogador
        self.player_name = dados_jogador.get('player_name', 'Hacker')
        self.codiname = dados_jogador.get('codiname', 'ANON')
        self.current_chapter = dados_jogador.get('current_chapter', 2)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 75)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.005)

        # Estado do capítulo
        self.capitulo_concluido = dados_jogador.get('completed', False)
        self.operacao_sucesso = dados_jogador.get('capitulo_2_operacao_sucesso', False)
        self.checkpoint = dados_jogador.get('chapter_02_checkpoint', 'inicio')
        self.saindo_para_menu = dados_jogador.get('saindo_para_menu', False)

        # Missões do capítulo 2
        self.missoes = {
            'instalar_tor': False,              # Instalar e configurar Tor
            'acessar_darkweb': False,           # Acessar onion site
            'criptografar_mensagem': False,     # Usar GPG para criptografar
            'explorar_forum': False,            # Navegar no fórum underground
            'baixar_ferramenta': False,         # Baixar primeira ferramenta
            'primeiro_post': False             # Fazer primeiro post anônimo
        }

        # Estado emocional
        self.nivel_depressao = 85  # Começa alto
        self.motivacao_hacker = 15  # Começa baixo

        # Dark web
        self.onion_sites_descobertos = dados_jogador.get('onion_sites_descobertos', [])
        self.ferramentas_baixadas = dados_jogador.get('ferramentas_baixadas', [])
        self.missoes = dados_jogador.get('missoes_capitulo_2', self.missoes)
        self.nivel_depressao = dados_jogador.get('nivel_depressao', self.nivel_depressao)
        self.motivacao_hacker = dados_jogador.get('motivacao_hacker', self.motivacao_hacker)

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.privacy_level = max(0, self.privacy_level - 1)
        self.motivacao_hacker += 5
        self.nivel_depressao = max(0, self.nivel_depressao - 3)

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.privacy_level = max(0, self.privacy_level - 8)
        self.nivel_depressao += 5

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(20)
            print(f"\n{C.VERDE}✓ MISSÃO CONCLUÍDA: {missao_nome.replace('_', ' ').upper()}{C.RESET}")

    def verificar_progresso(self):
        """Verifica progresso das missões"""
        completas = sum(self.missoes.values())
        total = len(self.missoes)
        return completas, total

    def to_dict(self):
        """Converte estado para dicionário"""
        dados = {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'completed_chapters': self.completed_chapters,
            'score': self.score,
            'privacy_level': self.privacy_level,
            'bitcoin_wallet': self.bitcoin_wallet,
            'chapter_02_checkpoint': self.checkpoint,
            'capitulo_2_resultado': None,
            'capitulo_2_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_2': self.missoes.copy(),
            'nivel_depressao': self.nivel_depressao,
            'motivacao_hacker': self.motivacao_hacker,
            'onion_sites_descobertos': self.onion_sites_descobertos,
            'ferramentas_baixadas': self.ferramentas_baixadas
        }
        return dados


# ========== FUNÇÕES AUXILIARES ==========

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')

def digitar(texto, delay=0.03, cor=C.BRANCO):
    """Função de digitação com efeito"""
    _digitar_padrao(texto, delay, cor)

def erro(mensagem):
    """Exibe mensagem de erro"""
    print(f"\n{C.VERMELHO}[ERRO] {mensagem}{C.RESET}")

def sucesso(mensagem):
    """Exibe mensagem de sucesso"""
    print(f"\n{C.VERDE}[SUCESSO] {mensagem}{C.RESET}")

def aviso(mensagem):
    """Exibe mensagem de aviso"""
    print(f"\n{C.AMARELO}[AVISO] {mensagem}{C.RESET}")

def prompt_kali(username="hacker"):
    """Retorna prompt estilo Kali Linux"""
    return f"{C.VERDE}{username}{C.CINZA}@{C.AMARELO}kali{C.RESET}{C.CINZA}:{C.AMARELO}~{C.RESET}{C.CINZA}$ {C.RESET}"

def exibir_header():
    """Exibe cabeçalho do capítulo"""
    limpar_tela()
    print(f"\n{C.ROXO}{'═' * 80}{C.RESET}")
    print(f"{C.ROXO}║{'ROOT EVOLUTION - CAPÍTULO 2: O VAZIO ENTRE OS BITS':^78}║{C.RESET}")
    print(f"{C.CINZA}║{'Brasília, 3 semanas depois | Terminal: Kali Linux 2024':^78}║{C.RESET}")
    print(f"{C.ROXO}{'═' * 80}{C.RESET}")
    print(f"\n{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.{C.RESET}")
    print(f"{C.CINZA}📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.{C.RESET}")
    print(f"{C.ROXO}{'═' * 80}{C.RESET}")

def exibir_status(state):
    """Exibe status atual do jogador"""
    completas, total = state.verificar_progresso()
    progresso = completas / total * 100

    print(f"\n{C.ROXO}┌─ STATUS DO HACKER ──────────────────────────────┐{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Score: {C.VERDE}{state.score:3d}{C.RESET} │ Privacidade: {C.CIANO}{state.privacy_level:2d}%{C.RESET} │ Missões: {C.VERDE}{completas}/{total}{C.RESET} ({C.VERDE}{progresso:3.0f}%{C.RESET}) {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Depressão: {C.VERMELHO}{state.nivel_depressao:2d}%{C.RESET} │ Motivação: {C.AMARELO}{state.motivacao_hacker:2d}%{C.RESET} │ Sites Onion: {C.ROXO}{len(state.onion_sites_descobertos)}{C.RESET} {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

def salvar_checkpoint(state, arquivo_save, checkpoint_nome):
    """Salva checkpoint do jogo"""
    state.checkpoint = checkpoint_nome
    dados = state.to_dict()

    try:
        with open(arquivo_save, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        print(f"\n{C.CINZA}[✓] Checkpoint salvo: {checkpoint_nome}{C.RESET}")
    except Exception as e:
        erro(f"Erro ao salvar checkpoint: {e}")

def carregar_manual():
    """Carrega o manual de hacking"""
    try:
        from manual_hacking import ManualHacking
        manual = ManualHacking()
        manual.mostrar_menu()
        return True
    except ImportError:
        erro("Manual de hacking não encontrado")
        return False

# ========== FUNÇÕES DE JOGABILIDADE ==========

def prompt_simples(cmd_esperado, descricao, state):
    """Prompt simples sem limite de tempo"""
    print(f"\n{C.CINZA}🎯 OBJETIVO: {descricao}{C.RESET}")
    print(f"{C.VERDE}💻 COMANDO: {cmd_esperado}{C.RESET}")

    while True:
        try:
            cmd = input(prompt_kali(state.codiname)).strip()
        except KeyboardInterrupt:
            print(f"\n{C.VERMELHO}Execução interrompida.{C.RESET}")
            return False

        if cmd.lower() == 'menu':
            state.saindo_para_menu = True
            print(f"\n{C.AMARELO}Retornando ao menu principal...{C.RESET}")
            return False

        if cmd.lower() == 'manual':
            if carregar_manual():
                aviso("Você perdeu tempo consultando o manual!")
                state.registrar_falha(3)
            continue

        if cmd == cmd_esperado:
            sucesso("Comando executado com sucesso!")
            return True
        else:
            erro("Comando incorreto. Tente novamente.")
            state.registrar_falha(2)

def mostrar_pensamentos_depressao(state):
    """Mostra pensamentos depressivos baseados no nível de depressão"""
    pensamentos = [
        "Por que continuar? Nada importa mesmo...",
        "O código é a única coisa que ainda faz sentido...",
        "Ela me traiu. O mundo é podre. Mas o código... o código é puro.",
        "Talvez eu devesse simplesmente desaparecer nos bits...",
        "Cada linha de código me lembra que ainda estou vivo."
    ]

    idx = min(int(state.nivel_depressao / 20), len(pensamentos) - 1)
    print(f"\n{C.CINZA}💭 {pensamentos[idx]}{C.RESET}")
    time.sleep(2)

def tutorial_darkweb():
    """Tutorial sobre dark web e anonimato"""
    print(f"\n{C.ROXO}┌─ GUIA PARA DARK WEB ────────────────────────────┐{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Conceitos fundamentais que você aprenderá:     {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Tor Browser{C.RESET} - Navegador anônimo          {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}.onion{C.RESET} - Domínios da dark web           {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}GPG{C.RESET} - Criptografia de mensagens         {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}VPN + Tor{C.RESET} - Camadas de anonimato       {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Bitcoin{C.RESET} - Moeda para transações         {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")
    input(f"\n{C.CINZA}[ENTER para continuar]{C.RESET}")

# ========== CAPÍTULO 2: SEQUÊNCIA PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save=None):
    """
    Função principal do Capítulo 2
    """
    state = GameState(dados_jogador)

    try:
        # Introdução dramática
        exibir_header()

        digitar("Três semanas se passaram desde aquela noite fatídica.", delay=0.05, cor=C.CIANO)
        time.sleep(1)
        digitar("O apartamento está um caos. Garrafas vazias espalhadas.", delay=0.05, cor=C.CIANO)
        digitar("A tela do laptop é a única luz neste vazio.", delay=0.05, cor=C.CIANO)
        digitar("A depressão me consome, mas... o código. O código faz sentido.", delay=0.05, cor=C.CIANO)

        mostrar_pensamentos_depressao(state)
        print(f"\n{C.CINZA}{'─' * 73}{C.RESET}")
        time.sleep(1)

        # Tutorial dark web
        tutorial_darkweb()

        if not state.missoes.get('instalar_tor', False):
            # MISSÃO 1: Instalar Tor
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 1/6: INSTALAÇÃO DO TOR{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Primeiro passo: anonimato. Vou instalar o Tor.", delay=0.03, cor=C.VERDE)
            digitar("# O Tor permite navegar na dark web anonimamente.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: sudo apt update && sudo apt install tor", delay=0.03, cor=C.CINZA)

            if prompt_simples("sudo apt update && sudo apt install tor", "Instalar o navegador Tor", state):
                state.completar_missao('instalar_tor')
                sucesso("Tor instalado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'tor_instalado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 1 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('acessar_darkweb', False):
            # MISSÃO 2: Acessar primeiro site .onion
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 2/6: PRIMEIRO ACESSO À DARK WEB{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora vou acessar a dark web.", delay=0.03, cor=C.VERDE)
            digitar("# Sites .onion só funcionam através do Tor.", delay=0.03, cor=C.CINZA)
            digitar("# Vou usar o torbrowser-launcher.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: torbrowser-launcher", delay=0.03, cor=C.CINZA)

            if prompt_simples("torbrowser-launcher", "Iniciar o Tor Browser", state):
                state.completar_missao('acessar_darkweb')
                print(f"\n{C.ROXO}🌐 Bem-vindo à Dark Web!{C.RESET}")
                print(f"{C.ROXO}📋 Sites descobertos: duckduckgo.com | protonmail.com{C.RESET}")
                state.onion_sites_descobertos.extend(['duckduckgo.com', 'protonmail.com'])
                sucesso("Conectado à dark web!")
                salvar_checkpoint(state, arquivo_save, 'darkweb_acessada')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 2 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        if not state.missoes.get('criptografar_mensagem', False):
            # MISSÃO 3: Criptografar mensagem
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 3/6: CRIPTOGRAFIA BÁSICA{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Hora de aprender criptografia. Vou usar GPG.", delay=0.03, cor=C.VERDE)
            digitar("# GPG permite criptografar mensagens e arquivos.", delay=0.03, cor=C.CINZA)
            digitar("# Primeiro, gerar chave: gpg --gen-key", delay=0.03, cor=C.CINZA)

            if prompt_simples("gpg --gen-key", "Gerar chave GPG para criptografia", state):
                digitar("\n[*] Chave gerada. Agora vou criptografar uma mensagem de teste.", delay=0.03, cor=C.VERDE)
                digitar("# Comando: echo 'teste' | gpg --encrypt --armor", delay=0.03, cor=C.CINZA)

                if prompt_simples("echo 'teste' | gpg --encrypt --armor", "Criptografar mensagem de teste", state):
                    state.completar_missao('criptografar_mensagem')
                    sucesso("Mensagem criptografada com sucesso!")
                    salvar_checkpoint(state, arquivo_save, 'mensagem_criptografada')
                else:
                    return state.to_dict()
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 3 já concluída. Continuando...{C.RESET}")

            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('explorar_forum', False):
            # MISSÃO 4: Explorar fórum underground
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 4/6: EXPLORAÇÃO DE FÓRUNS{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora vou explorar fóruns underground.", delay=0.03, cor=C.VERDE)
            digitar("# Encontrei um fórum interessante: hackforums.onion", delay=0.03, cor=C.CINZA)
            digitar("# Vou navegar e ver as discussões.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: lynx https://hackforums.onion", delay=0.03, cor=C.CINZA)

            if prompt_simples("lynx https://hackforums.onion", "Acessar fórum underground", state):
                state.completar_missao('explorar_forum')
                print(f"\n{C.ROXO}📋 Tópicos encontrados:{C.RESET}")
                print(f"{C.ROXO}• 'Como começar no hacking ético'{C.RESET}")
                print(f"{C.ROXO}• 'Ferramentas essenciais para Kali Linux'{C.RESET}")
                print(f"{C.ROXO}• 'Mercado negro - cuidados necessários'{C.RESET}")
                sucesso("Fórum explorado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'forum_explorado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 4 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('baixar_ferramenta', False):
            # MISSÃO 5: Baixar primeira ferramenta
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 5/6: DOWNLOAD DE FERRAMENTAS{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Vi uma ferramenta interessante no fórum: sqlmap.", delay=0.03, cor=C.VERDE)
            digitar("# Sqlmap é uma ferramenta para SQL injection.", delay=0.03, cor=C.CINZA)
            digitar("# Vou baixar do repositório oficial.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: git clone https://github.com/sqlmapproject/sqlmap.git", delay=0.03, cor=C.CINZA)

            if prompt_simples("git clone https://github.com/sqlmapproject/sqlmap.git", "Baixar ferramenta sqlmap", state):
                state.completar_missao('baixar_ferramenta')
                state.ferramentas_baixadas.append('sqlmap')
                sucesso("Sqlmap baixado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'ferramenta_baixada')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 5 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('primeiro_post', False):
            # MISSÃO 6: Primeiro post anônimo
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 6/6: PRIMEIRO POST ANÔNIMO{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora vou fazer meu primeiro post anônimo.", delay=0.03, cor=C.VERDE)
            digitar("# Preciso criar uma identidade anônima.", delay=0.03, cor=C.CINZA)
            digitar("# Vou usar um nickname aleatório.", delay=0.03, cor=C.CINZA)

            # Simulação de criação de post
            print(f"\n{C.ROXO}┌─ CRIANDO POST ANÔNIMO ──────────────────────────┐{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Nickname sugerido: {C.VERDE}VoidWalker_00{C.RESET}              {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Tópico: 'Novato procurando orientação'        {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

            digitar("# Vou postar uma pergunta sobre SQL injection.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: echo 'Como usar sqlmap para injeção SQL?' > post.txt && cat post.txt", delay=0.03, cor=C.CINZA)

            if prompt_simples("echo 'Como usar sqlmap para injeção SQL?' > post.txt && cat post.txt", "Criar e visualizar post anônimo", state):
                state.completar_missao('primeiro_post')
                sucesso("Post anônimo criado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'post_criado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 6 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        # FINAL DO CAPÍTULO
        exibir_status(state)

        # Momento de reflexão
        mostrar_pensamentos_depressao(state)

        digitar("\nPela primeira vez em semanas, sinto que tenho um propósito.", delay=0.05, cor=C.CIANO)
        digitar("O código não mente. O código não trai. O código é poder.", delay=0.05, cor=C.CIANO)

        state.capitulo_concluido = True
        state.operacao_sucesso = True
        salvar_checkpoint(state, arquivo_save, 'capitulo_concluido')

        # Resumo final
        completas, total = state.verificar_progresso()
        print(f"\n{C.VERDE}{'═' * 60}{C.RESET}")
        print(f"{C.VERDE}✓ CAPÍTULO 2 CONCLUÍDO!{C.RESET}")
        print(f"{C.CIANO}Missões completadas: {completas}/{total}{C.RESET}")
        print(f"{C.CIANO}Score final: {state.score}{C.RESET}")
        print(f"{C.CIANO}Motivação hacker: {state.motivacao_hacker}%{C.RESET}")
        print(f"{C.VERDE}{'═' * 60}{C.RESET}")

        input(f"\n{C.CINZA}[ENTER para continuar para o próximo capítulo]{C.RESET}")

        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}Capítulo interrompido pelo usuário.{C.RESET}")
        return state.to_dict()
    except Exception as e:
        erro(f"Erro inesperado no capítulo: {e}")
        return state.to_dict()


