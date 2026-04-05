#!/usr/bin/env python3
"""
CHAPTER_14.PY - "O Novo Amanhecer"
Finais múltiplos baseados nas escolhas do jogador ao longo da jornada.

Foco: Resolução da história, reflexão, finais alternativos
Habilidade: Síntese de todas as habilidades aprendidas
Objetivos: Encerramento completo do jogo
"""

import os
import sys
import time
import random
import json

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
        self.current_chapter = 14
        self.score = dados_jogador.get('score', 0)
        self.escolha_moral = dados_jogador.get('escolha_moral', 'justica')
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.final_alternativo = self.determinar_final()

    def determinar_final(self):
        escolha = self.escolha_moral
        if escolha == 'justica':
            return 'redencao'
        elif escolha == 'misericordia':
            return 'harmonia'
        else:
            return 'caos'

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'score': self.score,
            'escolha_moral': self.escolha_moral,
            'final_alternativo': self.final_alternativo,
            'chapter_14_checkpoint': 'concluido',
            'capitulo_14_operacao_sucesso': True,
            'completed': True,
            'saindo_para_menu': False,
            'jogo_concluido': True
        }

def iniciar(dados_jogador, arquivo_save):
    game_state = GameState(dados_jogador)

    print(f"{C.NEGRITO}{C.ROXO}")
    print("═" * 80)
    print("            [ROOT EVOLUTION - CAPÍTULO 14: O NOVO AMANHECER]")
    print("                 Fim da Jornada | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")

    final = game_state.final_alternativo

    print("""
Sua jornada chega ao fim...""")
    print(f"Final alternativo: {final.upper()}")

    if final == 'redencao':
        print("""
A justiça prevaleceu. Você expôs a conspiração,""")
        print("mas aprendeu que o verdadeiro poder vem da mudança interna.")
        print("O mundo começa a se curar...")

    elif final == 'harmonia':
        print("""
A misericórdia triunfou. Você escolheu perdoar,""")
        print("e isso trouxe paz onde havia apenas conflito.")
        print("Um novo amanhecer surge...")

    else:
        print("""
A vingança consumiu tudo. O caos que você criou""")
        print("agora governa o mundo digital.")
        print("Não há redenção neste final...")

    print(f"\n{C.AMARELO}Pontuação Final: {game_state.score}{C.RESET}")
    print(f"{C.CIANO}Obrigado por jogar Root Evolution!{C.RESET}")

    time.sleep(5)
    print(f"{C.VERDE}✓ JOGO CONCLUÍDO! ✓{C.RESET}")
    game_state.capitulo_concluido = True
    game_state.operacao_sucesso = True

    return game_state.to_dict()