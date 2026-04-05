#!/usr/bin/env python3
"""
CHAPTER_11.PY - "Alianças Perigosas"
Formação de alianças com outros hackers. Coordenação de ataques.

Foco: Networking avançado, coordenação de equipe
Objetivos: 4 missões principais + formação de alianças
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
        self.current_chapter = 11
        self.score = dados_jogador.get('score', 0)
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.missoes = {
            'contatar_aliados': False,
            'coordenar_ataque': False,
            'divulgar_informacoes': False,
            'consolidar_vitoria': False
        }
        self.aliados_recrutados = 0

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'score': self.score,
            'chapter_11_checkpoint': 'concluido',
            'capitulo_11_operacao_sucesso': True,
            'completed': True,
            'saindo_para_menu': False,
            'missoes_capitulo_11': self.missoes,
            'aliados_recrutados': self.aliados_recrutados
        }

def iniciar(dados_jogador, arquivo_save):
    game_state = GameState(dados_jogador)

    print(f"{C.NEGRITO}{C.ROXO}")
    print("═" * 80)
    print("            [ROOT EVOLUTION - CAPÍTULO 11: ALIANÇAS PERIGOSAS]")
    print("                 Dark Web, 08:30 AM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")

    print("Formando alianças com outros hackers...")
    print("A batalha final se aproxima.")

    time.sleep(2)
    print(f"{C.VERDE}✓ Alianças formadas! Contra-ataque coordenado preparado.{C.RESET}")
    game_state.capitulo_concluido = True
    game_state.operacao_sucesso = True

    return game_state.to_dict()