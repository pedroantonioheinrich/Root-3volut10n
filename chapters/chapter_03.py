#!/usr/bin/env python3
"""
CHAPTER_03.PY - "O Primeiro Chamado"
Introdução à economia (Bitcoin), privacidade e missões mais longas.
"""

import os
import sys
import time
import random
import base64
from datetime import datetime
import shutil

# Tentar importar utils
try:
    from utils.terminal_kali import C, digitar, fim_digitar, limpa_tela
except ImportError:
    # Fallback simplificado
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
        NEGRITO = '\033[1m'
        RESET = '\033[0m'
        KALI_AZUL = '\033[34m'
        IT = '\033[3m' # Italic
        
    def digitar(texto, delay=0.03, cor=C.BRANCO, fim="\n"):
        print(f"{cor}{texto}{C.RESET}", end=fim)
        time.sleep(len(texto) * delay)

    def limpa_tela():
        os.system('cls' if os.name == 'nt' else 'clear')


# ========== ESTADO DO CAPÍTULO ==========

class GameStateChapter3:
    def __init__(self, dados_anteriores):
        self.player_name = dados_anteriores.get('player_name', 'Neo')
        self.codinome = dados_anteriores.get('codiname', 'SHADOW_00')
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0)
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        
        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False
        
    def verificar_game_over(self):
        if self.privacy_level <= 0:
            self.game_over = True
            return True
        return False

    def registrar_falha(self, penalidade=10):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        return self.verificar_game_over()

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 5
        # Recupera um pouco de privacidade no sucesso
        self.privacy_level = min(100, self.privacy_level + 5)

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'reputation': self.reputation,
            'bitcoin_wallet': self.bitcoin,
            'inventory': self.inventory,
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu,
            'completed': (self.bitcoin > 0.01) and not self.saindo_para_menu # Simplificação de sucesso
        }

# ========== INTERFACE E HUD ==========

def mostrar_hud(state):
    """Mostra o HUD com status do jogador"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass
    
    # Barra Superior
    print(f"{C.CINZA}┌{'─' * (largura-2)}┐{C.RESET}") 
    status_msg = f" {C.VERDE}🕵 {state.codinome}{C.RESET} | {C.AMARELO}₿ {state.bitcoin:.6f}{C.RESET} | {C.ROXO}🛡️ PRIVACIDADE: {state.privacy_level}%{C.RESET}"
    
    # Simple print centered logic might fail with color codes length, so simple print for now
    print(f"│ {status_msg:<95} │")
    print(f"{C.CINZA}└{'─' * (largura-2)}┘{C.RESET}")
    print(f"{C.CINZA}[ ? ] Digite 'manual' p/ ajuda ou 'menu' p/ salvar e sair.{C.RESET}\n")

def prompt_kali(codinome, path="~"):
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}{path}{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

def narracao(texto):
    print(f"\n{C.BRANCO}{texto}{C.RESET}")
    time.sleep(1.5)

def missao_print(titulo, objetivo):
    print(f"\n{C.AMARELO}╔════ MISSÃO ATUAL: {titulo} ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: {objetivo:<46} ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*60}╝{C.RESET}\n")

def check_comandos_globais(cmd, state, arquivo_save):
    """Verifica comandos globais como 'menu' e 'manual'"""
    if cmd.lower() == 'menu':
        print(f"\n{C.AMARELO}[*] Salvando checkpoint e retornando ao menu...{C.RESET}")
        state.saindo_para_menu = True
        return "MENU"
        
    if cmd.lower() in ['manual', 'help', '?']:
        try:
            from manual_hacking import ManualHacking
            man = ManualHacking()
            man.mostrar_menu()
        except ImportError:
             print(f"{C.CINZA}Manual não disponível.{C.RESET}")
        return "MANUAL"
    
    return None

# ========== ANIMAÇÃO INTRO ==========

def animacao_boot_hacker():
    limpa_tela()
    
    # Efeito Matrix / Boot
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"
    green = C.VERDE
    reset = C.RESET
    
    print(f"{green}INITIALIZING SECURE CONNECTION...{reset}")
    time.sleep(1)
    
    # Scrolling lines
    for _ in range(15):
        line = "".join(random.choice(chars) for _ in range(shutil.get_terminal_size().columns))
        print(f"{C.CINZA}{line}{reset}")
        time.sleep(0.05)
        
    print(f"\n{C.VERDE}[+] BYPASSING FIREWALL... SUCCESS{reset}")
    time.sleep(0.5)
    print(f"{C.VERDE}[+] ESTABLISHING ENCRYPTED TUNNEL... SUCCESS{reset}")
    time.sleep(0.5)
    print(f"{C.VERDE}[+] MASKING IP ADDRESS... SUCCESS{reset}")
    time.sleep(0.8)
    
    limpa_tela()
    
    # Banner grande
    banner = [
        r"   _____  _    _  _____  ______  ______ ",
        r"  / ____|| |  | ||_   _||  ____||  ____|",
        r" | (___  | |__| |  | |  | |__   | |__   ",
        r"  \___ \ |  __  |  | |  |  __|  |  __|  ",
        r"  ____) || |  | | _| |_ | |     | |     ",
        r" |_____/ |_|  |_||_____||_|     |_|     ",
    ]
    
    for line in banner:
        print(f"{C.VERDE}{line.center(shutil.get_terminal_size().columns)}{reset}")
        time.sleep(0.1)
        
    print(f"\n{C.BRANCO}WELCOME TO THE UNDERGROUND, INITIATE.{reset}\n")
    time.sleep(2)

# ========== GAME OVER ==========

def tela_game_over_policia():
    limpa_tela()
    print(f"\n\n{C.VERMELHO}{C.NEGRITO}ALERTA CRÍTICO: PRIVACIDADE 0%{C.RESET}")
    time.sleep(1)
    digitar("Rastreamento confirmado.", cor=C.VERMELHO)
    digitar("Unidade Tática da Polícia Federal em deslocamento.", cor=C.VERMELHO)
    time.sleep(2)
    print(f"\n{C.BRANCO}Você ouve as sirenes. Não há mais tempo.{C.RESET}")
    time.sleep(2)
    print(f"\n{C.ROXO}GAME OVER{C.RESET}")
    time.sleep(3)

# ========== MISSÕES (QUESTS) ==========

def quest_1_decodificar(state, arquivo_save):
    """Quest 1: Decodificar mensagem de recrutamento"""
    mostrar_hud(state)
    missao_print("O CONVITE", "Decodificar a mensagem recebida")
    
    narracao("Você recebeu uma string estranha no chat criptografado.")
    msg_base64 = "U3FhIHBhcmEgbyBzZXJ2aWRvciAxOTIuMTY4LjU1LjEwIGUgZW5jb250cmUgYSBwb3J0YSBhYmVydGEu"
    
    print(f"{C.CINZA}MENSAGEM: {msg_base64}{C.RESET}")
    print(f"{C.CIANO}Dica: Parece codificação Base64. Use 'echo \"...\" | base64 -d'{C.RESET}\n")
    
    # PENSAMENTO DRAMÁTICO / DICA
    print(f"{C.CINZA}{C.IT}   (Pensamento: Minhas mãos suam... Ok, calma. Essa string termina com '='. Isso é a assinatura clássica de Base64. Preciso decodificar isso agora.){C.RESET}\n")
    
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return "MENU"
            
        status = check_comandos_globais(cmd, state, arquivo_save)
        if status == "MENU": return "MENU"
        if status == "MANUAL": continue
            
        # Lógica de validação mais flexível
        valid_cmd_parts = ["base64", "-d"]
        
        # Se o usuário digitar o comando correto de decode
        if all(part in cmd for part in valid_cmd_parts) or ("echo" in cmd and "| base64" in cmd and "-d" in cmd):
            print(f"\n{C.VERDE}Decodificado: 'Siga para o servidor 192.168.55.10 e encontre a porta aberta.'{C.RESET}")
            time.sleep(2)
            state.registrar_sucesso(10)
            return "SUCESSO"
        
        # Feedback parcial
        elif "base64" in cmd:
             print(f"{C.AMARELO}Você está no caminho certo. Lembre-se da flag para 'decode' (-d).{C.RESET}")
        elif "echo" in cmd and "|" not in cmd:
             print(f"{C.AMARELO}Você precisa passar a saída do echo para o base64 usando um pipe (|).{C.RESET}")
             
        else:
            print(f"{C.VERMELHO}Comando incorreto. Tente: echo 'mensagem' | base64 -d{C.RESET}")
            if state.registrar_falha(2): return "FALHA"

def quest_2_scanning(state, arquivo_save):
    """Quest 2: Escanear servidor"""
    mostrar_hud(state)
    missao_print("RECONHECIMENTO", "Escanear 192.168.55.10")
    
    print(f"{C.CIANO}Dica: Use o 'nmap' para descobrir portas abertas.{C.RESET}\n")
    target = "192.168.55.10"
    
    # PENSAMENTO DRAMÁTICO / DICA
    print(f"{C.CINZA}{C.IT}   (Pensamento: Estou dentro da rede. Mas onde? Preciso mapear o terreno. O comando 'nmap' é meus olhos aqui. Vamos ver o que está rodando no 192.168.55.10){C.RESET}\n")
    
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return "MENU"
            
        status = check_comandos_globais(cmd, state, arquivo_save)
        if status == "MENU": return "MENU"
        if status == "MANUAL": continue

        if cmd.startswith("nmap") and target in cmd:
            print(f"\n{C.CINZA}Starting Nmap 7.94...{C.RESET}")
            time.sleep(1.5)
            print(f"Nmap scan report for {target}")
            print(f"Host is up (0.0023s latency).")
            print(f"{C.VERDE}PORT     STATE SERVICE{C.RESET}")
            print(f"{C.VERDE}22/tcp   open  ssh{C.RESET}")
            print(f"{C.VERDE}80/tcp   open  http{C.RESET}")
            print(f"{C.VERDE}3306/tcp open  mysql{C.RESET}")
            time.sleep(2)
            state.registrar_sucesso(15)
            return "SUCESSO"
        else:
            print(f"{C.VERMELHO}Comando inválido. Use 'nmap <ip>'{C.RESET}")
            if state.registrar_falha(2): return "FALHA"

def quest_3_sql_injection(state, arquivo_save):
    """Quest 3: SQL Injection para login"""
    mostrar_hud(state)
    missao_print("INTRUSÃO", "Bypass de login no painel administrativo")
    
    narracao("O serviço HTTP na porta 80 tem um painel de login vulnerável.")
    print(f"{C.CINZA}URL: http://192.168.55.10/admin{C.RESET}")
    print(f"{C.CIANO}Dica: Tente uma injeção SQL clássica no campo de usuário.{C.RESET}\n")
    
    # PENSAMENTO DRAMÁTICO / DICA
    print(f"{C.CINZA}{C.IT}   (Pensamento: Um formulário de login... Tão anos 90. Se eles não sanitizaram a entrada, um simples ' OR '1'='1 pode enganar o banco de dados e me deixar entrar como admin.){C.RESET}\n")
    
    while True:
        try:
            user = input(f"{C.BRANCO}Username: {C.RESET}").strip()
            # User input handling for menu/manual inside username field
            status = check_comandos_globais(user, state, arquivo_save)
            if status == "MENU": return "MENU"
            if status == "MANUAL": continue
            
            password = input(f"{C.BRANCO}Password: {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return "MENU"
        
        # Simplificação de checks de SQLi
        if "' OR '1'='1" in user or "' or '1'='1" in user or '" OR "1"="1' in user:
            print(f"\n{C.VERDE}Login Bypass Successful! Welcome Administrator.{C.RESET}")
            time.sleep(1)
            state.registrar_sucesso(20)
            return "SUCESSO"
        else:
            print(f"{C.VERMELHO}Login Failed. Invalid credentials.{C.RESET}")
            if state.registrar_falha(5): return "FALHA"

def quest_4_privilege_escalation(state, arquivo_save):
    """Quest 4: Escalar privilégios e achar a flag"""
    mostrar_hud(state)
    missao_print("ESCALADA", "Encontrar a flag de root")
    
    narracao("Você está no sistema via shell web. Precisa virar root.")
    print(f"{C.CINZA}Você encontrou um binário SUID estranho: '/usr/bin/system_check'{C.RESET}")
    print(f"{C.CIANO}Dica: Execute o binário para tentar explorar.{C.RESET}\n")
    
    # PENSAMENTO DRAMÁTICO / DICA
    print(f"{C.CINZA}{C.IT}   (Pensamento: Eu sou apenas 'www-data'. Aquele arquivo 'system_check' roda como root.){C.RESET}")
    print(f"{C.CINZA}{C.IT}   (Dica de Hacker: No Linux, para executar um programa na pasta atual, usamos './'. Então devo digitar './system_check'){C.RESET}\n")
    
    passos = 0
    while passos < 2:
        try:
            cmd = input(prompt_kali(state.codinome, "www-data@srv")).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return "MENU"
            
        status = check_comandos_globais(cmd, state, arquivo_save)
        if status == "MENU": return "MENU"
        if status == "MANUAL": continue
             
        if passos == 0:
            if "./system_check" in cmd or "/usr/bin/system_check" in cmd:
                print(f"{C.CINZA}Executando diagnóstico de sistema...{C.RESET}")
                time.sleep(1)
                print(f"{C.VERDE}Buffer Overflow detectado! Shell spawnada como #root{C.RESET}")
                
                print(f"\n{C.AMARELO}>>> ACESSO ROOT CONCEDIDO <<<{C.RESET}")
                print(f"{C.CINZA}Agora você tem controle total. Tente:{C.RESET}")
                print(f"1. {C.BRANCO}whoami{C.RESET} (Para confirmar que é root)")
                print(f"2. {C.BRANCO}ls{C.RESET}     (Para ver os arquivos)")
                print(f"3. {C.BRANCO}cat <arquivo>{C.RESET} (Para ler o conteúdo da flag)")
                
                passos = 1
            else:
                print(f"{C.VERMELHO}Permissão negada ou comando irrelevante.{C.RESET}")
                if state.registrar_falha(2): return "FALHA"
        elif passos == 1:
            if cmd == "whoami":
                print("root")
            elif "cat" in cmd and "flag" in cmd:
                print(f"\n{C.VERDE}FLAG ENCONTRADA: {{fsociety_recruitment_complete}}{C.RESET}")
                state.registrar_sucesso(25)
                return "SUCESSO"
            elif cmd == "ls":
                print("flag.txt  logs  backup")
            else:
                print(f"{C.AMARELO}Você é root. Ache a flag.{C.RESET}")

def quest_5_limpeza(state, arquivo_save):
    """Quest 5: Apagar logs"""
    mostrar_hud(state)
    missao_print("RASTRO ZERO", "Apagar os logs de acesso")
    
    print(f"{C.CIANO}Dica: Os logs geralmente ficam em /var/log. Apague 'auth.log'.{C.RESET}\n")
    
    # PENSAMENTO DRAMÁTICO / DICA
    print(f"{C.CINZA}{C.IT}   (Pensamento: Quase lá. O arquivo 'auth.log' em /var/log registrou tudo.){C.RESET}")
    print(f"{C.CINZA}{C.IT}   (Dica de Hacker: Use o comando 'rm' para remover arquivos. Exemplo: 'rm /caminho/do/arquivo'){C.RESET}\n")
    
    while True:
        try:
            cmd = input(prompt_kali(state.codinome, "root@srv")).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return "MENU"
            
        status = check_comandos_globais(cmd, state, arquivo_save)
        if status == "MENU": return "MENU"
        if status == "MANUAL": continue
             
        if "rm" in cmd and "auth.log" in cmd:
            print(f"\n{C.VERDE}Logs removidos. Nenhum rastro deixado.{C.RESET}")
            state.registrar_sucesso(15, btc_reward=0.015) 
            return "SUCESSO"
        elif cmd == "ls /var/log":
            print("auth.log  syslog  kern.log")
        else:
             print(f"{C.VERMELHO}O arquivo de log ainda está lá.{C.RESET}")
             if state.registrar_falha(3): return "FALHA"

# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter3(dados_jogador)
    
    mostrar_hud(state)
    
    # Introdução Tutorial apenas se não estiver carregando checkpoint (simplificação)
    if not state.saindo_para_menu and 'current_quest_index' not in dados_jogador.get('completed_chapters', []): 
        # Mostra animação apenas se for início "real" (ou aproximado)
        animacao_boot_hacker()
    
    if not state.saindo_para_menu:
        narracao(f"{C.ROXO}V0id_Walker:{C.RESET} 'Bem-vindo à realidade, {state.codinome}.'")
        narracao("A partir de agora, suas ações têm custos.")
        
        print(f"\n{C.AMARELO}>>> TUTORIAL DE ECONOMIA E SOBREVIVÊNCIA <<<{C.RESET}")
        print(f"1. {C.AMARELO}BITCOIN (₿){C.RESET}: Use para comprar ferramentas no Mercado Negro.")
        print(f"2. {C.ROXO}PRIVACIDADE{C.RESET}: Representa seu anonimato. Se chegar a 0%, {C.VERMELHO}GAME OVER{C.RESET}.")
        print(f"3. {C.BRANCO}MANUAL{C.RESET}: Digite 'manual' p/ ajuda ou 'menu' p/ salvar/sair.\n")
        
        try:
            input(f"{C.CINZA}[ Pressione ENTER para aceitar o contrato ]{C.RESET}")
        except:
             pass
    
    # Executar Quests
    quests = [
        quest_1_decodificar,
        quest_2_scanning,
        quest_3_sql_injection,
        quest_4_privilege_escalation,
        quest_5_limpeza
    ]
    
    for quest in quests:
        resultado = quest(state, arquivo_save)
        
        if resultado == "MENU":
            return state.to_dict()
            
        if resultado == "FALHA":
            tela_game_over_policia()
            return None 
            
        time.sleep(1)
        
    limpa_tela()
    print(f"{C.VERDE}>>> CAPÍTULO 3 CONCLUÍDO <<<{C.RESET}")
    print(f"Recompensa recebida: {C.AMARELO}0.015 BTC{C.RESET}")
    time.sleep(3)
    
    return state.to_dict()

if __name__ == "__main__":
    # Teste rápido solo
    dados = {
        'player_name': 'Tester', 
        'codiname': 'TEST_USER',
        'privacy_level': 100,
        'bitcoin_wallet': 0.005
    }
    iniciar(dados)
