#!/usr/bin/env python3
"""
TERMINAL_KALI.PY - Sistema de Terminal Kali Linux para RoOt 3voluti0n
Versão corrigida com função digitar e compatibilidade completa
"""

import os
import sys
import time
import random
import readline
import subprocess
from datetime import datetime

# ========== PALETA DE CORES (importada de utils.colors) ==========
from utils.colors import C, Cores

# Constantes de status para compatibilidade
SUCESSO = C.KALI_VERDE + C.NEGRITO
ERRO = C.KALI_VERMELHO + C.NEGRITO
ALERTA = C.KALI_AMARELO + C.NEGRITO
INFO = C.KALI_CIANO + C.NEGRITO
DESTAQUE = C.KALI_ROXO + C.NEGRITO

# ========== FUNÇÃO DIGITAR PARA COMPATIBILIDADE ==========
def digitar(texto, delay=None, velocidade=None, cor=None, fim='\n', pausa_final=None, efeito_sonoro=False):
    """Compatível: aceita `delay` ou `velocidade` e `fim` (final string).

    Uso comum:
      digitar(texto, delay=0.02, cor=C.KALI_VERDE)
      digitar(texto, velocidade=0.02, cor=C.KALI_VERDE)

    Args:
        texto: str - texto a ser exibido
        delay / velocidade: float - tempo entre caracteres (segundos)
        cor: str - código ANSI da cor
        fim: str - caractere(s) ao final (padrão '\n')
        pausa_final: float - pausa após a impressão (opcional)
        efeito_sonoro: bool - ativa pequenos glitches durante digitação
    """
    # Resolver parâmetros compatíveis
    if delay is None:
        delay = velocidade if velocidade is not None else 0.03
    if cor is None:
        cor = C.KALI_BRANCO
    if pausa_final is None:
        pausa_final = 0.5

    sys.stdout.write(cor)

    for caractere in texto:
        sys.stdout.write(caractere)
        sys.stdout.flush()

        # Efeito de teclado aleatório (opcional)
        if efeito_sonoro and caractere not in [' ', '\n', '\t']:
            if random.random() > 0.7:
                time.sleep(delay * 0.5)
                sys.stdout.write('\b')
                time.sleep(delay * 0.3)
                sys.stdout.write(caractere)
                sys.stdout.flush()

        time.sleep(delay)

    # Reset de cor e fim de linha compatível
    sys.stdout.write(C.RESET + fim)
    sys.stdout.flush()
    time.sleep(pausa_final)

# ========== CONFIGURAÇÃO DO TERMINAL ==========
class TerminalKali:
    """
    Terminal Kali Linux simulado para o jogo
    """
    
    def __init__(self, username="root", hostname="kali"):
        """Inicializa o terminal Kali"""
        self.username = username
        self.hostname = hostname
        self.cwd = "~"
        self.historico = []
        self.max_historico = 100
        self.effects_enabled = True
        self.sound_enabled = False
        
        # Configurar readline para histórico
        readline.set_history_length(self.max_historico)
        
        # Comandos simulados
        self.commands_simulated = {
            'ls': self._cmd_ls,
            'cd': self._cmd_cd,
            'pwd': self._cmd_pwd,
            'whoami': self._cmd_whoami,
            'clear': self._cmd_clear,
            'cat': self._cmd_cat,
            'nano': self._cmd_nano,
            'ssh': self._cmd_ssh,
            'scp': self._cmd_scp,
            'nmap': self._cmd_nmap,
            'sqlmap': self._cmd_sqlmap,
            'ifconfig': self._cmd_ifconfig,
            'ping': self._cmd_ping,
            'help': self._cmd_help,
            'manual': self._cmd_manual,
            'history': self._cmd_history,
            'exit': self._cmd_exit,
        }
        
        # Sistema de arquivos simulado
        self.filesystem = self._criar_filesystem_simulado()
    
    # ========== SISTEMA DE ARQUIVOS SIMULADO ==========
    def _criar_filesystem_simulado(self):
        """Cria um sistema de arquivos simulado para o jogo"""
        return {
            '~': {
                '.hidden': '[arquivo oculto]',
                'Desktop': {
                    'hacking_tools.txt': 'Ferramentas para download...',
                    'notes.md': '# Anotações de hacking\n\n- SQLi em login.php\n- SSH admin@192.168.1.1\n- Hash: 5f4dcc3b5aa765d61d8327deb882cf99'
                },
                'Documents': {
                    'research.pdf': 'Pesquisa sobre vulnerabilidades web',
                    'passwords.txt': 'admin:password123\nroot:toor\nuser:123456'
                },
                'Downloads': {
                    'metasploit.deb': '[pacote Metasploit]',
                    'nmap-7.91.tar.gz': '[scanner de rede]'
                },
                'Private': {
                    '.conversa_hotel_nobile.pdf': '[ARQUIVO SENSÍVEL] Conversa comprometedora',
                    '.fotos_reserva_dupla.zip': '[ARQUIVO SENSÍVEL] Fotos da reserva',
                    'evidences': {
                        'email_traicao.txt': 'From: juliana@email.com\nTo: ricardo@email.com\nSubject: Hotel Nobile...',
                        'bank_transfer.pdf': 'Transferência bancária suspeita'
                    }
                },
                'scripts': {
                    'exploit.py': '#!/usr/bin/python3\n# SQL Injection exploit\nimport requests',
                    'port_scanner.sh': '#!/bin/bash\n# Simple port scanner\nfor port in {1..1000}; do'
                }
            }
        }
    
    # ========== INTERFACE DO TERMINAL ==========
    def prompt(self):
        """Retorna o prompt do Kali Linux"""
        # Cores baseadas no usuário
        user_color = C.KALI_VERDE if self.username == "root" else C.KALI_AZUL
        host_color = C.KALI_ROXO
        
        # Diretório atual formatado
        dir_display = self.cwd if len(self.cwd) < 30 else "..." + self.cwd[-27:]
        
        # Prompt de duas linhas estilo Kali
        prompt = f"{C.KALI_AZUL}┌──({user_color}{self.username}{C.KALI_AZUL}㉿{host_color}{self.hostname}{C.KALI_AZUL})-[{C.KALI_BRANCO}{dir_display}{C.KALI_AZUL}]\n{C.KALI_AZUL}└─{C.KALI_ROXO}#{C.RESET} "
        
        return prompt
    
    def prompt_compacto(self):
        """Prompt compacto de uma linha"""
        user_color = C.KALI_VERDE if self.username == "root" else C.KALI_AZUL
        return f"{C.KALI_AZUL}[{user_color}{self.username}{C.KALI_AZUL}@{C.KALI_ROXO}{self.hostname}{C.KALI_AZUL}]{C.RESET} {C.KALI_ROXO}#{C.RESET} "
    
    def prompt_emergencia(self):
        """Prompt para situações de emergência"""
        return f"{C.KALI_VERMELHO}{C.NEGRITO}[{self.username}@EMERGENCY]{C.RESET} {C.KALI_VERMELHO}#{C.RESET} "
    
    # ========== EFEITOS VISUAIS ==========
    def digitar(self, texto, delay=0.03, cor=C.KALI_BRANCO, efeito_teclado=True):
        """Efeito de digitação com sons de teclado opcionais"""
        sys.stdout.write(cor)
        
        for i, char in enumerate(texto):
            sys.stdout.write(char)
            sys.stdout.flush()
            
            # Efeito de teclado aleatório
            if efeito_teclado and self.effects_enabled and char not in ' \t\n':
                if random.random() > 0.7:
                    # Pequeno glitch
                    time.sleep(delay * 0.5)
                    sys.stdout.write('\b')
                    time.sleep(delay * 0.3)
                    sys.stdout.write(char)
                    sys.stdout.flush()
            
            time.sleep(delay)
        
        sys.stdout.write(C.RESET)
    
    def digitar_linha(self, texto, delay=0.03, cor=C.KALI_BRANCO):
        """Digita uma linha completa"""
        self.digitar(texto, delay, cor)
        print()
    
    def efeito_glitch(self, texto, repeticoes=2, duracao=0.1):
        """Efeito de glitch hacker"""
        for _ in range(repeticoes):
            # Texto glitchado
            chars_glitch = "01█▓▒░║╔╗╚╝═╬╩╦╠╣╞╡│┤╢╟╨╧╥╙╘╒╓╫╪┘┌"
            glitch_text = ''.join(
                random.choice(chars_glitch) if random.random() > 0.3 else char 
                for char in texto
            )
            
            sys.stdout.write(f"\r{C.KALI_VERMELHO}{glitch_text}{C.RESET}")
            sys.stdout.flush()
            time.sleep(duracao * 0.5)
            
            sys.stdout.write(f"\r{C.KALI_CIANO}{texto}{C.RESET}")
            sys.stdout.flush()
            time.sleep(duracao * 0.3)
        
        sys.stdout.write(f"\r{texto}")
        sys.stdout.flush()
    
    def animacao_comando(self, comando, delay=0.02):
        """Anima um comando sendo digitado"""
        self.digitar(f"{C.KALI_BRANCO}$ {C.KALI_VERDE}{comando}{C.RESET}", delay)
        print()
    
    def mostrar_saida(self, texto, tipo="normal"):
        """Mostra saída de comando formatada"""
        if tipo == "sucesso":
            print(f"{C.KALI_VERDE}[+] {texto}{C.RESET}")
        elif tipo == "erro":
            print(f"{C.KALI_VERMELHO}[-] {texto}{C.RESET}")
        elif tipo == "alerta":
            print(f"{C.KALI_AMARELO}[!] {texto}{C.RESET}")
        elif tipo == "info":
            print(f"{C.KALI_CIANO}[*] {texto}{C.RESET}")
        else:
            print(f"{C.KALI_CINZA}{texto}{C.RESET}")
    
    # ========== COMANDOS SIMULADOS ==========
    def _cmd_ls(self, args):
        """Simula o comando ls"""
        # Se nenhum argumento, listar diretório atual (~)
        raw = args[0] if args else "."
        if raw in ['.', './']:
            path = '~'
        else:
            path = self._resolve_path(raw)

        # Usar _find_file para navegar no filesystem simulado
        contents = self._find_file(path)

        if contents is None:
            self.mostrar_saida(f"ls: cannot access '{args[0] if args else '.'}': No such file or directory", "erro")
            return True

        if isinstance(contents, dict):
            # Listar diretório
            items = sorted(contents.keys())
            if not items:
                return True

            # Formatar em colunas
            cols = 3
            max_len = max(len(i) for i in items) + 2

            for i in range(0, len(items), cols):
                linha = ""
                for j in range(cols):
                    if i + j < len(items):
                        item = items[i + j]
                        val = contents[item]
                        cor = C.KALI_CINZA if item.startswith('.') else (C.KALI_AZUL if isinstance(val, dict) else C.KALI_BRANCO)
                        display = f"{item}/" if isinstance(val, dict) else item
                        linha += f"{cor}{display:<{max_len}}{C.RESET}"
                print(linha)
        else:
            # Arquivo - imprimir conteúdo
            print(f"{C.KALI_BRANCO}{contents}{C.RESET}")
        
        return True
    
    def _cmd_cd(self, args):
        """Simula o comando cd"""
        if not args:
            self.cwd = "~"
        else:
            path = args[0]
            if path == "..":
                if self.cwd != "~":
                    self.cwd = "/".join(self.cwd.split("/")[:-1]) or "~"
            elif path.startswith("/") or path.startswith("~"):
                self.cwd = path
            else:
                self.cwd = f"{self.cwd}/{path}" if self.cwd != "~" else f"~/{path}"
        
        # Normalizar caminho: apenas colapsar barras duplicadas
        self.cwd = self.cwd.replace("//", "/").rstrip("/")
        if not self.cwd:
            self.cwd = "~"
        
        return True
    
    def _cmd_pwd(self, args):
        """Simula o comando pwd"""
        print(f"{C.KALI_BRANCO}{self.cwd}{C.RESET}")
        return True
    
    def _cmd_whoami(self, args):
        """Simula o comando whoami"""
        print(f"{C.KALI_VERDE}{self.username}{C.RESET}")
        return True
    
    def _cmd_clear(self, args):
        """Simula o comando clear"""
        os.system('cls' if os.name == 'nt' else 'clear')
        return True
    
    def _cmd_cat(self, args):
        """Simula o comando cat"""
        if not args:
            self.mostrar_saida("cat: missing file operand", "erro")
            return False
        
        filename = args[0]
        path = self._resolve_path(filename)
        
        # Buscar arquivo no sistema simulado
        file_content = self._find_file(path)
        
        if file_content:
            if isinstance(file_content, dict):
                self.mostrar_saida(f"cat: {filename}: Is a directory", "erro")
            else:
                print(f"{C.KALI_BRANCO}{file_content}{C.RESET}")
        else:
            self.mostrar_saida(f"cat: {filename}: No such file or directory", "erro")
        
        return True
    
    def _cmd_nano(self, args):
        """Simula o editor nano"""
        if not args:
            self.mostrar_saida("No file specified", "erro")
            return False
        
        filename = args[0]
        print(f"{C.KALI_CIANO}GNU nano 5.4 - Editing: {filename}{C.RESET}")
        print(f"{C.KALI_CINZA}[ Press Ctrl+X to exit ]{C.RESET}")
        
        # Simular edição
        time.sleep(1)
        print(f"\n{C.KALI_VERDE}File saved successfully.{C.RESET}")
        
        return True
    
    def _cmd_ssh(self, args):
        """Simula conexão SSH"""
        if not args:
            self.mostrar_saida("ssh: missing hostname", "erro")
            return False
        
        target = args[0]
        print(f"{C.KALI_CIANO}Connecting to {target} via SSH...{C.RESET}")
        time.sleep(1)
        
        if "@backup-cloud" in target or "@192.168" in target:
            print(f"{C.KALI_VERDE}Connected to {target}{C.RESET}")
            print(f"{C.KALI_CINZA}Welcome to Ubuntu 20.04 LTS{C.RESET}")
            return True
        else:
            print(f"{C.KALI_VERMELHO}Connection refused{C.RESET}")
            return False
    
    def _cmd_scp(self, args):
        """Simula cópia via SCP"""
        if len(args) < 2:
            self.mostrar_saida("scp: missing file or destination", "erro")
            return False

        source = args[0]
        dest = args[1]

        # Validar existência do arquivo fonte no filesystem simulado
        src_path = self._resolve_path(source)
        src_val = self._find_file(src_path)
        if src_val is None:
            self.mostrar_saida(f"scp: {source}: No such file or directory", "erro")
            return False

        print(f"{C.KALI_CIANO}Copying {source} to {dest}...{C.RESET}")
        time.sleep(0.3)

        # Efeito de progresso
        for i in range(10):
            progress = "█" * (i + 1) + "░" * (9 - i)
            sys.stdout.write(f"\r[{progress}] {((i+1)*10)}%")
            sys.stdout.flush()
            time.sleep(0.08)

        print(f"\n{C.KALI_VERDE}Transfer completed successfully.{C.RESET}")
        return True
    
    def _cmd_nmap(self, args):
        """Simula varredura com Nmap"""
        if not args:
            self.mostrar_saida("nmap: missing target", "erro")
            return False
        
        target = args[0]
        print(f"{C.KALI_CIANO}Starting Nmap 7.91 scan on {target}{C.RESET}")
        time.sleep(0.5)
        
        # Resultado simulado
        print(f"{C.KALI_BRANCO}Nmap scan report for {target}{C.RESET}")
        print(f"{C.KALI_CINZA}Host is up (0.045s latency).{C.RESET}")
        print(f"{C.KALI_BRANCO}PORT     STATE SERVICE     VERSION{C.RESET}")
        print(f"{C.KALI_VERDE}22/tcp   open  ssh         OpenSSH 8.2p1{C.RESET}")
        print(f"{C.KALI_VERDE}80/tcp   open  http        Apache 2.4.41{C.RESET}")
        print(f"{C.KALI_AMARELO}443/tcp  open  ssl/http    Apache 2.4.41{C.RESET}")
        print(f"{C.KALI_VERMELHO}3306/tcp open  mysql       MySQL 8.0.23{C.RESET}")
        
        return True
    
    def _cmd_sqlmap(self, args):
        """Simula SQLMap"""
        print(f"{C.KALI_CIANO}Starting sqlmap 1.5.11{C.RESET}")
        time.sleep(0.5)
        
        if "--help" in args or "-h" in args:
            print(f"{C.KALI_BRANCO}Usage: sqlmap [options]{C.RESET}")
            print(f"{C.KALI_CINZA}  -u URL                    Target URL{C.RESET}")
            print(f"{C.KALI_CINZA}  --dbs                    Enumerate databases{C.RESET}")
            print(f"{C.KALI_CINZA}  --tables                 Enumerate tables{C.RESET}")
            print(f"{C.KALI_CINZA}  --dump                   Dump database entries{C.RESET}")
        elif "-u" in args:
            print(f"{C.KALI_VERDE}[+] SQL injection detected{C.RESET}")
            print(f"{C.KALI_BRANCO}[*] Database: webapp_db{C.RESET}")
            print(f"{C.KALI_BRANCO}[*] Tables: users, products, logs{C.RESET}")
        else:
            print(f"{C.KALI_VERMELHO}[!] No target specified{C.RESET}")
        
        return True
    
    def _cmd_ifconfig(self, args):
        """Simula ifconfig"""
        print(f"{C.KALI_BRANCO}eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500{C.RESET}")
        print(f"{C.KALI_CINZA}        inet 192.168.1.105  netmask 255.255.255.0  broadcast 192.168.1.255{C.RESET}")
        print(f"{C.KALI_CINZA}        ether 00:1a:2b:3c:4d:5e  txqueuelen 1000  (Ethernet){C.RESET}")
        print(f"{C.KALI_BRANCO}lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536{C.RESET}")
        print(f"{C.KALI_CINZA}        inet 127.0.0.1  netmask 255.0.0.0{C.RESET}")
        return True
    
    def _cmd_ping(self, args):
        """Simula ping"""
        if not args:
            self.mostrar_saida("ping: missing host", "erro")
            return False
        
        target = args[0]
        print(f"{C.KALI_CIANO}PING {target} (8.8.8.8) 56(84) bytes of data.{C.RESET}")
        
        for i in range(4):
            time.sleep(0.3)
            print(f"{C.KALI_BRANCO}64 bytes from {target}: icmp_seq={i+1} ttl=56 time={random.uniform(10, 50):.1f} ms{C.RESET}")
        
        print(f"{C.KALI_CINZA}--- {target} ping statistics ---{C.RESET}")
        print(f"{C.KALI_BRANCO}4 packets transmitted, 4 received, 0% packet loss, time 3002ms{C.RESET}")
        
        return True
    
    def _cmd_help(self, args):
        """Mostra ajuda"""
        print(f"{C.KALI_BRANCO}Available commands:{C.RESET}")
        print(f"{C.KALI_CINZA}  ls, cd, pwd, whoami, clear, cat, nano{C.RESET}")
        print(f"{C.KALI_CINZA}  ssh, scp, nmap, sqlmap, ifconfig, ping{C.RESET}")
        print(f"{C.KALI_CINZA}  help, manual, history, exit{C.RESET}")
        return True
    
    def _cmd_manual(self, args):
        """Abre o manual"""
        print(f"{C.KALI_CIANO}Opening Hacking Manual...{C.RESET}")
        # Será integrado com o manual.py
        return True
    
    def _cmd_history(self, args):
        """Mostra histórico de comandos"""
        for i, cmd in enumerate(self.historico[-10:], 1):
            print(f"{C.KALI_CINZA}{i:3d}  {cmd}{C.RESET}")
        return True
    
    def _cmd_exit(self, args):
        """Sai do terminal"""
        print(f"{C.KALI_CIANO}Closing terminal session...{C.RESET}")
        return False
    
    # ========== UTILIDADES ==========
    def _resolve_path(self, path):
        """Resolve um caminho relativo para absoluto"""
        if path.startswith("~"):
            return path
        elif path.startswith("/"):
            return path
        elif self.cwd == "~":
            return f"~/{path}"
        else:
            return f"{self.cwd}/{path}"
    
    def _find_file(self, path):
        """Encontra um arquivo no sistema simulado"""
        parts = path.strip("/").split("/")
        
        current = self.filesystem
        for part in parts:
            if part == "~" or part == "":
                current = self.filesystem.get("~", {})
            elif part in current:
                current = current[part]
            else:
                return None
        
        return current
    
    def executar_comando(self, comando):
        """Executa um comando no terminal simulado"""
        # Adicionar ao histórico
        self.historico.append(comando)
        if len(self.historico) > self.max_historico:
            self.historico.pop(0)
        
        # Parse do comando
        partes = comando.strip().split()
        if not partes:
            return True
        
        cmd = partes[0]
        args = partes[1:]
        
        # Verificar se é um comando simulado
        if cmd in self.commands_simulated:
            return self.commands_simulated[cmd](args)
        else:
            # Comando não reconhecido
            self.mostrar_saida(f"{cmd}: command not found", "erro")
            return True
    
    def sessao_interativa(self):
        """Inicia uma sessão interativa do terminal"""
        print(f"{C.KALI_AZUL}Kali Linux Terminal v2.0 - Type 'exit' to quit{C.RESET}")
        print(f"{C.KALI_CINZA}Simulated environment for RoOt 3voluti0n{C.RESET}\n")
        
        continuar = True
        while continuar:
            try:
                # Mostrar prompt e obter comando
                comando = input(self.prompt()).strip()
                
                if comando:
                    continuar = self.executar_comando(comando)
                
            except KeyboardInterrupt:
                print(f"\n{C.KALI_VERMELHO}^C{C.RESET}")
            except EOFError:
                print()
                break
        
        print(f"{C.KALI_CIANO}Session terminated.{C.RESET}")

# ========== FUNÇÕES PÚBLICAS ==========
def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mover_cursor(linha, coluna):
    """Move o cursor para posição específica"""
    sys.stdout.write(f"\033[{linha};{coluna}H")
    sys.stdout.flush()

def limpar_linha():
    """Limpa a linha atual"""
    sys.stdout.write("\033[2K")
    sys.stdout.flush()

def esconder_cursor():
    """Esconde o cursor"""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def mostrar_cursor():
    """Mostra o cursor"""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def obter_input_controlado(state, linha_input, prompt_func=None):
    """
    Obtém input com controle de cursor
    """
    mover_cursor(linha_input, 1)
    limpar_linha()
    
    esconder_cursor()
    
    # Usar terminal Kali se disponível
    if prompt_func:
        prompt = prompt_func()
    else:
        terminal = TerminalKali(state.codinome if hasattr(state, 'codinome') else "hacker")
        prompt = terminal.prompt_compacto()
    
    sys.stdout.write(prompt)
    sys.stdout.flush()
    
    mostrar_cursor()
    
    try:
        cmd = input().strip()
    except (KeyboardInterrupt, EOFError):
        cmd = "exit"
    
    return cmd

# ========== EXPORT PARA COMPATIBILIDADE ==========
# Exporta ambas as classes para compatibilidade
__all__ = ['CoresKali', 'Cores', 'C', 'TerminalKali', 'limpar_tela', 'mover_cursor', 
           'limpar_linha', 'esconder_cursor', 'mostrar_cursor', 'obter_input_controlado',
           'digitar']

# ========== TESTE ==========

def header_kali_v2(titulo="ROOT EVOLUTION", subtitulo=""):
    """
    Exibe um cabeçalho estilizado do Kali Linux v2
    """
    import os
    import time
    
    # Limpar tela
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Cores (usa variável module-level `C`)
    
    # Cabeçalho ASCII art
    header = f"""{C.KALI_ROXO}{C.NEGRITO}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  {C.KALI_CIANO}▓▓▓▓▓▓▓▓▓▓  {C.KALI_VERDE}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_AMARELO}▓▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_VERMELHO}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_ROXO}▓▓▓▓▓▓▓▓▓▓▓  ║
    ║  {C.KALI_CIANO}▓▓▓▓▓▓▓▓▓▓  {C.KALI_VERDE}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_AMARELO}▓▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_VERMELHO}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_ROXO}▓▓▓▓▓▓▓▓▓▓▓  ║
    ║  {C.KALI_CIANO}▓▓▓▓          {C.KALI_VERDE}▓▓▓▓      {C.KALI_AMARELO}▓▓▓▓        {C.KALI_VERMELHO}▓▓▓▓      {C.KALI_ROXO}▓▓▓▓          ║
    ║  {C.KALI_CIANO}▓▓▓▓          {C.KALI_VERDE}▓▓▓▓      {C.KALI_AMARELO}▓▓▓▓        {C.KALI_VERMELHO}▓▓▓▓      {C.KALI_ROXO}▓▓▓▓          ║
    ║  {C.KALI_CIANO}▓▓▓▓▓▓▓▓▓▓    {C.KALI_VERDE}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_AMARELO}▓▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_VERMELHO}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_ROXO}▓▓▓▓▓▓▓▓▓▓▓  ║
    ║  {C.KALI_CIANO}▓▓▓▓▓▓▓▓▓▓    {C.KALI_VERDE}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_AMARELO}▓▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_VERMELHO}▓▓▓▓▓▓▓▓▓▓▓▓  {C.KALI_ROXO}▓▓▓▓▓▓▓▓▓▓▓  ║
    ║        {C.KALI_CIANO}▓▓▓▓    {C.KALI_VERDE}▓▓▓▓      {C.KALI_AMARELO}▓▓▓▓        {C.KALI_VERMELHO}▓▓▓▓            {C.KALI_ROXO}▓▓▓▓          ║
    ║        {C.KALI_CIANO}▓▓▓▓    {C.KALI_VERDE}▓▓▓▓      {C.KALI_AMARELO}▓▓▓▓        {C.KALI_VERMELHO}▓▓▓▓            {C.KALI_ROXO}▓▓▓▓          ║
    ║  {C.KALI_CIANO}▓▓▓▓▓▓▓▓▓▓    {C.KALI_VERDE}▓▓▓▓      {C.KALI_AMARELO}▓▓▓▓        {C.KALI_VERMELHO}▓▓▓▓      {C.KALI_ROXO}▓▓▓▓▓▓▓▓▓▓▓  ║
    ║  {C.KALI_CIANO}▓▓▓▓▓▓▓▓▓▓    {C.KALI_VERDE}▓▓▓▓      {C.KALI_AMARELO}▓▓▓▓        {C.KALI_VERMELHO}▓▓▓▓      {C.KALI_ROXO}▓▓▓▓▓▓▓▓▓▓▓  ║
    ║                                                              ║
    ║               {C.KALI_BRANCO}{C.NEGRITO}{titulo}{C.RESET}{C.KALI_ROXO}                         ║
    """
    
    if subtitulo:
        header += f"""
    ║               {C.KALI_CIANO}{subtitulo}{C.RESET}{C.KALI_ROXO}                           ║
    """
    
    header += f"""{C.KALI_ROXO}
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    {C.RESET}
    """
    
    print(header)
    time.sleep(0.5)


def prompt_kali(username="root", hostname="kali"):
    """Retorna um prompt do Kali Linux formatado"""
    return f"{C.KALI_AZUL}[{C.KALI_VERDE}{username}{C.KALI_AZUL}@{C.KALI_ROXO}{hostname}{C.KALI_AZUL}]{C.RESET} {C.KALI_ROXO}#{C.RESET} "



def mostrar_banner():
    """Mostra um banner do Kali Linux"""
    header_kali_v2("KALI LINUX", "Simulation Environment")


if __name__ == "__main__":
    print(f"{C.KALI_CIANO}Testing Kali Linux Terminal...{C.RESET}")
    time.sleep(0.5)
    
    # Testar função digitar
    digitar("Testando função digitar... ", velocidade=0.05, cor=C.KALI_VERDE)
    print("✅ OK!")
    
    # Testar terminal
    terminal = TerminalKali("hacker", "kali")
    terminal.sessao_interativa()