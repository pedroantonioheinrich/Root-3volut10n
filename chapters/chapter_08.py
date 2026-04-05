#!/usr/bin/env python3
"""
CHAPTER_08.PY - "Revelações"
Com evidências em mãos, enfrento Juliana. A verdade sobre sua traição.
Motivos pessoais versus conspiração maior. Escolhas difíceis.

Foco: Confrontação emocional, descoberta da verdade
Habilidades: Interrogatório digital, análise psicológica, tomada de decisão
Objetivos: 5 missões principais + revelação completa
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
        self.current_chapter = dados_jogador.get('current_chapter', 8)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 60)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.08)
        self.reputation = dados_jogador.get('reputation', 100)

        # Estado do capítulo
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.checkpoint = 'inicio'

        # Missões do capítulo 8
        self.missoes = {
            'localizar_juliana': False,       # Localizar Juliana
            'infiltrar_comunicacao': False,   # Infiltrar comunicações dela
            'confrontar_juliana': False,      # Confrontação direta
            'descobrir_motivos': False,       # Descobrir verdadeiros motivos
            'fazer_escolha': False           # Fazer escolha final
        }

        # Contadores e flags
        self.nivel_tensao = 0
        self.revelacoes_descobertas = 0
        self.escolha_moral = None

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.reputation += 10

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.nivel_tensao += 25

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(40)
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
            'chapter_08_checkpoint': self.checkpoint,
            'capitulo_8_resultado': None,
            'capitulo_8_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_8': self.missoes.copy(),
            'nivel_tensao': self.nivel_tensao,
            'revelacoes_descobertas': self.revelacoes_descobertas,
            'escolha_moral': self.escolha_moral
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
    print("                 [ROOT EVOLUTION - CAPÍTULO 8: REVELAÇÕES]")
    print("                 Brasília, 02:30 AM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")
    print(f"{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.")
    print(f"📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.")
    print("═" * 80)
    print(f"{C.RESET}")


# ========== FUNÇÕES DE TUTORIAL ==========

def tutorial_interrogatorio():
    """Tutorial sobre interrogatório digital"""
    print(f"\n{C.CIANO}[TUTORIAL - INTERROGATÓRIO DIGITAL]{C.RESET}")
    print("Interrogatório digital combina psicologia e tecnologia:")
    print("  • Análise comportamental: Padrões de comunicação")
    print("  • Engenharia social reversa: Usar conhecimento contra o alvo")
    print("  • Pressão temporal: Criar urgência")
    print("  • Revelação gradual: Construir confiança para extrair informação")
    print("\nTécnicas avançadas:")
    print("  • Mirroring: Imitar padrões de comunicação")
    print("  • Foot-in-the-door: Começar com pedidos pequenos")
    print("  • Door-in-the-face: Contrastar pedidos")
    print(f"{C.AMARELO}Lembre-se: Pessoas sob pressão revelam verdades!{C.RESET}\n")


# ========== FUNÇÕES DE MISSÃO ==========

def simular_localizar_juliana(game_state):
    """Simula localização de Juliana"""
    print(f"\n{C.AMARELO}[LOCALIZANDO JULIANA]{C.RESET}")
    print("Rastreando sinais digitais de Juliana Silva...")

    # Simulação de rastreamento
    time.sleep(2)
    print(f"{C.CIANO}SINAIS ENCONTRADOS:{C.RESET}")
    print("  • Último login: 2 horas atrás - IP residencial")
    print("  • Atividade: Mensagens criptografadas via Signal")
    print("  • Localização aproximada: Asa Norte, Brasília")
    print("  • Status: Online, mas cautelosa")

    print(f"\n{C.VERDE}✓ Juliana localizada! Ela está em casa.{C.RESET}")
    print(f"{C.AMARELO}Preciso de uma forma de contatá-la sem alertar os outros.{C.RESET}")

    return True


def simular_infiltrar_comunicacao(game_state):
    """Simula infiltração nas comunicações"""
    print(f"\n{C.AMARELO}[INFILTRAÇÃO NAS COMUNICAÇÕES]{C.RESET}")
    print("Infiltrando canal de comunicação de Juliana...")

    mensagens = [
        "Juliana: Eles sabem que estou sendo investigada?",
        "Marcus: Ainda não. Mas o hacker está perto. Muito perto.",
        "Juliana: Ele era só um namorado. Não deveria ter descoberto nada.",
        "Marcus: Você subestimou ele. Como subestimou a nós.",
        "Juliana: Eu precisava do dinheiro. Minha família...",
        "Marcus: Família? Você nos vendeu por dinheiro?"
    ]

    print(f"{C.ROXO}MENSAGENS INTERCEPTADAS:{C.RESET}")
    for msg in mensagens:
        time.sleep(0.8)
        print(f"  {C.CINZA}{msg}{C.RESET}")

    print(f"\n{C.VERDE}✓ Comunicações infiltradas!{C.RESET}")
    print(f"{C.AMARELO}Juliana precisava de dinheiro... Mas por quê?{C.RESET}")

    game_state.revelacoes_descobertas += 1
    return True


def simular_confrontacao_juliana(game_state):
    """Simula confrontação direta com Juliana"""
    print(f"\n{C.ROXO}[CONFRONTAÇÃO COM JULIANA]{C.RESET}")
    print("Iniciando chamada de vídeo criptografada...")

    time.sleep(2)
    print(f"{C.CINZA}*** CONEXÃO ESTABELECIDA ***{C.RESET}")
    print(f"{C.CINZA}Juliana aparece na tela, visivelmente nervosa.{C.RESET}")

    dialogo = [
        ("Você", "Juliana... Como pôde me trair assim?"),
        ("Juliana", "Você não entende... Eu não tinha escolha."),
        ("Você", "Escolha? Você vendeu dados confidenciais!"),
        ("Juliana", "Minha irmã... Ela está doente. Câncer terminal."),
        ("Juliana", "O tratamento custa uma fortuna. Eles me ofereceram dinheiro."),
        ("Você", "E eu? Eu te amava! Como pôde me usar?"),
        ("Juliana", "Você era conveniente. Fácil de manipular."),
        ("Juliana", "Mas eu nunca imaginei que você descobriria tudo...")
    ]

    for falante, fala in dialogo:
        time.sleep(1.5)
        cor = C.VERDE if falante == "Você" else C.ROXO
        print(f"{cor}{falante}: {fala}{C.RESET}")

    print(f"\n{C.VERDE}✓ Confrontação realizada!{C.RESET}")
    print(f"{C.AMARELO}Motivos pessoais revelados, mas a conspiração continua.{C.RESET}")

    game_state.revelacoes_descobertas += 2
    game_state.nivel_tensao += 30
    return True


def simular_descobrir_motivos(game_state):
    """Simula descoberta dos verdadeiros motivos"""
    print(f"\n{C.AMARELO}[DESCOBRINDO OS VERDADEIROS MOTIVOS]{C.RESET}")
    print("Analisando dados financeiros de Juliana...")

    descobertas = {
        "Dívidas Médicas": "R$ 500.000 em tratamentos para irmã",
        "Ameaças": "Marcus ameaçou expor segredos da família",
        "Pagamentos": "Recebeu 50 BTC da TechCorp",
        "Conexões": "Irmã trabalha para empresa concorrente",
        "Chantagem": "Marcus usou doença da irmã como alavanca"
    }

    print(f"{C.ROXO}VERDADES DESCOBERTAS:{C.RESET}")
    for chave, valor in descobertas.items():
        print(f"  {chave}: {valor}")

    time.sleep(2)
    print(f"\n{C.VERMELHO}A traição de Juliana foi motivada por desespero.{C.RESET}")
    print("Mas ela escolheu o caminho errado.")
    print("Agora preciso decidir: Justiça ou misericórdia?")

    game_state.revelacoes_descobertas += 3
    return True


def simular_escolha_final(game_state):
    """Simula escolha moral final"""
    print(f"\n{C.ROXO}[ESCOLHA MORAL FINAL]{C.RESET}")
    print("Com todas as evidências em mãos, você tem uma decisão crucial:")
    print()
    print(f"{C.CIANO}OPÇÃO 1 - JUSTIÇA:{C.RESET} Expor Juliana e toda a conspiração")
    print("  • Ela será presa, conspiração desmantelada")
    print("  • Mas a irmã dela morrerá sem tratamento")
    print("  • Você se torna herói, mas destrói uma família")
    print()
    print(f"{C.AMARELO}OPÇÃO 2 - MISERICÓRDIA:{C.RESET} Confrontar Marcus, poupar Juliana")
    print("  • Juliana se arrepende, ajuda a derrubar a conspiração")
    print("  • Irmã recebe tratamento, família salva")
    print("  • Mas Juliana fica impune por seus crimes")
    print()
    print(f"{C.VERMELHO}OPÇÃO 3 - VINGANÇA:{C.RESET} Destruir tudo e todos")
    print("  • Expor tudo, causar caos máximo")
    print("  • Ninguém sai ileso da sua ira")
    print("  • Você se torna o vilão da história")

    while True:
        print(f"\n{C.BRANCO}Digite sua escolha (justica/misericordia/vinganca):{C.RESET}")
        escolha = input().strip().lower()

        if escolha in ['justica', 'misericordia', 'vinganca']:
            game_state.escolha_moral = escolha

            if escolha == 'justica':
                print(f"\n{C.VERDE}Você escolheu JUSTIÇA.{C.RESET}")
                print("Juliana será presa, mas a conspiração cai.")
            elif escolha == 'misericordia':
                print(f"\n{C.AMARELO}Você escolheu MISERICÓRDIA.{C.RESET}")
                print("Juliana se redime, conspiradores caem.")
            else:  # vinganca
                print(f"\n{C.VERMELHO}Você escolheu VINGANÇA.{C.RESET}")
                print("Caos total. Ninguém escapa.")

            return True
        else:
            erro("Escolha inválida! Digite: justica, misericordia ou vinganca")


# ========== FUNÇÃO PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save):
    """Função principal do capítulo 8"""
    game_state = GameState(dados_jogador)

    # Carregar checkpoint se existir
    if os.path.exists(arquivo_save):
        try:
            with open(arquivo_save, 'r') as f:
                dados_salvos = json.load(f)
            checkpoint = dados_salvos.get('chapter_08_checkpoint', 'inicio')
            if checkpoint != 'inicio':
                game_state.checkpoint = checkpoint
                game_state.missoes = dados_salvos.get('missoes_capitulo_8', game_state.missoes)
                game_state.revelacoes_descobertas = dados_salvos.get('revelacoes_descobertas', 0)
                game_state.nivel_tensao = dados_salvos.get('nivel_tensao', 0)
                game_state.escolha_moral = dados_salvos.get('escolha_moral')
                print(f"{C.AMARELO}Continuando do checkpoint: {checkpoint}{C.RESET}")
        except:
            pass

    exibir_header()

    # Narrativa inicial
    digitar("Tenho todas as evidências. Chegou a hora da verdade.", cor=C.BRANCO)
    digitar("Juliana... Minha ex-namorada. Minha traidora.", cor=C.CINZA)
    digitar("Preciso confrontá-la. Descobrir os motivos reais.", cor=C.CINZA)
    digitar("Mas será que estou preparado para a verdade?", cor=C.CINZA)
    digitar("E o que farei quando descobrir? Justiça ou misericórdia?", cor=C.VERMELHO)
    print()

    # Loop principal do jogo
    while not game_state.capitulo_concluido:
        try:
            # Verificar progresso
            completas, total = game_state.verificar_progresso()
            print(f"\n{C.AMARELO}Progresso: {completas}/{total} missões completas{C.RESET}")
            print(f"{C.AMARELO}Pontuação: {game_state.score} | Tensão: {game_state.nivel_tensao}{C.RESET}")
            print(f"{C.AMARELO}Revelações: {game_state.revelacoes_descobertas}{C.RESET}")

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
                tutorial_interrogatorio()
                continue

            # Missões
            elif 'localizar' in comando or 'juliana' in comando:
                if not game_state.missoes['localizar_juliana']:
                    if simular_localizar_juliana(game_state):
                        game_state.completar_missao('localizar_juliana')
                else:
                    aviso("Juliana já localizada!")

            elif 'infiltrar' in comando or 'comunicacao' in comando:
                if game_state.missoes['localizar_juliana']:
                    if not game_state.missoes['infiltrar_comunicacao']:
                        if simular_infiltrar_comunicacao(game_state):
                            game_state.completar_missao('infiltrar_comunicacao')
                    else:
                        aviso("Comunicações já infiltradas!")
                else:
                    erro("Localize Juliana primeiro!")

            elif 'confrontar' in comando or 'confronto' in comando:
                if game_state.missoes['infiltrar_comunicacao']:
                    if not game_state.missoes['confrontar_juliana']:
                        if simular_confrontacao_juliana(game_state):
                            game_state.completar_missao('confrontar_juliana')
                    else:
                        aviso("Confrontação já realizada!")
                else:
                    erro("Infiltre as comunicações primeiro!")

            elif 'motivos' in comando or 'descobrir' in comando:
                if game_state.missoes['confrontar_juliana']:
                    if not game_state.missoes['descobrir_motivos']:
                        if simular_descobrir_motivos(game_state):
                            game_state.completar_missao('descobrir_motivos')
                    else:
                        aviso("Motivos já descobertos!")
                else:
                    erro("Confronte Juliana primeiro!")

            elif 'escolha' in comando or 'escolher' in comando:
                if game_state.missoes['descobrir_motivos'] and game_state.revelacoes_descobertas >= 3:
                    if not game_state.missoes['fazer_escolha']:
                        if simular_escolha_final(game_state):
                            game_state.completar_missao('fazer_escolha')
                            game_state.capitulo_concluido = True
                            game_state.operacao_sucesso = True
                    else:
                        aviso("Escolha já feita!")
                else:
                    erro("Descubra todos os motivos primeiro!")

            else:
                erro("Comando não reconhecido. Tente: localizar, infiltrar, confrontar, motivos, escolha")

            # Verificar conclusão
            if game_state.capitulo_concluido:
                print(f"\n{C.VERDE}🎯 CAPÍTULO 8 CONCLUÍDO! 🎯{C.RESET}")
                print(f"Sua escolha moral determinará o rumo da conspiração...")
                if game_state.escolha_moral == 'justica':
                    print("Caminho da justiça escolhido. A luta continua.")
                elif game_state.escolha_moral == 'misericordia':
                    print("Caminho da redenção escolhido. Aliados inesperados surgem.")
                else:
                    print("Caminho da vingança escolhido. O caos se aproxima.")
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
        print("Capítulo 8 - Interrogatório Digital:")
        print("• Rastreamento de Alvos: Localização de indivíduos")
        print("• Infiltração de Comunicações: Interceptação de mensagens")
        print("• Análise Comportamental: Interpretação de motivações")
        print("• Engenharia Social Reversa: Extração de informação")
        print(f"{C.VERMELHO}⚠️  Você perdeu tempo consultando o manual! ⚠️{C.RESET}")


if __name__ == "__main__":
    # Para testes diretos
    dados_teste = {
        'player_name': 'Teste',
        'codiname': 'TESTE',
        'current_chapter': 8,
        'score': 400,
        'privacy_level': 60,
        'bitcoin_wallet': 0.08,
        'reputation': 100
    }

    resultado = iniciar(dados_teste, '/tmp/teste_chapter8.json')
    print("Resultado:", resultado)
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0) or 0
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        self.darknet_access = True
        self.aliados = dados_anteriores.get('aliados', 0)
        self.segredos_descobertos = dados_anteriores.get('segredos_descobertos', [])

        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False

        # Estado específico do capítulo
        self.firewalls_quebrados = 0
        self.sistemas_comprometidos = 0
        self.contador_ataque = 300  # 5 minutos em segundos

    def registrar_falha(self, penalidade=30):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        if self.privacy_level <= 0:
            self.game_over = True

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 25

    def quebrar_firewall(self):
        self.firewalls_quebrados += 1

    def comprometer_sistema(self):
        self.sistemas_comprometidos += 1

    def tick_contador(self):
        self.contador_ataque = max(0, self.contador_ataque - 10)

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 8,  # Sempre capítulo 8
            'completed_chapters': [1, 2, 3, 4, 5, 6, 7],  # Capítulos 1-7 devem estar completados
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
            'completed': getattr(self, 'capitulo_concluido', False),
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }


# ========== UI AUXILIAR ==========

def header_kali_v2(titulo="CAPÍTULO 8: O ÚLTIMO FIREWALL"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass

    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Cyber Warfare - Ataque Final | Status: EM GUERRA':^{largura}}{C.RESET}")
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
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/warfare{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

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

def mostrar_status_guerra(state):
    """Mostra status da guerra cibernética"""
    minutos = state.contador_ataque // 60
    segundos = state.contador_ataque % 60

    print(f"\n{C.VERMELHO}╔════ STATUS DA GUERRA ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Tempo: {minutos:02d}:{segundos:02d}              ║{C.RESET}")
    print(f"{C.VERMELHO}║ Firewalls: {state.firewalls_quebrados}/5         ║{C.RESET}")
    print(f"{C.VERMELHO}║ Sistemas: {state.sistemas_comprometidos}/3       ║{C.RESET}")
    print(f"{C.VERMELHO}║ Aliados: {state.aliados}                 ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*31}╝{C.RESET}\n")


# ========== QUESTS/DESAFIOS ==========

def quest_1_coordination_center(state):
    """Quest 1: Centro de coordenação - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 1: CENTRO DE COORDENAÇÃO ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Estabelecer comando central  ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*44}╝{C.RESET}\n")

    pensamento("Precisamos coordenar o ataque. Cada segundo conta.")

    # Parte 1: Configurar C2
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "covenant" in cmd or "c2" in cmd:
            print(f"{C.CINZA}[*] Inicializando servidor C2...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Covenant C2 ativo{C.RESET}")
            print(f"{C.VERDE}[+] Listeners configurados{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'covenant --listener http' para iniciar C2.{C.RESET}")
            state.registrar_falha(12)

    # Parte 2: Conectar aliados
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "grunts" in cmd or "connect" in cmd:
            print(f"{C.CINZA}[*] Conectando agentes...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] {state.aliados} aliados conectados{C.RESET}")
            print(f"{C.VERDE}[+] Coordenação estabelecida{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'covenant grunts connect' para conectar aliados.{C.RESET}")
            state.registrar_falha(10)

    pensamento("O exército cibernético está pronto. Vamos começar o ataque.")

    state.registrar_sucesso(50, 0.03)
    return True

def quest_2_firewall_breach(state):
    """Quest 2: Quebrar firewall - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 2: QUEBRAR FIREWALL ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Penetrar defesas externas ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*40}╝{C.RESET}\n")

    pensamento("O firewall deles é uma fortaleza. Precisamos de força bruta coordenada.")

    mostrar_status_guerra(state)

    # Parte 1: Ataque distribuído
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "hping3" in cmd and "flood" in cmd:
            print(f"{C.CINZA}[*] Iniciando ataque DDoS coordenado...{C.RESET}")
            time.sleep(4)
            print(f"{C.AMARELO}[!] Firewall sob ataque intenso{C.RESET}")
            print(f"{C.VERDE}[+] Primeiro firewall comprometido{C.RESET}")
            state.quebrar_firewall()
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'hping3 --flood -S firewall.anonimos.com' para DDoS.{C.RESET}")
            state.registrar_falha(15)
            state.tick_contador()

    # Parte 2: Exploit zero-day
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "metasploit" in cmd and "exploit" in cmd:
            print(f"{C.CINZA}[*] Executando exploit zero-day...{C.RESET}")
            time.sleep(5)
            print(f"{C.VERDE}[+] Exploit bem-sucedido!{C.RESET}")
            print(f"{C.VERDE}[+] Segundo firewall quebrado{C.RESET}")
            state.quebrar_firewall()
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'msfconsole -x \"use exploit/windows/zero_day\"' para exploit.{C.RESET}")
            state.registrar_falha(18)
            state.tick_contador()

    pensamento("Dois firewalls caídos. Estamos dentro do perímetro.")

    mostrar_status_guerra(state)
    state.registrar_sucesso(80, 0.05)
    return True

def quest_3_system_infiltration(state):
    """Quest 3: Infiltração de sistemas - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 3: INFILTRAÇÃO ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Comprometer servidores ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*37}╝{C.RESET}\n")

    pensamento("Agora precisamos tomar o controle dos sistemas principais.")

    # Parte 1: Servidor de banco de dados
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "sqlmap" in cmd and "dump" in cmd:
            print(f"{C.CINZA}[*] Explorando vulnerabilidade SQL...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERDE}[+] Banco de dados comprometido{C.RESET}")
            print(f"{C.VERDE}[+] Dados dos Anônimos extraídos{C.RESET}")
            state.comprometer_sistema()
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'sqlmap -u target.com --dump-all' para SQL injection.{C.RESET}")
            state.registrar_falha(16)
            state.tick_contador()

    # Parte 2: Servidor de controle
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "psexec" in cmd or "wmiexec" in cmd:
            print(f"{C.CINZA}[*] Escalando privilégios no domínio...{C.RESET}")
            time.sleep(5)
            print(f"{C.VERDE}[+] Controle total do domínio{C.RESET}")
            print(f"{C.VERDE}[+] Servidor de controle comprometido{C.RESET}")
            state.comprometer_sistema()
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'psexec.py domain/admin@target.com' para controle.{C.RESET}")
            state.registrar_falha(20)
            state.tick_contador()

    pensamento("Dois sistemas principais caídos. O coração da organização está exposto.")

    mostrar_status_guerra(state)
    state.registrar_sucesso(100, 0.07)
    return True

def quest_4_defense_countermeasures(state):
    """Quest 4: Contramedidas de defesa - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 4: CONTRAMEDIDAS ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Defender contra contra-ataque ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*43}╝{C.RESET}\n")

    pensamento("Eles estão contra-atacando. Precisamos nos defender!")

    # Parte 1: Detectar contra-ataque
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "snort" in cmd or "suricata" in cmd:
            print(f"{C.CINZA}[*] Monitorando tráfego de rede...{C.RESET}")
            time.sleep(3)
            print(f"{C.AMARELO}[!] ALERTA: Contra-ataque detectado!{C.RESET}")
            print(f"{C.AMARELO}[!] Origem: Servidores dos Anônimos{C.RESET}")
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'suricata -c rules.conf -i eth0' para detectar ataques.{C.RESET}")
            state.registrar_falha(14)
            state.tick_contador()

    # Parte 2: Implementar defesa
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "iptables" in cmd and "drop" in cmd:
            print(f"{C.CINZA}[*] Configurando firewall defensivo...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Regras de firewall aplicadas{C.RESET}")
            print(f"{C.VERDE}[+] Contra-ataque bloqueado{C.RESET}")
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'iptables -A INPUT -s attacker_ip -j DROP' para bloquear.{C.RESET}")
            state.registrar_falha(17)
            state.tick_contador()

    pensamento("Defesa estabelecida. Mas o tempo está se esgotando.")

    mostrar_status_guerra(state)
    state.registrar_sucesso(70, 0.04)
    return True

def quest_5_data_exfiltration(state):
    """Quest 5: Exfiltração de dados - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 5: EXFILTRAÇÃO ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Roubar dados críticos    ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*37}╝{C.RESET}\n")

    pensamento("Precisamos levar as evidências. Tudo depende disso.")

    # Parte 1: Localizar dados
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "find" in cmd and "evidence" in cmd:
            print(f"{C.CINZA}[*] Procurando arquivos de evidências...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Arquivos localizados: 47 arquivos{C.RESET}")
            print(f"{C.VERDE}[+] Tamanho total: 2.3GB{C.RESET}")
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'find / -name \"*evidence*\" -type f' para localizar.{C.RESET}")
            state.registrar_falha(11)
            state.tick_contador()

    # Parte 2: Exfiltrar dados
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "scp" in cmd and "recursive" in cmd:
            print(f"{C.CINZA}[*] Iniciando exfiltração de dados...{C.RESET}")
            time.sleep(6)
            print(f"{C.VERDE}[+] Transferência completa{C.RESET}")
            print(f"{C.VERDE}[+] Todas evidências seguras{C.RESET}")
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'scp -r evidence/ safe_server:/data/' para exfiltrar.{C.RESET}")
            state.registrar_falha(13)
            state.tick_contador()

    pensamento("As evidências estão seguras. Agora podemos expor tudo.")

    mostrar_status_guerra(state)
    state.registrar_sucesso(90, 0.06)
    return True

def quest_6_final_assault(state):
    """Quest 6: Assalto final - Dificuldade: Máxima"""
    print(f"\n{C.VERMELHO}╔════ QUEST 6: ASSALTO FINAL ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Objetivo: Destruir o sistema     ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*37}╝{C.RESET}\n")

    pensamento("Este é o momento final. Vamos acabar com eles.")

    mostrar_status_guerra(state)

    # Parte 1: Implantar malware
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "wannacry" in cmd or "ransomware" in cmd:
            print(f"{C.CINZA}[*] Implantando ransomware...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERDE}[+] Ransomware implantado{C.RESET}")
            print(f"{C.VERDE}[+] Sistemas criptografados{C.RESET}")
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use './wannacry_deploy.sh target_network' para ransomware.{C.RESET}")
            state.registrar_falha(19)
            state.tick_contador()

    # Parte 2: Destruir backups
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "shred" in cmd or "wipe" in cmd:
            print(f"{C.CINZA}[*] Destruindo backups...{C.RESET}")
            time.sleep(5)
            print(f"{C.VERDE}[+] Todos backups destruídos{C.RESET}")
            print(f"{C.VERDE}[+] Recuperação impossível{C.RESET}")
            state.tick_contador()
            break
        else:
            print(f"{C.VERMELHO}Use 'shred -u -v -n 3 /backup/*' para destruir backups.{C.RESET}")
            state.registrar_falha(21)
            state.tick_contador()

    pensamento("Está feito. Os Anônimos estão acabados.")

    state.registrar_sucesso(150, 0.1)
    return True


# ========== CENA PRINCIPAL ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)

    digitar(f"{C.CINZA}A guerra cibernética começou.{C.RESET}", delay=0.1)
    drama_pause(1)
    digitar(f"{C.CINZA}Alianças formadas, alvos identificados.{C.RESET}", delay=0.08)
    drama_pause(1)
    digitar(f"{C.CINZA}Agora é tudo ou nada.{C.RESET}", delay=0.08)

    drama_pause(2)

    header_kali_v2()
    drama_pause(1)

    narracao("O centro de comando pulsa com atividade.")
    narracao("Monitores mostram ataques coordenados ao redor do mundo.")
    drama_pause(1)

    pensamento("Cada firewall quebrado é uma vitória. Cada sistema comprometido é justiça.")
    pensamento("Mas o tempo... o tempo é nosso maior inimigo.")

    mostrar_status_guerra(state)
    drama_pause(2)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter8(dados_jogador)

    try:
        cena_abertura(state)

        if state.saindo_para_menu:
            return state.to_dict()

        # Executar quests em sequência
        quests = [
            quest_1_coordination_center,
            quest_2_firewall_breach,
            quest_3_system_infiltration,
            quest_4_defense_countermeasures,
            quest_5_data_exfiltration,
            quest_6_final_assault
        ]

        for quest in quests:
            if not quest(state):
                if state.saindo_para_menu:
                    return state.to_dict()
                break

            # Verificar se o tempo acabou
            if state.contador_ataque <= 0:
                print(f"\n{C.VERMELHO}TEMPO ESGOTADO! ATAQUE FALHADO!{C.RESET}")
                state.game_over = True
                break

        # Final do capítulo
        drama_pause(2)
        header_kali_v2()

        if state.game_over:
            print(f"\n{C.VERMELHO}{'═'*60}{C.RESET}")
            print(f"{C.VERMELHO}{'DERROTA - TEMPO ESGOTADO':^60}{C.RESET}")
            print(f"{C.VERMELHO}{'═'*60}{C.RESET}")
        else:
            print(f"\n{C.VERDE}{'═'*60}{C.RESET}")
            print(f"{C.VERDE}{'CAPÍTULO 8: VITÓRIA - CONCLUÍDO':^60}{C.RESET}")
            print(f"{C.VERDE}{'═'*60}{C.RESET}")

            print(f"\n{C.AMARELO}Resultado da Guerra Cibernética:{C.RESET}")
            print(f"{C.AMARELO}- Firewalls quebrados: {state.firewalls_quebrados}/5{C.RESET}")
            print(f"{C.AMARELO}- Sistemas comprometidos: {state.sistemas_comprometidos}/3{C.RESET}")
            print(f"{C.AMARELO}- Tempo restante: {state.contador_ataque//60}:{state.contador_ataque%60:02d}{C.RESET}")

        state.capitulo_concluido = True
        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

