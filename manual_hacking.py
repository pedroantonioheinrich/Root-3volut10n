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

C = Cores()

def obter_largura_terminal():
    """Retorna a largura atual do terminal"""
    return get_terminal_size().columns

def imprimir_linha(caractere="─"):
    """Imprime uma linha horizontal"""
    largura = obter_largura_terminal() - 2
    print(f"{C.CINZA}┌{caractere * largura}┐{C.RESET}")

def imprimir_titulo(titulo):
    """Imprime título centralizado com bordas"""
    largura = obter_largura_terminal() - 4
    titulo_centralizado = f" {titulo} ".center(largura, "·")
    print(f"{C.CINZA}│{C.ROXO}{C.NEGRITO}{titulo_centralizado}{C.RESET}{C.CINZA}│{C.RESET}")

def imprimir_texto(texto, cor=C.BRANCO, alinhamento="left"):
    """Imprime texto com bordas laterais"""
    largura = obter_largura_terminal() - 4
    linhas = textwrap.wrap(texto, width=largura)
    
    for linha in linhas:
        if alinhamento == "center":
            linha_formatada = linha.center(largura)
        elif alinhamento == "right":
            linha_formatada = linha.rjust(largura)
        else:
            linha_formatada = linha.ljust(largura)
        print(f"{C.CINZA}│{C.RESET}{cor}{linha_formatada}{C.RESET}{C.CINZA}│{C.RESET}")

def imprimir_item(numero, titulo, descricao, cor=C.CIANO):
    """Imprime um item do menu"""
    largura = obter_largura_terminal() - 4
    numero_titulo = f"{C.VERDE}{numero}. {C.AMARELO}{titulo}{C.RESET}"
    linha = f"{numero_titulo}"
    
    print(f"{C.CINZA}│{C.RESET} {linha.ljust(largura-1)}{C.CINZA}│{C.RESET}")
    
    # Descrição
    if descricao:
        desc_linhas = textwrap.wrap(f"{C.CINZA}  → {descricao}", width=largura-3)
        for linha_desc in desc_linhas:
            print(f"{C.CINZA}│{C.RESET}{linha_desc.ljust(largura-1)}{C.CINZA}│{C.RESET}")

def imprimir_comando(comando, exemplo, descricao):
    """Imprime um comando com exemplo e descrição"""
    largura = obter_largura_terminal() - 4
    
    # Comando
    comando_line = f"{C.AZUL}⌨ {C.CIANO}{comando}{C.RESET}"
    print(f"{C.CINZA}│{C.RESET} {comando_line.ljust(largura-1)}{C.CINZA}│{C.RESET}")
    
    # Exemplo
    if exemplo:
        exemplo_linhas = textwrap.wrap(f"{C.CINZA}  📟 Exemplo: {C.VERDE}{exemplo}", width=largura-3)
        for linha_ex in exemplo_linhas:
            print(f"{C.CINZA}│{C.RESET}{linha_ex.ljust(largura-1)}{C.CINZA}│{C.RESET}")
    
    # Descrição
    if descricao:
        desc_linhas = textwrap.wrap(f"{C.CINZA}  💡 {descricao}", width=largura-3)
        for linha_desc in desc_linhas:
            print(f"{C.CINZA}│{C.RESET}{linha_desc.ljust(largura-1)}{C.CINZA}│{C.RESET}")
    
    print(f"{C.CINZA}│{C.RESET}{' ' * (largura-1)}{C.CINZA}│{C.RESET}")

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def digitar(texto, delay=0.01, cor=C.BRANCO):
    """Efeito de digitação estilo terminal"""
    sys.stdout.write(cor)
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(C.RESET)

def exibir_banner():
    """Exibe banner estilo Mr. Robot"""
    limpar_tela()
    largura = obter_largura_terminal()
    
    print(f"\n{C.REVERSO}{' ' * largura}{C.RESET}")
    
    banner = f"""
{C.FUNDO_VERMELHO}{C.BRANCO}{' ' * largura}{C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO}  ███▄ ▄███▓ ▄▄▄       ██▀███   ▒█████   █     █░  ██████   {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▒██▒  ██▒▓█░ █ ░█░▒██    ▒   {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒██░  ██▒▒█░ █ ░█ ░ ▓██▄     {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▒██   ██░░█░ █ ░█   ▒   ██▒  {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒░ ████▓▒░░░██▒██▓ ▒██████▒▒  {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▓░▒ ▒  ▒ ▒▓▒ ▒ ░  {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░ ▒ ▒░   ▒ ░ ░  ░ ░▒  ░ ░  {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO} ░      ░     ░   ▒     ░░   ░ ░ ░ ░ ▒    ░   ░  ░  ░  ░    {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO}        ░         ░  ░   ░         ░ ░      ░          ░    {C.RESET}
{C.FUNDO_VERMELHO}{C.BRANCO}{' ' * largura}{C.RESET}
    """
    
    print(banner)
    
    print(f"{C.REVERSO}{C.FUNDO_VERMELHO}{C.BRANCO} MANUAL DE HACKING - ROOT EVOLUTION v2.0 ".center(largura) + f"{C.RESET}")
    print(f"{C.REVERSO}{C.FUNDO_VERMELHO}{C.BRANCO} " + "█" * (largura - 2) + f" {C.RESET}")
    print(f"{C.REVERSO}{C.FUNDO_VERMELHO}{C.BRANCO}  CONECTANDO AO SISTEMA... ACCESS: fsociety/root  ".center(largura) + f"{C.RESET}")
    print(f"{C.REVERSO}{' ' * largura}{C.RESET}\n")

def exibir_manual():
    """Exibe o manual completo de hacking"""
    while True:
        exibir_banner()
        
        # ÍNDICE PRINCIPAL
        imprimir_linha()
        imprimir_titulo("📖 MENU PRINCIPAL - SELECT AN OPTION")
        imprimir_linha("─")
        
        menu_itens = [
            ("Comandos Básicos do Terminal", "Comandos essenciais para navegação"),
            ("Manual de Comandos Linux", "Guia completo de comandos do Linux"),
            ("Técnicas de Reconhecimento", "Coleta de informações e footprinting"),
            ("Exploração de Redes", "SSH, FTP, varredura de portas"),
            ("Ataques Web", "SQLi, XSS, CSRF, Directory Traversal"),
            ("Cracking de Senhas", "Força bruta, dicionários, hash cracking"),
            ("Análise Forense", "Logs, investigação, rastreamento"),
            ("Ofuscação e Anonimato", "VPN, TOR, proxies, anti-forense"),
            ("Ferramentas Especiais", "Nmap, Metasploit, Wireshark, Burp Suite"),
            ("Sair do Sistema", "Encerrar conexão")
        ]
        
        for i, (titulo, desc) in enumerate(menu_itens, 1):
            imprimir_item(str(i), titulo, desc)
        
        imprimir_linha("─")
        
        try:
            escolha = input(f"\n{C.VERDE}{C.REVERSO} root@hacklab:~# {C.RESET} ").strip()
            
            if escolha == "10" or escolha.lower() == "exit" or escolha == "0":
                print(f"\n{C.VERMELHO}[!] Connection terminated.{C.RESET}")
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
                print(f"\n{C.VERMELHO}[!] Invalid option. Type 1-10 or 'exit'{C.RESET}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{C.VERMELHO}[!] Connection interrupted by user.{C.RESET}")
            break

def mostrar_comandos_basicos():
    """Seção 1: Comandos básicos do terminal"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("1. COMANDOS BÁSICOS DO TERMINAL")
    imprimir_linha("─")
    
    comandos = [
        ("ls", "ls -la", "Lista arquivos com detalhes (todos incluindo ocultos)"),
        ("cd", "cd /var/www && cd ..", "Navega entre diretórios"),
        ("pwd", "pwd", "Mostra diretório atual completo"),
        ("cp", "cp arquivo.txt backup/", "Copia arquivos/diretórios"),
        ("mv", "mv antigo.txt novo.txt", "Move ou renomeia arquivos"),
        ("rm", "rm -rf pasta/", "Remove arquivos/diretórios (CUIDADO!)"),
        ("mkdir", "mkdir nova_pasta", "Cria novo diretório"),
        ("cat", "cat config.txt | grep 'password'", "Exibe conteúdo de arquivo"),
        ("echo", "echo 'texto' > arquivo.txt", "Escreve em arquivos"),
        ("nano/vim", "nano script.sh", "Editores de texto no terminal"),
        ("chmod", "chmod +x script.sh", "Altera permissões de arquivo"),
        ("sudo", "sudo apt update", "Executa comando como superusuário"),
        ("man", "man grep", "Manual de ajuda de comandos"),
        ("clear", "clear", "Limpa a tela do terminal"),
        ("whoami", "whoami", "Mostra usuário atual"),
        ("history", "history | tail -20", "Histórico de comandos"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    imprimir_linha("─")
    imprimir_texto(f"{C.ROXO}💡 DICA: Use TAB para autocompletar e Ctrl+C para cancelar comandos.{C.RESET}", C.ROXO)
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

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
    """Categoria: Sistema de Arquivos"""
    limpar_tela()
    imprimir_linha()
    imprimir_titulo("📁 SISTEMA DE ARQUIVOS")
    imprimir_linha("─")
    
    comandos = [
        ("ls", "ls -lh", "Lista com tamanhos legíveis para humanos"),
        ("tree", "tree -L 3", "Mostra estrutura em árvore"),
        ("find", "find / -name '*.conf' -type f", "Busca arquivos"),
        ("locate", "locate passwd", "Busca rápida no banco de dados"),
        ("stat", "stat arquivo.txt", "Informações detalhadas do arquivo"),
        ("du", "du -sh * | sort -rh", "Uso de espaço por diretório"),
        ("df", "df -h", "Espaço livre em disco"),
        ("mount", "mount | grep /dev/sd", "Sistemas de arquivos montados"),
        ("ln", "ln -s /caminho/origem atalho", "Cria link simbólico"),
        ("touch", "touch novo_arquivo.txt", "Cria arquivo vazio"),
        ("file", "file arquivo.desconhecido", "Identifica tipo de arquivo"),
        ("diff", "diff arquivo1.txt arquivo2.txt", "Compara arquivos"),
        ("rsync", "rsync -avz origem/ destino/", "Sincroniza diretórios"),
    ]
    
    for cmd, exemplo, desc in comandos:
        imprimir_comando(cmd, exemplo, desc)
    
    input(f"\n{C.CINZA}[ Press ENTER to return ]{C.RESET}")

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