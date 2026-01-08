#!/usr/bin/env python3
"""
INTRO_MENU.PY - Tela Inicial do ROOT EVOLUTION v2.1
Com animações estilo Mr. Robot e terminal Kali Linux
"""

import os
import sys
import time
import random
import shutil
import threading
import json
from datetime import datetime
from pathlib import Path

# Importar dependências
try:
    from utils.terminal_kali import C
except ImportError as e:
    print("Certifique-se que utils/terminal_kali.py existe.")
    sys.exit(1)

# Importar Sistema de Bitcoin
try:
    from bitcoin_and_market import BitcoinSystem
except ImportError:
    print("Erro: bitcoin_and_market.py não encontrado.")
    sys.exit(1)

class IntroMenu:
    
    def __init__(self):
        try:
            self.term_width = shutil.get_terminal_size().columns
            self.term_height = shutil.get_terminal_size().lines
        except:
            self.term_width = 100
            self.term_height = 30
        
        self.padding = 30
        self.content_width = self.term_width - (self.padding * 2)
        
        self.current_state = None
        self.running = True
        
        # Cores estilo Mr. Robot
        self.VERDE = C.VERDE
        self.VERMELHO = C.VERMELHO
        self.BRANCO = C.BRANCO
        self.CINZA = C.CINZA
        self.CIANO = C.CIANO
        self.AMARELO = '\033[93m'
        self.RESET = C.RESET
        
        # Flag para controlar se já mostrou introdução
        self.intro_mostrada = False
        self.pular_introducao = False
        self.prompt_pular_mostrado = False
        
        # Estado atual do jogo (para menu de jogo)
        self.jogo_atual = None
        
        # Inicializar subsistemas
        self.bitcoin_system = BitcoinSystem(self)
        
    # ========== EFEITOS VISUAIS SIMPLIFICADOS ==========
    
    def _limpar_tela(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _efeito_digitacao(self, texto, delay=0.01, cor=None, fim="\n", 
                      pode_pular=True, verificar_pular_cada=1):
        """Efeito de digitação avançado"""
        
        try:
            if cor is None:
                cor = self.BRANCO
            
            sys.stdout.write(cor)
            sys.stdout.flush()
            
            total_caracteres = len(texto)
            
            for i, caractere in enumerate(texto):
                # Verificar se deve pular (não verificar em cada caractere para performance)
                if (pode_pular and self.pular_introducao and 
                    (i % verificar_pular_cada == 0 or i == total_caracteres - 1)):
                    # Completar texto rapidamente
                    sys.stdout.write(texto[i:] + self.RESET + fim)
                    sys.stdout.flush()
                    return True
                
                # Escrever caractere
                sys.stdout.write(caractere)
                
                # Flush periódico para melhor performance
                if i % 5 == 0 or i == total_caracteres - 1:
                    sys.stdout.flush()
                
                # Delay inteligente
                tempo_delay = delay
                
                # Ajustar delay baseado no caractere
                if caractere in ".,!?;:":
                    tempo_delay = delay * 4  # Pausa para pontuação
                elif caractere == " ":
                    tempo_delay = delay / 3  # Espaços mais rápidos
                elif caractere in "\n\t":
                    tempo_delay = 0  # Caracteres de controle instantâneos
                elif i < total_caracteres - 1 and texto[i+1] in ".,!?;:":
                    tempo_delay = delay * 0.7  # Antes da pontuação, mais rápido
                
                # Aplicar delay
                if tempo_delay > 0:
                    time.sleep(tempo_delay)
            
            # Finalizar
            sys.stdout.write(self.RESET + fim)
            sys.stdout.flush()
            
            return False
            
        except (IOError, BrokenPipeError):
            # Terminal foi fechado durante a digitação
            return True
        except Exception as e:
            # Em caso de erro, escrever texto completo
            sys.stdout.write(texto + self.RESET + fim)
            sys.stdout.flush()
        return False
    
    def _glitch_terminal(self, duracao=2.0):
        """Efeito de glitch de terminal"""
        tempo_inicial = time.time()
        caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/\\"
        
        while time.time() - tempo_inicial < duracao:
            # Verificar se deve pular
            if self.pular_introducao:
                return True
                
            # Limpar linha atual
            sys.stdout.write("\r")
            
            # Gerar texto glitchado
            texto_glitch = ''.join(random.choice(caracteres) for _ in range(self.term_width))
            sys.stdout.write(f"{self.VERDE}{texto_glitch}")
            sys.stdout.flush()
            time.sleep(0.05)
            
            # Limpar
            sys.stdout.write("\r" + " " * self.term_width + "\r")
            sys.stdout.flush()
            time.sleep(0.03)
        return False
    
    def _linhas_scan(self, linhas=20, velocidade=0.05):
        """Efeito de scanlines"""
        for _ in range(linhas):
            # Verificar se deve pular
            if self.pular_introducao:
                return True
                
            linha = "_" * self.term_width
            print(f"{self.VERDE}{linha}{self.RESET}")
            time.sleep(velocidade)
        self._limpar_tela()
        return False
    
    def _chuva_matrix(self, duracao=3.0):
        """Chuva de caracteres estilo Matrix"""
        caracteres = "01█▓▒░"
        colunas = [0] * (self.term_width // 2)
        tempo_inicial = time.time()
        
        print("\033[?25l")  # Esconder cursor
        
        try:
            while time.time() - tempo_inicial < duracao:
                # Verificar se deve pular
                if self.pular_introducao:
                    print("\033[?25h")  # Mostrar cursor novamente
                    self._limpar_tela()
                    return True
                    
                for i in range(len(colunas)):
                    if colunas[i] > 0 or random.random() > 0.95:
                        if colunas[i] >= self.term_height or random.random() > 0.9:
                            colunas[i] = 0
                        else:
                            colunas[i] += 1
                        
                        # Imprimir caractere
                        if colunas[i] > 0:
                            col = i * 2
                            linha = colunas[i]
                            caractere = random.choice(caracteres)
                            
                            # Posicionar cursor e imprimir
                            if linha > 0:
                                print(f"\033[{linha-1};{col}H {self.RESET}", end="")
                            print(f"\033[{linha};{col}H{self.VERDE}{caractere}{self.RESET}", end="")
                
                sys.stdout.flush()
                time.sleep(0.1)
        finally:
            print("\033[?25h")  # Mostrar cursor novamente
            self._limpar_tela()
        return False
    
    def _piscar_erro(self, texto, repeticoes=5):
        """Efeito de piscar erro - versão final corrigida"""
        
        # Verificar pulo imediatamente
        if self.pular_introducao:
            return True
        
        # Salvar posição do cursor
        sys.stdout.write("\033[s")
        sys.stdout.flush()
        
        try:
            for i in range(repeticoes):
                # Verificar a cada iteração
                if self.pular_introducao:
                    sys.stdout.write("\033[u\033[K")  # Restaurar e limpar
                    sys.stdout.flush()
                    return True
                
                # Mostrar texto
                print(f"{self.VERMELHO}{texto}{self.RESET}")
                sys.stdout.flush()
                time.sleep(0.1)
                
                # Restaurar posição e limpar
                sys.stdout.write("\033[u\033[K")
                sys.stdout.flush()
                
                # Última piscada não precisa esperar
                if i < repeticoes - 1:
                    time.sleep(0.1)
            
            # Garantir limpeza final
            sys.stdout.write("\033[u\033[K")
            sys.stdout.flush()
            
            return False
            
        except Exception as e:
            # Em caso de erro, tentar limpar
            try:
                sys.stdout.write("\033[u\033[K" + self.RESET)
                sys.stdout.flush()
            except:
                pass
            return False
    
#####################################################################    
    
    def _sequencia_boot(self):
        """Sequência de boot - versão otimizada"""
            
        # Não verificar pular_introducao aqui - quem chama decide
            
        self._limpar_tela()
            
            # Preparar sequência
        sequencia = self._preparar_sequencia_boot()
            
            # Calcular posicionamento
        self._posicionar_boot_sequence(sequencia)
            
            # Executar sequência
        self._executar_sequencia_boot(sequencia)
            
            # Finalizar
        self._finalizar_boot_sequence()

    def _preparar_sequencia_boot(self):
        """Prepara a sequência de boot"""
        return [
            # (texto, delay, cor, tem_borda)
            ("INICIALIZANDO ACESSO ROOT...", 0.01, self.VERDE, False),
            ("[OK] Root access enabled", 0.005, self.CINZA, False),
            ("", 0.0, None, False),
                
            ("CARREGANDO MÓDULOS DO KERNEL...", 0.01, self.VERDE, False),
            ("[OK] netfilter, iptables, crypto", 0.005, self.CINZA, False),
            ("[OK] tun, tap, bridge modules", 0.005, self.CINZA, False),
            ("", 0.0, None, False),
                
            ("MONTANDO PARTIÇÕES CRIPTOGRAFADAS...", 0.01, self.VERDE, False),
            ("[OK] /dev/sda1 (LUKS) mounted at /mnt/secure", 0.005, self.CINZA, False),
            ("", 0.0, None, False),
                
            ("ESTABELECENDO CONEXÃO SEGURA...", 0.01, self.VERDE, False),
            ("[OK] VPN tunnel established: 192.168.1.108 → 10.8.0.1", 0.005, self.CINZA, False),
            ("[OK] Tor circuit: 3 hops, 256-bit encryption", 0.005, self.CINZA, False),
            ("", 0.0, None, False),
                
            ("CONTORNANDO FIREWALL...", 0.01, self.VERDE, False),
            ("[OK] Bypassing Deep Packet Inspection", 0.005, self.CIANO, False),
            ("[OK] TCP/IP headers randomized", 0.005, self.CIANO, False),
            ("", 0.0, None, False),
                
            ("ACESSO CONCEDIDO.", 0.02, self.VERMELHO, False),
            ("", 0.0, None, False),
                
            # BOX - marcar como tendo borda
            (f"{self.VERDE}╔══════════════════════════════════════════╗", 0.0, self.VERDE, True),
            (f"{self.VERDE}║    BEM-VINDO AO SISTEMA ROOT EVOLUTION   ║", 0.02, self.VERDE, True),
            (f"{self.VERDE}╚══════════════════════════════════════════╝", 0.0, self.VERDE, True),
            ]

    def _posicionar_boot_sequence(self, sequencia):
        """Posiciona a sequência verticalmente"""
        linhas_nao_vazias = sum(1 for texto, _, _, _ in sequencia if texto.strip() != "")
        espacamento = max((self.term_height - linhas_nao_vazias) // 2, 1)
        print("\n" * espacamento)

    def _executar_sequencia_boot(self, sequencia):
        """Executa a sequência de boot"""
        for texto, delay, cor, tem_borda in sequencia:
            if texto.strip() == "":
                print()
                sys.stdout.flush()
                continue
                
            # CORREÇÃO CRÍTICA: se tem borda, NÃO usar .strip()
            comprimento = len(texto) if tem_borda else len(texto.strip())
            espacamento = " " * ((self.term_width - comprimento) // 2)
                
            linha_formatada = f"{espacamento}{texto}"
                
            if delay > 0:
                self._efeito_digitacao(linha_formatada, delay=delay, cor=cor, pode_pular=False)
            else:
                print(linha_formatada)
                sys.stdout.flush()
                
            if delay >= 0.01:
                time.sleep(0.1)

    def _finalizar_boot_sequence(self):
        """Finaliza a sequência de boot"""
        time.sleep(1.0)
        self._limpar_tela()


#####################################################################    
    # ========== ANIMAÇÃO TERMINAL KALI LINUX ==========
    
    def _mostrar_terminal_kali(self, codinome):
        """Mostra animação de terminal Kali Linux"""
        self._limpar_tela()
        
        # Cabeçalho do terminal
        cabecalho_kali = f"""{self.VERDE}
┌─[root@kali]-[~]
└──╼ {self.CIANO}#{self.RESET} """
        
        print(cabecalho_kali)
        
        # Comandos do Kali sendo executados
        comandos = [
            f"{self.VERDE}whoami{self.RESET}",
            f"root",
            "",
            f"{self.VERDE}hostname{self.RESET}",
            f"kali",
            "",
            f"{self.VERDE}ip a | grep inet{self.RESET}",
            f"    inet 192.168.1.108/24 brd 192.168.1.255 scope global dynamic eth0",
            f"    inet 127.0.0.1/8 scope host lo",
            "",
            f"{self.VERDE}cd /root{self.RESET}",
            f"",
            f"{self.VERDE}ls -la{self.RESET}",
            f"total 48",
            f"drwx------  6 root root 4096 Dec 10 14:23 .",
            f"drwxr-xr-x 18 root root 4096 Dec 10 14:20 ..",
            f"-rw-------  1 root root 3890 Dec 10 14:23 .bash_history",
            f"-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc",
            f"drwx------  2 root root 4096 Dec 10 14:20 .cache",
            f"drwx------  3 root root 4096 Dec 10 14:20 .config",
            f"-rw-r--r--  1 root root  148 Aug 17  2015 .profile",
            f"drwx------  2 root root 4096 Dec 10 14:20 .ssh",
            f"drwxr-xr-x  2 root root 4096 Dec 10 14:23 tools",
            "",
            f"{self.VERDE}echo 'USUÁRIO: {codinome}' > /tmp/user_id{self.RESET}",
            f"",
            f"{self.VERDE}cat /tmp/user_id{self.RESET}",
            f"USUÁRIO: {codinome}",
            "",
            f"{self.VERDE}msfconsole -q{self.RESET}",
            f"                                                   ",
            f"MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM  ",
            f"MMMMMMMMMMMN                              MMMMMMMM  ",
            f"MMMMMMMMMMM    Console Metasploit         MMMMMMMM  ",
            f"MMMMMMMMMMM                                MMMMMMMM  ",
            f"MMMMMMMMMMM    =[ metasploit v6.3.31      MMMMMMMM  ",
            f"MMMMMMMMMMM    --==--                 ]   MMMMMMMM  ",
            f"MMMMMMMMMMM    =[ 2296 exploits - 1214 auxiliary   ",
            f"MMMMMMMMMMM    =[ 786 payloads - 46 encoders       ",
            f"MMMMMMMMMMM    =[ 11 nops                         ",
            f"",
            f"msf6 > {self.VERDE}use auxiliary/scanner/ssh/ssh_login{self.RESET}",
            f"msf6 auxiliary(scanner/ssh/ssh_login) > {self.VERDE}set RHOSTS 192.168.1.0/24{self.RESET}",
            f"RHOSTS => 192.168.1.0/24",
            f"msf6 auxiliary(scanner/ssh/ssh_login) > {self.VERDE}run{self.RESET}",
            f"",
            f"[*] 192.168.1.1:22 - Iniciando varredura de login SSH",
            f"[*] 192.168.1.105:22 - SSH - Testando senhas em texto claro",
            f"[+] 192.168.1.105:22 - SSH - Sucesso: 'root:toor' 'uid=0(root) gid=0(root) groups=0(root)'",
            f"[*] Sessão de shell de comando 1 aberta (192.168.1.108:4444 -> 192.168.1.105:38264)",
            f"",
            f"{self.VERDE}exit{self.RESET}",
            f"",
            f"{self.VERDE}echo 'SESSÃO ESTABELECIDA' && sleep 1{self.RESET}",
            f"SESSÃO ESTABELECIDA",
            f"",
            f"{self.VERDE}clear{self.RESET}"
        ]
        
        # Executar comandos com efeito
        for cmd in comandos:
            # Verificar se deve pular
            if self.pular_introducao:
                break
                
            if cmd.startswith(f"{self.VERDE}"):
                # É um comando - digitar com delay
                self._efeito_digitacao(f"└──╼ {self.CIANO}#{self.RESET} {cmd}", delay=0.01, fim="")
                print()
                time.sleep(0.3)
            elif cmd.strip() == "":
                # Linha vazia
                print()
                time.sleep(0.1)
            else:
                # É output - mostrar rápido
                print(f"     {cmd}")
                time.sleep(0.05)
        
        if not self.pular_introducao:
            time.sleep(1)
        
        self._limpar_tela()
        
        # Mensagem final
        if not self.pular_introducao:
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERDE}╔══════════════════════════════════════╗")
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.VERDE}║   TERMINAL KALI - ACESSO ROOT         ║")
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.VERDE}║   USUÁRIO: {codinome:<24} ║")
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.VERDE}║   STATUS: CONECTADO                   ║")
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.VERDE}╚══════════════════════════════════════╝{self.RESET}")
            
            time.sleep(2)
 ########################################################################   
    # ========== INTRODUÇÃO ESTILO MR. ROBOT ==========
    
    def _mostrar_introducao_mr_robot(self):
    
        if self.intro_mostrada or self.pular_introducao:
            return
        
        self._limpar_tela()
        
        # Mostrar prompt para pular
        self._mostrar_prompt_pular()
        
        # Verificar se pulou antes de começar
        if self.pular_introducao:
            return
        
        # Executar sequência de animações
        animacoes = [
            self._animacao_inicial_glitch,
            self._animacao_linhas_digitacao,
            self._animacao_mensagens_iniciais,
            self._animacao_transicao_conexao,
            self._animacao_chuva_matrix,
            self._animacao_taglines_finais
        ]
        
        for animacao in animacoes:
            if self.pular_introducao:
                break
            animacao()
        
        # Marcar que já mostrou a introdução
        self.intro_mostrada = True

    # ========== ANIMAÇÕES INDIVIDUAIS ==========

    def _animacao_inicial_glitch(self):
        """Efeito inicial de terminal com glitch"""
        print("\n" * (self.term_height // 4))
        self._glitch_terminal(1.5)

    def _animacao_linhas_digitacao(self):
        """Linhas de digitalização"""
        self._linhas_scan(15, 0.03)

    def _animacao_mensagens_iniciais(self):
        """Mensagens iniciais estilo Mr. Robot"""
        print("\n" * 5)
        
        linhas = [
            ("VOCÊ NÃO ESTÁ SOZINHO.", self.VERDE, False),
            ("O SISTEMA ESTÁ OBSERVANDO.", self.VERDE, False),
            ("MAS NÓS TAMBÉM ESTAMOS.", self.VERDE, False),
            ("", self.VERDE, False),  # Linha vazia
            ("NÓS SOMOS A RESISTÊNCIA.", self.VERDE, False),
            ("SOMOS AS SOMBRAS DIGITAIS.", self.VERDE, False),
            ("SOMOS OS QUE ENXERGAM A VERDADE.", self.VERDE, False),
            ("", self.VERDE, False),  # Linha vazia
            ("E A VERDADE É...", self.VERDE, False),
            ("TUDO ESTÁ QUEBRADO.", self.VERDE, False),
            ("TUDO ESTÁ VULNERÁVEL.", self.VERDE, False),
            ("TUDO PODE SER HACKEADO.", self.VERMELHO, True),  # Com efeito especial
            ("", self.VERDE, False),  # Linha vazia
            ("INCLUSIVE VOCÊ.", self.VERDE, False)
        ]
        
        for texto, cor, tem_efeito in linhas:
            if self.pular_introducao:
                return
                
            if texto == "":
                time.sleep(0.1)
                continue
            
            espacamento = " " * ((self.term_width - len(texto)) // 2)
            
            if tem_efeito:
                # Linha com efeito especial
                self._efeito_digitacao(f"{espacamento}{cor}{texto}{self.RESET}", delay=0.01)
                self._piscar_erro(f"{espacamento}{cor}{texto}{self.RESET}", 3)
            else:
                # Linha normal
                self._efeito_digitacao(f"{espacamento}{cor}{texto}{self.RESET}", delay=0.01)
                time.sleep(0.1)
        
        if self.pular_introducao:
            return
            
        time.sleep(0.2)

    def _animacao_transicao_conexao(self):
        """Animação de transição e conexão"""
        self._limpar_tela()
        print("\n" * 3)
        
        # Mensagem de conexão
        self._efeito_digitacao(" " * 20 + "ESTABELECENDO CONEXÃO...", 
                            delay=0.02, cor=self.VERDE)
        
        # Animação dos pontos
        for i in range(5):
            if self.pular_introducao:
                return
                
            pontos = "." * ((i % 3) + 1)
            print(f"\r" + " " * 20 + f"ESTABELECENDO CONEXÃO{pontos}", end="")
            time.sleep(0.2)
        
        if not self.pular_introducao:
            print(f"\r" + " " * 20 + f"{self.VERDE}CONEXÃO ESTABELECIDA{self.RESET}")
            time.sleep(0.5)

    def _animacao_chuva_matrix(self):
        """Efeito de chuva de código estilo Matrix"""
        self._chuva_matrix(2)

    def _animacao_taglines_finais(self):
        """Taglines finais da introdução"""
        self._limpar_tela()
        print("\n" * (self.term_height // 3))
        
        taglines = [
            f"{self.CINZA}« O Sistema é o verdadeiro vírus. »{self.RESET}",
            f"{self.CINZA}« Nós somos a cura. »{self.RESET}",
            f"{self.CINZA}« Bem vindo à R3V0LUÇ40. »{self.RESET}"
        ]
        
        for tagline in taglines:
            if self.pular_introducao:
                return
                
            espacamento = " " * ((self.term_width - len(tagline)) // 2)
            print(espacamento + tagline)
            time.sleep(1)
        
        if not self.pular_introducao:
            time.sleep(1.5)
        
        self._limpar_tela()
#########################################################


    def _mostrar_prompt_pular(self):
        """Mostra o prompt para pular a introdução"""
        if self.prompt_pular_mostrado:
            return
            
        self._limpar_tela()
        
        print("\n" * (self.term_height // 3))
        
        # Mensagem de skip - calcular comprimento SEM cores ANSI
        prompt_text = "Pressione ENTER para pular introdução"
        prompt2_text = "ou aguarde para assistir a sequência completa"
        
        prompt = f"{self.CINZA}⏎ {self.CIANO}Pressione {self.BRANCO}ENTER{self.CIANO} para pular introdução{self.RESET}"
        prompt2 = f"{self.CINZA}⏎ {self.CIANO}ou aguarde para assistir a sequência completa{self.RESET}"
        
        # Centralização correta sem contar códigos ANSI
        espacamento = " " * ((self.term_width - len(prompt_text)) // 2)
        espacamento2 = " " * ((self.term_width - len(prompt2_text)) // 2)
        
        print(espacamento + prompt)
        print(espacamento2 + prompt2)
        
        print("\n" * 2)
        
        # Contador regressivo
        contador = 5
        texto_contador_base = "Aguarde X segundos..."
        
        # Thread para detectar Enter com sincronização
        enter_pressionado = threading.Event()
        
        def esperar_enter():
            try:
                input()  # Espera Enter
                enter_pressionado.set()
                self.pular_introducao = True
            except (EOFError, KeyboardInterrupt):
                enter_pressionado.set()
                self.pular_introducao = True
        
        # Iniciar thread para detectar Enter
        thread_enter = threading.Thread(target=esperar_enter, daemon=True)
        thread_enter.start()
        
        # Mostrar contador
        for i in range(contador, 0, -1):
            if self.pular_introducao or enter_pressionado.is_set():
                break
                
            texto_contador_display = f"Aguarde {i} segundos..."
            texto_contador = f"{self.CINZA}Aguarde {self.BRANCO}{i}{self.CINZA} segundos...{self.RESET}"
            espacamento3 = " " * ((self.term_width - len(texto_contador_display)) // 2)
            
            # Voltar à linha do contador
            if i < contador:
                print(f"\033[F\033[K", end="")  # Voltar linha e limpar
            print(espacamento3 + texto_contador)
            
            # Esperar 1 segundo ou até Enter ser pressionado
            for _ in range(10):
                if self.pular_introducao or enter_pressionado.is_set():
                    break
                time.sleep(0.1)

          
        self.prompt_pular_mostrado = True
        self._limpar_tela()
    
    
    # ========== LOGO SIMPLIFICADO ==========
    
    def _mostrar_logo(self):
        """Mostra o logo de forma mais limpa"""
        self._limpar_tela()
        
        logo = f"""
{self.VERDE}
{' ' * ((self.term_width - 50) // 2)}╔══════════════════════════════════════════════════╗
{' ' * ((self.term_width - 50) // 2)}║                                                  ║
{' ' * ((self.term_width - 50) // 2)}║        ██████╗  ██████╗  ██████╗ ████████╗       ║
{' ' * ((self.term_width - 50) // 2)}║        ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝       ║
{' ' * ((self.term_width - 50) // 2)}║        ██████╔╝██║   ██║██║   ██║   ██║          ║
{' ' * ((self.term_width - 50) // 2)}║        ██╔══██╗██║   ██║██║   ██║   ██║          ║
{' ' * ((self.term_width - 50) // 2)}║        ██║  ██║╚██████╔╝╚██████╔╝   ██║          ║
{' ' * ((self.term_width - 50) // 2)}║        ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝          ║
{' ' * ((self.term_width - 50) // 2)}║                                                  ║
{' ' * ((self.term_width - 50) // 2)}║        ROOT EVOLUTION v2.1                       ║
{' ' * ((self.term_width - 50) // 2)}║                                                  ║
{' ' * ((self.term_width - 50) // 2)}╚══════════════════════════════════════════════════╝
{self.RESET}
"""
        
        # Animar logo aparecendo
        for linha in logo.split('\n'):
            if linha.strip():
                self._efeito_digitacao(linha, delay=0.00, cor=self.VERDE, fim="")
                print()
        
        
        # Sub-título
        subtitulo = f"{self.CINZA}« hack the system. become root. »{self.RESET}"
        espacamento = " " * ((self.term_width - len(subtitulo)) // 2)
        print(f"\n{espacamento}{subtitulo}")
        
        time.sleep(0.1)
    
    # ========== SISTEMA DE SAVE/LOAD COMPATÍVEL ==========
    
    def _listar_saves_disponiveis(self):
        """Lista jogos salvos compatíveis"""
        pasta_saves = Path("saves")
        saves = []
        
        if pasta_saves.exists():
            for arquivo_save in pasta_saves.glob("*.json"):
                try:
                    with open(arquivo_save, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    # Verificar se é um save compatível
                    if 'player_name' in dados and 'codiname' in dados:
                        saves.append({
                            'arquivo': str(arquivo_save),
                            'nome_jogador': dados['player_name'],
                            'codinome': dados['codiname'],
                            'capitulo': dados.get('current_chapter', 1),
                            'data': dados.get('last_seen', datetime.now().isoformat()),
                            'bitcoin': dados.get('bitcoin_wallet', 0)
                        })
                except:
                    continue
        
        return sorted(saves, key=lambda x: x['data'], reverse=True)
    
    def _carregar_jogo(self, arquivo_save):
        """Carrega jogo salvado"""
        try:
            with open(arquivo_save, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Atualizar última vez visto
            dados['last_seen'] = datetime.now().isoformat()
            
            # Salvar de volta
            with open(arquivo_save, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            return dados
        except Exception as e:
            print(f"{self.VERMELHO}Erro ao carregar jogo: {e}{self.RESET}")
            return None
    
    def _salvar_jogo(self, dados_jogador, arquivo_save=None):
        """Salva jogo no formato compatível"""
        if arquivo_save is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo_save = f"saves/{dados_jogador['codiname']}_{timestamp}.json"
        
        # Garantir diretório existe
        Path("saves").mkdir(exist_ok=True)
        
        with open(arquivo_save, 'w', encoding='utf-8') as f:
            json.dump(dados_jogador, f, indent=2, ensure_ascii=False)
        
        return arquivo_save
    
    # ========== SISTEMA DE CAPÍTULOS ==========
    
    def _verificar_capitulos_disponiveis(self):
        """Verifica quais capítulos estão disponíveis na pasta chapters/"""
        pasta_capitulos = Path("chapters")
        capitulos = []
        
        if not pasta_capitulos.exists():
            return capitulos
        
        for arquivo in pasta_capitulos.glob("chapter_*.py"):
            try:
                # Extrair número do capítulo do nome do arquivo
                nome = arquivo.stem  # "chapter_01"
                num = nome.split("_")[1]  # "01"
                capitulos.append({
                    'arquivo': str(arquivo),
                    'numero': int(num),
                    'nome': nome
                })
            except:
                continue
        
        return sorted(capitulos, key=lambda x: x['numero'])
    
    def _executar_capitulo(self, numero_capitulo, dados_jogador, arquivo_save):
        """Executa um capítulo específico usando o Controlador Central"""
        # Garantir imports corretos
        import sys
        import importlib.util
        from chapters.chapters_control import ChapterController
        
        capitulos = self._verificar_capitulos_disponiveis()
        
        if not capitulos:
            self._mostrar_erro_sem_capitulos()
            return False
        
        # Encontrar o capítulo correto
        capitulo_alvo = None
        for cap in capitulos:
            if cap['numero'] == numero_capitulo:
                capitulo_alvo = cap
                break
        
        if not capitulo_alvo:
            print(f"{self.VERMELHO}Capítulo {numero_capitulo} não encontrado!{self.RESET}")
            time.sleep(1.5)
            # Retorna dados sem alterar progresso
            return dados_jogador
        
        try:
            # Salvar estado atual antes de iniciar capítulo
            # IMPORTANTE: Não atualizamos 'current_chapter' aqui cegamente, o controlador fará isso
            self._salvar_jogo(dados_jogador, arquivo_save)
            
            # Efeito de transição
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERDE}INICIANDO CAPÍTULO {numero_capitulo}...{self.RESET}")
            time.sleep(1)
            
            # Executar capítulo (usando importlib como já estava)
            spec = importlib.util.spec_from_file_location(f"chapter_{numero_capitulo:02d}", capitulo_alvo['arquivo'])
            modulo = importlib.util.module_from_spec(spec)
            
            # Carregar módulo
            sys.modules[f"chapter_{numero_capitulo:02d}"] = modulo # Registrar em sys.modules
            spec.loader.exec_module(modulo)
            
            # Verificar se tem função iniciar
            if not hasattr(modulo, 'iniciar'):
                print(f"{self.VERMELHO}ERRO: Capítulo mal formatado (sem função iniciar){self.RESET}")
                return False
                
            # Executar função iniciar
            resultado_bruto = modulo.iniciar(dados_jogador, arquivo_save)
            
            # Se retornou None, erro fatal
            if resultado_bruto is None:
                return None

            # PROCESSAR RESULTADO VIA CONTROLADOR
            controller = ChapterController()
            dados_processados = controller.processar_resultado(dados_jogador, resultado_bruto)
            
            return dados_processados
                
        except Exception as e:
            print(f"{self.VERMELHO}Erro crítico ao executar capítulo {numero_capitulo}: {e}{self.RESET}")
            import traceback
            traceback.print_exc()
            input("Pressione ENTER para voltar ao menu...")
            return None
            return False
    
    def _mostrar_erro_sem_capitulos(self):
        """Mostra mensagem de erro quando não há capítulos"""
        self._limpar_tela()
        print(f"\n{' ' * ((self.term_width - 50) // 2)}{self.VERMELHO}══════════════════════════════════════════════════{self.RESET}")
        print(f"{' ' * ((self.term_width - 50) // 2)}{self.VERMELHO} ERRO: NENHUM CAPÍTULO ENCONTRADO")
        print(f"{' ' * ((self.term_width - 50) // 2)}{self.VERMELHO}══════════════════════════════════════════════════{self.RESET}")
        print(f"\n{' ' * ((self.term_width - 60) // 2)}{self.CINZA}A pasta 'chapters/' está vazia ou não existe.")
        print(f"{' ' * ((self.term_width - 60) // 2)}{self.CINZA}Certifique-se de que os arquivos chapter_01.py, chapter_02.py, etc.")
        print(f"{' ' * ((self.term_width - 60) // 2)}{self.CINZA}estão presentes na pasta chapters/.{self.RESET}")
        
        input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
    
    # ========== MENU PRINCIPAL ==========
    
    def _mostrar_menu_principal(self):
        """Menu principal com controle de estado correto"""
        
        menu_ativo = True
        
        while menu_ativo:
            self._limpar_tela()
            self._mostrar_logo()
            
            print(f"\n{' ' * ((self.term_width - 20) // 2)}{self.VERDE}MENU PRINCIPAL{self.RESET}")
            print(f"{' ' * ((self.term_width - 20) // 2)}{self.CINZA}════════════════════{self.RESET}\n")
            
            opcoes = [
                ("1", "NOVO JOGO", self.VERDE),
                ("2", "CARREGAR JOGO", self.VERDE),
                ("3", "MANUAL HACKER", self.VERDE),
                ("4", "INFORMAÇÕES DO SISTEMA", self.CINZA),
                ("0", "SAIR", self.VERMELHO)
            ]
            
            for num, texto, cor in opcoes:
                espacamento = " " * ((self.term_width - 25) // 2)
                print(f"{espacamento}{cor}[{num}] {texto}{self.RESET}")
            
            print('Pressione [ENTER]...') ## temporario??? 
            
            try:
                escolha = input(f"{' ' * ((self.term_width - 20) // 2)}{self.BRANCO}SELECIONE > {self.RESET}").strip()
                
                if escolha == "1":
                    self._novo_jogo()
                    
                elif escolha == "2":
                    self._carregar_jogo_menu()
                    
                elif escolha == "3":
                    self._abrir_manual()
                    
                elif escolha == "4":
                    self._informacoes_sistema()
                    
                elif escolha == "0":
                    if self._confirmar_saida():
                        self._sair_jogo()
                        menu_ativo = False  # Para o loop
                        self.running = False  # Para o programa
                    # Se não confirmar, continua no loop
                    
                else:
                    print(f"\n{' ' * ((self.term_width - 15) // 2)}{self.VERMELHO}Opção inválida!{self.RESET}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                if self._confirmar_saida():
                    self._sair_jogo()
                    menu_ativo = False
                    self.running = False

    def _confirmar_saida(self, mensagem=None):
        """Confirma se o jogador quer realmente sair"""
        self._limpar_tela()
        # Calcular comprimento SEM cores para centralização correta
        msg_display = "TEM CERTEZA QUE DESEJA SAIR?"
        print(f"\n{' ' * ((self.term_width - len(msg_display)) // 2)}{self.VERMELHO}{msg_display}{self.RESET}")
        
        opcoes_text = "[S] Sim  [N] Não"
        print(f"{' ' * ((self.term_width - len(opcoes_text)) // 2)}{self.CINZA}{opcoes_text}{self.RESET}")
        
        resposta = input(f"{' ' * ((self.term_width - 2) // 2)}{self.BRANCO}> {self.RESET}").strip().upper()
        
        return resposta == "S" or resposta == "SIM"

    def _mostrar_erro(self, mensagem):
        """Mostra mensagem de erro temporária"""
        print(f"\n{' ' * ((self.term_width - len(mensagem)) // 2)}{self.VERMELHO}{mensagem}{self.RESET}")
        time.sleep(1.2)



    # ========== MENU DE JOGO (após criar/carregar jogo) ==========
    
    def _mostrar_menu_jogo(self, dados_jogador, arquivo_save):
        """Menu principal do jogo (mostrado depois de criar/carregar jogo)"""
        self.jogo_atual = {
            'dados': dados_jogador,
            'arquivo': arquivo_save
        }
        
        menu_jogo_ativo = True
        while menu_jogo_ativo and self.running:
            self._limpar_tela()
            
            # Cabeçalho com informações do jogador
            print(f"\n{' ' * ((self.term_width - 50) // 2)}{self.VERDE}┌──────────────────────────────────────────────────┐")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.VERDE}│           R O O T  E V O L U T I O N             │")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.VERDE}└──────────────────────────────────────────────────┘{self.RESET}")
            
            # Informações do jogador
            print(f"\n{' ' * ((self.term_width - 50) // 2)}{self.CIANO}JOGADOR: {self.BRANCO}{dados_jogador['player_name']}")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.CIANO}CODINOME: {self.VERDE}{dados_jogador['codiname']}")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.CIANO}CAPÍTULO ATUAL: {self.AMARELO}{dados_jogador.get('current_chapter', 1)}")
            
            # Mostrar Bitcoin se disponível
            if 'bitcoin_wallet' in dados_jogador:
                btc = dados_jogador['bitcoin_wallet']
                print(f"{' ' * ((self.term_width - 50) // 2)}{self.CIANO}BITCOIN: {self.VERDE}{btc:.6f} BTC")
            
            print(f"\n{' ' * ((self.term_width - 30) // 2)}{self.CINZA}{'─' * 30}{self.RESET}\n")
            
            # Opções do menu de jogo
            opcoes = [
                ("[1]", "CONTINUAR JOGO", self.VERDE),
                ("[2]", "CARTEIRA BITCOIN", self.AMARELO),
                ("[3]", "MANUAL DE HACKING", self.CIANO),
                ("[4]", "STATUS DO JOGO", self.BRANCO),
                ("[5]", "SALVAR JOGO", self.VERDE),
                ("[6]", "VOLTAR AO MENU PRINCIPAL", self.CINZA),
                ("[0]", "SAIR DO JOGO", self.VERMELHO)
            ]
            
            for num, texto, cor in opcoes:
                espacamento = " " * ((self.term_width - 35) // 2)
                opcao = f"{espacamento}{cor}[{num}] {texto}{self.RESET}"
                print(opcao)
                time.sleep(0.01)
            
            print()
            
            # Input
            try:
                escolha = input(f"{' ' * ((self.term_width - 20) // 2)}{self.BRANCO}SELECIONE > {self.RESET}").strip()
                
                if escolha == "1":
                    self._continuar_jogo(dados_jogador, arquivo_save)
                elif escolha == "2":
                    self.bitcoin_system.mostrar_carteira(dados_jogador, arquivo_save)
                elif escolha == "3":
                    self._abrir_manual_hacking()
                elif escolha == "4":
                    self._mostrar_status_jogo(dados_jogador)
                elif escolha == "5":
                    self._salvar_jogo_atual(dados_jogador, arquivo_save)
                elif escolha == "6":
                    # Salvar antes de voltar
                    self._salvar_jogo_atual(dados_jogador, arquivo_save)
                    menu_jogo_ativo = False
                elif escolha == "0":
                    self._sair_do_jogo(dados_jogador, arquivo_save)
                    menu_jogo_ativo = False
                else:
                    print(f"\n{' ' * ((self.term_width - 15) // 2)}{self.VERMELHO}NÚMERO INVÁLIDO{self.RESET}")
                    time.sleep(0.5)
                    
            except KeyboardInterrupt:
                print(f"\n\n{self.VERMELHO}INTERROMPIDO{self.RESET}")
                time.sleep(1)
    
    # ========== FUNÇÕES DO MENU DE JOGO ==========
    
    def _continuar_jogo(self, dados_jogador, arquivo_save):
        """Continua o jogo do ponto onde parou - loop dinâmico"""
        
        jogando = True
        while jogando and self.running:
            # Limpar flag antes de começar
            if 'saindo_para_menu' in dados_jogador:
                del dados_jogador['saindo_para_menu']

            capitulo_atual = dados_jogador.get('current_chapter', 1)
            
            # Executar o capítulo atual
            sucesso = self._executar_capitulo(capitulo_atual, dados_jogador, arquivo_save)
            
            if sucesso:
                if dados_jogador.get('saindo_para_menu'):
                    print(f"\n{self.AMARELO}Retornando ao menu principal...{self.RESET}")
                    time.sleep(1)
                    jogando = False
                    continue
                # Verificar se o jogador completou o jogo ou se deve continuar
                # Logicamente, se o capítulo retornou sucesso e atualizou o current_chapter,
                # o loop vai pegar o novo capítulo na próxima iteração.
                
                # Se o capítulo atual não mudou após sucesso, pode ser um "fim de jogo" ou erro lógico
                # Mas assumindo que chapters incrementam current_chapter ao final:
                novo_capitulo = dados_jogador.get('current_chapter', capitulo_atual)
                
                if novo_capitulo == capitulo_atual:
                    # Se não avançou de capítulo mesmo com sucesso, talvez seja o fim do conteúdo atual
                    print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERDE}FIM DO CONTEÚDO DISPONÍVEL{self.RESET}")
                    print(f"{' ' * ((self.term_width - 50) // 2)}{self.CINZA}Aguarde por novas atualizações...{self.RESET}")
                    time.sleep(3)
                    jogando = False
                else:
                    # Avançou para o próximo, loop continua e carrega o novo
                    # Pequena pausa dramática entre capítulos
                    time.sleep(1)
            else:
                # Se falhou (Game Over ou saiu para menu)
                jogando = False
    
    # Funções de Bitcoin movidas para bitcoin_and_market.py
    
    def _abrir_manual_hacking(self):
        """Abre o manual de hacking completo do arquivo manual_hacking.py"""
        try:
            from manual_hacking import ManualHacking
            manual = ManualHacking()
            manual.mostrar_menu()
        except ImportError:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERMELHO}ERRO: manual_hacking.py não encontrado{self.RESET}")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.CINZA}Certifique-se que o arquivo existe no diretório raiz.{self.RESET}")
            input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
        except AttributeError:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERMELHO}ERRO: Classe ManualHacking não encontrada{self.RESET}")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.CINZA}Verifique se o arquivo manual_hacking.py possui a classe correta.{self.RESET}")
            input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
        except Exception as e:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERMELHO}ERRO ao abrir manual: {str(e)}{self.RESET}")
            input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
    
    def _mostrar_status_jogo(self, dados_jogador):
        """Mostra status completo do jogo"""
        self._limpar_tela()
        
        print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERDE}╔══════════════════════════════════════╗")
        print(f"{' ' * ((self.term_width - 40) // 2)}{self.VERDE}║          STATUS DO JOGO              ║")
        print(f"{' ' * ((self.term_width - 40) // 2)}{self.VERDE}╚══════════════════════════════════════╝{self.RESET}\n")
        
        # Informações do jogador
        print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}JOGADOR: {self.BRANCO}{dados_jogador['player_name']}")
        print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}CODINOME: {self.VERDE}{dados_jogador['codiname']}")
        print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}CAPÍTULO ATUAL: {self.AMARELO}{dados_jogador.get('current_chapter', 1)}")
        print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}CAPÍTULOS COMPLETADOS: {self.AMARELO}{len(dados_jogador.get('completed_chapters', []))}")
        
        # Bitcoin
        if 'bitcoin_wallet' in dados_jogador:
            btc = dados_jogador['bitcoin_wallet']
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}BITCOIN: {self.VERDE}{btc:.6f} BTC")
        
        # Nível de privacidade
        if 'privacy_level' in dados_jogador:
            privacidade = dados_jogador['privacy_level']
            barra = "█" * (privacidade // 10) + "░" * (10 - privacidade // 10)
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}PRIVACIDADE: {self.VERDE}[{barra}] {privacidade}%")
        
        # Reputação
        if 'reputation' in dados_jogador:
            reputacao = dados_jogador['reputation']
            cor_reputacao = self.VERDE if reputacao >= 0 else self.VERMELHO
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}REPUTAÇÃO: {cor_reputacao}{reputacao}{self.RESET}")
        
        # Acesso à darknet
        if 'darknet_access' in dados_jogador:
            acesso = "SIM" if dados_jogador['darknet_access'] else "NÃO"
            cor_acesso = self.VERDE if dados_jogador['darknet_access'] else self.VERMELHO
            print(f"{' ' * ((self.term_width - 40) // 2)}{self.CIANO}DARKNET: {cor_acesso}{acesso}{self.RESET}")
        
        print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.CINZA}{'─' * 36}{self.RESET}")
        print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.CINZA}Último acesso: {dados_jogador.get('last_seen', 'N/A')}{self.RESET}")
        
        input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA VOLTAR]{self.RESET}")
    
    def _salvar_jogo_atual(self, dados_jogador, arquivo_save):
        """Salva o jogo atual"""
        try:
            # Atualizar timestamp
            dados_jogador['last_seen'] = datetime.now().isoformat()
            
            # Salvar
            with open(arquivo_save, 'w', encoding='utf-8') as f:
                json.dump(dados_jogador, f, indent=2, ensure_ascii=False)
            
            print(f"\n{' ' * ((self.term_width - 30) // 2)}{self.VERDE}Jogo salvo com sucesso!{self.RESET}")
            time.sleep(1)
            
        except Exception as e:
            print(f"\n{' ' * ((self.term_width - 30) // 2)}{self.VERMELHO}Erro ao salvar: {e}{self.RESET}")
            time.sleep(1.5)
    
    def _sair_do_jogo(self, dados_jogador, arquivo_save):
        """Sai do jogo atual, salvando primeiro"""
        # Salvar antes de sair
        self._salvar_jogo_atual(dados_jogador, arquivo_save)
        
        print(f"\n{' ' * ((self.term_width - 30) // 2)}{self.CINZA}Saindo do jogo...{self.RESET}")
        time.sleep(1)
        
        self.jogo_atual = None
        self.running = False
    
    # ========== FUNÇÕES DO MENU PRINCIPAL ==========
    
    def _novo_jogo(self):
        """Cria novo jogo"""
        self._limpar_tela()
        print(f"\n{' ' * ((self.term_width - 20) // 2)}{self.VERDE}NOVO JOGO{self.RESET}")
        print(f"{' ' * ((self.term_width - 20) // 2)}{self.CINZA}════════════════════{self.RESET}\n")
        
        # Nome do jogador
        nome = input(f"{' ' * ((self.term_width - 25) // 2)}{self.BRANCO}SEU NOME > {self.RESET}").strip()
        
        if not nome:
            nome = "Neo"
        
        # Gerar codinome
        codinomes = ["PHANTOM", "ZERO", "VOID", "CRYPT", "GHOST", "NULL", "SHADOW", "NEO",
                    "RIDDLE", "ECHO", "VENOM", "SILENT", "FROST", "BLADE", "NIGHT", "REAPER",
                    "CYPHER", "RAVEN", "STORM", "STEALTH", "PYTHON", "JAVA", "RUST", "KALI",
                    "DARK", "SMOKE", "ASH", "EMBER", "FLAME", "ICE", "STONE", "IRON",
                    "ORACLE", "PROPHET", "SAGE", "WIZARD", "SORCER", "MAGE", "WARLOCK",
                    "HUNTER", "SENTRY", "WATCHER", "GUARDIAN", "SENTINEL", "DEFENDER",
                    "NINJA", "SAMURAI", "RONIN", "SHINOBI", "KAGE", "ONI", "KITSUNE"]
        codinome = random.choice(codinomes) + "_" + str(random.randint(10, 99))
        
        print(f"\n{' ' * ((self.term_width - 30) // 2)}{self.CINZA}APELIDO DESIGNADO: {self.VERDE}{codinome}{self.RESET}")
        time.sleep(0.5)
        
        # Criar estado do jogador
        dados_jogador = {
            'player_name': nome,
            'codiname': codinome,
            'current_chapter': 1,
            'completed_chapters': [],
            'score': 0,
            'inventory': [],
            'bitcoin_wallet': 0.005,
            'privacy_level': 80,
            'darknet_access': False,
            'reputation': 0,
            'last_seen': datetime.now().isoformat()
        }
        
        # Salvar jogo
        arquivo_save = self._salvar_jogo(dados_jogador, f"saves/{codinome}_initial.json")
        
        print(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}CRIANDO IDENTIDADE...")
        time.sleep(0.5)
        
        # MOSTRA ANIMAÇÃO DO TERMINAL KALI
        self._mostrar_terminal_kali(codinome)
        
        # Ir para menu de jogo (NÃO inicia capítulo automaticamente)
        self._mostrar_menu_jogo(dados_jogador, arquivo_save)
    
    def _carregar_jogo_menu(self):
        """Carrega jogo salvo"""
        self._limpar_tela()
        print(f"\n{' ' * ((self.term_width - 20) // 2)}{self.VERDE}CARREGAR JOGO{self.RESET}")
        print(f"{' ' * ((self.term_width - 20) // 2)}{self.CINZA}════════════════════{self.RESET}\n")
        
        saves = self._listar_saves_disponiveis()
        
        if not saves:
            print(f"{' ' * ((self.term_width - 30) // 2)}{self.VERMELHO}NENHUM ARQUIVO SALVO ENCONTRADO{self.RESET}")
            time.sleep(1.5)
            return
        
        # Listar saves
        for i, save in enumerate(saves, 1):
            espacamento = " " * ((self.term_width - 50) // 2)
            print(f"{espacamento}{self.CINZA}[{i}] {self.VERDE}{save['codinome']}")
            print(f"{espacamento}    {save['nome_jogador']} - Capítulo {save['capitulo']}")
            if 'bitcoin' in save:
                print(f"{espacamento}    Bitcoin: {save['bitcoin']:.4f} BTC")
            print(f"{espacamento}    {save['data'][:10]}{self.RESET}\n")
        
        try:
            escolha = input(f"{' ' * ((self.term_width - 20) // 2)}{self.BRANCO}SELECIONE (0 para voltar) > {self.RESET}").strip()
            if escolha == "0":
                return
            
            idx = int(escolha) - 1
            if 0 <= idx < len(saves):
                dados_jogador = self._carregar_jogo(saves[idx]['arquivo'])
                if dados_jogador:
                    print(f"\n{' ' * ((self.term_width - 25) // 2)}{self.VERDE}CARREGANDO...{self.RESET}")
                    time.sleep(0.5)
                    
                    # Mostra animação rápida do terminal
                    self._mostrar_terminal_kali(dados_jogador['codiname'])
                    
                    # Ir para menu de jogo
                    self._mostrar_menu_jogo(dados_jogador, saves[idx]['arquivo'])
                else:
                    print(f"\n{' ' * ((self.term_width - 30) // 2)}{self.VERMELHO}ERRO AO CARREGAR ARQUIVO{self.RESET}")
                    time.sleep(1)
        except (ValueError, IndexError):
            print(f"\n{' ' * ((self.term_width - 20) // 2)}{self.VERMELHO}OPÇÃO INVÁLIDA{self.RESET}")
            time.sleep(1)
        except Exception as e:
            print(f"\n{' ' * ((self.term_width - 20) // 2)}{self.VERMELHO}ERRO: {e}{self.RESET}")
            time.sleep(1)
    
    def _abrir_manual(self):
        """Abre manual de hacking do arquivo manual_hacking.py"""
        self._limpar_tela()
        print(f"\n{' ' * ((self.term_width - 25) // 2)}{self.VERDE}ACESSANDO MANUAL...{self.RESET}")
        time.sleep(0.5)
        
        try:
            # Importar manual completo
            from manual_hacking import ManualHacking
            manual = ManualHacking()
            manual.mostrar_menu()
        except ImportError:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERMELHO}ERRO: manual_hacking.py não encontrado{self.RESET}")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.CINZA}Certifique-se que o arquivo existe no diretório raiz.{self.RESET}")
            input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
        except AttributeError:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERMELHO}ERRO: Classe ManualHacking não encontrada{self.RESET}")
            print(f"{' ' * ((self.term_width - 50) // 2)}{self.CINZA}Verifique se o arquivo manual_hacking.py possui a classe correta.{self.RESET}")
            input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
        except Exception as e:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{self.VERMELHO}ERRO ao abrir manual: {str(e)}{self.RESET}")
            input(f"\n{' ' * ((self.term_width - 25) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
    
    def _informacoes_sistema(self):
        """Informações do sistema"""
        self._limpar_tela()
        print(f"\n{' ' * ((self.term_width - 20) // 2)}{self.VERDE}INFORMAÇÕES DO SISTEMA{self.RESET}")
        print(f"{' ' * ((self.term_width - 20) // 2)}{self.CINZA}════════════════════{self.RESET}\n")
        
        info = [
            f"{self.CINZA}ROOT EVOLUTION v2.1{self.RESET}",
            f"{self.CINZA}Build: {datetime.now().strftime('%Y%m%d')}{self.RESET}",
            f"{self.CINZA}Terminal: {self.term_width}x{self.term_height}{self.RESET}",
            f"{self.CINZA}Desenvolvedor: Pedro Antônio Heinrich{self.RESET}",
            f"{self.CINZA}Contato: @streetegist{self.RESET}",
            "",
            f"{self.CINZA}« Qualquer semelhança com a realidade não é coincidência. »{self.RESET}",
        ]
        
        for linha in info:
            espacamento = " " * ((self.term_width - len(linha.strip())) // 2)
            print(f"{espacamento}{linha}")
        
        input(f"\n{' ' * ((self.term_width - 20) // 2)}{self.CINZA}[ENTER PARA CONTINUAR]{self.RESET}")
    
    def _sair_jogo(self):
        """Sai do jogo"""
        self._limpar_tela()
        
        # Mensagem de despedida
        mensagens = [
            "ENCERRANDO CONEXÃO...",
            "LIMPANDO RASTROS...",
            "CRIPTOGRAFANDO LOGS...",
            "ATÉ MAIS.",
            "LEMBRE-SE:",
            "O SISTEMA ESTÁ VIGIANDO.",
            "MAS NÓS TAMBÉM ESTAMOS."
        ]
        
        print("\n" * (self.term_height // 3))
        
        for msg in mensagens:
            espacamento = " " * ((self.term_width - len(msg)) // 2)
            if msg == "ATÉ MAIS.":
                print(f"{espacamento}{self.VERMELHO}{msg}{self.RESET}")
            else:
                print(f"{espacamento}{self.CINZA}{msg}{self.RESET}")
            time.sleep(0.2)
        
        time.sleep(1)
        self._limpar_tela()
        self.running = False
    
    # ========== EXECUTAR ==========

    def executar(self):
        """FLUXO CORRETO - Boot sempre aparece!"""
        try:
            # LÓGICA: Boot sequence SEMPRE aparece após introdução
            
            # SE PRIMEIRA VEZ
            if not self.intro_mostrada:
                self.pular_introducao = False
                
                # 1. Introdução (pode ser pulada)
                self._mostrar_introducao_mr_robot()
                
                # 2. Boot sequence SEMPRE (mesmo se pulou)
                self._sequencia_boot()  # ← SEMPRE CHAMADO!
                
                # Marcar como visto
                self.intro_mostrada = True
                
            # SE JÁ VIU ANTES
            else:
                # Boot sequence SEMPRE (para atmosfera)
                self._sequencia_boot()  # ← SEMPRE CHAMADO!
        
            # 3. Menu principal
            self._mostrar_menu_principal()
               
        except KeyboardInterrupt:
            print(f"\n{self.VERMELHO}[SISTEMA] Execução interrompida{self.RESET}")
            self._sair_jogo()
        except Exception as e:
            print(f"\n{self.VERMELHO}[SISTEMA] ERRO: {str(e)}{self.RESET}")
            time.sleep(2)
            self._sair_jogo()

# ========== PONTO DE ENTRADA ==========
if __name__ == "__main__":
    # Adicionar cores extras se necessário
    if 'C' not in globals():
        class C:
            VERDE = '\033[92m'
            VERMELHO = '\033[91m'
            BRANCO = '\033[97m'
            CINZA = '\033[90m'
            CIANO = '\033[96m'
            RESET = '\033[0m'
    
    menu = IntroMenu()
    menu.executar()