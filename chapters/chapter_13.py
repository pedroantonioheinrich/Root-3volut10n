#!/usr/bin/env python3
"""
CHAPTER_13.PY - "Justiça ou Vingança"
Decisão final baseada na escolha moral do capítulo 8.

Foco: Consequências das escolhas, reflexão
Objetivos: 2 missões principais + encerramento
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
        self.current_chapter = 13
        self.score = dados_jogador.get('score', 0)
        self.escolha_moral = dados_jogador.get('escolha_moral', 'justica')
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.missoes = {
            'reflexao_final': False,
            'decisao_final': False
        }

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'score': self.score,
            'escolha_moral': self.escolha_moral,
            'chapter_13_checkpoint': 'concluido',
            'capitulo_13_operacao_sucesso': True,
            'completed': True,
            'saindo_para_menu': False,
            'missoes_capitulo_13': self.missoes
        }

def iniciar(dados_jogador, arquivo_save):
    game_state = GameState(dados_jogador)

    print(f"{C.NEGRITO}{C.ROXO}")
    print("═" * 80)
    print("           [ROOT EVOLUTION - CAPÍTULO 13: JUSTIÇA OU VINGANÇA]")
    print("                 Reflexão Final | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")

    escolha = game_state.escolha_moral
    print("""
Reflexão final sobre suas escolhas:""")
    print(f"Sua decisão de {escolha} moldou o mundo...")

    if escolha == 'justica':
        print("Justiça prevaleceu. O sistema foi exposto, mas permanece.")
    elif escolha == 'misericordia':
        print("Misericórdia triunfou. Mudanças reais aconteceram.")
    else:
        print("Vingança consumiu tudo. O que resta é cinzas.")

    time.sleep(3)
    print(f"{C.VERDE}✓ Jornada de reflexão concluída.{C.RESET}")
    game_state.capitulo_concluido = True
    game_state.operacao_sucesso = True

    return game_state.to_dict()