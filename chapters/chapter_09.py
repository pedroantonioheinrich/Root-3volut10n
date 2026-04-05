#!/usr/bin/env python3
"""
CHAPTER_09.PY - "Infiltração Governamental"
Com aliados e evidências, invade sistemas governamentais.
Descobre a extensão real da conspiração 'Raiz Digital'.

Foco: Invasão de sistemas críticos, descoberta de segredos de estado
Habilidades: Exploits avançados, pivotamento lateral, escalada de privilégios
Objetivos: 6 missões principais + acesso aos servidores centrais
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
        self.current_chapter = dados_jogador.get('current_chapter', 9)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 50)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.1)
        self.reputation = dados_jogador.get('reputation', 150)

        # Estado do capítulo
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.checkpoint = 'inicio'

        # Missões do capítulo 9
        self.missoes = {
            'acessar_rede_gov': False,        # Acessar rede governamental
            'escalar_privilegios': False,     # Escalar privilégios no sistema
            'pivotar_servidores': False,      # Pivotar para servidores críticos
            'extrair_documentos': False,      # Extrair documentos classificados
            'descobrir_extensao': False,      # Descobrir extensão da conspiração
            'preparar_ataque': False         # Preparar contra-ataque
        }

        # Contadores e flags
        self.alertas_seguranca = 0
        self.documentos_comprometidos = 0
        self.nivel_infiltracao = 0

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.reputation += 15
        self.nivel_infiltracao += 20

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.alertas_seguranca += 1
        self.privacy_level = max(0, self.privacy_level - 15)

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(50)
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
            'reputation': self.reputation,
            'chapter_09_checkpoint': self.checkpoint,
            'capitulo_9_resultado': None,
            'capitulo_9_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_9': self.missoes.copy(),
            'alertas_seguranca': self.alertas_seguranca,
            'documentos_comprometidos': self.documentos_comprometidos,
            'nivel_infiltracao': self.nivel_infiltracao
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
    print("           [ROOT EVOLUTION - CAPÍTULO 9: INFILTRAÇÃO GOVERNAMENTAL]")
    print("                 Brasília, 04:15 AM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")
    print(f"{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.")
    print(f"📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.")
    print("═" * 80)
    print(f"{C.RESET}")


# ========== FUNÇÕES DE TUTORIAL ==========

def tutorial_exploits():
    """Tutorial sobre exploits avançados"""
    print(f"\n{C.CIANO}[TUTORIAL - EXPLOITS AVANÇADOS]{C.RESET}")
    print("Exploits são vulnerabilidades em sistemas:")
    print("  • Zero-day: Vulnerabilidades desconhecidas")
    print("  • Buffer overflow: Sobrescrever memória")
    print("  • SQL injection: Ataques a bancos de dados")
    print("  • RCE (Remote Code Execution): Execução remota de código")
    print("\nTécnicas de escalada:")
    print("  • Privilege escalation: Ganhar privilégios elevados")
    print("  • Lateral movement: Mover-se pela rede")
    print("  • Persistence: Manter acesso persistente")
    print(f"{C.AMARELO}Cuidado: Sistemas governamentais têm detecção avançada!{C.RESET}\n")


# ========== FUNÇÕES DE MISSÃO ==========

def simular_acesso_rede_gov(game_state):
    """Simula acesso à rede governamental"""
    print(f"\n{C.AMARELO}[ACESSO À REDE GOVERNAMENTAL]{C.RESET}")
    print("Usando credenciais de Marcus para acessar rede do Ministério...")

    # Simulação de acesso
    time.sleep(2)
    print(f"{C.CIANO}CONEXÃO ESTABELECIDA - REDE GOV.BR{C.RESET}")
    print("  • Firewall: Comprometido ✓")
    print("  • Autenticação: Bypassada ✓")
    print("  • Logs: Suprimidos ✓")

    print(f"\n{C.VERDE}✓ Acesso à rede governamental concedido!{C.RESET}")
    print(f"{C.AMARELO}Agora estou dentro do sistema do governo.{C.RESET}")

    return True


def simular_escalar_privilegios(game_state):
    """Simula escalada de privilégios"""
    print(f"\n{C.AMARELO}[ESCALADA DE PRIVILÉGIOS]{C.RESET}")
    print("Escalando privilégios no servidor do Ministério...")

    exploits = [
        "Dirty COW (CVE-2016-5195)",
        "Heartbleed (CVE-2014-0160)",
        "Shellshock (CVE-2014-6271)"
    ]

    for exploit in exploits:
        time.sleep(1)
        print(f"Tentando exploit: {C.ROXO}{exploit}{C.RESET}")
        if random.random() > 0.4:  # 60% chance de sucesso
            print(f"{C.VERDE}✓ Exploit funcionou! Privilégios elevados.{C.RESET}")
            return True
        else:
            print(f"{C.VERMELHO}✗ Exploit falhou.{C.RESET}")

    print(f"{C.AMARELO}Escalada bem-sucedida através de combinação de exploits.{C.RESET}")
    return True


def simular_pivotar_servidores(game_state):
    """Simula pivotamento para servidores críticos"""
    print(f"\n{C.AMARELO}[PIVOTAMENTO LATERAL]{C.RESET}")
    print("Movendo-se lateralmente pela rede governamental...")

    servidores = [
        {"nome": "servidor-rh", "importancia": "Dados pessoais"},
        {"nome": "servidor-financeiro", "importancia": "Orçamentos secretos"},
        {"nome": "servidor-inteligencia", "importancia": "Operações confidenciais"}
    ]

    for servidor in servidores:
        print(f"Acessando {C.CIANO}{servidor['nome']}{C.RESET} - {servidor['importancia']}")
        time.sleep(1)
        print(f"{C.VERDE}✓ Servidor comprometido!{C.RESET}")

    print(f"\n{C.VERDE}✓ Pivotamento completo!{C.RESET}")
    print(f"{C.AMARELO}Acesso a servidores críticos estabelecido.{C.RESET}")

    game_state.documentos_comprometidos += 5
    return True


def simular_extrair_documentos(game_state):
    """Simula extração de documentos classificados"""
    print(f"\n{C.AMARELO}[EXTRAÇÃO DE DOCUMENTOS]{C.RESET}")
    print("Extraindo documentos classificados dos servidores...")

    documentos = [
        "Operação Raiz Digital - Fase 1.pdf",
        "Lista de Informantes Governamentais.xlsx",
        "Planos de Controle Populacional.docx",
        "Contratos com TechCorp - Valores.confidencial",
        "Comunicações com Empresas Estrangeiras.enc"
    ]

    for doc in documentos:
        time.sleep(0.8)
        print(f"Extraindo: {C.ROXO}{doc}{C.RESET}")
        print(f"{C.VERDE}✓ Documento baixado e criptografado.{C.RESET}")

    print(f"\n{C.VERDE}✓ {len(documentos)} documentos extraídos!{C.RESET}")
    print(f"{C.AMARELO}Provas irrefutáveis da conspiração.{C.RESET}")

    game_state.documentos_comprometidos += 10
    return True


def simular_descobrir_extensao(game_state):
    """Simula descoberta da extensão da conspiração"""
    print(f"\n{C.ROXO}[EXTENSÃO DA CONSPIRAÇÃO]{C.RESET}")
    print("Analisando documentos extraídos...")

    revelacoes = {
        "Alcance Global": "Operação presente em 15 países",
        "Envolvimento Corporativo": "TechCorp, DataMiners, SecureNet",
        "Objetivo Final": "Controle total de dados pessoais mundiais",
        "Financiamento": "R$ 2 bilhões em contratos secretos",
        "Participação Governamental": "Ministérios da Justiça, Defesa e Economia",
        "Prazo": "Implementação completa em 18 meses"
    }

    print(f"{C.VERMELHO}REVELAÇÕES CHOQUE:{C.RESET}")
    for chave, valor in revelacoes.items():
        print(f"  {chave}: {valor}")

    time.sleep(3)
    print(f"\n{C.VERMELHO}A conspiração é GLOBAL.{C.RESET}")
    print("Não é só sobre Juliana ou o Brasil.")
    print("É sobre controle total da sociedade digital.")

    game_state.documentos_comprometidos += 15
    return True


def simular_preparar_ataque(game_state):
    """Simula preparação de contra-ataque"""
    print(f"\n{C.AMARELO}[PREPARAÇÃO DE CONTRA-ATAQUE]{C.RESET}")
    print("Preparando contra-ataque coordenado...")

    plano_ataque = [
        "✓ Identificar vulnerabilidades em servidores críticos",
        "✓ Coordenar com aliados da dark web",
        "✓ Preparar divulgação seletiva de documentos",
        "✓ Criar backdoors para monitoramento futuro",
        "✓ Estabelecer plano de extração segura"
    ]

    for item in plano_ataque:
        time.sleep(1)
        print(f"  {item}")

    print(f"\n{C.VERDE}✓ Contra-ataque preparado!{C.RESET}")
    print(f"{C.AMARELO}A batalha final se aproxima.{C.RESET}")

    return True


# ========== FUNÇÃO PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save):
    """Função principal do capítulo 9"""
    game_state = GameState(dados_jogador)

    # Carregar checkpoint se existir
    if os.path.exists(arquivo_save):
        try:
            with open(arquivo_save, 'r') as f:
                dados_salvos = json.load(f)
            checkpoint = dados_salvos.get('chapter_09_checkpoint', 'inicio')
            if checkpoint != 'inicio':
                game_state.checkpoint = checkpoint
                game_state.missoes = dados_salvos.get('missoes_capitulo_9', game_state.missoes)
                game_state.documentos_comprometidos = dados_salvos.get('documentos_comprometidos', 0)
                game_state.alertas_seguranca = dados_salvos.get('alertas_seguranca', 0)
                game_state.nivel_infiltracao = dados_salvos.get('nivel_infiltracao', 0)
                print(f"{C.AMARELO}Continuando do checkpoint: {checkpoint}{C.RESET}")
        except:
            pass

    exibir_header()

    # Narrativa inicial
    digitar("Com as credenciais de Marcus, tenho acesso ao governo.", cor=C.BRANCO)
    digitar("A conspiração 'Raiz Digital' vai muito além do que imaginava.", cor=C.CINZA)
    digitar("Preciso descobrir tudo. A extensão real desta operação.", cor=C.CINZA)
    digitar("Mas cada passo aumenta o risco. Eles sabem que estou aqui.", cor=C.CINZA)
    digitar("Será que conseguirei sair vivo desta rede?", cor=C.VERMELHO)
    print()

    # Loop principal do jogo
    while not game_state.capitulo_concluido:
        try:
            # Verificar progresso
            completas, total = game_state.verificar_progresso()
            print(f"\n{C.AMARELO}Progresso: {completas}/{total} missões completas{C.RESET}")
            print(f"{C.AMARELO}Pontuação: {game_state.score} | Alertas: {game_state.alertas_seguranca}{C.RESET}")
            print(f"{C.AMARELO}Documentos: {game_state.documentos_comprometidos} | Infiltração: {game_state.nivel_infiltracao}%{C.RESET}")

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
                tutorial_exploits()
                continue

            # Missões
            elif 'acessar' in comando or 'rede' in comando:
                if not game_state.missoes['acessar_rede_gov']:
                    if simular_acesso_rede_gov(game_state):
                        game_state.completar_missao('acessar_rede_gov')
                else:
                    aviso("Rede já acessada!")

            elif 'escalar' in comando or 'privilegios' in comando:
                if game_state.missoes['acessar_rede_gov']:
                    if not game_state.missoes['escalar_privilegios']:
                        if simular_escalar_privilegios(game_state):
                            game_state.completar_missao('escalar_privilegios')
                        else:
                            game_state.registrar_falha()
                    else:
                        aviso("Privilégios já escalados!")
                else:
                    erro("Acesse a rede primeiro!")

            elif 'pivotar' in comando or 'servidores' in comando:
                if game_state.missoes['escalar_privilegios']:
                    if not game_state.missoes['pivotar_servidores']:
                        if simular_pivotar_servidores(game_state):
                            game_state.completar_missao('pivotar_servidores')
                    else:
                        aviso("Servidores já pivotados!")
                else:
                    erro("Escale privilégios primeiro!")

            elif 'extrair' in comando or 'documentos' in comando:
                if game_state.missoes['pivotar_servidores']:
                    if not game_state.missoes['extrair_documentos']:
                        if simular_extrair_documentos(game_state):
                            game_state.completar_missao('extrair_documentos')
                    else:
                        aviso("Documentos já extraídos!")
                else:
                    erro("Pivote para servidores críticos primeiro!")

            elif 'extensao' in comando or 'conspiracao' in comando:
                if game_state.missoes['extrair_documentos'] and game_state.documentos_comprometidos >= 10:
                    if not game_state.missoes['descobrir_extensao']:
                        if simular_descobrir_extensao(game_state):
                            game_state.completar_missao('descobrir_extensao')
                    else:
                        aviso("Extensão já descoberta!")
                else:
                    erro("Extraia documentos suficientes primeiro!")

            elif 'preparar' in comando or 'ataque' in comando:
                if game_state.missoes['descobrir_extensao'] and game_state.nivel_infiltracao >= 80:
                    if not game_state.missoes['preparar_ataque']:
                        if simular_preparar_ataque(game_state):
                            game_state.completar_missao('preparar_ataque')
                            game_state.capitulo_concluido = True
                            game_state.operacao_sucesso = True
                    else:
                        aviso("Ataque já preparado!")
                else:
                    erro("Complete todas as missões anteriores!")

            else:
                erro("Comando não reconhecido. Tente: acessar, escalar, pivotar, extrair, extensao, preparar")

            # Verificar conclusão
            if game_state.capitulo_concluido:
                print(f"\n{C.VERDE}🎯 CAPÍTULO 9 CONCLUÍDO! 🎯{C.RESET}")
                print("A extensão global da conspiração foi revelada. A batalha final se aproxima...")
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
        print("Capítulo 9 - Exploits Avançados:")
        print("• Acesso a Redes Governamentais: Bypass de firewalls")
        print("• Escalada de Privilégios: Exploração de vulnerabilidades")
        print("• Pivotamento Lateral: Movimento na rede")
        print("• Extração de Dados Críticos: Acesso a informações sensíveis")
        print(f"{C.VERMELHO}⚠️  Você perdeu tempo consultando o manual! ⚠️{C.RESET}")


if __name__ == "__main__":
    # Para testes diretos
    dados_teste = {
        'player_name': 'Teste',
        'codiname': 'TESTE',
        'current_chapter': 9,
        'score': 500,
        'privacy_level': 50,
        'bitcoin_wallet': 0.1,
        'reputation': 150
    }

    resultado = iniciar(dados_teste, '/tmp/teste_chapter9.json')
    print("Resultado:", resultado)
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0) or 0
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        self.darknet_access = True
        self.aliados = dados_anteriores.get('aliados', 0)
        self.segredos_descobertos = dados_anteriores.get('segredos_descobertos', [])
        self.firewalls_quebrados = dados_anteriores.get('firewalls_quebrados', 0)
        self.sistemas_comprometidos = dados_anteriores.get('sistemas_comprometidos', 0)

        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False

        # Estado específico do capítulo
        self.revelacoes = 0
        self.confrontos = 0

    def registrar_falha(self, penalidade=35):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        if self.privacy_level <= 0:
            self.game_over = True

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 30

    def adicionar_revelacao(self):
        self.revelacoes += 1

    def adicionar_confronto(self):
        self.confrontos += 1

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 9,  # Sempre capítulo 9
            'completed_chapters': [1, 2, 3, 4, 5, 6, 7, 8],  # Capítulos 1-8 devem estar completados
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy_level,
            'reputation': self.reputation,
            'score': self.score,
            'inventory': self.inventory,
            'darknet_access': self.darknet_access,
            'aliados': self.aliados,
            'segredos_descobertos': self.segredos_descobertos,
            'firewalls_quebrados': self.firewalls_quebrados,
            'sistemas_comprometidos': self.sistemas_comprometidos,
            'revelacoes': self.revelacoes,
            'confrontos': self.confrontos,
            'completed': getattr(self, 'capitulo_concluido', False),
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }


# ========== UI AUXILIAR ==========

def header_kali_v2(titulo="CAPÍTULO 9: A VERDADE DESVELADA"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass

    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Revelações - Confronto Final | Status: DESVELANDO':^{largura}}{C.RESET}")
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
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/truth{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

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

def mostrar_status_revelacao(state):
    """Mostra status das revelações"""
    print(f"\n{C.ROXO}╔════ STATUS DAS REVELAÇÕES ════╗{C.RESET}")
    print(f"{C.ROXO}║ Revelações: {state.revelacoes:>2}               ║{C.RESET}")
    print(f"{C.ROXO}║ Confrontos: {state.confrontos:>2}                ║{C.RESET}")
    print(f"{C.ROXO}║ Reputation: {state.reputation:>3}              ║{C.RESET}")
    print(f"{C.ROXO}╚{'═'*34}╝{C.RESET}\n")


# ========== QUESTS/DESAFIOS ==========

def quest_1_data_analysis(state):
    """Quest 1: Análise profunda de dados - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 1: ANÁLISE DE DADOS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Decifrar dados roubados  ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*40}╝{C.RESET}\n")

    pensamento("Os dados que roubamos... eles contêm a verdade completa.")

    # Parte 1: Descriptografar arquivos
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "gpg" in cmd and "decrypt" in cmd:
            print(f"{C.CINZA}[*] Descriptografando arquivos...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Arquivos descriptografados{C.RESET}")
            print(f"{C.AMARELO}[!] Conteúdo sensível detectado{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'gpg --decrypt arquivo.gpg' para descriptografar.{C.RESET}")
            state.registrar_falha(12)

    # Parte 2: Analisar conteúdo
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "grep" in cmd and "origem" in cmd:
            print(f"{C.CINZA}[*] Procurando origem da conspiração...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Conspiração começa em 1998{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Envolve ex-presidentes{C.RESET}")
            state.adicionar_revelacao()
            break
        else:
            print(f"{C.VERMELHO}Use 'grep -r \"origem\" dados/' para procurar.{C.RESET}")
            state.registrar_falha(10)

    pensamento("Isso vai mais fundo do que imaginava. A conspiração é antiga.")

    state.registrar_sucesso(60, 0.03)
    return True

def quest_2_personal_confrontation(state):
    """Quest 2: Confrontação pessoal - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 2: CONFRONTAÇÃO PESSOAL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Enfrentar V0id_Walker      ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*42}╝{C.RESET}\n")

    pensamento("V0id_Walker... preciso confrontá-lo uma última vez.")

    # Cena de confronto
    print(f"\n{C.ROXO}[V0id_Walker]: Você destruiu tudo que construímos.{C.RESET}")
    print(f"{C.CIANO}[Você]: Vocês traíram a todos. Inclusive a mim.{C.RESET}")
    print(f"{C.ROXO}[V0id_Walker]: Traição? Nós salvamos o mundo da anarquia.{C.RESET}")
    print(f"{C.CIANO}[Você]: Salvamento? Vocês controlam como ditadores digitais!{C.RESET}")

    drama_pause(2)

    # Parte 1: Revelar evidências
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "show" in cmd and "evidence" in cmd:
            print(f"{C.CINZA}[*] Apresentando evidências...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Logs de manipulação eleitoral exibidos{C.RESET}")
            print(f"{C.VERDE}[+] Comprovantes de propinas mostrados{C.RESET}")
            state.adicionar_confronto()
            break
        else:
            print(f"{C.VERMELHO}Use 'show_evidence --all' para apresentar provas.{C.RESET}")
            state.registrar_falha(15)

    pensamento("Ele está encurralado. Mas ainda tem segredos guardados.")

    state.registrar_sucesso(80, 0.04)
    return True

def quest_3_hidden_motives(state):
    """Quest 3: Motivos ocultos - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 3: MOTIVOS OCULTOS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Descobrir razões reais    ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*39}╝{C.RESET}\n")

    pensamento("Por que eles realmente fazem isso? Qual é o motivo verdadeiro?")

    # Parte 1: Investigar background
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "whois" in cmd or "recon" in cmd:
            print(f"{C.CINZA}[*] Investigando background de V0id_Walker...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Nome real - Carlos Eduardo Silva{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Ex-agente da ABIN{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Despedido por corrupção{C.RESET}")
            state.adicionar_revelacao()
            break
        else:
            print(f"{C.VERMELHO}Use 'whois void_walker.onion' para investigar.{C.RESET}")
            state.registrar_falha(13)

    # Parte 2: Conectar pontos
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "timeline" in cmd or "connect" in cmd:
            print(f"{C.CINZA}[*] Conectando pontos da conspiração...{C.RESET}")
            time.sleep(5)
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Motivo - Vingança pessoal{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO: ABIN o demitiu injustamente{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO: Criou Anônimos para se vingar{C.RESET}")
            state.adicionar_revelacao()
            break
        else:
            print(f"{C.VERMELHO}Use 'timeline_analysis eventos.txt' para conectar.{C.RESET}")
            state.registrar_falha(14)

    pensamento("Tudo começou com vingança pessoal. Mas cresceu para algo muito maior.")

    state.registrar_sucesso(90, 0.05)
    return True

def quest_4_moral_dilemma(state):
    """Quest 4: Dilema moral - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 4: DILEMA MORAL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Decidir o destino final  ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*39}╝{C.RESET}\n")

    pensamento("Agora sei a verdade. Mas o que fazer com ela?")

    mostrar_status_revelacao(state)

    print(f"{C.AMARELO}[DILEMA]: Você descobriu que V0id_Walker foi injustiçado.{C.RESET}")
    print(f"{C.AMARELO}         Mas seus métodos causaram danos irreparáveis.{C.RESET}")
    print(f"{C.AMARELO}         O que você faz?{C.RESET}\n")

    print(f"{C.BRANCO}[1] PERDOAR - Dar uma segunda chance a V0id_Walker{C.RESET}")
    print(f"{C.BRANCO}[2] JUSTIÇA - Entregá-lo às autoridades{C.RESET}")
    print(f"{C.BRANCO}[3] AMBIGUIDADE - Deixar o destino decidir{C.RESET}")

    while True:
        try:
            escolha = input(f"\n{C.VERMELHO}[ESCOLHA 1, 2 ou 3]: {C.RESET}").strip()
        except:
            state.saindo_para_menu = True
            return False

        if escolha == "1":
            print(f"\n{C.CIANO}[PERDÃO] Você decide perdoar.{C.RESET}")
            print(f"{C.CINZA}Consequências: Aliança frágil, mas possibilidade de redenção.{C.RESET}")
            state.dilema_escolha = "perdao"
            break
        elif escolha == "2":
            print(f"\n{C.VERMELHO}[JUSTIÇA] Você escolhe justiça.{C.RESET}")
            print(f"{C.CINZA}Consequências: Fim da conspiração, mas culpa pessoal.{C.RESET}")
            state.dilema_escolha = "justica"
            break
        elif escolha == "3":
            print(f"\n{C.AMARELO}[AMBIGUIDADE] Você deixa o destino decidir.{C.RESET}")
            print(f"{C.CINZA}Consequências: Resultado incerto, mas paz interior.{C.RESET}")
            state.dilema_escolha = "ambiguidade"
            break
        else:
            print(f"{C.VERMELHO}Escolha inválida. Digite 1, 2 ou 3.{C.RESET}")

    state.adicionar_confronto()
    state.registrar_sucesso(100, 0.06)
    return True

def quest_5_final_revelation(state):
    """Quest 5: Revelação final - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 5: REVELAÇÃO FINAL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: A verdade completa        ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*38}╝{C.RESET}\n")

    pensamento("Há mais uma camada. Preciso descobrir tudo.")

    # Parte 1: Arquivo secreto
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "cat" in cmd and "secret" in cmd:
            print(f"{C.CINZA}[*] Lendo arquivo secreto...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERMELHO}[!] REVELAÇÃO FINAL: Os Anônimos foram criados pela ABIN{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO FINAL: Era um experimento de controle social{C.RESET}")
            print(f"{C.VERMELHO}[!] REVELAÇÃO FINAL: V0id_Walker era o rato de laboratório{C.RESET}")
            state.adicionar_revelacao()
            break
        else:
            print(f"{C.VERMELHO}Use 'cat arquivo_secreto.txt' para ler.{C.RESET}")
            state.registrar_falha(16)

    pensamento("Tudo era uma farsa. Os Anônimos eram controlados desde o início.")

    state.registrar_sucesso(120, 0.07)
    return True

def quest_6_closing_decision(state):
    """Quest 6: Decisão final - Dificuldade: Máxima"""
    print(f"\n{C.VERMELHO}╔════ QUEST 6: DECISÃO FINAL ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Objetivo: Escolher seu legado     ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*37}╝{C.RESET}\n")

    pensamento("Com toda a verdade revelada, qual será minha escolha final?")

    mostrar_status_revelacao(state)

    print(f"{C.AMARELO}[DECISÃO FINAL]: Você sabe de tudo agora.{C.RESET}")
    print(f"{C.AMARELO}                 O sistema está quebrado.{C.RESET}")
    print(f"{C.AMARELO}                 Você pode reconstruí-lo.{C.RESET}\n")

    print(f"{C.BRANCO}[1] DESTRUIR - Queimar tudo e começar do zero{C.RESET}")
    print(f"{C.BRANCO}[2] REFORMAR - Usar o conhecimento para mudanças{C.RESET}")
    print(f"{C.BRANCO}[3] DESAPARECER - Sair de cena para sempre{C.RESET}")

    while True:
        try:
            escolha = input(f"\n{C.VERMELHO}[ESCOLHA 1, 2 ou 3]: {C.RESET}").strip()
        except:
            state.saindo_para_menu = True
            return False

        if escolha == "1":
            print(f"\n{C.VERMELHO}[DESTRUIÇÃO] Você escolhe queimar tudo.{C.RESET}")
            print(f"{C.CINZA}Consequências: Caos total, mas possibilidade de renascimento.{C.RESET}")
            state.final_escolha = "destruir"
            break
        elif escolha == "2":
            print(f"\n{C.CIANO}[REFORMA] Você escolhe reformar.{C.RESET}")
            print(f"{C.CINZA}Consequências: Mudanças graduais, mas duradouras.{C.RESET}")
            state.final_escolha = "reformar"
            break
        elif escolha == "3":
            print(f"\n{C.AMARELO}[DESAPARECIMENTO] Você desaparece.{C.RESET}")
            print(f"{C.CINZA}Consequências: Paz pessoal, mas questões não resolvidas.{C.RESET}")
            state.final_escolha = "desaparecer"
            break
        else:
            print(f"{C.VERMELHO}Escolha inválida. Digite 1, 2 ou 3.{C.RESET}")

    state.adicionar_confronto()
    state.registrar_sucesso(150, 0.08)
    return True


# ========== CENA PRINCIPAL ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)

    digitar(f"{C.CINZA}A poeira baixou.{C.RESET}", delay=0.1)
    drama_pause(1)
    digitar(f"{C.CINZA}Os sistemas estão expostos.{C.RESET}", delay=0.08)
    drama_pause(1)
    digitar(f"{C.CINZA}Agora vem a parte mais difícil.{C.RESET}", delay=0.08)

    drama_pause(2)

    header_kali_v2()
    drama_pause(1)

    narracao("Você tem acesso a tudo agora.")
    narracao("Os segredos mais profundos dos Anônimos.")
    drama_pause(1)

    pensamento("A verdade é mais complexa do que imaginava.")
    pensamento("Cada revelação traz mais perguntas.")

    mostrar_status_revelacao(state)
    drama_pause(2)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter9(dados_jogador)

    try:
        cena_abertura(state)

        if state.saindo_para_menu:
            return state.to_dict()

        # Executar quests em sequência
        quests = [
            quest_1_data_analysis,
            quest_2_personal_confrontation,
            quest_3_hidden_motives,
            quest_4_moral_dilemma,
            quest_5_final_revelation,
            quest_6_closing_decision
        ]

        for quest in quests:
            if not quest(state):
                if state.saindo_para_menu:
                    return state.to_dict()
                break

        # Final do capítulo
        drama_pause(2)
        header_kali_v2()

        print(f"\n{C.VERDE}{'═'*60}{C.RESET}")
        print(f"{C.VERDE}{'CAPÍTULO 9: VERDADE - CONCLUÍDO':^60}{C.RESET}")
        print(f"{C.VERDE}{'═'*60}{C.RESET}")

        print(f"\n{C.AMARELO}Resultado das Revelações:{C.RESET}")
        print(f"{C.AMARELO}- Revelações descobertas: {state.revelacoes}{C.RESET}")
        print(f"{C.AMARELO}- Confrontos realizados: {state.confrontos}{C.RESET}")
        if hasattr(state, 'dilema_escolha'):
            print(f"{C.AMARELO}- Dilema moral: {state.dilema_escolha}{C.RESET}")
        if hasattr(state, 'final_escolha'):
            print(f"{C.AMARELO}- Escolha final: {state.final_escolha}{C.RESET}")

        state.capitulo_concluido = True
        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

