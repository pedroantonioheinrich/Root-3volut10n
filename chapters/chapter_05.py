#!/usr/bin/env python3
"""
CHAPTER_05.PY - "Sombras Digitais"
Duas semanas depois. As evidências de Juliana levam a algo maior.
Um padrão emerge: ela não estava sozinha. Há outros envolvidos.
Primeiro sinal de conspiração maior.

Foco: Investigação avançada, análise de dados
Habilidades: SQL injection, análise de logs, rastreamento digital
Objetivos: 6 missões principais + descoberta de conspiração
"""

import os
import sys
import time
import random
import json
import shutil
from datetime import datetime
from pathlib import Path

# Importar dependências
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
        """Fallback para função de digitação"""
        for char in texto:
            print(f"{cor}{char}{C.RESET}", end='', flush=True)
            time.sleep(delay)
        print(fim, end=''


# ========== GERENCIADOR DE ESTADO DO JOGO ==========

class GameState:
    """Gerencia o estado durante o capítulo"""

    def __init__(self, dados_jogador):
        # Dados originais do jogador
        self.player_name = dados_jogador.get('player_name', 'Hacker')
        self.codiname = dados_jogador.get('codiname', 'ANON')
        self.current_chapter = dados_jogador.get('current_chapter', 5)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 75)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.01)

        # Estado do capítulo
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.checkpoint = 'inicio'

        # Missões do capítulo 5
        self.missoes = {
            'analisar_logs': False,         # Analisar logs do servidor comprometido
            'sql_injection': False,         # Executar SQL injection no banco
            'extrair_dados': False,         # Extrair dados dos usuários
            'rastrear_ip': False,           # Rastrear IPs suspeitos
            'descobrir_padrao': False,      # Descobrir padrão de conspiração
            'cobrir_rastros': False        # Limpar evidências da investigação
        }

        # Contadores e flags
        self.tentativas_sql = 0
        self.tempo_decorrido = 0
        self.risco_descoberta = 0
        self.dicas_conspiracao = 0

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.privacy_level = max(0, self.privacy_level - 3)  # Maior perda de privacidade

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.privacy_level = max(0, self.privacy_level - 8)
        self.risco_descoberta += 15

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(20)
            print(f"\n{C.VERDE}✓ MISSÃO CONCLUÍDA: {missao_nome.replace('_', ' ').upper()}{C.RESET}")

    def verificar_progresso(self):
        """Verifica progresso das missões"""
        completas = sum(self.missoes.values())
        total = len(self.missoes)
        return completas, total

    def to_dict(self):
        """Converte estado para dicionário"""
        dados = {
            'player_name': self.player_name,
            'codiname': self.codiname,
            'current_chapter': self.current_chapter,
            'completed_chapters': self.completed_chapters,
            'score': self.score,
            'privacy_level': self.privacy_level,
            'bitcoin_wallet': self.bitcoin_wallet,
            'chapter_05_checkpoint': self.checkpoint,
            'capitulo_5_resultado': None,
            'capitulo_5_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_5': self.missoes.copy(),
            'dicas_conspiracao': self.dicas_conspiracao
        }
        return dados


# ========== FUNÇÕES AUXILIARES ==========

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')

def digitar(texto, delay=0.03, cor=C.BRANCO):
    """Função de digitação com efeito"""
    _digitar_padrao(texto, delay, cor)

def erro(mensagem):
    """Exibe mensagem de erro"""
    print(f"\n{C.VERMELHO}[ERRO] {mensagem}{C.RESET}")

def sucesso(mensagem):
    """Exibe mensagem de sucesso"""
    print(f"\n{C.VERDE}[SUCESSO] {mensagem}{C.RESET}")

def aviso(mensagem):
    """Exibe mensagem de aviso"""
    print(f"\n{C.AMARELO}[AVISO] {mensagem}{C.RESET}")

def prompt_kali(username="hacker"):
    """Retorna prompt estilo Kali Linux"""
    return f"{C.VERDE}{username}{C.CINZA}@{C.AMARELO}kali{C.RESET}{C.CINZA}:{C.AMARELO}~{C.RESET}{C.CINZA}$ {C.RESET}"

def exibir_header():
    """Exibe cabeçalho do capítulo"""
    limpar_tela()
    print(f"{C.NEGRITO}{C.ROXO}")
    print("═" * 80)
    print("                [ROOT EVOLUTION - CAPÍTULO 5: SOMBRAS DIGITAIS]")
    print("                 Brasília, 11:23 PM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")
    print(f"{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.")
    print(f"📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.")
    print("═" * 80)
    print(f"{C.RESET}")


# ========== FUNÇÕES DE TUTORIAL ==========

def tutorial_sql_injection():
    """Tutorial sobre SQL injection"""
    print(f"\n{C.CIANO}[TUTORIAL - SQL INJECTION]{C.RESET}")
    print("SQL Injection é uma técnica onde inserimos código SQL malicioso em campos de entrada.")
    print("Exemplos básicos:")
    print("  - ' OR '1'='1  (bypass de login)")
    print("  - '; DROP TABLE users;  (execução de comandos)")
    print("  - UNION SELECT * FROM admin_table")
    print("\nSintaxe básica para dump de dados:")
    print("  ' UNION SELECT username,password FROM users --")
    print(f"{C.AMARELO}Pratique com cuidado - pode danificar bancos de dados!{C.RESET}\n")


# ========== FUNÇÕES DE MISSÃO ==========

def simular_analise_logs(game_state):
    """Simula análise de logs do servidor"""
    print(f"\n{C.AMARELO}[ANÁLISE DE LOGS]{C.RESET}")
    print("Analisando logs de acesso do servidor backup-cloud...")

    # Simulação de análise
    logs = [
        "2024-01-15 02:47:22 - SSH login: admin@backup-cloud from 192.168.1.108",
        "2024-01-15 02:48:15 - File access: /home/admin/Private/photos/",
        "2024-01-15 02:49:33 - Download: evidence_001.zip",
        "2024-01-15 03:15:47 - SSH login: juliana@backup-cloud from 10.0.0.50",
        "2024-01-15 03:16:02 - File upload: classified_docs.pdf",
        "2024-01-15 03:17:18 - Database query: SELECT * FROM users WHERE role='admin'",
        "2024-01-15 03:18:45 - SSH login: unknown@backup-cloud from 203.0.113.1",
        "2024-01-15 03:19:12 - File access: /var/log/auth.log"
    ]

    for log in logs:
        time.sleep(0.5)
        print(f"  {C.CINZA}{log}{C.RESET}")

    print(f"\n{C.VERDE}✓ Padrão identificado: Juliana não estava sozinha!{C.RESET}")
    print(f"{C.AMARELO}Há acessos de IP 203.0.113.1 - servidor governamental?{C.RESET}")

    game_state.dicas_conspiracao += 1
    return True


def simular_sql_injection(game_state):
    """Simula SQL injection no banco de dados"""
    print(f"\n{C.AMARELO}[SQL INJECTION]{C.RESET}")
    print("Tentando injetar SQL no formulário de login do backup-cloud...")

    # Simulação de tentativa
    payloads = [
        "' OR '1'='1 --",
        "admin'; --",
        "' UNION SELECT username,password FROM users --"
    ]

    for payload in payloads:
        time.sleep(1)
        print(f"Tentando payload: {C.ROXO}{payload}{C.RESET}")
        if random.random() > 0.3:  # 70% chance de sucesso
            print(f"{C.VERDE}✓ Payload funcionou! Dados extraídos.{C.RESET}")
            return True
        else:
            print(f"{C.VERMELHO}✗ Payload bloqueado.{C.RESET}")

    print(f"{C.AMARELO}Tentativa falhou. Sistema pode ter proteção WAF.{C.RESET}")
    return False


def simular_rastreamento_ip(game_state):
    """Simula rastreamento de IP suspeito"""
    print(f"\n{C.AMARELO}[RASTREAMENTO DE IP]{C.RESET}")
    print("Rastreando IP suspeito: 203.0.113.1...")

    # Simulação de whois e traceroute
    time.sleep(2)
    print(f"{C.CIANO}WHOIS Result:{C.RESET}")
    print("  Domain: gov.br")
    print("  Organization: Ministério da Justiça")
    print("  Location: Brasília, DF")

    time.sleep(1)
    print(f"\n{C.CIANO}Traceroute:{C.RESET}")
    print("  1. router.local (192.168.1.1)")
    print("  2. isp.gateway (200.1.2.3)")
    print("  3. gov.firewall (203.0.113.1)")

    print(f"\n{C.VERDE}✓ IP pertence ao Ministério da Justiça!{C.RESET}")
    print(f"{C.AMARELO}Juliana estava colaborando com o governo?{C.RESET}")

    game_state.dicas_conspiracao += 2
    return True


def mostrar_descoberta_conspiracao(game_state):
    """Mostra descoberta da conspiração"""
    print(f"\n{C.ROXO}[DESCOBERTA DA CONSPIRAÇÃO]{C.RESET}")
    print("Conectando os pontos...")

    time.sleep(2)
    print(f"\n{C.VERMELHO}A traição de Juliana não foi pessoal.{C.RESET}")
    print("Ela fazia parte de uma operação maior:")
    print("  • Vazamento de dados classificados")
    print("  • Colaboração com agentes governamentais")
    print("  • Rede de informantes em empresas de tecnologia")
    print("  • Possível envolvimento com espionagem corporativa")

    print(f"\n{C.AMARELO}Mas por quê? O que eles querem?{C.RESET}")
    print(f"{C.CIANO}Preciso investigar mais fundo...{C.RESET}")

    game_state.dicas_conspiracao += 3
    return True


# ========== FUNÇÃO PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save):
    """Função principal do capítulo 5"""
    game_state = GameState(dados_jogador)

    # Carregar checkpoint se existir
    if os.path.exists(arquivo_save):
        try:
            with open(arquivo_save, 'r') as f:
                dados_salvos = json.load(f)
            checkpoint = dados_salvos.get('chapter_05_checkpoint', 'inicio')
            if checkpoint != 'inicio':
                game_state.checkpoint = checkpoint
                game_state.missoes = dados_salvos.get('missoes_capitulo_5', game_state.missoes)
                game_state.score = dados_salvos.get('score', game_state.score)
                game_state.dicas_conspiracao = dados_salvos.get('dicas_conspiracao', 0)
                print(f"{C.AMARELO}Continuando do checkpoint: {checkpoint}{C.RESET}")
        except:
            pass

    exibir_header()

    # Narrativa inicial
    digitar("Duas semanas se passaram desde aquela noite fatídica.", cor=C.BRANCO)
    digitar("As evidências que encontrei no backup de Juliana não param de me assombrar.", cor=C.CINZA)
    digitar("Ela não estava sozinha. Há outros envolvidos.", cor=C.CINZA)
    digitar("Preciso investigar mais fundo. Descobrir quem são esses 'outros'.", cor=C.CINZA)
    digitar("O que Juliana realmente fazia? Por que me traiu?", cor=C.VERMELHO)
    print()

    # Loop principal do jogo
    while not game_state.capitulo_concluido:
        try:
            # Verificar progresso
            completas, total = game_state.verificar_progresso()
            print(f"\n{C.AMARELO}Progresso: {completas}/{total} missões completas{C.RESET}")
            print(f"{C.AMARELO}Pontuação: {game_state.score} | Privacidade: {game_state.privacy_level}%{C.RESET}")
            print(f"{C.AMARELO}Dicas de conspiração: {game_state.dicas_conspiracao}{C.RESET}")

            # Prompt do jogador
            comando = input(prompt_kali()).strip().lower()

            if comando == 'menu':
                game_state.checkpoint = 'menu'
                salvar_progresso(game_state, arquivo_save)
                return game_state.to_dict()

            elif comando == 'manual':
                mostrar_manual_hacking()
                continue

            elif comando == 'tutorial':
                tutorial_sql_injection()
                continue

            # Missões
            elif 'log' in comando or 'logs' in comando:
                if not game_state.missoes['analisar_logs']:
                    if simular_analise_logs(game_state):
                        game_state.completar_missao('analisar_logs')
                else:
                    aviso("Logs já analisados!")

            elif 'sql' in comando or 'injection' in comando:
                if not game_state.missoes['sql_injection']:
                    if simular_sql_injection(game_state):
                        game_state.completar_missao('sql_injection')
                    else:
                        game_state.registrar_falha()
                else:
                    aviso("SQL injection já executada!")

            elif 'ip' in comando or 'rastrear' in comando:
                if game_state.missoes['analisar_logs']:  # Depende de logs
                    if not game_state.missoes['rastrear_ip']:
                        if simular_rastreamento_ip(game_state):
                            game_state.completar_missao('rastrear_ip')
                    else:
                        aviso("IP já rastreado!")
                else:
                    erro("Analise os logs primeiro!")

            elif 'dados' in comando or 'extrair' in comando:
                if game_state.missoes['sql_injection']:  # Depende de SQL injection
                    if not game_state.missoes['extrair_dados']:
                        game_state.completar_missao('extrair_dados')
                        sucesso("Dados confidenciais extraídos com sucesso!")
                    else:
                        aviso("Dados já extraídos!")
                else:
                    erro("Execute SQL injection primeiro!")

            elif 'padrao' in comando or 'conspiracao' in comando:
                if game_state.dicas_conspiracao >= 3:  # Precisa de dicas suficientes
                    if not game_state.missoes['descobrir_padrao']:
                        if mostrar_descoberta_conspiracao(game_state):
                            game_state.completar_missao('descobrir_padrao')
                    else:
                        aviso("Padrão já descoberto!")
                else:
                    erro("Preciso de mais evidências!")

            elif 'cobrir' in comando or 'limpar' in comando:
                if completas >= 4:  # Precisa completar maioria das missões
                    if not game_state.missoes['cobrir_rastros']:
                        game_state.completar_missao('cobrir_rastros')
                        sucesso("Rastros cobertos. Investigação concluída!")
                        game_state.capitulo_concluido = True
                        game_state.operacao_sucesso = True
                    else:
                        aviso("Rastros já cobertos!")
                else:
                    erro("Complete mais missões antes de cobrir rastros!")

            else:
                erro("Comando não reconhecido. Tente: logs, sql, ip, dados, padrao, cobrir")

            # Verificar conclusão
            if game_state.capitulo_concluido:
                print(f"\n{C.VERDE}🎯 CAPÍTULO 5 CONCLUÍDO! 🎯{C.RESET}")
                print("A conspiração começa a se revelar...")
                salvar_progresso(game_state, arquivo_save)
                return game_state.to_dict()

            # Salvar progresso automaticamente
            salvar_progresso(game_state, arquivo_save)

        except KeyboardInterrupt:
            print(f"\n{C.AMARELO}Saindo...{C.RESET}")
            salvar_progresso(game_state, arquivo_save)
            return game_state.to_dict()
        except Exception as e:
            erro(f"Erro inesperado: {e}")
            continue


def salvar_progresso(game_state, arquivo_save):
    """Salva o progresso em arquivo JSON"""
    try:
        dados = game_state.to_dict()
        with open(arquivo_save, 'w') as f:
            json.dump(dados, f, indent=2)
    except Exception as e:
        erro(f"Erro ao salvar progresso: {e}")


def mostrar_manual_hacking():
    """Mostra interface do manual de hacking"""
    try:
        from manual_hacking import mostrar_manual
        mostrar_manual()
    except ImportError:
        print(f"\n{C.AMARELO}[MANUAL DE HACKING - SIMULAÇÃO]{C.RESET}")
        print("Capítulo 5 - Técnicas Avançadas:")
        print("• SQL Injection: Injeção de código SQL em formulários")
        print("• Análise de Logs: Interpretação de registros de sistema")
        print("• Rastreamento IP: Geolocalização e identificação de origem")
        print("• Extração de Dados: Dump de informações de bancos")
        print(f"{C.VERMELHO}⚠️  Você perdeu tempo consultando o manual! ⚠️{C.RESET}")


if __name__ == "__main__":
    # Para testes diretos
    dados_teste = {
        'player_name': 'Teste',
        'codiname': 'TESTE',
        'current_chapter': 5,
        'score': 100,
        'privacy_level': 75,
        'bitcoin_wallet': 0.01
    }

    resultado = iniciar(dados_teste, '/tmp/teste_chapter5.json')
    print("Resultado:", resultado)
        self.codinome = dados_anteriores.get('codiname', 'SHADOW_00')
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0) or 0
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        self.darknet_access = dados_anteriores.get('darknet_access', False)

        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False

        # Escolhas críticas do capítulo
        self.escolha_final = None  # 'expor', 'controlar', 'terceira_via'

    def registrar_falha(self, penalidade=15):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 10

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 5,  # Sempre capítulo 5
            'completed_chapters': [1, 2, 3, 4],  # Capítulos 1-4 devem estar completados
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy_level,
            'reputation': self.reputation,
            'score': self.score,
            'inventory': self.inventory,
            'darknet_access': self.darknet_access,
            'escolha_final': self.escolha_final,
            'completed': getattr(self, 'capitulo_concluido', False),
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }


# ========== UI AUXILIAR ==========

def header_kali_v2(titulo="CAPÍTULO 5: ROOTKIT NA REALIDADE"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass

    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Brasília - Base Secreta dos Anônimos | 03:47 AM':^{largura}}{C.RESET}")
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
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/rootkit{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

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


# ========== QUESTS/DESAFIOS ==========

def quest_1_infiltracao_servidor(state):
    """Quest 1: Infiltrar servidor eleitoral - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 1: INFILTRAÇÃO SERVIDOR ELEITORAL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Acessar sistema de votação TSE         ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*55}╝{C.RESET}\n")

    pensamento("O servidor eleitoral... o coração da democracia brasileira. Se eu conseguir acesso root aqui...")

    # Parte 1: Reconhecimento
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "nmap" in cmd and "tse.gov.br" in cmd:
            print(f"{C.CINZA}[*] Scanning tse.gov.br...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] PORT 22/tcp SSH OPEN{C.RESET}")
            print(f"{C.VERDE}[+] PORT 80/tcp HTTP OPEN{C.RESET}")
            print(f"{C.VERDE}[+] PORT 443/tcp HTTPS OPEN{C.RESET}")
            print(f"{C.AMARELO}[!] PORT 3389/tcp RDP OPEN - VULNERÁVEL!{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'nmap -sV tse.gov.br' para reconhecimento.{C.RESET}")
            state.registrar_falha(5)

    pensamento("RDP aberto... clássico erro de administração. Hora de tentar credenciais padrão.")

    # Parte 2: Ataque RDP
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "hydra" in cmd and "rdp" in cmd:
            print(f"{C.CINZA}[*] Iniciando ataque Hydra no RDP...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] login: admin | password: Admin123!{C.RESET}")
            print(f"{C.VERDE}[+] Acesso RDP concedido!{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'hydra -l admin -P wordlist.txt rdp://tse.gov.br' para brute force.{C.RESET}")
            state.registrar_falha(8)

    pensamento("Dentro do sistema... Agora preciso escalar privilégios para root.")

    # Parte 3: Escalação de privilégios
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "sudo" in cmd and "su" in cmd:
            print(f"{C.CINZA}[*] Escalando privilégios...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Root access granted!{C.RESET}")
            print(f"{C.VERDE}[+] Você agora tem controle total do servidor eleitoral.{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'sudo su' para se tornar root.{C.RESET}")
            state.registrar_falha(10)

    state.registrar_sucesso(50, 0.1)
    return True

def quest_2_analise_logs(state):
    """Quest 2: Analisar logs do sistema - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 2: ANÁLISE DE LOGS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Descobrir evidências da conspiração ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*45}╝{C.RESET}\n")

    pensamento("Os logs... eles nunca mentem. Vamos ver o que o sistema tem a dizer.")

    # Parte 1: Examinar logs de acesso
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "grep" in cmd and "access.log" in cmd:
            print(f"{C.CINZA}[*] Analisando access.log...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] 192.168.1.100 - V0id_Walker - 15:30:22 - LOGIN ROOT{C.RESET}")
            print(f"{C.VERDE}[+] 192.168.1.100 - V0id_Walker - 15:45:10 - UPLOAD ROOTKIT{C.RESET}")
            print(f"{C.VERDE}[+] 192.168.1.100 - V0id_Walker - 16:00:05 - MODIFY VOTES{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'grep -i login /var/log/access.log' para analisar acessos.{C.RESET}")
            state.registrar_falha(6)

    pensamento("V0id_Walker... Ele já estava aqui. Modificando votos. Isso confirma tudo.")

    # Parte 2: Examinar logs de sistema
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "journalctl" in cmd or "dmesg" in cmd:
            print(f"{C.CINZA}[*] Examinando logs do kernel...{C.RESET}")
            time.sleep(2)
            print(f"{C.AMARELO}[!] ROOTKIT DETECTADO: kernel_module_backdoor.ko{C.RESET}")
            print(f"{C.AMARELO}[!] ORIGEM: Upload via SSH - IP: 192.168.1.100{C.RESET}")
            print(f"{C.AMARELO}[!] FUNÇÃO: Manipulação de dados eleitorais{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'journalctl -u kernel' ou 'dmesg | grep rootkit' para logs.{C.RESET}")
            state.registrar_falha(7)

    pensamento("Um rootkit no kernel... Isso permite controle total. Os Anônimos não querem derrubar o governo. Eles querem ser o governo.")

    state.registrar_sucesso(40, 0.05)
    return True

def quest_3_extracao_evidencias(state):
    """Quest 3: Extrair evidências - Dificuldade: Média-Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 3: EXTRAÇÃO DE EVIDÊNCIAS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Copiar arquivos comprometedores ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*47}╝{C.RESET}\n")

    pensamento("Preciso levar essas evidências comigo. Elas podem ser minha única proteção.")

    # Parte 1: Localizar arquivos
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "find" in cmd and "rootkit" in cmd:
            print(f"{C.CINZA}[*] Procurando arquivos relacionados ao rootkit...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] /etc/rootkit_config.conf{C.RESET}")
            print(f"{C.VERDE}[+] /var/log/vote_manipulation.log{C.RESET}")
            print(f"{C.VERDE}[+] /usr/local/bin/backdoor_server{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'find / -name *rootkit* -type f' para localizar arquivos.{C.RESET}")
            state.registrar_falha(5)

    # Parte 2: Copiar arquivos
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "scp" in cmd and "rootkit_config.conf" in cmd:
            print(f"{C.CINZA}[*] Copiando arquivos via SCP...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Transferência completa: 3 arquivos copiados.{C.RESET}")
            print(f"{C.VERDE}[+] Evidências armazenadas em ~/evidence/{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'scp root@server:/etc/rootkit_config.conf ~/' para copiar.{C.RESET}")
            state.registrar_falha(6)

    pensamento("Agora tenho as provas. Mas o que fazer com elas? Expor tudo ou usar como moeda de troca?")

    state.registrar_sucesso(30, 0.03)
    return True

def quest_4_encontro_v0id(state):
    """Quest 4: Encontro com V0id_Walker - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 4: ENCONTRO COM V0ID_WALKER ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Confrontar o líder dos Anônimos ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*47}╝{C.RESET}\n")

    pensamento("V0id_Walker está online. Hora de confrontá-lo.")

    # Parte 1: Iniciar chat seguro
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "nc" in cmd and "chat" in cmd:
            print(f"{C.CINZA}[*] Conectando ao servidor de chat seguro...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Conexão estabelecida com V0id_Walker{C.RESET}")
            print(f"\n{C.ROXO}[V0id_Walker]: Você foi longe demais, {state.codinome}.{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'nc -c chat.anonymous.br 6667' para conectar.{C.RESET}")
            state.registrar_falha(8)

    # Diálogo interativo
    dialogo = [
        f"{C.BRANCO}[Você]: Eu vi os logs. O rootkit. As manipulações.{C.RESET}",
        f"{C.ROXO}[V0id_Walker]: E o que você viu? Uma conspiração? Ou uma oportunidade?{C.RESET}",
        f"{C.BRANCO}[Você]: Isso não é anarquia. É ditadura digital!{C.RESET}",
        f"{C.ROXO}[V0id_Walker]: Ditadura? Não. Controle. Ordem. O povo quer líderes, não caos.{C.RESET}",
        f"{C.BRANCO}[Você]: E eu? Sou apenas uma ferramenta descartável?{C.RESET}",
        f"{C.ROXO}[V0id_Walker]: Você é especial. Junte-se a nós. Ou seja eliminado.{C.RESET}"
    ]

    for linha in dialogo:
        print(f"\n{linha}")
        time.sleep(2)

    pensamento("Ele está me dando uma escolha. Mas será que é real?")

    state.registrar_sucesso(60, 0.08)
    return True

def quest_5_decisao_critica(state):
    """Quest 5: Decisão crítica - Dificuldade: Máxima"""
    print(f"\n{C.VERMELHO}╔════ QUEST 5: DECISÃO CRÍTICA ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Objetivo: Escolher seu caminho final ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*42}╝{C.RESET}\n")

    pensamento("Este é o momento. Minha escolha definirá tudo.")

    print(f"{C.AMARELO}[1] EXPOR TUDO - Liberar evidências para a imprensa internacional{C.RESET}")
    print(f"{C.AMARELO}[2] CONTROLAR - Assumir o lugar de V0id_Walker{C.RESET}")
    print(f"{C.AMARELO}[3] TERCEIRA VIA - Criar um novo sistema híbrido{C.RESET}")

    while True:
        try:
            escolha = input(f"\n{C.VERMELHO}[ESCOLHA 1, 2 ou 3]: {C.RESET}").strip()
        except:
            state.saindo_para_menu = True
            return False

        if escolha == "1":
            state.escolha_final = "expor"
            print(f"\n{C.VERDE}[EXPOSIÇÃO] Você decide expor tudo.{C.RESET}")
            print(f"{C.CINZA}Consequências: Fama internacional, mas vida como fugitivo.{C.RESET}")
            break
        elif escolha == "2":
            state.escolha_final = "controlar"
            print(f"\n{C.ROXO}[CONTROLE] Você decide assumir o controle.{C.RESET}")
            print(f"{C.CINZA}Consequências: Poder absoluto, mas alma perdida.{C.RESET}")
            break
        elif escolha == "3":
            state.escolha_final = "terceira_via"
            print(f"\n{C.CIANO}[TERCEIRA VIA] Você cria algo novo.{C.RESET}")
            print(f"{C.CINZA}Consequências: Inovação, mas riscos desconhecidos.{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Escolha inválida. Digite 1, 2 ou 3.{C.RESET}")

    state.registrar_sucesso(100, 0.2)
    return True

def quest_6_execucao_plano(state):
    """Quest 6: Execução do plano - Dificuldade: Máxima"""
    print(f"\n{C.VERMELHO}╔════ QUEST 6: EXECUÇÃO DO PLANO ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Objetivo: Implementar sua escolha final ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*44}╝{C.RESET}\n")

    if state.escolha_final == "expor":
        pensamento("Hora de liberar tudo. O mundo precisa saber.")

        # Simulação de upload para imprensa
        print(f"{C.CINZA}[*] Fazendo upload para servidores da imprensa...{C.RESET}")
        time.sleep(3)
        print(f"{C.VERDE}[+] Arquivos enviados para The Guardian, BBC, e Folha de S.Paulo{C.RESET}")
        print(f"{C.AMARELO}[!] ALERTA: Autoridades detectaram vazamento!{C.RESET}")

    elif state.escolha_final == "controlar":
        pensamento("O trono está vazio. É hora de ocupá-lo.")

        # Simulação de assumir controle
        print(f"{C.CINZA}[*] Iniciando protocolo de sucessão...{C.RESET}")
        time.sleep(3)
        print(f"{C.ROXO}[+] Você é agora o novo V0id_Walker{C.RESET}")
        print(f"{C.ROXO}[+] Todos os sistemas sob seu comando{C.RESET}")

    else:  # terceira_via
        pensamento("Nem anarquia, nem controle. Algo novo.")

        # Simulação de sistema híbrido
        print(f"{C.CINZA}[*] Desenvolvendo novo algoritmo de governança...{C.RESET}")
        time.sleep(3)
        print(f"{C.CIANO}[+] Sistema híbrido implementado{C.RESET}")
        print(f"{C.CIANO}[+] Democracia + Transparência Digital{C.RESET}")

    state.registrar_sucesso(150, 0.5)
    return True


# ========== CENA PRINCIPAL ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)

    digitar(f"{C.CINZA}A base secreta dos Anônimos.{C.RESET}", delay=0.1)
    drama_pause(1)
    digitar(f"{C.CINZA}Brasília, 03:47 da manhã.{C.RESET}", delay=0.06)
    drama_pause(1)

    header_kali_v2()
    drama_pause(2)

    narracao("Você está no coração da conspiração.")
    narracao("Os monitores ao redor mostram feeds de câmeras de segurança, logs de sistema, mapas de rede.")
    drama_pause(1)

    pensamento("Como cheguei aqui? Um mês atrás eu era apenas um cara traído. Agora... agora eu controlo o destino de uma nação.")
    pensamento("Mas será que ainda controlo meu próprio destino?")
    drama_pause(1)

    narracao("V0id_Walker entra na sala. Seu rosto é sério.")
    print(f"\n{C.ROXO}[V0id_Walker]: 'É hora, {state.codinome}. A Operação Raiz começa agora.'{C.RESET}")
    drama_pause(2)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter5(dados_jogador)

    try:
        cena_abertura(state)

        if state.saindo_para_menu:
            return state.to_dict()

        # Executar quests em sequência
        quests = [
            quest_1_infiltracao_servidor,
            quest_2_analise_logs,
            quest_3_extracao_evidencias,
            quest_4_encontro_v0id,
            quest_5_decisao_critica,
            quest_6_execucao_plano
        ]

        for quest in quests:
            if not quest(state):
                if state.saindo_para_menu:
                    return state.to_dict()
                break

        # Final do capítulo
        drama_pause(2)
        header_kali_v2()

        if state.escolha_final == "expor":
            print(f"\n{C.VERDE}{'═'*60}{C.RESET}")
            print(f"{C.VERDE}{'CAPÍTULO 5: EXPOSIÇÃO - CONCLUÍDO':^60}{C.RESET}")
            print(f"{C.VERDE}{'═'*60}{C.RESET}")
            print(f"\n{C.AMARELO}Final: O Mártir Anônimo{C.RESET}")

        elif state.escolha_final == "controlar":
            print(f"\n{C.ROXO}{'═'*60}{C.RESET}")
            print(f"{C.ROXO}{'CAPÍTULO 5: ASCENSÃO - CONCLUÍDO':^60}{C.RESET}")
            print(f"{C.ROXO}{'═'*60}{C.RESET}")
            print(f"\n{C.AMARELO}Final: O Novo Controlador{C.RESET}")

        else:
            print(f"\n{C.CIANO}{'═'*60}{C.RESET}")
            print(f"{C.CIANO}{'CAPÍTULO 5: INOVAÇÃO - CONCLUÍDO':^60}{C.RESET}")
            print(f"{C.CIANO}{'═'*60}{C.RESET}")
            print(f"\n{C.AMARELO}Final: A Terceira Via{C.RESET}")

        state.capitulo_concluido = True
        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

