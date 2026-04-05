#!/usr/bin/env python3
"""
CHAPTER_10.PY - "A Caçada"
O governo contra-ataca. Evasão, contra-inteligência, e fuga desesperada.

Foco: Sobrevivência digital, evasão de autoridades
Habilidades: Contra-inteligência, anonimato avançado, extração segura
Objetivos: 5 missões principais + sobrevivência
"""

import os
import sys
import time
import random
import json
import shutil
from datetime import datetime
from pathlib import Path

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
        for char in texto:
            print(f"{cor}{char}{C.RESET}", end='', flush=True)
            time.sleep(delay)
        print(fim, end='')

class GameState:
    def __init__(self, dados_jogador):
        self.player_name = dados_jogador.get('player_name', 'Hacker')
        self.codiname = dados_jogador.get('codiname', 'ANON')
        self.current_chapter = dados_jogador.get('current_chapter', 10)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 40)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.15)
        self.reputation = dados_jogador.get('reputation', 200)

        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.checkpoint = 'inicio'

        self.missoes = {
            'detectar_rastreamento': False,
            'evadir_autoridades': False,
            'cobrir_rastros': False,
            'preparar_extracao': False,
            'executar_fuga': False
        }

        self.nivel_ameaca = 0
        self.tempo_restante = 300

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'completed_chapters': self.completed_chapters,
            'score': self.score,
            'privacy_level': self.privacy_level,
            'bitcoin_wallet': self.bitcoin_wallet,
            'reputation': self.reputation,
            'chapter_10_checkpoint': self.checkpoint,
            'capitulo_10_resultado': None,
            'capitulo_10_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_10': self.missoes.copy(),
            'nivel_ameaca': self.nivel_ameaca,
            'tempo_restante': self.tempo_restante
        }

def iniciar(dados_jogador, arquivo_save):
    game_state = GameState(dados_jogador)

    print(f"{C.NEGRITO}{C.ROXO}")
    print("═" * 80)
    print("               [ROOT EVOLUTION - CAPÍTULO 10: A CAÇADA]")
    print("                 Brasília, 06:00 AM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")

    print("Eles sabem que estou aqui. A caçada começou...")
    print("Preciso sobreviver e escapar com as informações.")

    # Simulação simplificada
    time.sleep(2)
    print(f"{C.VERDE}✓ Capítulo 10 concluído - Fuga bem-sucedida!{C.RESET}")
    game_state.capitulo_concluido = True
    game_state.operacao_sucesso = True

    return game_state.to_dict()

    def digitar(texto, delay=0.03, cor=C.BRANCO, fim="\n"):
        print(f"{cor}{texto}{C.RESET}", end=fim)
        time.sleep(len(texto) * delay)

    def limpa_tela():
        os.system('cls' if os.name == 'nt' else 'clear')


# ========== ESTADO DO JOGO ==========

class GameStateChapter10:
    def __init__(self, dados_anteriores):
        self.player_name = dados_anteriores.get('player_name', 'Neo')
        self.codinome = dados_anteriores.get('codiname', 'SHADOW_00')
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0) or 0
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        self.darknet_access = True
        self.aliados = dados_anteriores.get('aliados', 0)
        self.segredos_descobertos = dados_anteriores.get('segredos_descobertos', [])
        self.firewalls_quebrados = dados_anteriores.get('firewalls_quebrados', 0)
        self.sistemas_comprometidos = dados_anteriores.get('sistemas_comprometidos', 0)
        self.revelacoes = dados_anteriores.get('revelacoes', 0)
        self.confrontos = dados_anteriores.get('confrontos', 0)

        # Escolhas anteriores
        self.escolha_final_cap5 = dados_anteriores.get('escolha_final', 'expor')
        self.dilema_moral = getattr(dados_anteriores, 'dilema_escolha', 'justica')
        self.final_escolha = getattr(dados_anteriores, 'final_escolha', 'reformar')

        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False

        # Estado específico do capítulo
        self.final_determinado = None

    def registrar_falha(self, penalidade=40):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        if self.privacy_level <= 0:
            self.game_over = True

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 35

    def determinar_final(self):
        """Determina o final baseado em todas as escolhas"""
        # Lógica complexa baseada em todas as escolhas do jogador
        score_moral = 0

        # Escolha do capítulo 5
        if self.escolha_final_cap5 == 'expor':
            score_moral += 2
        elif self.escolha_final_cap5 == 'controlar':
            score_moral -= 2
        else:  # terceira_via
            score_moral += 1

        # Dilema moral
        if self.dilema_moral == 'perdao':
            score_moral += 1
        elif self.dilema_moral == 'justica':
            score_moral += 2
        else:  # ambiguidade
            score_moral += 0

        # Escolha final
        if self.final_escolha == 'destruir':
            score_moral -= 1
        elif self.final_escolha == 'reformar':
            score_moral += 2
        else:  # desaparecer
            score_moral += 0

        # Estatísticas do jogo
        if self.reputation >= 500:
            score_moral += 1
        if self.aliados >= 5:
            score_moral += 1
        if self.revelacoes >= 5:
            score_moral += 1

        # Determinar final
        if score_moral >= 6:
            self.final_determinado = "redencao"
        elif score_moral >= 3:
            self.final_determinado = "equilibrio"
        elif score_moral >= 0:
            self.final_determinado = "sobrevivencia"
        else:
            self.final_determinado = "trevas"

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 10,  # Sempre capítulo 10
            'completed_chapters': [1, 2, 3, 4, 5, 6, 7, 8, 9],  # Capítulos 1-9 devem estar completados
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy_level,
            'reputation': self.reputation,
            'score': self.score,
            'inventory': self.inventory,
            'darknet_access': self.darknet_access,
            'aliados': self.aliados,
            'segredos_descobertos': self.segredos_descobertos,
            'firewalls_quebrados': self.firewalls_quebrados,
            'sistemas_comprometidos': self.sistemas_comprometidos,
            'revelacoes': self.revelacoes,
            'confrontos': self.confrontos,
            'escolha_final': self.escolha_final_cap5,
            'dilema_escolha': self.dilema_moral,
            'final_escolha': self.final_escolha,
            'final_determinado': self.final_determinado,
            'completed': getattr(self, 'capitulo_concluido', False),
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }


# ========== UI AUXILIAR ==========

def header_kali_v2(titulo="CAPÍTULO 10: O NOVO AMANHECER"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass

    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Finais - Novo Amanhecer | Status: CONCLUINDO':^{largura}}{C.RESET}")
    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print()
    print(f"{C.AMARELO}💡 DICA: Digite {C.RESET}{C.VERMELHO}'menu'{C.RESET}{C.AMARELO} para retornar ao menu do jogo a qualquer momento.{C.RESET}")
    print(f"{C.AMARELO}📖 Acesse{C.RESET}{C.VERMELHO}'manual'{C.RESET}{C.AMARELO}para consultar o Manual de Hacking durante o jogo.{C.RESET}")
    print(f"{C.VERDE}{'═' * largura}{C.RESET}\n")

def pensamento(texto):
    """Exibe um pensamento do personagem"""
    print(f"\n{C.CIANO}{C.NEGRITO}>> {texto}{C.RESET}")
    time.sleep(1.5)

def narracao(texto, delay=0.04):
    """Exibe texto narrativo"""
    digitar(texto, delay=delay, cor=C.BRANCO)
    time.sleep(0.5)

def drama_pause(segundos=1):
    time.sleep(segundos)

def prompt_kali(codinome):
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/dawn{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

def check_comandos_globais(cmd, state):
    if cmd.lower() == 'menu':
        state.saindo_para_menu = True
        return "MENU"
    if cmd.lower() in ['manual', 'help']:
        try:
            from manual_hacking import ManualHacking
            man = ManualHacking()
            man.mostrar_menu()
        except:
            print(f"\n{C.AMARELO}[SISTEMA]: Manual indisponível neste setor.{C.RESET}")
        return "MANUAL"
    return None

def mostrar_resumo_jornada(state):
    """Mostra resumo da jornada completa"""
    print(f"\n{C.ROXO}╔════ RESUMO DA JORNADA ════╗{C.RESET}")
    print(f"{C.ROXO}║ Score Final: {state.score:>5}          ║{C.RESET}")
    print(f"{C.ROXO}║ Reputation: {state.reputation:>3}            ║{C.RESET}")
    print(f"{C.ROXO}║ Aliados: {state.aliados:>2}                 ║{C.RESET}")
    print(f"{C.ROXO}║ Revelações: {state.revelacoes:>2}             ║{C.RESET}")
    print(f"{C.ROXO}║ Bitcoin: {state.bitcoin:>5.3f}         ║{C.RESET}")
    print(f"{C.ROXO}╚{'═'*32}╝{C.RESET}\n")


# ========== QUESTS/DESAFIOS ==========

def quest_1_reflection(state):
    """Quest 1: Reflexão sobre a jornada - Dificuldade: Média"""
    print(f"\n{C.AMARELO}╔════ QUEST 1: REFLEXÃO ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Analisar jornada ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*31}╝{C.RESET}\n")

    pensamento("Olhando para trás... como cheguei até aqui?")

    mostrar_resumo_jornada(state)

    # Parte 1: Revisar escolhas
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "history" in cmd or "log" in cmd:
            print(f"{C.CINZA}[*] Revisando histórico de escolhas...{C.RESET}")
            time.sleep(3)
            print(f"{C.BRANCO}[Capítulo 5]: {state.escolha_final_cap5}{C.RESET}")
            print(f"{C.BRANCO}[Dilema]: {state.dilema_moral}{C.RESET}")
            print(f"{C.BRANCO}[Final]: {state.final_escolha}{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'history --choices' para revisar escolhas.{C.RESET}")
            state.registrar_falha(8)

    pensamento("Cada escolha moldou quem me tornei. Não há arrependimentos.")

    state.registrar_sucesso(50, 0.02)
    return True

def quest_2_legacy_creation(state):
    """Quest 2: Criação do legado - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 2: LEGADO ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Deixar marca    ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*28}╝{C.RESET}\n")

    pensamento("O que deixarei para o mundo? Qual será meu legado?")

    # Parte 1: Criar manifesto
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "nano" in cmd or "vim" in cmd:
            print(f"{C.CINZA}[*] Criando manifesto final...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERDE}[+] Manifesto 'Código da Liberdade' criado{C.RESET}")
            print(f"{C.VERDE}[+] Documento de 12 páginas escrito{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'nano manifesto.txt' para escrever.{C.RESET}")
            state.registrar_falha(10)

    # Parte 2: Publicar legado
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "publish" in cmd or "upload" in cmd:
            print(f"{C.CINZA}[*] Publicando legado na dark web...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Manifesto publicado anonimamente{C.RESET}")
            print(f"{C.VERDE}[+] Tornou-se viral na comunidade hacker{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'publish --anonymous manifesto.txt' para publicar.{C.RESET}")
            state.registrar_falha(12)

    pensamento("Meu legado está definido. Que sirva de inspiração para outros.")

    state.registrar_sucesso(70, 0.03)
    return True

def quest_3_final_goodbye(state):
    """Quest 3: Adeus final - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 3: ADEUS FINAL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Encerrar jornada   ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*32}╝{C.RESET}\n")

    pensamento("É hora de dizer adeus. Mas adeus a quê?")

    # Cena emocional baseada no final determinado
    state.determinar_final()

    if state.final_determinado == "redencao":
        print(f"\n{C.CIANO}[CENA FINAL - REDENÇÃO]{C.RESET}")
        narracao("Você encontra Juliana novamente. Não como inimiga, mas como alguém que entende.")
        print(f"\n{C.BRANCO}[Juliana]: Você mudou. Mas ainda há bondade em você.{C.RESET}")
        print(f"{C.CIANO}[Você]: Aprendi que o código pode curar tanto quanto destruir.{C.RESET}")

    elif state.final_determinado == "equilibrio":
        print(f"\n{C.AMARELO}[CENA FINAL - EQUILÍBRIO]{C.RESET}")
        narracao("Você se torna um guardião das sombras. Nem herói, nem vilão.")
        print(f"\n{C.BRANCO}[V0id_Walker]: Você encontrou o equilíbrio que eu nunca consegui.{C.RESET}")
        print(f"{C.CIANO}[Você]: Equilíbrio é só outra forma de controle.{C.RESET}")

    elif state.final_determinado == "sobrevivencia":
        print(f"\n{C.CINZA}[CENA FINAL - SOBREVIVÊNCIA]{C.RESET}")
        narracao("Você desaparece na rede. Sobrevivendo, mas sempre olhando por cima do ombro.")
        print(f"\n{C.BRANCO}[Agente Costa]: Você ganhou esta batalha. Mas a guerra continua.{C.RESET}")
        print(f"{C.CIANO}[Você]: Toda guerra tem um vencedor. Até que o próximo ciclo comece.{C.RESET}")

    else:  # trevas
        print(f"\n{C.VERMELHO}[CENA FINAL - TREVAS]{C.RESET}")
        narracao("Você se torna o que mais temia. O novo V0id_Walker, mas pior.")
        print(f"\n{C.ROXO}[Novo Você]: O sistema precisava ser quebrado. Eu o quebrei.{C.RESET}")
        print(f"{C.CIANO}[Último Pensamento]: Era para ser diferente...{C.RESET}")

    drama_pause(3)

    # Parte 1: Última ação
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "shutdown" in cmd or "exit" in cmd:
            print(f"{C.CINZA}[*] Desligando sistemas...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Jornada concluída{C.RESET}")
            print(f"{C.VERDE}[+] Adeus, {state.codinome}{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'shutdown -h now' para finalizar.{C.RESET}")
            state.registrar_falha(15)

    state.registrar_sucesso(200, 0.1)
    return True


# ========== CENA PRINCIPAL ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)

    digitar(f"{C.CINZA}O sol nasce.{C.RESET}", delay=0.1)
    drama_pause(1)
    digitar(f"{C.CINZA}Um novo dia.{C.RESET}", delay=0.08)
    drama_pause(1)
    digitar(f"{C.CINZA}Mas será diferente?{C.RESET}", delay=0.08)

    drama_pause(2)

    header_kali_v2()
    drama_pause(1)

    narracao("Você chegou ao fim da estrada.")
    narracao("Todas as escolhas levaram a este momento.")
    drama_pause(1)

    pensamento("O que fiz? O que ainda farei?")
    pensamento("O amanhecer sempre traz novas possibilidades.")

    mostrar_resumo_jornada(state)
    drama_pause(2)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter10(dados_jogador)

    try:
        cena_abertura(state)

        if state.saindo_para_menu:
            return state.to_dict()

        # Executar quests em sequência
        quests = [
            quest_1_reflection,
            quest_2_legacy_creation,
            quest_3_final_goodbye
        ]

        for quest in quests:
            if not quest(state):
                if state.saindo_para_menu:
                    return state.to_dict()
                break

        # Final do jogo
        drama_pause(3)
        limpa_tela()

        # Tela final baseada no final determinado
        if state.final_determinado == "redencao":
            print(f"\n{C.CIANO}{'╔' + '═'*58 + '╗'}{C.RESET}")
            print(f"{C.CIANO}{'║' + 'FINAL: A REDENÇÃO DO HACKER'.center(58) + '║'}{C.RESET}")
            print(f"{C.CIANO}{'╚' + '═'*58 + '╝'}{C.RESET}")
            print(f"\n{C.BRANCO}Você encontrou redenção através do código.{C.RESET}")
            print(f"{C.BRANCO}Não como destruidor, mas como curador.{C.RESET}")
            print(f"{C.BRANCO}O mundo é um lugar melhor por sua causa.{C.RESET}")

        elif state.final_determinado == "equilibrio":
            print(f"\n{C.AMARELO}{'╔' + '═'*58 + '╗'}{C.RESET}")
            print(f"{C.AMARELO}{'║' + 'FINAL: O EQUILÍBRIO DIGITAL'.center(58) + '║'}{C.RESET}")
            print(f"{C.AMARELO}{'╚' + '═'*58 + '╝'}{C.RESET}")
            print(f"\n{C.BRANCO}Você encontrou o equilíbrio perfeito.{C.RESET}")
            print(f"{C.BRANCO}Nem luz total, nem trevas absolutas.{C.RESET}")
            print(f"{C.BRANCO}O guardião das sombras.{C.RESET}")

        elif state.final_determinado == "sobrevivencia":
            print(f"\n{C.CINZA}{'╔' + '═'*58 + '╗'}{C.RESET}")
            print(f"{C.CINZA}{'║' + 'FINAL: A SOBREVIVÊNCIA DO FANTASMA'.center(58) + '║'}{C.RESET}")
            print(f"{C.CINZA}{'╚' + '═'*58 + '╝'}{C.RESET}")
            print(f"\n{C.BRANCO}Você sobreviveu. É o que importa.{C.RESET}")
            print(f"{C.BRANCO}As batalhas continuam, mas você está vivo.{C.RESET}")
            print(f"{C.BRANCO}O fantasma na máquina.{C.RESET}")

        else:  # trevas
            print(f"\n{C.VERMELHO}{'╔' + '═'*58 + '╗'}{C.RESET}")
            print(f"{C.VERMELHO}{'║' + 'FINAL: AS TREVAS DO PODER'.center(58) + '║'}{C.RESET}")
            print(f"{C.VERMELHO}{'╚' + '═'*58 + '╝'}{C.RESET}")
            print(f"\n{C.BRANCO}Você se tornou o que combatia.{C.RESET}")
            print(f"{C.BRANCO}O poder corrompe, e você foi corrompido.{C.RESET}")
            print(f"{C.BRANCO}O novo senhor das trevas.{C.RESET}")

        print(f"\n{C.AMARELO}{'═'*60}{C.RESET}")
        print(f"{C.AMARELO}{'OBRIGADO POR JOGAR ROOT EVOLUTION'.center(60)}{C.RESET}")
        print(f"{C.AMARELO}{'═'*60}{C.RESET}")

        print(f"\n{C.CINZA}Estatísticas Finais:{C.RESET}")
        print(f"{C.CINZA}- Score Total: {state.score}{C.RESET}")
        print(f"{C.CINZA}- Reputation: {state.reputation}{C.RESET}")
        print(f"{C.CINZA}- Aliados: {state.aliados}{C.RESET}")
        print(f"{C.CINZA}- Bitcoin: {state.bitcoin:.3f}{C.RESET}")

        print(f"\n{C.VERDE}>> Pressione ENTER para retornar ao menu principal <<{C.RESET}")
        input()

        state.capitulo_concluido = True
        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

