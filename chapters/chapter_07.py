#!/usr/bin/env python3
"""
CHAPTER_07.PY - "O Cerco se Fecha"
Com aliados conquistados, preciso coletar inteligência concreta.
Engenharia social, phishing direcionado, e coleta de evidências irrefutáveis.

Foco: Engenharia social avançada, coleta de inteligência
Habilidades: Phishing direcionado, engenharia social, análise comportamental
Objetivos: 6 missões principais + coleta de evidências
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
        self.current_chapter = dados_jogador.get('current_chapter', 7)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 65)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.05)
        self.reputation = dados_jogador.get('reputation', 50)

        # Estado do capítulo
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.checkpoint = 'inicio'

        # Missões do capítulo 7
        self.missoes = {
            'analisar_alvo': False,           # Analisar perfil do alvo
            'criar_phishing': False,          # Criar email de phishing direcionado
            'enviar_phishing': False,         # Enviar phishing e aguardar resposta
            'acessar_conta': False,           # Acessar conta comprometida
            'extrair_inteligencia': False,    # Extrair inteligência valiosa
            'compilar_evidencias': False      # Compilar evidências contra conspiradores
        }

        # Contadores e flags
        self.tentativas_phishing = 0
        self.evidencias_coletadas = 0
        self.nivel_risco = 0

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.reputation += 8
        self.privacy_level = max(0, self.privacy_level - 5)

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.reputation = max(0, self.reputation - 5)
        self.privacy_level = max(0, self.privacy_level - 12)
        self.nivel_risco += 20

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(30)
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
            'chapter_07_checkpoint': self.checkpoint,
            'capitulo_7_resultado': None,
            'capitulo_7_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_7': self.missoes.copy(),
            'evidencias_coletadas': self.evidencias_coletadas,
            'nivel_risco': self.nivel_risco
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
    print("                [ROOT EVOLUTION - CAPÍTULO 7: O CERCO SE FECHA]")
    print("                 Dark Web, 08:15 PM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")
    print(f"{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.")
    print(f"📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.")
    print("═" * 80)
    print(f"{C.RESET}")


# ========== FUNÇÕES DE TUTORIAL ==========

def tutorial_phishing():
    """Tutorial sobre phishing direcionado"""
    print(f"\n{C.CIANO}[TUTORIAL - PHISHING DIRECIONADO]{C.RESET}")
    print("Phishing direcionado (spear-phishing) é muito mais efetivo que phishing em massa.")
    print("Elementos chave:")
    print("  • Pesquisa prévia: Conheça seu alvo profundamente")
    print("  • Personalização: Use detalhes específicos da vida do alvo")
    print("  • Urgência: Crie pressão temporal")
    print("  • Confiança: Finja ser alguém que o alvo conhece")
    print("\nTécnicas avançadas:")
    print("  • Pretexting: Crie um cenário plausível")
    print("  • Baiting: Use isca irresistível")
    print("  • Vishing: Ataque por voz/telefone")
    print(f"{C.AMARELO}Lembre-se: O alvo é humano, explore fraquezas emocionais!{C.RESET}\n")


# ========== FUNÇÕES DE MISSÃO ==========

def simular_analise_alvo(game_state):
    """Simula análise de perfil do alvo"""
    print(f"\n{C.AMARELO}[ANÁLISE DE PERFIL DO ALVO]{C.RESET}")
    print("Analisando Marcus Silva - possível superior de Juliana...")

    perfil = {
        "Nome": "Marcus Silva",
        "Cargo": "Coordenador de TI - Ministério da Justiça",
        "Email": "marcus.silva@justica.gov.br",
        "Redes Sociais": "LinkedIn, Facebook (privado)",
        "Interesses": "Futebol, política, tecnologia",
        "Fraquezas": "Orgulhoso de conquistas profissionais",
        "Contatos": "Juliana Silva (subordinada), vários políticos"
    }

    print(f"{C.CIANO}PERFIL DO ALVO:{C.RESET}")
    for chave, valor in perfil.items():
        print(f"  {chave}: {valor}")

    print(f"\n{C.VERDE}✓ Perfil mapeado! Ponto fraco identificado.{C.RESET}")
    print(f"{C.AMARELO}Marcus é orgulhoso - use isso contra ele.{C.RESET}")

    return True


def simular_criacao_phishing(game_state):
    """Simula criação de email de phishing"""
    print(f"\n{C.AMARELO}[CRIAÇÃO DE PHISHING DIRECIONADO]{C.RESET}")
    print("Criando email personalizado para Marcus Silva...")

    email = """
Assunto: Reconhecimento pelo Projeto de Modernização

Prezado Marcus,

Espero que esta mensagem o encontre bem. Meu nome é Ana Costa, sou coordenadora
do programa de reconhecimento profissional da Associação Brasileira de TI.

Tivemos conhecimento do seu excelente trabalho no projeto de modernização dos
sistemas do Ministério da Justiça, especialmente na implementação das novas
ferramentas de análise de dados.

Gostaríamos de convidá-lo para participar do nosso evento anual de tecnologia,
onde será homenageado como "Profissional do Ano em Governo Digital".

Para confirmar sua participação e receber mais detalhes (incluindo passagens
e hospedagem gratuitas), acesse o link abaixo e faça seu cadastro:

[LINK PHISHING: https://reconhecimento-abti.com/confirmacao/marcus-silva]

Atenciosamente,
Ana Costa
Coordenadora de Reconhecimento
Associação Brasileira de TI
    """

    print(f"{C.ROXO}EMAIL CRIADO:{C.RESET}")
    print(email)

    print(f"\n{C.VERDE}✓ Email de phishing criado!{C.RESET}")
    print(f"{C.AMARELO}Personalizado com detalhes específicos do alvo.{C.RESET}")

    return True


def simular_envio_phishing(game_state):
    """Simula envio e resposta ao phishing"""
    print(f"\n{C.AMARELO}[ENVIO DE PHISHING]{C.RESET}")
    print("Enviando email para marcus.silva@justica.gov.br...")

    time.sleep(2)
    print(f"{C.CINZA}Email enviado via servidor SMTP spoofed...{C.RESET}")

    # Simulação de resposta
    time.sleep(3)
    print(f"\n{C.VERDE}✓ RESPOSTA RECEBIDA!{C.RESET}")
    print(f"{C.CINZA}De: marcus.silva@justica.gov.br{C.RESET}")
    print(f"{C.CINZA}Assunto: Re: Reconhecimento pelo Projeto{C.RESET}")
    print(f"{C.CINZA}Mensagem: Obrigado pelo reconhecimento! Cliquei no link e me cadastrei.{C.RESET}")
    print(f"{C.CINZA}Anexo: comprovante.pdf (contém malware){C.RESET}")

    print(f"\n{C.VERDE}✓ Phishing funcionou! Credenciais capturadas.{C.RESET}")
    print(f"{C.AMARELO}Agora tenho acesso à conta de email de Marcus.{C.RESET}")

    game_state.evidencias_coletadas += 1
    return True


def simular_acesso_conta(game_state):
    """Simula acesso à conta comprometida"""
    print(f"\n{C.AMARELO}[ACESSO À CONTA COMPROMETIDA]{C.RESET}")
    print("Acessando conta de email de Marcus Silva...")

    emails_interessantes = [
        {
            "de": "juliana.silva@empresa.com",
            "assunto": "Relatório Semanal - Projeto Raiz",
            "conteudo": "Anexo: relatório_confidencial.pdf (detalhes da operação)"
        },
        {
            "de": "diretor@justica.gov.br",
            "assunto": "Aprovação - Fase 2 do Projeto",
            "conteudo": "Aprovado investimento de R$ 50 milhões para expansão"
        },
        {
            "de": "contato@techcorp.com",
            "assunto": "Pagamento Recebido - Serviços Prestados",
            "conteudo": "Transferência de 2.5 BTC confirmada"
        }
    ]

    for email in emails_interessantes:
        print(f"\n{C.CIANO}EMAIL ENCONTRADO:{C.RESET}")
        print(f"  De: {email['de']}")
        print(f"  Assunto: {email['assunto']}")
        print(f"  Conteúdo: {email['conteudo']}")

    print(f"\n{C.VERDE}✓ Acesso completo à conta!{C.RESET}")
    print(f"{C.AMARELO}Evidências claras da conspiração.{C.RESET}")

    game_state.evidencias_coletadas += 3
    return True


def simular_extracao_inteligencia(game_state):
    """Simula extração de inteligência valiosa"""
    print(f"\n{C.AMARELO}[EXTRAÇÃO DE INTELIGÊNCIA]{C.RESET}")
    print("Analisando dados extraídos da conta de Marcus...")

    inteligencia = {
        "Objetivo da Operação": "Controle de dados pessoais de cidadãos brasileiros",
        "Envolvidos": ["Ministério da Justiça", "TechCorp", "Juliana Silva", "Marcus Silva"],
        "Financiamento": "R$ 50 milhões + criptomoedas",
        "Próximos Passos": "Implementação de backdoors em sistemas bancários",
        "Riscos": "Possível descoberta por hackers éticos"
    }

    print(f"{C.ROXO}INTELIGÊNCIA COLETADA:{C.RESET}")
    for chave, valor in inteligencia.items():
        print(f"  {chave}: {valor}")

    print(f"\n{C.VERDE}✓ Inteligência crítica extraída!{C.RESET}")
    print(f"{C.AMARELO}A conspiração é sobre controle total de dados pessoais.{C.RESET}")

    game_state.evidencias_coletadas += 5
    return True


def simular_compilacao_evidencias(game_state):
    """Simula compilação de evidências"""
    print(f"\n{C.ROXO}[COMPILAÇÃO DE EVIDÊNCIAS]{C.RESET}")
    print("Compilando todas as evidências coletadas...")

    evidencias = [
        "✓ Emails entre Juliana e Marcus",
        "✓ Relatórios confidenciais do governo",
        "✓ Registros de pagamentos em BTC",
        "✓ Documentos sobre backdoors",
        "✓ Provas de conspiração corporativa",
        "✓ Lista completa de envolvidos"
    ]

    print(f"{C.CIANO}EVIDÊNCIAS COMPILADAS:{C.RESET}")
    for evidencia in evidencias:
        print(f"  {evidencia}")

    time.sleep(2)
    print(f"\n{C.VERDE}✓ Dossiê completo criado!{C.RESET}")
    print(f"{C.AMARELO}Agora tenho provas irrefutáveis da conspiração.{C.RESET}")
    print(f"{C.VERMELHO}Mas isso me torna um alvo...{C.RESET}")

    game_state.evidencias_coletadas += 10
    return True


# ========== FUNÇÃO PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save):
    """Função principal do capítulo 7"""
    game_state = GameState(dados_jogador)

    # Carregar checkpoint se existir
    if os.path.exists(arquivo_save):
        try:
            with open(arquivo_save, 'r') as f:
                dados_salvos = json.load(f)
            checkpoint = dados_salvos.get('chapter_07_checkpoint', 'inicio')
            if checkpoint != 'inicio':
                game_state.checkpoint = checkpoint
                game_state.missoes = dados_salvos.get('missoes_capitulo_7', game_state.missoes)
                game_state.evidencias_coletadas = dados_salvos.get('evidencias_coletadas', 0)
                game_state.nivel_risco = dados_salvos.get('nivel_risco', 0)
                print(f"{C.AMARELO}Continuando do checkpoint: {checkpoint}{C.RESET}")
        except:
            pass

    exibir_header()

    # Narrativa inicial
    digitar("Com GhostWriter como aliado, tenho um nome: Marcus Silva.", cor=C.BRANCO)
    digitar("Superior de Juliana no Ministério da Justiça.", cor=C.CINZA)
    digitar("Preciso de evidências concretas. Emails, documentos, provas.", cor=C.CINZA)
    digitar("Engenharia social é a chave. Conhecer o alvo, explorar fraquezas.", cor=C.CINZA)
    digitar("Mas cada passo aumenta o risco. Eles sabem que estou chegando.", cor=C.VERMELHO)
    print()

    # Loop principal do jogo
    while not game_state.capitulo_concluido:
        try:
            # Verificar progresso
            completas, total = game_state.verificar_progresso()
            print(f"\n{C.AMARELO}Progresso: {completas}/{total} missões completas{C.RESET}")
            print(f"{C.AMARELO}Pontuação: {game_state.score} | Reputação: {game_state.reputation}{C.RESET}")
            print(f"{C.AMARELO}Evidências: {game_state.evidencias_coletadas} | Risco: {game_state.nivel_risco}{C.RESET}")

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
                tutorial_phishing()
                continue

            # Missões
            elif 'analisar' in comando or 'alvo' in comando:
                if not game_state.missoes['analisar_alvo']:
                    if simular_analise_alvo(game_state):
                        game_state.completar_missao('analisar_alvo')
                else:
                    aviso("Alvo já analisado!")

            elif 'criar' in comando or 'phishing' in comando:
                if game_state.missoes['analisar_alvo']:
                    if not game_state.missoes['criar_phishing']:
                        if simular_criacao_phishing(game_state):
                            game_state.completar_missao('criar_phishing')
                    else:
                        aviso("Phishing já criado!")
                else:
                    erro("Analise o alvo primeiro!")

            elif 'enviar' in comando or 'email' in comando:
                if game_state.missoes['criar_phishing']:
                    if not game_state.missoes['enviar_phishing']:
                        if simular_envio_phishing(game_state):
                            game_state.completar_missao('enviar_phishing')
                        else:
                            game_state.registrar_falha()
                    else:
                        aviso("Phishing já enviado!")
                else:
                    erro("Crie o phishing primeiro!")

            elif 'acessar' in comando or 'conta' in comando:
                if game_state.missoes['enviar_phishing']:
                    if not game_state.missoes['acessar_conta']:
                        if simular_acesso_conta(game_state):
                            game_state.completar_missao('acessar_conta')
                    else:
                        aviso("Conta já acessada!")
                else:
                    erro("Envie o phishing primeiro!")

            elif 'extrair' in comando or 'inteligencia' in comando:
                if game_state.missoes['acessar_conta']:
                    if not game_state.missoes['extrair_inteligencia']:
                        if simular_extracao_inteligencia(game_state):
                            game_state.completar_missao('extrair_inteligencia')
                    else:
                        aviso("Inteligência já extraída!")
                else:
                    erro("Acesse a conta primeiro!")

            elif 'compilar' in comando or 'evidencias' in comando:
                if game_state.missoes['extrair_inteligencia'] and game_state.evidencias_coletadas >= 5:
                    if not game_state.missoes['compilar_evidencias']:
                        if simular_compilacao_evidencias(game_state):
                            game_state.completar_missao('compilar_evidencias')
                            game_state.capitulo_concluido = True
                            game_state.operacao_sucesso = True
                    else:
                        aviso("Evidências já compiladas!")
                else:
                    erro("Extraia inteligência e colete evidências suficientes!")

            else:
                erro("Comando não reconhecido. Tente: analisar, criar, enviar, acessar, extrair, compilar")

            # Verificar conclusão
            if game_state.capitulo_concluido:
                print(f"\n{C.VERDE}🎯 CAPÍTULO 7 CONCLUÍDO! 🎯{C.RESET}")
                print("Evidências irrefutáveis coletadas. A conspiração está exposta...")
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
        print("Capítulo 7 - Engenharia Social Avançada:")
        print("• Análise de Alvo: Mapeamento de perfil e fraquezas")
        print("• Phishing Direcionado: Ataques personalizados")
        print("• Extração de Dados: Análise de informações comprometidas")
        print("• Compilação de Evidências: Construção de dossiês")
        print(f"{C.VERMELHO}⚠️  Você perdeu tempo consultando o manual! ⚠️{C.RESET}")


if __name__ == "__main__":
    # Para testes diretos
    dados_teste = {
        'player_name': 'Teste',
        'codiname': 'TESTE',
        'current_chapter': 7,
        'score': 300,
        'privacy_level': 65,
        'bitcoin_wallet': 0.05,
        'reputation': 50
    }

    resultado = iniciar(dados_teste, '/tmp/teste_chapter7.json')
    print("Resultado:", resultado)
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0) or 0
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        self.darknet_access = True  # Sempre true neste capítulo
        self.perseguidores = dados_anteriores.get('perseguidores', 0)

        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False

        # Estado específico do capítulo
        self.aliados = 0
        self.segredos_descobertos = []

    def registrar_falha(self, penalidade=25):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        if self.privacy_level <= 0:
            self.game_over = True

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 20

    def adicionar_aliado(self):
        self.aliados += 1

    def adicionar_segredo(self, segredo):
        self.segredos_descobertos.append(segredo)

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 7,  # Sempre capítulo 7
            'completed_chapters': [1, 2, 3, 4, 5, 6],  # Capítulos 1-6 devem estar completados
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy_level,
            'reputation': self.reputation,
            'score': self.score,
            'inventory': self.inventory,
            'darknet_access': self.darknet_access,
            'perseguidores': self.perseguidores,
            'aliados': self.aliados,
            'segredos_descobertos': self.segredos_descobertos,
            'completed': getattr(self, 'capitulo_concluido', False),
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }


# ========== UI AUXILIAR ==========

def header_kali_v2(titulo="CAPÍTULO 7: A REDE SOMBRIA"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass

    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Dark Web Deep - Alianças | Status: EXPLORANDO':^{largura}}{C.RESET}")
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
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/darknet{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

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

def mostrar_status_rede(state):
    """Mostra status da rede sombria"""
    print(f"\n{C.ROXO}╔════ STATUS DA REDE ════╗{C.RESET}")
    print(f"{C.ROXO}║ Aliados: {state.aliados:>2}              ║{C.RESET}")
    print(f"{C.ROXO}║ Segredos: {len(state.segredos_descobertos):>2}             ║{C.RESET}")
    print(f"{C.ROXO}║ Reputation: {state.reputation:>3}         ║{C.RESET}")
    print(f"{C.ROXO}╚{'═'*27}╝{C.RESET}\n")


# ========== QUESTS/DESAFIOS ==========

def quest_1_hidden_services(state):
    """Quest 1: Serviços ocultos - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 1: SERVIÇOS OCULTOS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Descobrir fóruns secretos ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*40}╝{C.RESET}\n")

    pensamento("A dark web é como uma cebola. Cada camada esconde mais segredos.")

    # Parte 1: Onion scanner
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "onion" in cmd and "scan" in cmd:
            print(f"{C.CINZA}[*] Escaneando serviços .onion...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Forum Secreto: dreadforum.onion{C.RESET}")
            print(f"{C.VERDE}[+] Mercado Negro: blackmarket.onion{C.RESET}")
            print(f"{C.VERDE}[+] Biblioteca Hacker: hacklib.onion{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'onionscan dreadforum.onion' para escanear.{C.RESET}")
            state.registrar_falha(10)

    # Parte 2: Acessar fórum
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "torsocks" in cmd and "dreadforum" in cmd:
            print(f"{C.CINZA}[*] Acessando Dread Forum...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Conectado ao fórum underground{C.RESET}")
            print(f"{C.VERDE}[+] Threads ativos: 1.247{C.RESET}")
            print(f"{C.AMARELO}[!] Thread interessante: 'Os Anônimos traíram a todos'{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'torsocks wget http://dreadforum.onion' para acessar.{C.RESET}")
            state.registrar_falha(12)

    pensamento("Há discussões sobre traição dos Anônimos. Preciso investigar mais fundo.")

    state.adicionar_segredo("Traição dos Anônimos")
    state.registrar_sucesso(40, 0.02)
    return True

def quest_2_ally_recruitment(state):
    """Quest 2: Recrutamento de aliados - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 2: RECRUTAMENTO ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Ganhar confiança      ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*34}╝{C.RESET}\n")

    pensamento("Aliados são essenciais na dark web. Mas como confiar em estranhos?")

    # Parte 1: Verificar reputação
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "pgp" in cmd and "verify" in cmd:
            print(f"{C.CINZA}[*] Verificando assinatura PGP...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Assinatura válida - Usuário: ShadowBroker{C.RESET}")
            print(f"{C.VERDE}[+] Reputação: Alta (94% confiança){C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'gpg --verify mensagem.asc' para verificar PGP.{C.RESET}")
            state.registrar_falha(8)

    # Parte 2: Negociação
    print(f"\n{C.BRANCO}[ShadowBroker]: Quem é você? O que quer?{C.RESET}")
    print(f"{C.CIANO}[Você]: Sou {state.codinome}. Os Anônimos me traíram.{C.RESET}")

    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "bitcoin" in cmd or "btc" in cmd:
            print(f"{C.CINZA}[*] Enviando 0.05 BTC como sinal de boa fé...{C.RESET}")
            time.sleep(2)
            if state.bitcoin >= 0.05:
                state.bitcoin -= 0.05
                print(f"{C.VERDE}[+] Pagamento confirmado{C.RESET}")
                print(f"{C.VERDE}[+] ShadowBroker aceitou aliança{C.RESET}")
                state.adicionar_aliado()
                break
            else:
                print(f"{C.VERMELHO}[!] BTC insuficiente!{C.RESET}")
                state.registrar_falha(15)
        else:
            print(f"{C.VERMELHO}Envie BTC como sinal de confiança.{C.RESET}")
            state.registrar_falha(10)

    pensamento("Meu primeiro aliado na dark web. Isso pode mudar tudo.")

    state.registrar_sucesso(50, 0.01)  # BTC já foi debitado
    return True

def quest_3_data_mining(state):
    """Quest 3: Mineração de dados - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 3: MINERAÇÃO DE DADOS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Analisar dados globais    ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*39}╝{C.RESET}\n")

    pensamento("Os dados são o novo petróleo. Vamos extrair alguns segredos.")

    # Parte 1: Coletar dados
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "scrapy" in cmd or "crawl" in cmd:
            print(f"{C.CINZA}[*] Executando crawler na dark web...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERDE}[+] Dados coletados: 15.7GB{C.RESET}")
            print(f"{C.VERDE}[+] Páginas indexadas: 2.341{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'scrapy crawl darkweb_spider' para minerar dados.{C.RESET}")
            state.registrar_falha(14)

    # Parte 2: Analisar dados
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "grep" in cmd and "anonimos" in cmd:
            print(f"{C.CINZA}[*] Procurando referências aos Anônimos...{C.RESET}")
            time.sleep(3)
            print(f"{C.AMARELO}[!] SEGREDO DESCOBERTO: 'Operação Global'{C.RESET}")
            print(f"{C.AMARELO}[!] Os Anônimos operam em 15 países{C.RESET}")
            print(f"{C.AMARELO}[!] Conexão com governos europeus{C.RESET}")
            state.adicionar_segredo("Operação Global")
            break
        else:
            print(f"{C.VERMELHO}Use 'grep -r \"anonimos\" dados/' para procurar.{C.RESET}")
            state.registrar_falha(11)

    pensamento("Isso é maior do que imaginava. Os Anônimos são uma organização global.")

    state.registrar_sucesso(70, 0.03)
    return True

def quest_4_secure_meeting(state):
    """Quest 4: Reunião segura - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 4: REUNIÃO SEGURA ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Encontro com aliados    ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*37}╝{C.RESET}\n")

    pensamento("Precisamos nos encontrar fisicamente. Mas como garantir segurança?")

    # Parte 1: Coordenar local
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "geoi" in cmd or "location" in cmd:
            print(f"{C.CINZA}[*] Coordenando localização segura...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Local: Parque da Cidade - Brasília{C.RESET}")
            print(f"{C.VERDE}[+] Hora: 02:00 AM{C.RESET}")
            print(f"{C.VERDE}[+] Método: Dead drop digital{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'geoi.pl -l parque' para coordenar local.{C.RESET}")
            state.registrar_falha(9)

    # Parte 2: Verificar segurança
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "nmap" in cmd and "parque" in cmd:
            print(f"{C.CINZA}[*] Verificando segurança do local...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Câmeras: 0 ativas{C.RESET}")
            print(f"{C.VERDE}[+] Dispositivos: 2 smartphones (aliados){C.RESET}")
            print(f"{C.VERDE}[+] Segurança: Alta{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'nmap -sn 192.168.1.0/24' para verificar rede local.{C.RESET}")
            state.registrar_falha(10)

    # Cena da reunião
    print(f"\n{C.BRANCO}[ShadowBroker]: Você trouxe as evidências?{C.RESET}")
    print(f"{C.CIANO}[Você]: Tudo está aqui. Mas preciso de mais informações.{C.RESET}")
    print(f"{C.BRANCO}[ShadowBroker]: Os Anônimos controlam eleições em 3 continentes.{C.RESET}")
    print(f"{C.BRANCO}[ShadowBroker]: Junte-se a nós. Formaremos uma nova aliança.{C.RESET}")

    state.adicionar_aliado()
    pensamento("Mais um aliado. A rede cresce.")

    state.registrar_sucesso(60, 0.04)
    return True

def quest_5_global_conspiracy(state):
    """Quest 5: Conspiração global - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 5: CONSPIRAÇÃO GLOBAL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Revelar plano maior       ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*39}╝{C.RESET}\n")

    pensamento("Isso vai além do Brasil. É uma conspiração global.")

    # Parte 1: Analisar comunicações
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "wireshark" in cmd or "tcpdump" in cmd:
            print(f"{C.CINZA}[*] Interceptando comunicações criptografadas...{C.RESET}")
            time.sleep(4)
            print(f"{C.AMARELO}[!] Comunicação interceptada: 'Fase 2 iniciada'{C.RESET}")
            print(f"{C.AMARELO}[!] Origem: Servidor na Suíça{C.RESET}")
            print(f"{C.AMARELO}[!] Destino: 15 países{C.RESET}")
            state.adicionar_segredo("Fase 2 Global")
            break
        else:
            print(f"{C.VERMELHO}Use 'wireshark -i eth0 -f \"port 6667\"' para interceptar.{C.RESET}")
            state.registrar_falha(16)

    # Parte 2: Decifrar mensagens
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "john" in cmd or "hashcat" in cmd:
            print(f"{C.CINZA}[*] Quebrando criptografia...{C.RESET}")
            time.sleep(5)
            print(f"{C.VERMELHO}[!] SEGREDO REVELADO: 'Operação Dominação'{C.RESET}")
            print(f"{C.VERMELHO}[!] OBJETIVO: Controle total de governos mundiais{C.RESET}")
            print(f"{C.VERMELHO}[!] MÉTODO: Manipulação eleitoral + IA{C.RESET}")
            state.adicionar_segredo("Operação Dominação")
            break
        else:
            print(f"{C.VERMELHO}Use 'hashcat -m 0 -a 3 hash.txt wordlist.txt' para quebrar.{C.RESET}")
            state.registrar_falha(18)

    pensamento("Isso é apocalíptico. Eles querem controlar o mundo todo.")

    state.registrar_sucesso(90, 0.06)
    return True

def quest_6_alliance_formation(state):
    """Quest 6: Formação da aliança - Dificuldade: Máxima"""
    print(f"\n{C.VERMELHO}╔════ QUEST 6: ALIANÇA GLOBAL ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Objetivo: Unir forças contra eles ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*38}╝{C.RESET}\n")

    pensamento("Precisamos formar uma aliança global. Esta é nossa única chance.")

    mostrar_status_rede(state)

    # Parte 1: Reunião virtual
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "mumble" in cmd or "teamspeak" in cmd:
            print(f"{C.CINZA}[*] Iniciando conferência segura...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Conectado à sala: Alliance_Global{C.RESET}")
            print(f"{C.VERDE}[+] Participantes: 12 hackers de 8 países{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'mumble mumble://alliance.onion:64738' para conectar.{C.RESET}")
            state.registrar_falha(12)

    # Parte 2: Votação da aliança
    print(f"\n{C.BRANCO}[Aliança Global]: Todos concordam em se unir contra os Anônimos?{C.RESET}")

    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "vote" in cmd and "yes" in cmd:
            print(f"{C.CINZA}[*] Registrando voto...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Voto confirmado: SIM{C.RESET}")
            print(f"{C.VERDE}[+] Aliança formada: 'Os Verdadeiros Anônimos'{C.RESET}")
            print(f"{C.VERDE}[+] Membros: {12 + state.aliados}{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Vote 'yes' para formar a aliança.{C.RESET}")
            state.registrar_falha(20)

    pensamento("A aliança está formada. Agora temos uma chance real.")

    state.registrar_sucesso(120, 0.08)
    return True


# ========== CENA PRINCIPAL ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)

    digitar(f"{C.CINZA}Você mergulhou profundamente na dark web.{C.RESET}", delay=0.1)
    drama_pause(1)
    digitar(f"{C.CINZA}Aqui, as regras são diferentes.{C.RESET}", delay=0.08)
    drama_pause(1)
    digitar(f"{C.CINZA}Aqui, você não está sozinho.{C.RESET}", delay=0.08)

    drama_pause(2)

    header_kali_v2()
    drama_pause(1)

    narracao("A rede sombria pulsa com atividade.")
    narracao("Fóruns secretos, mercados negros, bibliotecas proibidas.")
    drama_pause(1)

    pensamento("Cada conexão é um risco. Mas também uma oportunidade.")
    pensamento("Vamos construir nossa própria rede...")

    mostrar_status_rede(state)
    drama_pause(2)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter7(dados_jogador)

    try:
        cena_abertura(state)

        if state.saindo_para_menu:
            return state.to_dict()

        # Executar quests em sequência
        quests = [
            quest_1_hidden_services,
            quest_2_ally_recruitment,
            quest_3_data_mining,
            quest_4_secure_meeting,
            quest_5_global_conspiracy,
            quest_6_alliance_formation
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
        print(f"{C.VERDE}{'CAPÍTULO 7: ALIANÇAS - CONCLUÍDO':^60}{C.RESET}")
        print(f"{C.VERDE}{'═'*60}{C.RESET}")

        print(f"\n{C.AMARELO}Resultado da Rede Sombria:{C.RESET}")
        print(f"{C.AMARELO}- Aliados recrutados: {state.aliados}{C.RESET}")
        print(f"{C.AMARELO}- Segredos descobertos: {len(state.segredos_descobertos)}{C.RESET}")
        print(f"{C.AMARELO}- Nova aliança: 'Os Verdadeiros Anônimos'{C.RESET}")

        state.capitulo_concluido = True
        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

