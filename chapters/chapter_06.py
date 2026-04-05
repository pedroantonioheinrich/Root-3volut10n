#!/usr/bin/env python3
"""
CHAPTER_06.PY - "Redes Ocultas"
A conspiração se revela maior do que imaginava. Preciso encontrar aliados.
Fóruns underground, comunidades de hackers, e primeiros sinais de resistência.

Foco: Infiltração em comunidades, networking underground
Habilidades: Engenharia social, navegação avançada na dark web, verificação de identidade
Objetivos: 6 missões principais + estabelecimento de contatos
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
        self.current_chapter = dados_jogador.get('current_chapter', 6)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 70)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.02)
        self.reputation = dados_jogador.get('reputation', 10)

        # Estado do capítulo
        self.capitulo_concluido = False
        self.operacao_sucesso = False
        self.checkpoint = 'inicio'

        # Missões do capítulo 6
        self.missoes = {
            'acessar_forum': False,          # Acessar fórum underground
            'criar_perfil': False,           # Criar perfil anônimo
            'postar_topico': False,          # Postar sobre conspiração
            'verificar_contatos': False,     # Verificar potenciais aliados
            'trocar_mensagens': False,       # Trocar mensagens criptografadas
            'estabelecer_contato': False     # Estabelecer primeiro contato real
        }

        # Contadores e flags
        self.tentativas_forum = 0
        self.contatos_encontrados = 0
        self.nivel_confianca = 0

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.reputation += 5
        self.privacy_level = max(0, self.privacy_level - 4)

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.reputation = max(0, self.reputation - 3)
        self.privacy_level = max(0, self.privacy_level - 10)

    def completar_missao(self, missao_nome):
        """Marca missão como completa"""
        if missao_nome in self.missoes:
            self.missoes[missao_nome] = True
            self.registrar_sucesso(25)
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
            'chapter_06_checkpoint': self.checkpoint,
            'capitulo_6_resultado': None,
            'capitulo_6_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_6': self.missoes.copy(),
            'contatos_encontrados': self.contatos_encontrados,
            'nivel_confianca': self.nivel_confianca
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
    print("                [ROOT EVOLUTION - CAPÍTULO 6: REDES OCULTAS]")
    print("                 Dark Web, 03:47 AM | Terminal: Kali Linux 2024")
    print("═" * 80)
    print(f"{C.RESET}")
    print(f"{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.")
    print(f"📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.")
    print("═" * 80)
    print(f"{C.RESET}")


# ========== FUNÇÕES DE TUTORIAL ==========

def tutorial_engenharia_social():
    """Tutorial sobre engenharia social"""
    print(f"\n{C.CIANO}[TUTORIAL - ENGENHARIA SOCIAL]{C.RESET}")
    print("Engenharia social é a arte de manipular pessoas para obter informações.")
    print("Técnicas básicas:")
    print("  • Pretexting: Criar uma história falsa para obter acesso")
    print("  • Phishing: Enganar através de emails/fóruns falsos")
    print("  • Baiting: Deixar 'isca' para que a vítima morda")
    print("  • Quid pro quo: Oferecer algo em troca de informação")
    print("\nDicas para fóruns underground:")
    print("  • Construa reputação gradualmente")
    print("  • Use linguagem apropriada da comunidade")
    print("  • Verifique identidades com PGP")
    print(f"{C.AMARELO}Lembre-se: confiança é conquistada, não comprada!{C.RESET}\n")


# ========== FUNÇÕES DE MISSÃO ==========

def simular_acesso_forum(game_state):
    """Simula acesso a fórum underground"""
    print(f"\n{C.AMARELO}[ACESSO A FÓRUM UNDERGROUND]{C.RESET}")
    print("Conectando ao fórum 'ShadowNet' via Tor...")

    time.sleep(2)
    print(f"{C.CIANO}FÓRUM SHADOWNET - SEÇÃO: CONSPIRAÇÕES GOVERNAMENTAIS{C.RESET}")
    print("Tópicos recentes:")
    print("  • [URGENTE] Vazamento no Ministério da Justiça")
    print("  • Informante anônimo: Operação 'Raiz Digital'")
    print("  • Busca: Aliados contra vigilância corporativa")
    print("  • [VERIFICADO] Contatos no governo - preços em BTC")

    print(f"\n{C.VERDE}✓ Acesso concedido ao fórum!{C.RESET}")
    print(f"{C.AMARELO}Cuidado: Qualquer post errado pode comprometer sua identidade.{C.RESET}")

    return True


def simular_criacao_perfil(game_state):
    """Simula criação de perfil anônimo"""
    print(f"\n{C.AMARELO}[CRIAÇÃO DE PERFIL ANÔNIMO]{C.RESET}")
    print("Criando perfil no ShadowNet...")

    # Simulação de criação
    time.sleep(1)
    print("Nome de usuário: ShadowHunter_42")
    print("Chave PGP gerada: ABCD-1234-EFGH-5678")
    print("Assinatura digital criada")

    time.sleep(1)
    print(f"{C.VERDE}✓ Perfil criado com sucesso!{C.RESET}")
    print(f"{C.AMARELO}Reputação inicial: {game_state.reputation} pontos{C.RESET}")
    print(f"{C.CINZA}Lembre-se: Uma reputação leva tempo para ser construída.{C.RESET}")

    return True


def simular_post_conspiracao(game_state):
    """Simula post sobre conspiração"""
    print(f"\n{C.AMARELO}[POST SOBRE CONSPIRAÇÃO]{C.RESET}")
    print("Postando tópico no fórum...")

    topico = "INVESTIGAÇÃO: Conexões entre Juliana Silva e Ministério da Justiça"
    conteudo = """
    Fontes confiáveis indicam que Juliana Silva, analista de sistemas,
    estava envolvida em operações de vazamento de dados classificados.
    Possível conexão com IP governamental 203.0.113.1.

    Busco informações sobre:
    - Outros envolvidos na operação
    - Motivos por trás do vazamento
    - Contatos para colaboração

    PGP: ABCD-1234-EFGH-5678
    """

    print(f"Tópico: {C.ROXO}{topico}{C.RESET}")
    print(f"Conteúdo: {C.CINZA}{conteudo}{C.RESET}")

    time.sleep(2)
    print(f"{C.VERDE}✓ Tópico postado! Aguardando respostas...{C.RESET}")
    print(f"{C.AMARELO}Isso pode atrair atenção indesejada.{C.RESET}")

    game_state.contatos_encontrados += 2
    return True


def simular_verificacao_contatos(game_state):
    """Simula verificação de contatos potenciais"""
    print(f"\n{C.AMARELO}[VERIFICAÇÃO DE CONTATOS]{C.RESET}")
    print("Analisando respostas ao seu tópico...")

    contatos = [
        {"nome": "GhostWriter", "reputacao": 850, "especialidade": "Inteligência governamental"},
        {"nome": "CryptoQueen", "reputacao": 720, "especialidade": "Análise de dados"},
        {"nome": "PhantomOps", "reputacao": 680, "especialidade": "Operações especiais"}
    ]

    for contato in contatos:
        print(f"\n{C.CIANO}Contato: {contato['nome']}{C.RESET}")
        print(f"  Reputação: {contato['reputacao']}")
        print(f"  Especialidade: {contato['especialidade']}")
        print(f"  Status PGP: Verificado ✓")

    print(f"\n{C.VERDE}✓ Contatos verificados!{C.RESET}")
    print(f"{C.AMARELO}Escolha com cuidado quem contatar.{C.RESET}")

    game_state.contatos_encontrados += 3
    return True


def simular_troca_mensagens(game_state):
    """Simula troca de mensagens criptografadas"""
    print(f"\n{C.AMARELO}[TROCA DE MENSAGENS CRIPTOGRAFADAS]{C.RESET}")
    print("Iniciando conversa com GhostWriter...")

    # Simulação de conversa
    mensagens = [
        ("Você", "Tenho informações sobre Juliana Silva. Podemos conversar?"),
        ("GhostWriter", "Interessante. Que tipo de informação?"),
        ("Você", "Vazamento de dados do governo. Ministério da Justiça envolvido."),
        ("GhostWriter", "Conheço essa operação. É maior do que imagina."),
        ("Você", "Preciso de detalhes. Posso pagar em BTC."),
        ("GhostWriter", "Encontre-me no canal #shadow_ops amanhã. Traga prova de identidade.")
    ]

    for remetente, msg in mensagens:
        time.sleep(1)
        cor = C.VERDE if remetente == "Você" else C.ROXO
        print(f"{cor}{remetente}: {msg}{C.RESET}")

    print(f"\n{C.VERDE}✓ Conversa estabelecida!{C.RESET}")
    print(f"{C.AMARELO}Próximo passo: encontrar GhostWriter pessoalmente.{C.RESET}")

    game_state.nivel_confianca += 20
    return True


def simular_contato_real(game_state):
    """Simula estabelecimento de contato real"""
    print(f"\n{C.ROXO}[CONTATO REAL ESTABELECIDO]{C.RESET}")
    print("Conectando ao canal #shadow_ops...")

    time.sleep(3)
    print(f"{C.CIANO}*** GhostWriter entrou no canal ***{C.RESET}")
    print(f"{C.CINZA}GhostWriter: Você tem 5 minutos. Mostre suas cartas.{C.RESET}")
    print(f"{C.CINZA}Você: [envia evidências criptografadas]{C.RESET}")
    print(f"{C.CINZA}GhostWriter: Interessante... Você pode ser útil.{C.RESET}")
    print(f"{C.CINZA}GhostWriter: Juliana não era apenas uma informante.{C.RESET}")
    print(f"{C.CINZA}GhostWriter: Ela era parte de uma rede maior.{C.RESET}")
    print(f"{C.CINZA}GhostWriter: Rede 'Raiz Digital' - espionagem corporativa.{C.RESET}")

    print(f"\n{C.VERDE}✓ Primeiro aliado conquistado!{C.RESET}")
    print(f"{C.AMARELO}A conspiração é ainda maior do que imaginava...{C.RESET}")

    game_state.nivel_confianca += 30
    return True


# ========== FUNÇÃO PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save):
    """Função principal do capítulo 6"""
    game_state = GameState(dados_jogador)

    # Carregar checkpoint se existir
    if os.path.exists(arquivo_save):
        try:
            with open(arquivo_save, 'r') as f:
                dados_salvos = json.load(f)
            checkpoint = dados_salvos.get('chapter_06_checkpoint', 'inicio')
            if checkpoint != 'inicio':
                game_state.checkpoint = checkpoint
                game_state.missoes = dados_salvos.get('missoes_capitulo_6', game_state.missoes)
                game_state.contatos_encontrados = dados_salvos.get('contatos_encontrados', 0)
                game_state.nivel_confianca = dados_salvos.get('nivel_confianca', 0)
                print(f"{C.AMARELO}Continuando do checkpoint: {checkpoint}{C.RESET}")
        except:
            pass

    exibir_header()

    # Narrativa inicial
    digitar("A conspiração se revela maior do que eu imaginava.", cor=C.BRANCO)
    digitar("Juliana não agia sozinha. Há uma rede inteira por trás disso.", cor=C.CINZA)
    digitar("Preciso encontrar aliados. Pessoas que sabem mais do que eu.", cor=C.CINZA)
    digitar("Os fóruns underground podem ter as respostas que procuro.", cor=C.CINZA)
    digitar("Mas preciso ser cuidadoso... uma palavra errada e estou morto.", cor=C.VERMELHO)
    print()

    # Loop principal do jogo
    while not game_state.capitulo_concluido:
        try:
            # Verificar progresso
            completas, total = game_state.verificar_progresso()
            print(f"\n{C.AMARELO}Progresso: {completas}/{total} missões completas{C.RESET}")
            print(f"{C.AMARELO}Pontuação: {game_state.score} | Reputação: {game_state.reputation}{C.RESET}")
            print(f"{C.AMARELO}Contatos: {game_state.contatos_encontrados} | Confiança: {game_state.nivel_confianca}{C.RESET}")

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
                tutorial_engenharia_social()
                continue

            # Missões
            elif 'forum' in comando or 'acessar' in comando:
                if not game_state.missoes['acessar_forum']:
                    if simular_acesso_forum(game_state):
                        game_state.completar_missao('acessar_forum')
                else:
                    aviso("Fórum já acessado!")

            elif 'perfil' in comando or 'criar' in comando:
                if game_state.missoes['acessar_forum']:
                    if not game_state.missoes['criar_perfil']:
                        if simular_criacao_perfil(game_state):
                            game_state.completar_missao('criar_perfil')
                    else:
                        aviso("Perfil já criado!")
                else:
                    erro("Acesse o fórum primeiro!")

            elif 'postar' in comando or 'topico' in comando:
                if game_state.missoes['criar_perfil']:
                    if not game_state.missoes['postar_topico']:
                        if simular_post_conspiracao(game_state):
                            game_state.completar_missao('postar_topico')
                    else:
                        aviso("Tópico já postado!")
                else:
                    erro("Crie um perfil primeiro!")

            elif 'verificar' in comando or 'contatos' in comando:
                if game_state.missoes['postar_topico']:
                    if not game_state.missoes['verificar_contatos']:
                        if simular_verificacao_contatos(game_state):
                            game_state.completar_missao('verificar_contatos')
                    else:
                        aviso("Contatos já verificados!")
                else:
                    erro("Poste um tópico primeiro!")

            elif 'mensagens' in comando or 'trocar' in comando:
                if game_state.missoes['verificar_contatos']:
                    if not game_state.missoes['trocar_mensagens']:
                        if simular_troca_mensagens(game_state):
                            game_state.completar_missao('trocar_mensagens')
                    else:
                        aviso("Mensagens já trocadas!")
                else:
                    erro("Verifique contatos primeiro!")

            elif 'contato' in comando or 'estabelecer' in comando:
                if game_state.missoes['trocar_mensagens'] and game_state.nivel_confianca >= 30:
                    if not game_state.missoes['estabelecer_contato']:
                        if simular_contato_real(game_state):
                            game_state.completar_missao('estabelecer_contato')
                            game_state.capitulo_concluido = True
                            game_state.operacao_sucesso = True
                    else:
                        aviso("Contato já estabelecido!")
                else:
                    erro("Complete as missões anteriores e construa confiança!")

            else:
                erro("Comando não reconhecido. Tente: forum, perfil, postar, verificar, mensagens, contato")

            # Verificar conclusão
            if game_state.capitulo_concluido:
                print(f"\n{C.VERDE}🎯 CAPÍTULO 6 CONCLUÍDO! 🎯{C.RESET}")
                print("Primeiro aliado conquistado. A rede 'Raiz Digital' começa a se revelar...")
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
        print("Capítulo 6 - Engenharia Social:")
        print("• Acesso a Fóruns: Navegação segura na dark web")
        print("• Criação de Perfil: Construção de identidade anônima")
        print("• Verificação PGP: Autenticação de contatos")
        print("• Troca de Mensagens: Comunicação criptografada")
        print(f"{C.VERMELHO}⚠️  Você perdeu tempo consultando o manual! ⚠️{C.RESET}")


if __name__ == "__main__":
    # Para testes diretos
    dados_teste = {
        'player_name': 'Teste',
        'codiname': 'TESTE',
        'current_chapter': 6,
        'score': 200,
        'privacy_level': 70,
        'bitcoin_wallet': 0.02,
        'reputation': 10
    }

    resultado = iniciar(dados_teste, '/tmp/teste_chapter6.json')
    print("Resultado:", resultado)
        self.privacy_level = dados_anteriores.get('privacy_level', 100)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0) or 0
        self.bitcoin = dados_anteriores.get('bitcoin_wallet', 0.005)
        self.inventory = dados_anteriores.get('inventory', [])
        self.darknet_access = dados_anteriores.get('darknet_access', False)
        self.escolha_final_anterior = dados_anteriores.get('escolha_final', 'expor')

        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False

        # Estado específico do capítulo
        self.fugindo = True
        self.perseguidores = 3  # Número de agentes atrás de você

    def registrar_falha(self, penalidade=20):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        if self.privacy_level <= 0:
            self.game_over = True

    def registrar_sucesso(self, pontos, btc_reward=0.0):
        self.score += pontos
        self.bitcoin += btc_reward
        self.reputation += 15

    def reduzir_perseguidores(self):
        self.perseguidores = max(0, self.perseguidores - 1)

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 6,  # Sempre capítulo 6
            'completed_chapters': [1, 2, 3, 4, 5],  # Capítulos 1-5 devem estar completados
            'bitcoin_wallet': self.bitcoin,
            'privacy_level': self.privacy_level,
            'reputation': self.reputation,
            'score': self.score,
            'inventory': self.inventory,
            'darknet_access': self.darknet_access,
            'escolha_final': self.escolha_final_anterior,
            'perseguidores': self.perseguidores,
            'completed': getattr(self, 'capitulo_concluido', False),
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu
        }


# ========== UI AUXILIAR ==========

def header_kali_v2(titulo="CAPÍTULO 6: O FANTASMA DIGITAL"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass

    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Dark Web - Em Fuga | Status: PERSEGUIDO':^{largura}}{C.RESET}")
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
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/ghost{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

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

def mostrar_status_perseguicao(state):
    """Mostra status da perseguição"""
    print(f"\n{C.VERMELHO}╔════ STATUS DE PERSEGUIÇÃO ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Privacy Level: {state.privacy_level:>3}%{' '*13}║{C.RESET}")
    print(f"{C.VERMELHO}║ Perseguidores: {state.perseguidores:>3}{' '*13}║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*35}╝{C.RESET}\n")


# ========== QUESTS/DESAFIOS ==========

def quest_1_darknet_navigation(state):
    """Quest 1: Navegação na Dark Web - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 1: NAVEGAÇÃO DARK WEB ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Acessar mercados ocultos     ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*42}╝{C.RESET}\n")

    pensamento("A dark web é meu único refúgio agora. Mas ela tem seus próprios perigos.")

    # Parte 1: Configurar Tor
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "tor" in cmd and "start" in cmd:
            print(f"{C.CINZA}[*] Iniciando serviço Tor...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Tor conectado. IP: 192.168.1.108 -> Tor Network{C.RESET}")
            print(f"{C.VERDE}[+] Anonimato: 95%{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'systemctl start tor' para iniciar o Tor.{C.RESET}")
            state.registrar_falha(8)

    # Parte 2: Acessar onion site
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "torsocks" in cmd and "onion" in cmd:
            print(f"{C.CINZA}[*] Conectando ao mercado .onion...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Bem-vindo ao Black Market Hub{C.RESET}")
            print(f"{C.VERDE}[+] Serviços disponíveis: VPNs, identidades falsas, armas digitais{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'torsocks wget http://blackmarket.onion' para acessar.{C.RESET}")
            state.registrar_falha(10)

    pensamento("Aqui posso conseguir ferramentas para sobreviver. Mas cada transação deixa rastros...")

    state.registrar_sucesso(40, 0.02)
    return True

def quest_2_identity_forgery(state):
    """Quest 2: Forjar nova identidade - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 2: FORJAR IDENTIDADE ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Criar persona falsa        ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*39}╝{C.RESET}\n")

    pensamento("Preciso me tornar alguém novo. Alguém que não existe.")

    # Parte 1: Gerar dados falsos
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "faker" in cmd or "fake-name" in cmd:
            print(f"{C.CINZA}[*] Gerando identidade falsa...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Nome: Marcus Silva{C.RESET}")
            print(f"{C.VERDE}[+] CPF: 123.456.789-00{C.RESET}")
            print(f"{C.VERDE}[+] Endereço: Rua das Sombras, 666 - São Paulo{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'python3 -c \"from faker import Faker; f = Faker('pt_BR'); print(f.name())\"' para gerar.{C.RESET}")
            state.registrar_falha(7)

    # Parte 2: Criar documentos digitais
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "openssl" in cmd and "cert" in cmd:
            print(f"{C.CINZA}[*] Criando certificados digitais...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Certificado SSL gerado{C.RESET}")
            print(f"{C.VERDE}[+] Documentos PDF criados{C.RESET}")
            print(f"{C.VERDE}[+] Nova identidade: Marcus Silva{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'openssl req -new -x509 -keyout key.pem -out cert.pem -days 365' para certificados.{C.RESET}")
            state.registrar_falha(9)

    pensamento("Agora sou Marcus Silva. Mas por quanto tempo antes que descubram?")

    state.registrar_sucesso(50, 0.03)
    return True

def quest_3_counter_intelligence(state):
    """Quest 3: Contra-inteligência - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 3: CONTRA-INTELIGÊNCIA ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Despistar perseguidores     ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*42}╝{C.RESET}\n")

    pensamento("Eles estão me rastreando. Preciso plantar pistas falsas.")

    # Parte 1: Criar honeypot
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "honeypot" in cmd or "cowrie" in cmd:
            print(f"{C.CINZA}[*] Configurando honeypot...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Honeypot ativo na porta 2222{C.RESET}")
            print(f"{C.VERDE}[+] Agentes mordendo a isca...{C.RESET}")
            state.reduzir_perseguidores()
            break
        else:
            print(f"{C.VERMELHO}Use 'docker run -p 2222:2222 cowrie/cowrie' para honeypot.{C.RESET}")
            state.registrar_falha(12)

    # Parte 2: Ataque de distração
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "ddos" in cmd or "hping3" in cmd:
            print(f"{C.CINZA}[*] Iniciando ataque de distração...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Ataque DDoS contra servidores do governo{C.RESET}")
            print(f"{C.VERDE}[+] Agentes desviados para investigar{C.RESET}")
            state.reduzir_perseguidores()
            break
        else:
            print(f"{C.VERMELHO}Use 'hping3 --flood -S governo.br' para DDoS.{C.RESET}")
            state.registrar_falha(15)

    pensamento("Dois agentes despistados. Mas ainda resta um...")

    mostrar_status_perseguicao(state)
    state.registrar_sucesso(60, 0.04)
    return True

def quest_4_encrypted_communication(state):
    """Quest 4: Comunicação criptografada - Dificuldade: Alta"""
    print(f"\n{C.AMARELO}╔════ QUEST 4: COMUNICAÇÃO CRIPTOGRAFADA ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Contatar aliados na dark web ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*45}╝{C.RESET}\n")

    pensamento("Preciso de aliados. Mas como confiar em alguém na dark web?")

    # Parte 1: Configurar PGP
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "gpg" in cmd and "gen-key" in cmd:
            print(f"{C.CINZA}[*] Gerando chave PGP...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Chave PGP criada: 4096-bit RSA{C.RESET}")
            print(f"{C.VERDE}[+] ID: ABC123DEF456{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'gpg --gen-key' para gerar chave PGP.{C.RESET}")
            state.registrar_falha(8)

    # Parte 2: Enviar mensagem criptografada
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "gpg" in cmd and "encrypt" in cmd:
            print(f"{C.CINZA}[*] Criptografando mensagem...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Mensagem enviada para contato anônimo{C.RESET}")
            print(f"{C.VERDE}[+] 'Procurando aliados contra os Anônimos'{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'gpg --encrypt --recipient contato mensagem.txt' para criptografar.{C.RESET}")
            state.registrar_falha(10)

    pensamento("A mensagem foi enviada. Agora espero que alguém responda...")

    state.registrar_sucesso(45, 0.025)
    return True

def quest_5_escape_route(state):
    """Quest 5: Rota de fuga - Dificuldade: Máxima"""
    print(f"\n{C.AMARELO}╔════ QUEST 5: ROTA DE FUGA ════╗{C.RESET}")
    print(f"{C.AMARELO}║ Objetivo: Planejar saída segura      ║{C.RESET}")
    print(f"{C.AMARELO}╚{'═'*38}╝{C.RESET}\n")

    pensamento("Preciso sair do Brasil. Mas como cruzar fronteiras digitais e físicas?")

    # Parte 1: Verificar rotas
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "traceroute" in cmd or "tracepath" in cmd:
            print(f"{C.CINZA}[*] Mapeando rotas de fuga...{C.RESET}")
            time.sleep(3)
            print(f"{C.VERDE}[+] Rota 1: Brasil -> Paraguai -> Argentina{C.RESET}")
            print(f"{C.VERDE}[+] Rota 2: Brasil -> Uruguai -> Chile{C.RESET}")
            print(f"{C.VERDE}[+] Rota 3: Voo direto para Europa{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'traceroute fronteira.gov.br' para mapear rotas.{C.RESET}")
            state.registrar_falha(11)

    # Parte 2: Preparar documentos
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "convert" in cmd and "pdf" in cmd:
            print(f"{C.CINZA}[*] Forjando documentos de viagem...{C.RESET}")
            time.sleep(2)
            print(f"{C.VERDE}[+] Passaporte falso gerado{C.RESET}")
            print(f"{C.VERDE}[+] Visto europeu criado{C.RESET}")
            print(f"{C.VERDE}[+] Identidade: Marcus Silva{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'convert documento.jpg passaporte.pdf' para converter.{C.RESET}")
            state.registrar_falha(9)

    pensamento("Os documentos estão prontos. Agora é só esperar o momento certo...")

    state.registrar_sucesso(70, 0.05)
    return True

def quest_6_final_confrontation(state):
    """Quest 6: Confrontação final - Dificuldade: Máxima"""
    print(f"\n{C.VERMELHO}╔════ QUEST 6: CONFRONTAÇÃO FINAL ════╗{C.RESET}")
    print(f"{C.VERMELHO}║ Objetivo: Enfrentar o último agente  ║{C.RESET}")
    print(f"{C.VERMELHO}╚{'═'*42}╝{C.RESET}\n")

    pensamento("Resta apenas um perseguidor. O mais perigoso: Agente Costa.")

    mostrar_status_perseguicao(state)

    # Parte 1: Localizar agente
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "shodan" in cmd or "censys" in cmd:
            print(f"{C.CINZA}[*] Procurando sinais do Agente Costa...{C.RESET}")
            time.sleep(3)
            print(f"{C.AMARELO}[!] Agente localizado: IP 200.123.45.67{C.RESET}")
            print(f"{C.AMARELO}[!] Localização: Centro de Brasília{C.RESET}")
            break
        else:
            print(f"{C.VERMELHO}Use 'shodan search \"Agente Costa\"' para localizar.{C.RESET}")
            state.registrar_falha(13)

    # Parte 2: Ataque preventivo
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except:
            state.saindo_para_menu = True
            return False

        status = check_comandos_globais(cmd, state)
        if status == "MENU": return False
        if status == "MANUAL": continue

        if "metasploit" in cmd or "msfconsole" in cmd:
            print(f"{C.CINZA}[*] Preparando exploit contra sistema do agente...{C.RESET}")
            time.sleep(4)
            print(f"{C.VERDE}[+] Exploit EternalBlue executado{C.RESET}")
            print(f"{C.VERDE}[+] Sistema do agente comprometido{C.RESET}")
            print(f"{C.VERDE}[+] Agente Costa neutralizado!{C.RESET}")
            state.reduzir_perseguidores()
            break
        else:
            print(f"{C.VERMELHO}Use 'msfconsole -q -x \"use exploit/windows/smb/ms17_010_eternalblue\"' para exploit.{C.RESET}")
            state.registrar_falha(16)

    pensamento("O último perseguidor foi neutralizado. Agora sou verdadeiramente livre... ou sou?")

    state.registrar_sucesso(100, 0.1)
    return True


# ========== CENA PRINCIPAL ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)

    if state.escolha_final_anterior == "expor":
        digitar(f"{C.CINZA}As manchetes explodem pelo mundo.{C.RESET}", delay=0.1)
        digitar(f"{C.CINZA}'HACKER EXPOE CONSPIRAÇÃO ELEITORAL NO BRASIL'{C.RESET}", delay=0.08)
        drama_pause(1)
        digitar(f"{C.CINZA}Mas você sabe que eles virão atrás de você.{C.RESET}", delay=0.08)

    elif state.escolha_final_anterior == "controlar":
        digitar(f"{C.CINZA}Você é o novo V0id_Walker.{C.RESET}", delay=0.1)
        digitar(f"{C.CINZA}Mas há dissidentes. Traidores.{C.RESET}", delay=0.08)
        drama_pause(1)
        digitar(f"{C.CINZA}Eles sabem que você tomou o trono.{C.RESET}", delay=0.08)

    else:
        digitar(f"{C.CINZA}Seu sistema híbrido está online.{C.RESET}", delay=0.1)
        digitar(f"{C.CINZA}Mas nem todos concordam com mudanças.{C.RESET}", delay=0.08)
        drama_pause(1)
        digitar(f"{C.CINZA}A caçada começou.{C.RESET}", delay=0.08)

    drama_pause(2)

    header_kali_v2()
    drama_pause(1)

    narracao("Você está na dark web agora.")
    narracao("Cada clique deixa um rastro. Cada conexão é um risco.")
    drama_pause(1)

    pensamento("Eles me caçam. Mas eu sou o fantasma na máquina.")
    pensamento("Vamos ver quem assombra quem...")

    mostrar_status_perseguicao(state)
    drama_pause(2)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    state = GameStateChapter6(dados_jogador)

    try:
        cena_abertura(state)

        if state.saindo_para_menu:
            return state.to_dict()

        # Executar quests em sequência
        quests = [
            quest_1_darknet_navigation,
            quest_2_identity_forgery,
            quest_3_counter_intelligence,
            quest_4_encrypted_communication,
            quest_5_escape_route,
            quest_6_final_confrontation
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
        print(f"{C.VERDE}{'CAPÍTULO 6: FUGA - CONCLUÍDO':^60}{C.RESET}")
        print(f"{C.VERDE}{'═'*60}{C.RESET}")

        if state.perseguidores == 0:
            print(f"\n{C.AMARELO}Resultado: Você escapou completamente!{C.RESET}")
        else:
            print(f"\n{C.AMARELO}Resultado: Sobrevivência parcial - {state.perseguidores} agentes ainda ativos{C.RESET}")

        state.capitulo_concluido = True
        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

