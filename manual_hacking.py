#!/usr/bin/env python3
"""
MANUAL DE HACKING - ROOT EVOLUTION v2.0
Referência completa de comandos e técnicas - Interface Mr. Robot Style
"""
import time
import os
import sys
import textwrap
from shutil import get_terminal_size

# Tentar importar utils para cores padronizadas
try:
    from utils.terminal_kali import C, digitar, limpar_tela, header_kali_v2
    # Wrapper para compatibilidade se necessário
    def _digitar_wrapper(texto, delay=0.01, cor=C.BRANCO, fim='\n'):
        digitar(texto, delay=delay, cor=cor)
        print(end=fim)
except ImportError:
    # Fallback caso não encontre utils (uso standalone)
    class C:
        VERDE = '\033[92m'
        CIANO = '\033[96m'
        VERMELHO = '\033[91m'
        AMARELO = '\033[93m'
        BRANCO = '\033[97m'
        CINZA = '\033[90m'
        ROXO = '\033[95m'
        AZUL = '\033[94m'
        RESET = '\033[0m'
        NEGRITO = '\033[1m'
    
    def limpar_tela():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def digitar(texto, delay=0.01, cor=C.BRANCO):
        print(f"{cor}{texto}{C.RESET}")

def obter_largura_terminal():
    try:
        return get_terminal_size().columns
    except:
        return 80

def imprimir_separador(tipo="duplo"):
    largura = obter_largura_terminal()
    if tipo == "duplo":
        print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    elif tipo == "simples":
        print(f"{C.CINZA}{'─' * largura}{C.RESET}")

def imprimir_titulo_secao(titulo, icone="►"):
    limpar_tela()
    imprimir_separador("duplo")
    largura = obter_largura_terminal()
    texto = f"{icone} {titulo} {icone}"
    print(f"{C.AMARELO}{texto.center(largura)}{C.RESET}")
    imprimir_separador("duplo")
    print()

def imprimir_comando_bonito(comando, descricao, exemplo=None):
    largura = obter_largura_terminal() - 4
    
    print(f"{C.VERDE}┌──[{C.BRANCO}{comando}{C.VERDE}]")
    
    # Descrição com quebra de linha
    desc_lines = textwrap.wrap(descricao, width=largura)
    for line in desc_lines:
        print(f"{C.VERDE}│  {C.CINZA}{line}")
    
    if exemplo:
        print(f"{C.VERDE}│  {C.AMARELO}Ex: {C.CIANO}{exemplo}")
    
    print(f"{C.VERDE}└──────────────────────────────────────{C.RESET}")

# ================= SEÇÕES DO MANUAL =================

def mostrar_comandos_basicos():
    imprimir_titulo_secao("COMANDOS BÁSICOS DO TERMINAL", "💻")
    
    cmds = [
        ("ls", "Lista arquivos no diretório", "ls -la"),
        ("cd", "Navega entre pastas", "cd /var/www"),
        ("cat", "Lê conteúdo de arquivos", "cat senha.txt"),
        ("grep", "Busca texto dentro de arquivos/saída", "cat log.txt | grep 'erro'"),
        ("chmod", "Altera permissões de arquivos", "chmod +x exploit.py"),
        ("sudo", "Executa como Super Usuário (Root)", "sudo su"),
        ("pwd", "Mostra diretório atual", "pwd"),
        ("man", "Manual do sistema Linux", "man nmap")
    ]
    
    for c, d, e in cmds:
        imprimir_comando_bonito(c, d, e)
    
    input(f"\n{C.CINZA}[ENTER para voltar]{C.RESET}")

def mostrar_reconhecimento():
    imprimir_titulo_secao("RECONHECIMENTO & SCANNING", "👁️")
    print(f"{C.CINZA}Antes de atacar, você precisa conhecer o alvo.{C.RESET}\n")
    
    cmds = [
        ("nmap", "Scanner de rede e portas. Essencial.", "nmap -sS -p- 192.168.1.1"),
        ("whois", "Informações de registro de domínio", "whois alvo.com"),
        ("dig", "Consultas DNS detalhadas", "dig alvo.com ANY"),
        ("theHarvester", "Coleta emails e subdomínios (OSINT)", "theHarvester -d alvo.com -b google")
    ]
    
    for c, d, e in cmds:
        imprimir_comando_bonito(c, d, e)
        
    input(f"\n{C.CINZA}[ENTER para voltar]{C.RESET}")

def mostrar_ataques_web():
    imprimir_titulo_secao("ATAQUES WEB & SQL INJECTION", "🌐")
    
    print(f"{C.ROXO}Técnicas para explorar falhas em websites.{C.RESET}\n")
    
    cmds = [
        ("SQL Injection", "Inserir comandos SQL em inputs", "' OR '1'='1"),
        ("XSS (Cross-Site Scripting)", "Injetar scripts maliciosos", "<script>alert(1)</script>"),
        ("LFI (Local File Inclusion)", "Ler arquivos do servidor", "../../../etc/passwd"),
        ("sqlmap", "Ferramenta automática de SQLi", "sqlmap -u http://site.com/id=1 --dbs")
    ]
    
    for c, d, e in cmds:
        imprimir_comando_bonito(c, d, e)

    print(f"\n{C.AMARELO}[!] DICA: Sempre verifique o código-fonte (View Source){C.RESET}")
    input(f"\n{C.CINZA}[ENTER para voltar]{C.RESET}")

def mostrar_criptografia():
    imprimir_titulo_secao("CRIPTOGRAFIA & DECODIFICAÇÃO", "🔓")
    
    print(f"{C.CIANO}Desvende mensagens ocultas e arquivos protegidos.{C.RESET}\n")
    
    cmds = [
        ("base64 detect", "Identificar base64", "Termina com '=' (ex: bXlfcGFzcw==)"),
        ("base64 decode", "Decodificar mensagem", "echo 'bXlfcGFzcw==' | base64 -d"),
        ("base64 encode", "Codificar mensagem", "echo 'senha' | base64"),
        ("dec gpg", "Descriptografar arquivo GPG", "dec gpg <chave_numérica>"),
        ("rot13", "Cifra de César simples", "tr 'A-Za-z' 'N-ZA-Mn-za-m'"),
        ("steghide", "Esteganografia (arquivos ocultos)", "steghide extract -sf img.jpg")
    ]
    
    for c, d, e in cmds:
        imprimir_comando_bonito(c, d, e)

    print(f"\n{C.AMARELO}[!] DICA: Base64 é muito comum em CTFs. Se vir texto aleatório, tente decode!{C.RESET}")
    input(f"\n{C.CINZA}[ENTER para voltar]{C.RESET}")

def mostrar_cracking():
    imprimir_titulo_secao("QUEBRA DE SENHAS (CRACKING)", "🔐")
    
    cmds = [
        ("john", "John The Ripper - Quebra hashes", "john --wordlist=rockyou.txt hash.txt"),
        ("hydra", "Brute-force em serviços (SSH, FTP)", "hydra -l user -P pass.txt ssh://alvo"),
        ("hashcat", "Cracker avançado (usa GPU)", "hashcat -m 0 hash.txt lista.txt")
    ]
    
    for c, d, e in cmds:
        imprimir_comando_bonito(c, d, e)
        
    input(f"\n{C.CINZA}[ENTER para voltar]{C.RESET}")

def mostrar_anonimato():
    imprimir_titulo_secao("ANONIMATO & RASTROS", "👻")
    
    print(f"{C.VERMELHO}Um hacker pego é um hacker ruim.{C.RESET}\n")
    
    cmds = [
        ("tor", "Rede de anonimato", "service tor start"),
        ("macchanger", "Troca seu endereço MAC físico", "macchanger -r eth0"),
        ("shred", "Deleta arquivos permanentemente", "shred -u log.txt"),
        ("history -c", "Limpa histórico do terminal", "history -c")
    ]
    
    for c, d, e in cmds:
        imprimir_comando_bonito(c, d, e)
        
    input(f"\n{C.CINZA}[ENTER para voltar]{C.RESET}")

# ================= MENU PRINCIPAL =================

class ManualHacking:
    def mostrar_menu(self):
        while True:
            limpar_tela()
            imprimir_separador("duplo")
            print(f"{C.AMARELO}             📖 MANUAL DE HACKING v2.0{C.RESET}")
            print(f"{C.CINZA}      A Conhecimento é a arma mais poderosa.{C.RESET}")
            imprimir_separador("duplo")
            print()
            
            opcoes = [
                "Comandos Básicos Linux",
                "Reconhecimento & Scanning",
                "Ataques Web (SQLi, XSS)",
                "Criptografia & Decodificação",
                "Cracking de Senhas",
                "Anonimato & Limpeza",
                "Ferramentas (Hex/Bin)",
                "Sair"
            ]
            
            for i, op in enumerate(opcoes, 1):
                # Formatação bonita do menu
                prefixo = "└──" if i == len(opcoes) else "├──"
                cor = C.VERMELHO if i == len(opcoes) else C.BRANCO
                print(f"{C.VERDE} {prefixo} {C.AMARELO}[{i}] {cor}{op}{C.RESET}")
                
            print()
            imprimir_separador("simples")
            
            try:
                escolha = input(f"{C.VERDE} man > {C.RESET}").strip()
            except:
                break
                
            if escolha == "1":
                mostrar_comandos_basicos()
            elif escolha == "2":
                mostrar_reconhecimento()
            elif escolha == "3":
                mostrar_ataques_web()
            elif escolha == "4":
                mostrar_criptografia()
            elif escolha == "5":
                mostrar_cracking()
            elif escolha == "6":
                mostrar_anonimato()
            elif escolha == "7":
                self.mostrar_ferramentas_conversao()
            elif escolha == "8" or escolha == "0":
                break

    def mostrar_ferramentas_conversao(self):
        """Menu de ferramentas de conversão dentro do manual"""
        while True:
            limpar_tela()
            imprimir_separador("duplo")
            print(f"{C.AMARELO}             🛠️  FERRAMENTAS HACKER (BIN/HEX){C.RESET}")
            imprimir_separador("duplo")
            
            opcoes = [
                "Texto -> Hexadecimal",
                "Hexadecimal -> Texto",
                "Texto -> Binário",
                "Binário -> Texto",
                "Decimal -> Hex/Bin",
                "Voltar"
            ]
            
            for i, op in enumerate(opcoes, 1):
                prefixo = "└──" if i == len(opcoes) else "├──"
                print(f"{C.VERDE} {prefixo} {C.AMARELO}[{i}] {C.BRANCO}{op}{C.RESET}")
                
            print()
            imprimir_separador("simples")
            
            try:
                escolha = input(f"{C.VERDE} tools > {C.RESET}").strip()
                
                if escolha == "6" or escolha == "0": break
                
                if escolha == "1":
                    txt = input(f"\n{C.CINZA}Digite o texto: {C.RESET}")
                    res = " ".join("{:02x}".format(ord(c)) for c in txt)
                    print(f"{C.VERDE}HEX: {C.BRANCO}{res}{C.RESET}")
                elif escolha == "2":
                    try:
                        hexa = input(f"\n{C.CINZA}Digite o Hex (ex: 41 42): {C.RESET}").replace(" ", "")
                        res = bytes.fromhex(hexa).decode('utf-8')
                        print(f"{C.VERDE}TEXTO: {C.BRANCO}{res}{C.RESET}")
                    except: print(f"{C.VERMELHO}Hex inválido.{C.RESET}")
                elif escolha == "3":
                    txt = input(f"\n{C.CINZA}Digite o texto: {C.RESET}")
                    res = " ".join(format(ord(c), '08b') for c in txt)
                    print(f"{C.VERDE}BIN: {C.BRANCO}{res}{C.RESET}")
                elif escolha == "4":
                    try:
                        binario = input(f"\n{C.CINZA}Digite o Binário: {C.RESET}").replace(" ", "")
                        chars = [binario[i:i+8] for i in range(0, len(binario), 8)]
                        res = "".join(chr(int(c, 2)) for c in chars)
                        print(f"{C.VERDE}TEXTO: {C.BRANCO}{res}{C.RESET}")
                    except: print(f"{C.VERMELHO}Binário inválido.{C.RESET}")
                elif escolha == "5":
                    try:
                        dec = int(input(f"\n{C.CINZA}Digite o Decimal: {C.RESET}"))
                        print(f"{C.VERDE}HEX: {hex(dec)[2:].upper()} | BIN: {bin(dec)[2:]}{C.RESET}")
                    except: print(f"{C.VERMELHO}Número inválido.{C.RESET}")
                
                input(f"\n{C.CINZA}[ENTER]{C.RESET}")
            except:
                break

if __name__ == "__main__":
    man = ManualHacking()
    man.mostrar_menu()

class Cores:
    VERDE = '\033[92m'
    CIANO = '\033[96m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    BRANCO = '\033[97m'
    CINZA = '\033[90m'
    ROXO = '\033[95m'
    AZUL = '\033[94m'
    RESET = '\033[0m'
    NEGRITO = '\033[1m'
    REVERSO = '\033[7m'
    FUNDO_VERDE = '\033[42m'
    FUNDO_VERMELHO = '\033[41m'
    # Cores adicionais para Mr. Robot style
    VERDE_ESCURO = '\033[32m'
    CIANO_ESCURO = '\033[36m'
    CINZA_CLARO = '\033[37m'

C = Cores()

def obter_largura_terminal():
    """Retorna a largura atual do terminal"""
    return get_terminal_size().columns

def imprimir_linha(caractere="─", estilo="normal"):
    """Imprime uma linha horizontal estilo Mr. Robot"""
    largura = obter_largura_terminal() - 2
    
    if estilo == "dupla":
        print(f"{C.VERDE}╔{caractere * largura}╗{C.RESET}")
    elif estilo == "fundo":
        print(f"{C.VERDE}╠{caractere * largura}╣{C.RESET}")
    elif estilo == "inferior":
        print(f"{C.VERDE}╚{caractere * largura}╝{C.RESET}")
    else:
        print(f"{C.VERDE}{caractere * (largura + 2)}{C.RESET}")

def imprimir_titulo(titulo):
    """Imprime título centralizado com bordas estilo hacker"""
    largura = obter_largura_terminal() - 2
    titulo_fmt = f"► {titulo} ◄"
    titulo_centralizado = titulo_fmt.center(largura, "═")
    print(f"{C.CIANO}{C.NEGRITO}{titulo_centralizado}{C.RESET}")

def imprimir_secao(titulo):
    """Imprime título de seção com efeito Mr. Robot"""
    limpar_tela()
    largura = obter_largura_terminal()
    print()
    imprimir_linha("═", "dupla")
    imprimir_titulo(titulo)
    imprimir_linha("═", "fundo")

def imprimir_texto(texto, cor=C.BRANCO, alinhamento="left"):
    """Imprime texto sem bordas laterais"""
    largura = obter_largura_terminal() - 2
    linhas = textwrap.wrap(texto, width=largura)
    
    for linha in linhas:
        if alinhamento == "center":
            linha_formatada = linha.center(largura)
        elif alinhamento == "right":
            linha_formatada = linha.rjust(largura)
        else:
            linha_formatada = linha.ljust(largura)
        print(f"{cor}{linha_formatada}{C.RESET}")

def imprimir_item(numero, titulo, descricao, cor=C.CIANO):
    """Imprime um item do menu com seta hacker"""
    largura = obter_largura_terminal() - 2
    numero_titulo = f"{C.AMARELO}[{numero}]{C.RESET} {C.CIANO}{titulo}{C.RESET}"
    linha = f"{numero_titulo}"
    
    print(f" {linha}")
    
    # Descrição com símbolo hacker
    if descricao:
        desc_linhas = textwrap.wrap(f"{C.CINZA}    ➜ {descricao}", width=largura-3)
        for linha_desc in desc_linhas:
            print(f"{linha_desc}")

def imprimir_comando(comando, exemplo, descricao):
    """Imprime um comando com formatação hacker"""
    largura = obter_largura_terminal() - 2
    
    # Comando em destaque
    comando_line = f"{C.AMARELO}$ {C.CIANO}{C.NEGRITO}{comando}{C.RESET}"
    print(f" {comando_line}")
    
    # Exemplo em verde (cor de terminal hacker)
    if exemplo:
        exemplo_linhas = textwrap.wrap(f"{C.CINZA}  ├─ {C.VERDE}{exemplo}", width=largura-3)
        for linha_ex in exemplo_linhas:
            print(f"{linha_ex}")
    
    # Descrição em cinza
    if descricao:
        desc_linhas = textwrap.wrap(f"{C.CINZA}  └─ {descricao}", width=largura-3)
        for linha_desc in desc_linhas:
            print(f"{linha_desc}")
    
    print()

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Usar a função padronizada de digitação do utils
from utils.terminal_kali import digitar as _digitar_padrao

def digitar(texto, delay=0.01, cor=C.BRANCO, fim='\n'):
    """Wrapper compatível que encaminha para `utils.terminal_kali.digitar`.

    Mantém assinatura simples usada historicamente neste módulo.
    """
    return _digitar_padrao(texto, delay=delay, cor=cor, fim=fim)

def exibir_banner():
    """Exibe banner estilo Mr. Robot com efeitos"""
    limpar_tela()
    largura = obter_largura_terminal()
    
    # Banner principal
    banner_linhas = [
        f"{C.VERDE}{'═' * largura}{C.RESET}",
        f"{C.CIANO}{C.NEGRITO}  ███▒░ HACKING MANUAL - ROOT EVOLUTION v2.0 ░▒███{C.RESET}",
        f"{C.CINZA}  [*] Sistema   : GNU/Linux  │  [*] Acesso: root  │  [*] Status: Conectado{C.RESET}",
        f"{C.CINZA}  [*] IP Local  : 192.168.1.108  │  [*] Gateway: Tor  │  [*] Anonimato: 100%{C.RESET}",
        f"{C.VERDE}{'═' * largura}{C.RESET}",
    ]
    
    for linha in banner_linhas:
        print(linha)
    
    print()
    
    # Mensagem de acesso com digitação
    print(f"{C.CINZA}[*] ", end="")
    digitar("Acessando banco de dados do manual de hacking...", delay=0.01, cor=C.VERDE)
    time.sleep(0.5)
    print(f"{C.CINZA}[✓] {C.VERDE}Acesso concedido!{C.RESET}")
    print()

def exibir_manual():
    """Exibe o manual completo de hacking com estetica Mr. Robot"""
    while True:
        exibir_banner()
        
        # ÍNDICE PRINCIPAL
        imprimir_linha("═", "dupla")
        imprimir_titulo("📖 MENU PRINCIPAL - SELECIONE UMA OPÇÃO")
        imprimir_linha("═", "fundo")
        print()
        
        menu_itens = [
            ("Comandos Básicos do Terminal", "Comandos essenciais para navegação e controle"),
            ("Manual de Comandos Linux", "Guia completo de comandos do GNU/Linux"),
            ("Técnicas de Reconhecimento", "Coleta de informações, footprinting e scanning"),
            ("Exploração de Redes", "SSH, FTP, varredura de portas e vulnerabilidades"),
            ("Ataques Web", "SQLi, XSS, CSRF, Directory Traversal, RCE"),
            ("Cracking de Senhas", "Força bruta, dicionários, hash cracking"),
            ("Análise Forense", "Logs, investigação, rastreamento de atividades"),
            ("Ofuscação e Anonimato", "VPN, TOR, proxies, anti-forense avançado"),
            ("Ferramentas Especiais", "Nmap, Metasploit, Wireshark, Burp Suite"),
            ("Sair do Sistema", "Encerrar conexão e retornar")
        ]
        
        for i, (titulo, desc) in enumerate(menu_itens, 1):
            imprimir_item(str(i), titulo, desc)
        
        imprimir_linha("═", "inferior")
        print()
        
        try:
            escolha = input(f"{C.VERDE}root@manual:~${C.RESET} ").strip()
            
            if escolha == "10" or escolha.lower() == "exit" or escolha == "0":
                limpar_tela()
                print(f"\n{C.VERDE}╔════════════════════════════════════════════╗{C.RESET}")
                print(f"{C.VERDE}║{C.CIANO}  [*] Encerrando conexão do manual...{C.RESET}{C.VERDE}       ║{C.RESET}")
                print(f"{C.VERDE}║{C.VERMELHO}  [!] Limpando rastros...{C.RESET}{C.VERDE}                  ║{C.RESET}")
                print(f"{C.VERDE}║{C.AMARELO}  [✓] Desconectado com sucesso!{C.RESET}{C.VERDE}            ║{C.RESET}")
                print(f"{C.VERDE}╚════════════════════════════════════════════╝{C.RESET}\n")
                time.sleep(1)
                break
            elif escolha == "1":
                mostrar_comandos_basicos()
            elif escolha == "2":
                mostrar_manual_linux()
            elif escolha == "3":
                mostrar_reconhecimento()
            elif escolha == "4":
                mostrar_exploracao_redes()
            elif escolha == "5":
                mostrar_ataques_web()
            elif escolha == "6":
                mostrar_cracking_senhas()
            elif escolha == "7":
                mostrar_analise_forense()
            elif escolha == "8":
                mostrar_ofuscacao()
            elif escolha == "9":
                mostrar_ferramentas()
            else:
                print(f"\n{C.VERMELHO}[!] Opção inválida. Digite 1-10 ou 'exit'{C.RESET}")
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            print(f"\n\n{C.VERMELHO}[!] Conexão interrompida pelo usuário.{C.RESET}")
            time.sleep(1)
            break

def mostrar_comandos_basicos():
    """Seção 1: Comandos básicos do terminal com estetica Mr. Robot"""
    imprimir_secao("1. COMANDOS BÁSICOS DO TERMINAL")
    print()
    
    comandos = [
        ("ls", "ls -la", "Lista arquivos com detalhes (incluindo ocultos)"),
        ("cd", "cd /var/www && cd ..", "Navega entre diretórios do sistema"),
        ("pwd", "pwd", "Mostra o caminho completo do diretório atual"),
        ("cp", "cp arquivo.txt backup/", "Copia arquivos ou diretórios inteiros"),
        ("mv", "mv antigo.txt novo.txt", "Move ou renomeia arquivos/pastas"),
        ("rm", "rm -rf pasta/", "Remove arquivos/diretórios (⚠️ CUIDADO!)"),
        ("mkdir", "mkdir nova_pasta", "Cria um novo diretório"),
        ("cat", "cat config.txt | grep 'password'", "Exibe conteúdo de arquivo ou combina"),
        ("echo", "echo 'texto' > arquivo.txt", "Escreve texto em arquivo ou exibe"),
        ("nano/vim", "nano script.sh", "Editores de texto poderosos"),
        ("chmod", "chmod +x script.sh", "Altera permissões de arquivo (modo hacker)"),
        ("sudo", "sudo apt update", "Executa comando com privilégios de root"),
        ("man", "man grep", "Acessa manual de ajuda de qualquer comando"),
        ("clear", "clear", "Limpa a tela do terminal"),
        ("whoami", "whoami", "Mostra qual usuário você está usando"),
        ("history", "history | tail -20", "Mostra histórico de últimos comandos"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    imprimir_linha("─", "inferior")
    print()
    imprimir_texto(f"{C.AMARELO}[*] DICA: Use TAB para autocompletar e Ctrl+C para cancelar!{C.RESET}", C.AMARELO)
    imprimir_linha("─", "inferior")
    input(f"\n{C.CINZA}[ Pressione ENTER para retornar ao menu ]{C.RESET}")


def mostrar_manual_linux():
    """MANUAL COMPLETO DE COMANDOS LINUX"""
    limpar_tela()
    
    while True:
        imprimir_linha()
        imprimir_titulo("📚 MANUAL COMPLETO DE COMANDOS LINUX")
        imprimir_linha("─")
        
        categorias = [
            ("Sistema de Arquivos", "Navegação e manipulação"),
            ("Processos", "Gerenciamento de processos"),
            ("Rede", "Comandos de rede e conectividade"),
            ("Usuários e Permissões", "Controle de acesso"),
            ("Pesquisa e Filtro", "Busca e processamento"),
            ("Compactação", "Arquivos compactados"),
            ("Monitoramento", "Sistema e desempenho"),
            ("Voltar ao Menu Principal", "Retornar")
        ]
        
        for i, (titulo, desc) in enumerate(categorias, 1):
            imprimir_item(str(i), titulo, desc)
        
        imprimir_linha("─")
        
        escolha = input(f"\n{C.VERDE}Select category (1-8): {C.RESET}").strip()
        
        if escolha == "8" or escolha == "0":
            break
        elif escolha == "1":
            mostrar_categoria_arquivos()
        elif escolha == "2":
            mostrar_categoria_processos()
        elif escolha == "3":
            mostrar_categoria_rede()
        elif escolha == "4":
            mostrar_categoria_usuarios()
        elif escolha == "5":
            mostrar_categoria_pesquisa()
        elif escolha == "6":
            mostrar_categoria_compactacao()
        elif escolha == "7":
            mostrar_categoria_monitoramento()
        else:
            print(f"{C.VERMELHO}[!] Invalid option{C.RESET}")

def mostrar_categoria_arquivos():
    """Categoria: Sistema de Arquivos com estetica Mr. Robot"""
    imprimir_secao("📁 SISTEMA DE ARQUIVOS")
    print()
    
    comandos = [
        ("ls", "ls -lh", "Lista com tamanhos legíveis para humanos"),
        ("tree", "tree -L 3", "Mostra estrutura em árvore do diretório"),
        ("find", "find / -name '*.conf' -type f", "Busca arquivos por padrão em todo sistema"),
        ("locate", "locate passwd", "Busca rápida no banco de dados do sistema"),
        ("stat", "stat arquivo.txt", "Informações detalhadas do arquivo (metadados)"),
        ("du", "du -sh * | sort -rh", "Uso de espaço em disco por diretório"),
        ("df", "df -h", "Espaço livre em disco em todos os pontos"),
        ("mount", "mount | grep /dev/sd", "Sistemas de arquivos montados no sistema"),
        ("ln", "ln -s /caminho/origem atalho", "Cria link simbólico (atalho para arquivo)"),
        ("touch", "touch novo_arquivo.txt", "Cria arquivo vazio ou altera timestamp"),
        ("file", "file arquivo.desconhecido", "Identifica tipo de arquivo automaticamente"),
        ("diff", "diff arquivo1.txt arquivo2.txt", "Compara dois arquivos e mostra diferenças"),
        ("rsync", "rsync -avz origem/ destino/", "Sincroniza diretórios de forma eficiente"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    imprimir_linha("─", "inferior")
    input(f"\n{C.CINZA}[ Pressione ENTER para retornar ]{C.RESET}")

def mostrar_categoria_processos():
    """Categoria: Processos"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("⚙️  GERENCIAMENTO DE PROCESSOS")
    imprimir_linha("─")
    
    comandos = [
        ("ps", "ps aux | grep apache", "Lista processos em execução"),
        ("top", "top", "Monitor de processos em tempo real"),
        ("htop", "htop", "Top melhorado (interativo)"),
        ("kill", "kill -9 1234", "Mata processo pelo PID"),
        ("pkill", "pkill firefox", "Mata processo pelo nome"),
        ("nice", "nice -n 10 comando", "Altera prioridade do processo"),
        ("renice", "renice 5 -p 1234", "Altera prioridade de processo em execução"),
        ("bg / fg", "bg %1 ou fg %1", "Coloca processo em background/foreground"),
        ("jobs", "jobs", "Lista jobs em background"),
        ("nohup", "nohup script.sh &", "Executa processo que sobrevive ao logout"),
        ("systemctl", "systemctl status ssh", "Controla serviços systemd"),
        ("service", "service apache2 restart", "Controla serviços (SysV)"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_categoria_rede():
    """Categoria: Rede"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("🌐 COMANDOS DE REDE")
    imprimir_linha("─")
    
    comandos = [
        ("ifconfig / ip", "ip addr show", "Configuração de interfaces"),
        ("ping", "ping -c 4 google.com", "Testa conectividade"),
        ("traceroute", "traceroute facebook.com", "Traça rota até destino"),
        ("netstat", "netstat -tulpn", "Conexões de rede ativas"),
        ("ss", "ss -tunap", "Netstat moderno (mais rápido)"),
        ("curl", "curl -I https://exemplo.com", "Transferência de dados via URL"),
        ("wget", "wget -c http://site.com/arquivo.iso", "Download de arquivos"),
        ("dig", "dig mx google.com", "Consultas DNS avançadas"),
        ("nslookup", "nslookup exemplo.com", "Consulta DNS básica"),
        ("whois", "whois dominio.com", "Informações de registro"),
        ("route", "route -n", "Tabela de roteamento"),
        ("iptables", "iptables -L -n -v", "Firewall do Linux"),
        ("tcpdump", "tcpdump -i eth0 port 80", "Sniffer de pacotes"),
        ("nc", "nc -zv host 22", "Netcat - canivete suíço da rede"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_categoria_usuarios():
    """Categoria: Usuários e Permissões"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("👥 USUÁRIOS E PERMISSÕES")
    imprimir_linha("─")
    
    comandos = [
        ("who", "who", "Usuários logados"),
        ("w", "w", "Usuários logados e processos"),
        ("last", "last", "Histórico de logins"),
        ("id", "id", "Identidade do usuário"),
        ("groups", "groups usuario", "Grupos do usuário"),
        ("useradd", "sudo useradd -m novo_user", "Adiciona usuário"),
        ("passwd", "sudo passwd usuario", "Altera senha"),
        ("chown", "chown usuario:grupo arquivo", "Altera dono do arquivo"),
        ("chgrp", "chgrp grupo arquivo", "Altera grupo do arquivo"),
        ("umask", "umask 022", "Define permissões padrão"),
        ("su", "su - outro_user", "Muda de usuário"),
        ("sudo", "sudo visudo", "Edita configuração do sudo"),
        ("visudo", "visudo", "Edita sudoers com segurança"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_categoria_pesquisa():
    """Categoria: Pesquisa e Filtro"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("🔍 PESQUISA E FILTRO")
    imprimir_linha("─")
    
    comandos = [
        ("grep", "grep -r 'password' /etc/", "Busca padrão em arquivos"),
        ("awk", "awk '{print $1}' arquivo.txt", "Processamento de texto"),
        ("sed", "sed 's/velho/novo/g' arquivo", "Editor de fluxo de texto"),
        ("sort", "sort -u arquivo.txt", "Ordena linhas"),
        ("uniq", "uniq -c arquivo.txt", "Remove duplicatas"),
        ("cut", "cut -d: -f1 /etc/passwd", "Extrai colunas do texto"),
        ("tr", "cat arquivo | tr 'a-z' 'A-Z'", "Traduz ou deleta caracteres"),
        ("wc", "wc -l arquivo.txt", "Conta linhas, palavras, caracteres"),
        ("head", "head -20 arquivo.log", "Mostra primeiras linhas"),
        ("tail", "tail -f /var/log/syslog", "Mostra últimas linhas (follow)"),
        ("less", "less arquivo_grande.txt", "Visualizador de arquivos"),
        ("more", "more arquivo.txt", "Visualizador básico (paginação)"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_categoria_compactacao():
    """Categoria: Compactação"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("🗜️  COMPACTAÇÃO DE ARQUIVOS")
    imprimir_linha("─")
    
    comandos = [
        ("tar", "tar -czvf backup.tar.gz pasta/", "Cria tarball compactado"),
        ("gzip", "gzip -9 arquivo.txt", "Compacta com gzip"),
        ("gunzip", "gunzip arquivo.txt.gz", "Descompacta gzip"),
        ("bzip2", "bzip2 arquivo.txt", "Compacta com bzip2"),
        ("xz", "xz -z arquivo.txt", "Compacta com xz"),
        ("zip", "zip -r backup.zip pasta/", "Cria arquivo zip"),
        ("unzip", "unzip arquivo.zip -d destino/", "Extrai zip"),
        ("7z", "7z a backup.7z pasta/", "Compacta com 7zip"),
        ("rar", "rar a backup.rar pasta/", "Compacta com rar"),
        ("unar", "unar arquivo.rar", "Extrai rar"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_categoria_monitoramento():
    """Categoria: Monitoramento"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("📊 MONITORAMENTO DO SISTEMA")
    imprimir_linha("─")
    
    comandos = [
        ("free", "free -h", "Uso de memória RAM"),
        ("vmstat", "vmstat 1 10", "Estatísticas do sistema"),
        ("iostat", "iostat -x 2", "Estatísticas de I/O"),
        ("mpstat", "mpstat -P ALL", "Estatísticas de CPU"),
        ("sar", "sar -u 1 3", "Coletor de estatísticas do sistema"),
        ("lsof", "lsof -i :80", "Arquivos abertos por processos"),
        ("strace", "strace -p 1234", "Traça chamadas de sistema"),
        ("dmesg", "dmesg | tail -20", "Mensagens do kernel"),
        ("journalctl", "journalctl -xe", "Logs do systemd"),
        ("uptime", "uptime", "Tempo de atividade do sistema"),
        ("uname", "uname -a", "Informações do kernel"),
        ("lsblk", "lsblk", "Lista dispositivos de bloco"),
        ("lscpu", "lscpu", "Informações da CPU"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_reconhecimento():
    """Seção 3: Técnicas de reconhecimento"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("3. TÉCNICAS DE RECONHECIMENTO")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}⌨️  COMANDOS DE REDE E INFORMAÇÃO:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    tecnicas = [
        ("ifconfig / ip addr", "ip -4 addr show eth0", "Mostra seu IP e interfaces"),
        ("ping", "ping -c 3 192.168.1.1", "Testa conectividade básica"),
        ("nmap -sP", "nmap -sP 192.168.1.0/24", "Descobre hosts ativos na rede"),
        ("whois", "whois exemplo.com", "Informações de registro de domínio"),
        ("dig ANY", "dig ANY exemplo.com @8.8.8.8", "Consulta DNS completa"),
        ("nslookup", "nslookup -type=MX exemplo.com", "Busca registros específicos"),
        ("traceroute", "traceroute -I google.com", "Traça rota (usando ICMP)"),
        ("netdiscover", "netdiscover -r 192.168.1.0/24", "Descobre hosts ARP"),
        ("theHarvester", "theHarvester -d dominio -b google", "Coleta e-mails/subdomínios"),
    ]
    
    for cmd, exemplo, desc in tecnicas:
        imprimir_comando(cmd, exemplo, desc)
    
    imprimir_linha("─")
    imprimir_texto(f"{C.ROXO}💡 DICA: Reconhecimento é 70% do hacking. Colete MÁXIMO de informações antes de qualquer ação!{C.RESET}", C.ROXO)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_exploracao_redes():
    """Seção 4: Exploração de redes"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("4. EXPLORAÇÃO DE REDES")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🔌 CONEXÕES REMOTAS E EXPLORAÇÃO:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    conexoes = [
        ("ssh", "ssh -i chave.pem user@192.168.1.100", "Conexão SSH com chave privada"),
        ("ssh -L", "ssh -L 8080:localhost:80 user@host", "Túnel SSH local (port forwarding)"),
        ("ftp", "ftp 192.168.1.50", "Conexão FTP interativa"),
        ("wget FTP", "wget ftp://user:pass@host/arquivo", "Download via FTP"),
        ("smbclient", "smbclient //192.168.1.10/shared", "Acesso a compartilhamento SMB"),
    ]
    
    for cmd, exemplo, desc in conexoes:
        imprimir_comando(cmd, exemplo, desc)
    
    print(f"{C.CINZA}│{C.RESET}")
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🔍 VARREDURA DE PORTAS AVANÇADA:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    nmap_comandos = [
        ("nmap básico", "nmap -v -A 192.168.1.1", "Varredura agressiva com detecção"),
        ("nmap stealth", "nmap -sS -sV -O -T4 alvo", "SYN scan + versões + OS"),
        ("nmap scripts", "nmap --script vuln alvo", "Executa scripts de vulnerabilidade"),
        ("nmap UDP", "nmap -sU -p 53,161 alvo", "Varredura de portas UDP"),
        ("nmap completo", "nmap -p- -sV -sC -O alvo", "Portas todas + scripts + OS"),
    ]
    
    for cmd, exemplo, desc in nmap_comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    imprimir_linha("─")
    imprimir_texto(f"{C.VERMELHO}⚠️  AVISO: Varredura não-autorizada é crime! Use apenas em redes próprias ou autorizadas.{C.RESET}", C.VERMELHO)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_ataques_web():
    """Seção 5: Ataques Web"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("5. ATAQUES WEB")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🗄️  SQL INJECTION (SQLI):{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    payloads = [
        ("Bypass Login", "' OR '1'='1'--", "Bypass de login clássico"),
        ("Union Based", "' UNION SELECT 1,2,3--", "Testa número de colunas"),
        ("Extract Data", "' UNION SELECT null,username,password FROM users--", "Extrai dados sensíveis"),
        ("Time Based", "' AND SLEEP(5)--", "Testa vulnerabilidade por tempo"),
        ("Error Based", "' AND 1=CONVERT(int,@@version)--", "Extrai info via mensagens de erro"),
    ]
    
    for nome, exemplo, desc in payloads:
        imprimir_comando(nome, exemplo, desc)
    
    print(f"{C.CINZA}│{C.RESET}")
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🌐 CROSS-SITE SCRIPTING (XSS):{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    xss_payloads = [
        ("Reflected XSS", "<script>alert('XSS')</script>", "Teste básico de XSS"),
        ("Stored XSS", "<img src=x onerror=alert(document.cookie)>", "XSS que rouba cookies"),
        ("DOM XSS", "#<script>alert(1)</script>", "XSS baseado em DOM"),
        ("Filter Evasion", "<ScRiPt>alert(String.fromCharCode(88,83,83))</ScRiPt>", "Evade filtros simples"),
    ]
    
    for nome, exemplo, desc in xss_payloads:
        imprimir_comando(nome, exemplo, desc)
    
    print(f"{C.CINZA}│{C.RESET}")
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}📁 DIRECTORY TRAVERSAL:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    imprimir_comando("Path Traversal", "../../../etc/passwd", "Acesso a arquivos do sistema")
    imprimir_comando("Null Byte", "../../../etc/passwd%00", "Bypass de filtros com null byte")
    
    imprimir_linha("─")
    imprimir_texto(f"{C.ROXO}💡 Use ferramentas como sqlmap, Burp Suite e OWASP ZAP para automatizar testes.{C.RESET}", C.ROXO)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_cracking_senhas():
    """Seção 6: Cracking de senhas"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("6. CRACKING DE SENHAS")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🔓 TÉCNICAS E FERRAMENTAS:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    tecnicas = [
        ("Hashcat", "hashcat -m 0 hash.txt rockyou.txt", "GPU accelerated password cracking"),
        ("John", "john --format=md5 hash.txt --wordlist=rockyou.txt", "John the Ripper clássico"),
        ("Hydra SSH", "hydra -l user -P wordlist.txt ssh://192.168.1.1", "Força bruta em SSH"),
        ("Hydra FTP", "hydra -L users.txt -P passes.txt ftp://target", "Força bruta em FTP"),
        ("Medusa", "medusa -h target -u admin -P wordlist.txt -M http", "Força bruta web"),
    ]
    
    for nome, exemplo, desc in tecnicas:
        imprimir_comando(nome, exemplo, desc)
    
    print(f"{C.CINZA}│{C.RESET}")
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}📁 DICIONÁRIOS RECOMENDADOS:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    dicionarios = [
        ("rockyou.txt", "/usr/share/wordlists/rockyou.txt", "14 milhões de senhas"),
        ("darkc0de.txt", "/usr/share/wordlists/darkc0de.txt", "Senhas de vazamentos"),
        ("fasttrack.txt", "/usr/share/wordlists/fasttrack.txt", "Senhas comuns"),
        ("ssh-betterdefaultpasslist", "/usr/share/wordlists/ssh-betterdefaultpasslist.txt", "Específico para SSH"),
    ]
    
    for nome, caminho, desc in dicionarios:
        imprimir_comando(nome, caminho, desc)
    
    imprimir_linha("─")
    imprimir_texto(f"{C.VERDE}💡 DICA: Combine wordlists e use regras do Hashcat para aumentar eficiência.{C.RESET}", C.VERDE)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_analise_forense():
    """Seção 7: Análise forense"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("7. ANÁLISE FORENSE")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}📊 COMANDOS DE ANÁLISE E LOGS:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    comandos = [
        ("grep", "grep -r 'Failed password' /var/log/auth.log", "Busca tentativas de login falhas"),
        ("tail -f", "tail -f /var/log/apache2/access.log", "Monitora logs em tempo real"),
        ("journalctl", "journalctl -u ssh --since '2 hours ago'", "Logs do systemd por serviço"),
        ("last", "last -i | head -20", "Últimos logins com IPs"),
        ("lastb", "lastb", "Logins malsucedidos"),
        ("who", "who -u", "Usuários atualmente logados"),
        ("w", "w", "Usuários e seus processos"),
        ("lsof", "lsof -i :22", "Processos usando porta SSH"),
        ("netstat", "netstat -anp | grep ESTABLISHED", "Conexões estabelecidas"),
        ("ps", "ps aux --sort=-%cpu | head -10", "Top 10 processos por CPU"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    print(f"{C.CINZA}│{C.RESET}")
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🕵️  INVESTIGAÇÃO DE ARQUIVOS:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    investigacao = [
        ("strings", "strings malware.bin | grep 'http'", "Extrai strings de binários"),
        ("file", "file arquivo.desconhecido", "Identifica tipo real do arquivo"),
        ("md5sum", "md5sum arquivo > hash.txt", "Cria hash para verificação"),
        ("sha256sum", "sha256sum arquivo", "Hash SHA256 mais seguro"),
        ("stat", "stat -c '%n %U %G %a %x %y %z' arquivo", "Metadados completos"),
        ("find mtime", "find / -mtime -1 -type f 2>/dev/null", "Arquivos modificados no último dia"),
    ]
    
    for cmd, exemplo, desc in investigacao:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_ofuscacao():
    """Seção 8: Ofuscação e anonimato"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("8. OFUSCAÇÃO E ANONIMATO")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🎭 TÉCNICAS DE ANONIMIZAÇÃO:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    tecnicas = [
        ("TOR", "tor &", "Inicia serviço TOR"),
        ("proxychains", "proxychains firefox", "Navega através da cadeia de proxies"),
        ("macchanger", "macchanger -r eth0", "Altera MAC address para aleatório"),
        ("VPN", "openvpn config.ovpn", "Conecta via VPN"),
        ("tshark", "tshark -i eth0 -w captura.pcap", "Captura pacotes sem GUI"),
        ("wipe", "wipe -rf arquivo", "Apaga arquivo de forma segura"),
    ]
    
    for cmd, exemplo, desc in tecnicas:
        imprimir_comando(cmd, exemplo, desc)
    
    print(f"{C.CINZA}│{C.RESET}")
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🛡️  ANTI-FORENSE BÁSICO:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    antiforense = [
        ("shred", "shred -zuf arquivo.conf", "Sobrescreve e deleta arquivo"),
        ("dd wipe", "dd if=/dev/urandom of=arquivo bs=1M count=3", "Sobrescreve com dados aleatórios"),
        ("history clean", "history -c && history -w", "Limpa histórico do shell"),
        ("tmpfs", "mount -t tmpfs -o size=512m tmpfs /tmp/seguro", "Cria RAM disk temporário"),
        ("encrypt", "gpg -c arquivo.txt", "Criptografa arquivo com senha"),
    ]
    
    for cmd, exemplo, desc in antiforense:
        imprimir_comando(cmd, exemplo, desc)
    
    imprimir_linha("─")
    imprimir_texto(f"{C.VERMELHO}⚠️  AVISO: NENHUMA técnica oferece 100% de anonimato! Sempre há riscos.{C.RESET}", C.VERMELHO)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

def mostrar_ferramentas():
    """Seção 9: Ferramentas especiais"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("9. FERRAMENTAS ESPECIAIS")
    imprimir_linha("─")
    
    print(f"{C.CINZA}│{C.RESET} {C.AMARELO}🛠️  KIT COMPLETO DO HACKER:{C.RESET}")
    print(f"{C.CINZA}│{C.RESET}")
    
    ferramentas = [
        ("Nmap", "nmap -sC -sV -oA scan_target target.com", "Varredura e enumeração"),
        ("Metasploit", "msfconsole -q", "Framework de exploração"),
        ("Wireshark", "tshark -r captura.pcap -Y 'http'", "Análise de tráfego"),
        ("Burp Suite", "java -jar burpsuite.jar", "Proxy para pentest web"),
        ("Sqlmap", "sqlmap -u 'site.com/page?id=1' --dbs", "Automatiza SQLi"),
        ("John", "john --test", "Testa performance do cracker"),
        ("Hydra", "hydra -h", "Mostra ajuda da ferramenta"),
        ("Aircrack-ng", "aircrack-ng captura.cap -w wordlist.txt", "Crack WiFi WPA"),
        ("Metagoofil", "metagoofil -d empresa.com -t pdf,doc -l 20", "Coleta metadata"),
        ("Nikto", "nikto -h target.com -o scan.html", "Scanner web automático"),
        ("Gobuster", "gobuster dir -u target.com -w wordlist.txt", "Força bruta diretórios"),
        ("Searchsploit", "searchsploit apache 2.4", "Busca exploits no Exploit-DB"),
    ]
    
    for tool, exemplo, desc in ferramentas:
        imprimir_comando(tool, exemplo, desc)
    
    imprimir_linha("─")
    imprimir_texto(f"{C.ROXO}💡 No ROOT EVOLUTION, você pode comprar versões virtuais dessas ferramentas no mercado!{C.RESET}", C.ROXO)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

# ========== CLASSE PARA INTEGRAÇÃO COM ROOT_EVOLUTION ==========

class ManualHacking:
    """Classe wrapper para integração do manual com o ROOT EVOLUTION"""
    
    def __init__(self):
        """Inicializa o manual de hacking"""
        pass
    
    def mostrar_menu(self):
        """Exibe o menu principal do manual de hacking"""
        try:
            exibir_manual()
        except KeyboardInterrupt:
            pass  # Apenas retorna ao menu anterior
        except Exception as e:
            print(f"\n{C.VERMELHO}[!] Erro ao exibir manual: {e}{C.RESET}")

# ========== EXECUÇÃO PRINCIPAL ==========

# Execução principal
if __name__ == "__main__":
    try:
        print(f"{C.VERDE}[*] Initializing hacking manual...{C.RESET}")
        time.sleep(1)
        exibir_manual()
        print(f"\n{C.CIANO}[+] MANUAL FECHADO. Stay anonymous, hacker.{C.RESET}")
    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}[!] Connection terminated by user.{C.RESET}")
    except Exception as e:
        print(f"\n{C.VERMELHO}[!] Error: {e}{C.RESET}")