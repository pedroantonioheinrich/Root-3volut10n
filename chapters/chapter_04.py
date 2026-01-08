#!/usr/bin/env python3
"""
CHAPTER_04.PY - "O Abismo Olha de Volta"
Foco em narrativa, suspense e criptografia.
"""

import os
import sys
import time
import random
from datetime import datetime
import shutil

# Importação de Utils (Fallbacks se necessário)
try:
    from utils.terminal_kali import C, digitar, limpa_tela, header_kali_v2
except ImportError:
    class C:
        VERDE = '\033[92m'
        VERMELHO = '\033[91m'
        BRANCO = '\033[97m'
        CINZA = '\033[90m'
        CIANO = '\033[96m'
        AMARELO = '\033[93m'
        ROXO = '\033[95m'
        AZUL = '\033[94m'
        RESET = '\033[0m'
        NEGRITO = '\033[1m'
        IT = '\033[3m'
        
    def digitar(texto, delay=0.04, cor=C.BRANCO, fim="\n"):
        for char in texto:
            print(f"{cor}{char}{C.RESET}", end='', flush=True)
            time.sleep(delay)
        print(end=fim)

    def limpa_tela():
        os.system('cls' if os.name == 'nt' else 'clear')


# ========== ESTADO DO CAPÍTULO ==========

class GameStateChapter4:
    def __init__(self, dados_anteriores):
        self.player_name = dados_anteriores.get('player_name', 'Neo')
        self.codinome = dados_anteriores.get('codiname', 'GHOST')
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.0)
        self.privacy = dados_anteriores.get('privacy_level', 100)
        self.inventory = dados_anteriores.get('inventory', [])
        
        # Novo status temporário: Paranoia
        self.paranoia = 0 
        self.saindo_para_menu = False

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy,
            'inventory': self.inventory,
            'completed': getattr(self, 'capitulo_concluido', False),
            'saindo_para_menu': self.saindo_para_menu
        }
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy,
            'inventory': self.inventory,
            'paranoia_level': self.paranoia, # Persiste? Talvez para consequencias futuras
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }

# ========== UI AUXILIAR ==========

def narrar_pensamento(texto):
    """Exibe um pensamento interno do personagem (cinemático)"""
    print(f"\n{C.CINZA}{C.IT}( {texto} ){C.RESET}")
    time.sleep(2)

def narrar_ambiente(texto):
    """Exibe descrição do ambiente"""
    print(f"\n{C.AZUL}▒ {texto}{C.RESET}")
    time.sleep(1.5)

def prompt_hacker(codinome):
    return f"{C.VERMELHO}┌──({C.BRANCO}{codinome}@darkbox{C.VERMELHO})-[{C.BRANCO}~/encrypted{C.VERMELHO}]\n└─$ {C.RESET}"

def check_comandos_globais(cmd, state):
    if cmd.lower() == 'menu':
        state.saindo_para_menu = True
        return "MENU"
    if cmd.lower() in ['manual', 'help']:
        print(f"\n{C.AMARELO}[SISTEMA]: O manual está corrompido neste setor da memória.{C.RESET}") 
        # Bloqueio narrativo temporário ou poderia abrir normal. 
        # Vamos abrir normal para não frustrar, mas com aviso.
        try:
            from manual_hacking import ManualHacking
            man = ManualHacking()
            man.mostrar_menu()
        except:
            pass
        return "MANUAL"
    return None

# ========== CENA DO ARQUIVO CRIPTOGRAFADO ==========

def mostrar_arquivo_bloqueado():
    print(f"\n{C.VERMELHO}")
    print("╔════════════════════════════════════════╗")
    print("║     ARQUIVO: BLACK_BOX_OMEGA.enc       ║")
    print("║     STATUS:  CRIPTOGRAFIA AES-256      ║")
    print("║     ORIGEM:  DESCONHECIDA              ║")
    print("╚════════════════════════════════════════╝")
    print(f"{C.RESET}")
    print(f"{C.CINZA}01001011 00110010 11010010 ... [TRUNCATED]{C.RESET}\n")

def puzzle_descriptografia(state):
    """Quebra-cabeça principal do capítulo"""
    
    limpa_tela()
    narrar_ambiente("O arquivo que você extraiu pulsa na tela. É pesado. Sombrio.")
    narrar_pensamento("Eles disseram que era apenas um teste. Mas isso... isso parece um dossiê.")
    
    mostrar_arquivo_bloqueado()
    
    narrar_ambiente("Uma nota de texto anexada, quase corrompida, diz:")
    print(f"\n{C.AMARELO}'A chave... lembre-se de onde tudo começou. O ano da queda. A revolução silenciosa.'{C.RESET}")
    
    narrar_pensamento("Ano da queda... Revolução silenciosa... Preciso da chave numérica de 4 dígitos.")
    
    print(f"{C.CINZA}Dica: O arquivo termina com .enc (Encriptado). Geralmente usamos 'gpg'.{C.RESET}")
    print(f"{C.CINZA}{C.IT}   (Pensamento: GPG... GNU Privacy Guard. Se eu tiver a chave simétrica, o comando é 'gpg -d arquivo'. Mas qual é a senha? A mensagem dizia 'ano de fundação'.){C.RESET}\n")
    
    tentativas = 3
    
    while tentativas > 0:
        try:
            cmd = input(prompt_hacker(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return "MENU"
            
        status = check_comandos_globais(cmd, state)
        if status == "MENU": return "MENU"
        if status == "MANUAL": continue
        
        # PENSAMENTO NARRATIVO DINÂMICO
        if tentativas == 3:
             narrar_pensamento("Tente 'dec gpg <chave>'. Preciso pensar... O grande crash cibernético de 2077? Não, muito óbvio.")
        
        # COMANDO DE DECRIPTAR
        if cmd.startswith("dec gpg") or cmd.startswith("decrypt"):
            partes = cmd.split()
            if len(partes) < 3 and cmd.startswith("dec"): 
                print(f"{C.VERMELHO}Sintaxe: dec gpg <chave>{C.RESET}")
                continue
                
            chave = partes[-1]
            
            # A CHAVE É "2025" (Ano "atual" ou próximo, ou uma data lore específica. Vamos usar 2033 como lore do jogo Root Evolution)
            # Vamos estabelecer 2033 como o ano do "Grande Apagão" na lore.
            if chave == "2033":
                print(f"\n{C.VERDE}[!] CHAVE ACEITA. INICIANDO DECRIPTOGRAFIA...{C.RESET}")
                time.sleep(1)
                barra_progresso()
                return "SUCESSO"
            else:
                print(f"\n{C.VERMELHO}[!] ACESSO NEGADO. CHAVE INCORRETA.{C.RESET}")
                tentativas -= 1
                state.paranoia += 10
                narrar_pensamento(f"Merda. Errado. {tentativas} tentativas restantes antes do wipe automático.")
        
        # DICA EXTRA SE O JOGADOR ESTIVER PERDIDO
        elif "dica" in cmd or "hint" in cmd:
             print(f"\n{C.CINZA}System Note: O arquivo menciona 'Projeto Gênesis {C.VERDE}v20.33{C.CINZA}' nos metadados.{C.RESET}")
        
        else:
             print(f"{C.VERMELHO}Comando desconhecido. Use 'dec gpg <chave>'.{C.RESET}")

    return "FALHA"

def barra_progresso():
    print(f"\n{C.VERDE}", end="")
    for i in range(20):
        time.sleep(0.1)
        print("█", end="", flush=True)
    print(f" 100%{C.RESET}\n")

# ========== CENA PÓS-PUZZLE ==========

def ler_conteudo_arquivo(state):
    limpa_tela()
    print(f"\n{C.VERMELHO}>>> BLACK_BOX_OMEGA DECRYPTED <<<{C.RESET}\n")
    time.sleep(1)
    
    texto_secreto = [
        "ALVO: PROJETO HUMANIDADE 2.0",
        "STATUS: COMPROMETIDO",
        "AGENTE: [REDIGIDO]",
        "DATA: 12/12/2033",
        "",
        "OBSERVAÇÃO: A inserção do código Root na população foi um sucesso.",
        "Apenas 40% rejeitaram o implante neural.",
        "A 'Evolução' não é opcional. É mandatória.",
        "",
        "--- FIM DA TRANSMISSÃO ---"
    ]
    
    for linha in texto_secreto:
        print(f"{C.CINZA}{linha}{C.RESET}")
        time.sleep(1.5 if linha.strip() else 0.5)
    
    narrar_pensamento("Meu Deus... Não somos hackers lutando contra corporações.")
    narrar_pensamento("Somos cobaias.")
    
    time.sleep(3)
    
    # ESCOLHA DRAMÁTICA
    print(f"\n{C.AMARELO}[1] Copiar os dados e guardar segredo")
    print(f"[2] Deletar tudo e fingir que não viu (Ignorância é uma bênção){C.RESET}")
    
    while True:
        try:
            esc = input(f"\n{C.BRANCO}ESCOLHA > {C.RESET}")
        except:
             state.saindo_para_menu = True
             return "MENU"
             
        if esc == "1":
            narrar_pensamento("Vou guardar isso. Pode ser minha única garantia de vida.")
            state.inventory.append("arquivo_omega_encrypted")
            state.paranoia += 20
            break
        elif esc == "2":
            narrar_pensamento("Não... eu não vi nada. Não quero fazer parte disso.")
            print(f"\n{C.VERMELHO}Apagando dados...{C.RESET}")
            time.sleep(1)
            state.paranoia -= 10 # Menos paranoia, mas menos poder
            break

    return "FIM"

# ========== MAIN DO CAPÍTULO ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter4(dados_jogador)
    
    limpa_tela()
    print(f"\n\n{C.CINZA}{' ' * 30}CAPÍTULO 04{C.RESET}")
    print(f"{C.VERMELHO}{C.NEGRITO}{' ' * 20}O ABISMO OLHA DE VOLTA{C.RESET}\n")
    time.sleep(3)
    
    narrar_ambiente("O zumbido do seu servidor parece mais alto hoje.")
    narrar_pensamento("Desde que aceitei aquele trabalho... sinto que estou sendo observado.")
    
    # 1. PUZZLE
    resultado = puzzle_descriptografia(state)
    
    if resultado == "MENU":
        return state.to_dict()
    
    if resultado == "FALHA":
        print(f"\n{C.VERMELHO}FATAL ERROR: O arquivo se autodestruiu.{C.RESET}")
        time.sleep(2)
        print(f"{C.CINZA}Você perdeu uma informação vital.{C.RESET}")
        time.sleep(2)
        # Não dá game over, mas perde chance de lore
    
    # 2. REVELAÇÃO (Se sucesso)
    if resultado == "SUCESSO":
        res_leitura = ler_conteudo_arquivo(state)
        if res_leitura == "MENU":
            return state.to_dict()

    narrar_ambiente("A tela escurece. Uma nova mensagem surge no terminal.")
    print(f"\n{C.VERDE}UNKNOWN: 'Você viu demais, {state.codinome}.'{C.RESET}")
    time.sleep(2)
    
    # EFEITO FINAL DE CAPÍTULO
    limpa_tela()
    print(f"\n{C.VERDE}{'='*60}{C.RESET}")
    print(f"{C.VERDE}{'CAPÍTULO 4: OMENS - CONCLUÍDO':^60}{C.RESET}")
    print(f"{C.VERDE}{'='*60}{C.RESET}")
    print(f"\n{C.AMARELO}Recompensas:{C.RESET}")
    print(f" {C.VERDE}+ 0.05 BTC{C.RESET}")
    print(f" {C.VERDE}+ Acesso à Rede Omega{C.RESET}")
    print(f" {C.VERMELHO}+ Nível de Paranoia Crítico{C.RESET}")
    time.sleep(4)
    
    return state.to_dict()
