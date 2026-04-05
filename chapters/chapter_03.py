#!/usr/bin/env python3
"""
CHAPTER_03.PY - "Primeiros Contatos na Sombra"
Uma semana depois. Começo a sair do fundo do poço. Os fóruns underground
me deram esperança. Há outros como eu. Outros que sabem a verdade.

Foco: Recuperação emocional, primeiros contatos na dark web
Habilidades: Comunicação anônima, análise de risco, primeiros contatos
Objetivos: 5 missões principais + exploração livre
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
        print(fim, end='')


# ========== GERENCIADOR DE ESTADO DO JOGO ==========

class GameState:
    """Gerencia o estado durante o capítulo"""

    def __init__(self, dados_jogador):
        # Dados originais do jogador
        self.player_name = dados_jogador.get('player_name', 'Hacker')
        self.codiname = dados_jogador.get('codiname', 'ANON')
        self.current_chapter = dados_jogador.get('current_chapter', 3)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 75)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.005)

        # Estado do capítulo
        self.capitulo_concluido = dados_jogador.get('completed', False)
        self.operacao_sucesso = dados_jogador.get('capitulo_3_operacao_sucesso', False)
        self.checkpoint = dados_jogador.get('chapter_03_checkpoint', 'inicio')
        self.saindo_para_menu = dados_jogador.get('saindo_para_menu', False)

        # Missões do capítulo 3
        self.missoes = {
            'configurar_ricochet': False,       # Configurar Ricochet IM
            'analisar_perfil': False,           # Analisar perfil suspeito
            'enviar_mensagem': False,           # Enviar primeira mensagem
            'receber_resposta': False,          # Receber resposta do contato
            'verificar_seguranca': False       # Verificar segurança da comunicação
        }

        # Estado emocional (melhorando)
        self.nivel_depressao = dados_jogador.get('nivel_depressao', 85) - 20
        self.motivacao_hacker = dados_jogador.get('motivacao_hacker', 15) + 15

        # Contatos na dark web
        self.contatos_darkweb = dados_jogador.get('contatos_darkweb', [])
        self.mensagens_trocadas = dados_jogador.get('mensagens_trocadas', [])
        self.nivel_confianca = dados_jogador.get('nivel_confianca', 0)
        self.missoes = dados_jogador.get('missoes_capitulo_3', self.missoes)
        self.nivel_depressao = dados_jogador.get('nivel_depressao', self.nivel_depressao)
        self.motivacao_hacker = dados_jogador.get('motivacao_hacker', self.motivacao_hacker)

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.privacy_level = max(0, self.privacy_level - 1)
        self.motivacao_hacker = min(100, self.motivacao_hacker + 8)
        self.nivel_depressao = max(0, self.nivel_depressao - 5)
        self.nivel_confianca += 10

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.privacy_level = max(0, self.privacy_level - 10)
        self.nivel_depressao += 8
        self.nivel_confianca = max(0, self.nivel_confianca - 15)

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
            'chapter_03_checkpoint': self.checkpoint,
            'capitulo_3_resultado': None,
            'capitulo_3_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_3': self.missoes.copy(),
            'nivel_depressao': self.nivel_depressao,
            'motivacao_hacker': self.motivacao_hacker,
            'contatos_darkweb': self.contatos_darkweb,
            'mensagens_trocadas': self.mensagens_trocadas,
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
    print(f"\n{C.ROXO}{'═' * 80}{C.RESET}")
    print(f"{C.ROXO}║{'ROOT EVOLUTION - CAPÍTULO 3: PRIMEIROS CONTATOS NA SOMBRA':^78}║{C.RESET}")
    print(f"{C.CINZA}║{'Brasília, 1 mês depois | Terminal: Kali Linux 2024':^78}║{C.RESET}")
    print(f"{C.ROXO}{'═' * 80}{C.RESET}")
    print(f"\n{C.CINZA}💡 DICA: Digite 'menu' para retornar ao menu do jogo a qualquer momento.{C.RESET}")
    print(f"{C.CINZA}📖 Acesse 'manual' para consultar o Manual de Hacking durante o jogo.{C.RESET}")
    print(f"{C.ROXO}{'═' * 80}{C.RESET}")

def exibir_status(state):
    """Exibe status atual do jogador"""
    completas, total = state.verificar_progresso()
    progresso = completas / total * 100

    print(f"\n{C.ROXO}┌─ STATUS DO HACKER ──────────────────────────────┐{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Score: {C.VERDE}{state.score:3d}{C.RESET} │ Privacidade: {C.CIANO}{state.privacy_level:2d}%{C.RESET} │ Missões: {C.VERDE}{completas}/{total}{C.RESET} ({C.VERDE}{progresso:3.0f}%{C.RESET}) {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Depressão: {C.VERMELHO}{state.nivel_depressao:2d}%{C.RESET} │ Motivação: {C.AMARELO}{state.motivacao_hacker:2d}%{C.RESET} │ Confiança: {C.ROXO}{state.nivel_confianca:2d}%{C.RESET} {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

def salvar_checkpoint(state, arquivo_save, checkpoint_nome):
    """Salva checkpoint do jogo"""
    state.checkpoint = checkpoint_nome
    dados = state.to_dict()

    try:
        with open(arquivo_save, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        print(f"\n{C.CINZA}[✓] Checkpoint salvo: {checkpoint_nome}{C.RESET}")
    except Exception as e:
        erro(f"Erro ao salvar checkpoint: {e}")

def carregar_manual():
    """Carrega o manual de hacking"""
    try:
        from manual_hacking import ManualHacking
        manual = ManualHacking()
        manual.mostrar_menu()
        return True
    except ImportError:
        erro("Manual de hacking não encontrado")
        return False

# ========== FUNÇÕES DE JOGABILIDADE ==========

def prompt_simples(cmd_esperado, descricao, state):
    """Prompt simples sem limite de tempo"""
    print(f"\n{C.CINZA}🎯 OBJETIVO: {descricao}{C.RESET}")
    print(f"{C.VERDE}💻 COMANDO: {cmd_esperado}{C.RESET}")

    while True:
        try:
            cmd = input(prompt_kali(state.codiname)).strip()
        except KeyboardInterrupt:
            print(f"\n{C.VERMELHO}Execução interrompida.{C.RESET}")
            return False

        if cmd.lower() == 'menu':
            state.saindo_para_menu = True
            print(f"\n{C.AMARELO}Retornando ao menu principal...{C.RESET}")
            return False

        if cmd.lower() == 'manual':
            if carregar_manual():
                aviso("Você perdeu tempo consultando o manual!")
                state.registrar_falha(3)
            continue

        if cmd == cmd_esperado:
            sucesso("Comando executado com sucesso!")
            return True
        else:
            erro("Comando incorreto. Tente novamente.")
            state.registrar_falha(2)

def mostrar_pensamentos_recuperacao(state):
    """Mostra pensamentos de recuperação baseados no nível de depressão"""
    pensamentos = [
        "Talvez ainda haja esperança neste mundo podre...",
        "Os fóruns mostram que não estou sozinho nesta luta.",
        "Cada linha de código me aproxima da verdade.",
        "Ela me traiu, mas o código... o código nunca mente.",
        "Vou descobrir tudo. Vou expor todos eles."
    ]

    idx = max(0, 4 - int(state.nivel_depressao / 20))
    print(f"\n{C.CINZA}💭 {pensamentos[idx]}{C.RESET}")
    time.sleep(2)

def tutorial_comunicacao_anonima():
    """Tutorial sobre comunicação anônima"""
    print(f"\n{C.ROXO}┌─ COMUNICAÇÃO ANÔNIMA ───────────────────────────┐{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Ferramentas essenciais para comunicação segura: {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Ricochet IM{C.RESET} - Chat anônimo via Tor         {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}OTR{C.RESET} - Criptografia de mensagens          {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}PGP/GPG{C.RESET} - Criptografia de emails         {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Tails OS{C.RESET} - Sistema operacional anônimo  {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Verificação{C.RESET} - Nunca confiar cegamente     {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")
    input(f"\n{C.CINZA}[ENTER para continuar]{C.RESET}")

def simular_conversa_ricochet(state, contato, mensagens):
    """Simula uma conversa no Ricochet IM"""
    print(f"\n{C.ROXO}┌─ RICOCHET IM - CONVERSA COM {contato} ──────────────┐{C.RESET}")

    for i, msg in enumerate(mensagens):
        if i % 2 == 0:  # Mensagem do jogador
            print(f"{C.VERDE}Você: {msg}{C.RESET}")
        else:  # Mensagem do contato
            print(f"{C.CIANO}{contato}: {msg}{C.RESET}")
        time.sleep(1)

    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

# ========== CAPÍTULO 3: SEQUÊNCIA PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save=None):
    """
    Função principal do Capítulo 3
    """
    state = GameState(dados_jogador)

    try:
        # Introdução dramática
        exibir_header()

        digitar("Uma semana se passou desde meu primeiro post anônimo.", delay=0.05, cor=C.CIANO)
        time.sleep(1)
        digitar("Começo a sair do fundo do poço. Os fóruns underground me deram esperança.", delay=0.05, cor=C.CIANO)
        digitar("Há outros como eu. Outros que sabem a verdade sobre Juliana.", delay=0.05, cor=C.CIANO)
        digitar("É hora de fazer meu primeiro contato real na dark web.", delay=0.05, cor=C.CIANO)

        mostrar_pensamentos_recuperacao(state)
        print(f"\n{C.CINZA}{'─' * 73}{C.RESET}")
        time.sleep(1)

        # Tutorial comunicação anônima
        tutorial_comunicacao_anonima()

        if not state.missoes.get('configurar_ricochet', False):
            # MISSÃO 1: Configurar Ricochet IM
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 1/5: CONFIGURAÇÃO DO RICOCHET IM{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Preciso de uma forma segura de conversar anonimamente.", delay=0.03, cor=C.VERDE)
            digitar("# Ricochet IM usa Tor para comunicação peer-to-peer.", delay=0.03, cor=C.CINZA)
            digitar("# Vou instalar e configurar.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: sudo apt install ricochet-im", delay=0.03, cor=C.CINZA)

            if prompt_simples("sudo apt install ricochet-im", "Instalar Ricochet IM", state):
                state.completar_missao('configurar_ricochet')
                sucesso("Ricochet IM instalado e configurado!")
                salvar_checkpoint(state, arquivo_save, 'ricochet_configurado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 1 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('analisar_perfil', False):
            # MISSÃO 2: Analisar perfil suspeito
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 2/5: ANÁLISE DE PERFIL SUSPEITO{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Encontrei um perfil interessante no fórum.", delay=0.03, cor=C.VERDE)
            digitar("# Nome: ShadowBroker_89", delay=0.03, cor=C.CINZA)
            digitar("# Parece saber sobre corrupção governamental.", delay=0.03, cor=C.CINZA)
            digitar("# Vou analisar o histórico de posts.", delay=0.03, cor=C.CINZA)

            print(f"\n{C.ROXO}┌─ PERFIL: ShadowBroker_89 ────────────────────────┐{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Posts recentes:                                 {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • 'Corrupção no governo brasileiro'           {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • 'Como hackear sistemas governamentais'     {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • 'Provas de espionagem corporativa'         {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Membro desde: 2018                            {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Reputação: Alta                               {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

            digitar("# Vou verificar se há sinais de honeypot.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: whois shadowbroker89.onion", delay=0.03, cor=C.CINZA)

            if prompt_simples("whois shadowbroker89.onion", "Analisar perfil ShadowBroker_89", state):
                state.completar_missao('analisar_perfil')
                print(f"\n{C.VERDE}✓ Análise concluída: Perfil parece legítimo.{C.RESET}")
                state.contatos_darkweb.append('ShadowBroker_89')
                sucesso("Perfil analisado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'perfil_analisado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 2 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('enviar_mensagem', False):
            # MISSÃO 3: Enviar primeira mensagem
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 3/5: PRIMEIRA MENSAGEM{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora vou enviar minha primeira mensagem.", delay=0.03, cor=C.VERDE)
            digitar("# Preciso ser cuidadoso com o que digo.", delay=0.03, cor=C.CINZA)
            digitar("# Não posso revelar minha identidade real.", delay=0.03, cor=C.CINZA)

            print(f"\n{C.ROXO}💬 DIGITE SUA MENSAGEM PARA ShadowBroker_89:{C.RESET}")
            print(f"{C.CINZA}(Dica: Mantenha-se vago, mas mostre interesse genuíno){C.RESET}")

            mensagem = input(f"{C.VERDE}Mensagem: {C.RESET}").strip()

            if len(mensagem) < 10:
                erro("Mensagem muito curta. Seja mais específico.")
                state.registrar_falha(5)
                return state.to_dict()

            if "juliana" in mensagem.lower() or "namorada" in mensagem.lower():
                erro("ERRO DE SEGURANÇA: Não revele informações pessoais!")
                state.registrar_falha(15)
                return state.to_dict()

            state.mensagens_trocadas.append(f"Você: {mensagem}")
            state.completar_missao('enviar_mensagem')
            sucesso("Mensagem enviada com sucesso!")
            salvar_checkpoint(state, arquivo_save, 'mensagem_enviada')
        else:
            print(f"\n{C.AMARELO}Missão 3 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('receber_resposta', False):
            # MISSÃO 4: Receber resposta
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 4/5: RECEBER RESPOSTA{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora espero pela resposta...", delay=0.03, cor=C.VERDE)
            time.sleep(3)

            # Simular conversa
            conversa = [
                "Vi seu post sobre SQL injection. Interessante.",
                "ShadowBroker_89: Olá. Seu post no fórum chamou minha atenção.",
                "Você: Obrigado. Estou aprendendo sobre segurança.",
                "ShadowBroker_89: Bom ver mais gente interessada. O que te trouxe para cá?",
                "Você: Procuro respostas sobre corrupção governamental.",
                "ShadowBroker_89: Perigoso território. Mas se você é sério, posso ajudar."
            ]

            simular_conversa_ricochet(state, "ShadowBroker_89", conversa)

            state.mensagens_trocadas.extend([
                "ShadowBroker_89: Olá. Seu post no fórum chamou minha atenção.",
                "ShadowBroker_89: Bom ver mais gente interessada. O que te trouxe para cá?",
                "ShadowBroker_89: Perigoso território. Mas se você é sério, posso ajudar."
            ])

            state.completar_missao('receber_resposta')
            sucesso("Resposta recebida! Contato estabelecido.")
            salvar_checkpoint(state, arquivo_save, 'resposta_recebida')
        else:
            print(f"\n{C.AMARELO}Missão 4 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('verificar_seguranca', False):
            # MISSÃO 5: Verificar segurança
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 5/5: VERIFICAÇÃO DE SEGURANÇA{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Antes de continuar, preciso verificar a segurança.", delay=0.03, cor=C.VERDE)
            digitar("# Vou verificar se a conexão está realmente criptografada.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: ricochet-im --check-security", delay=0.03, cor=C.CINZA)

            if prompt_simples("ricochet-im --check-security", "Verificar segurança da comunicação", state):
                state.completar_missao('verificar_seguranca')
                print(f"\n{C.VERDE}✓ Verificação de segurança: CONEXÃO SEGURA{C.RESET}")
                print(f"{C.VERDE}✓ Criptografia OTR: ATIVADA{C.RESET}")
                print(f"{C.VERDE}✓ Roteamento Tor: CONFIRMADO{C.RESET}")
                sucesso("Comunicação verificada como segura!")
                salvar_checkpoint(state, arquivo_save, 'seguranca_verificada')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 5 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        # FINAL DO CAPÍTULO
        exibir_status(state)

        # Momento de reflexão
        mostrar_pensamentos_recuperacao(state)

        digitar("\nNão estou mais sozinho nesta luta.", delay=0.05, cor=C.CIANO)
        digitar("ShadowBroker_89 pode ter as respostas que procuro.", delay=0.05, cor=C.CIANO)
        digitar("Mas preciso ser cuidadoso. Confiança é uma moeda rara na dark web.", delay=0.05, cor=C.CIANO)

        state.capitulo_concluido = True
        state.operacao_sucesso = True
        salvar_checkpoint(state, arquivo_save, 'capitulo_concluido')

        # Resumo final
        completas, total = state.verificar_progresso()
        print(f"\n{C.VERDE}{'═' * 60}{C.RESET}")
        print(f"{C.VERDE}✓ CAPÍTULO 3 CONCLUÍDO!{C.RESET}")
        print(f"{C.CIANO}Missões completadas: {completas}/{total}{C.RESET}")
        print(f"{C.CIANO}Score final: {state.score}{C.RESET}")
        print(f"{C.CIANO}Nível de confiança: {state.nivel_confianca}%{C.RESET}")
        print(f"{C.VERDE}{'═' * 60}{C.RESET}")

        input(f"\n{C.CINZA}[ENTER para continuar para o próximo capítulo]{C.RESET}")

        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}Capítulo interrompido pelo usuário.{C.RESET}")
        return state.to_dict()
    except Exception as e:
        erro(f"Erro inesperado no capítulo: {e}")
        return state.to_dict()


