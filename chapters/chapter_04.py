#!/usr/bin/env python3
"""
CHAPTER_04.PY - "O Mercado Negro"
ShadowBroker_89 me deu uma dica valiosa: o mercado negro da dark web.
É hora de comprar minhas primeiras ferramentas reais. Mas tudo tem um preço.

Foco: Primeiro acesso ao mercado negro, compra de ferramentas
Habilidades: Navegação em mercados dark web, transações bitcoin, avaliação de risco
Objetivos: 6 missões principais + exploração livre
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
        self.current_chapter = dados_jogador.get('current_chapter', 4)
        self.completed_chapters = dados_jogador.get('completed_chapters', [])
        self.score = dados_jogador.get('score', 0)
        self.privacy_level = dados_jogador.get('privacy_level', 75)
        self.bitcoin_wallet = dados_jogador.get('bitcoin_wallet', 0.005)

        # Estado do capítulo
        self.capitulo_concluido = dados_jogador.get('completed', False)
        self.operacao_sucesso = dados_jogador.get('capitulo_4_operacao_sucesso', False)
        self.checkpoint = dados_jogador.get('chapter_04_checkpoint', 'inicio')
        self.saindo_para_menu = dados_jogador.get('saindo_para_menu', False)

        # Missões do capítulo 4
        self.missoes = {
            'acessar_mercado': False,           # Acessar mercado negro
            'avaliar_vendedor': False,          # Avaliar reputação de vendedor
            'comprar_ferramenta': False,        # Comprar primeira ferramenta
            'verificar_pagamento': False,       # Verificar transação bitcoin
            'receber_entrega': False,           # Receber ferramenta comprada
            'testar_ferramenta': False          # Testar ferramenta adquirida
        }

        # Estado emocional (continuando recuperação)
        self.nivel_depressao = dados_jogador.get('nivel_depressao', 65) - 10
        self.motivacao_hacker = dados_jogador.get('motivacao_hacker', 40) + 10

        # Mercado negro
        self.mercados_visitados = dados_jogador.get('mercados_visitados', [])
        self.ferramentas_compradas = dados_jogador.get('ferramentas_compradas', [])
        self.bitcoin_gasto = dados_jogador.get('bitcoin_gasto', 0.0)
        self.reputacao_mercado = dados_jogador.get('reputacao_mercado', 0)
        self.missoes = dados_jogador.get('missoes_capitulo_4', self.missoes)
        self.nivel_depressao = dados_jogador.get('nivel_depressao', self.nivel_depressao)
        self.motivacao_hacker = dados_jogador.get('motivacao_hacker', self.motivacao_hacker)

    def registrar_sucesso(self, pontos=10):
        """Registra sucesso e adiciona pontos"""
        self.score += pontos
        self.privacy_level = max(0, self.privacy_level - 2)
        self.motivacao_hacker = min(100, self.motivacao_hacker + 10)
        self.nivel_depressao = max(0, self.nivel_depressao - 8)
        self.reputacao_mercado += 5

    def registrar_falha(self, pontos_perdidos=5):
        """Registra falha e penaliza"""
        self.score = max(0, self.score - pontos_perdidos)
        self.privacy_level = max(0, self.privacy_level - 15)
        self.nivel_depressao += 10
        self.reputacao_mercado = max(0, self.reputacao_mercado - 20)

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

    def gastar_bitcoin(self, quantidade):
        """Gasta bitcoin da carteira"""
        if self.bitcoin_wallet >= quantidade:
            self.bitcoin_wallet -= quantidade
            self.bitcoin_gasto += quantidade
            return True
        return False

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
            'chapter_04_checkpoint': self.checkpoint,
            'capitulo_4_resultado': None,
            'capitulo_4_operacao_sucesso': self.operacao_sucesso,
            'completed': self.capitulo_concluido,
            'saindo_para_menu': False,
            'missoes_capitulo_4': self.missoes.copy(),
            'nivel_depressao': self.nivel_depressao,
            'motivacao_hacker': self.motivacao_hacker,
            'mercados_visitados': self.mercados_visitados,
            'ferramentas_compradas': self.ferramentas_compradas,
            'bitcoin_gasto': self.bitcoin_gasto,
            'reputacao_mercado': self.reputacao_mercado
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
    print(f"{C.ROXO}║{'ROOT EVOLUTION - CAPÍTULO 4: O MERCADO NEGRO':^78}║{C.RESET}")
    print(f"{C.CINZA}║{'Brasília, 5 semanas depois | Terminal: Kali Linux 2024':^78}║{C.RESET}")
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
    print(f"{C.ROXO}│{C.RESET} Depressão: {C.VERMELHO}{state.nivel_depressao:2d}%{C.RESET} │ Motivação: {C.AMARELO}{state.motivacao_hacker:2d}%{C.RESET} │ Rep. Mercado: {C.ROXO}{state.reputacao_mercado:2d}%{C.RESET} {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} BTC: {C.AMARELO}{state.bitcoin_wallet:.4f}{C.RESET} │ Gasto: {C.VERMELHO}{state.bitcoin_gasto:.4f}{C.RESET} │ Ferramentas: {C.VERDE}{len(state.ferramentas_compradas)}{C.RESET} {C.ROXO}│{C.RESET}")
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

def mostrar_pensamentos_mercado(state):
    """Mostra pensamentos sobre o mercado negro"""
    pensamentos = [
        "Este lugar é perigoso... mas necessário.",
        "Cada ferramenta que compro me aproxima da verdade.",
        "Bitcoin é a moeda da liberdade digital.",
        "Preciso ser cuidadoso. Um passo em falso e estou perdido.",
        "O conhecimento tem preço. Estou disposto a pagar."
    ]

    idx = min(int(state.reputacao_mercado / 25), len(pensamentos) - 1)
    print(f"\n{C.CINZA}💭 {pensamentos[idx]}{C.RESET}")
    time.sleep(2)

def tutorial_mercado_negro():
    """Tutorial sobre mercados da dark web"""
    print(f"\n{C.ROXO}┌─ MERCADOS DA DARK WEB ──────────────────────────┐{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} Como navegar com segurança nos mercados:       {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Avaliação{C.RESET} - Verifique reputação do vendedor {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}PGP{C.RESET} - Use criptografia para comunicações   {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Multisig{C.RESET} - Proteção contra golpes          {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Escrow{C.RESET} - Serviço de garantia de pagamento  {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} • {C.VERDE}Avaliações{C.RESET} - Leia reviews de outros compradores{C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")
    input(f"\n{C.CINZA}[ENTER para continuar]{C.RESET}")

def exibir_catalogo_mercado():
    """Exibe catálogo de ferramentas disponíveis"""
    print(f"\n{C.ROXO}┌─ CATÁLOGO: DARK MARKET ─────────────────────────┐{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} 🛠️  FERRAMENTAS DISPONÍVEIS:                     {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} 1. {C.VERDE}Metasploit Framework{C.RESET} - 0.002 BTC       {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}    Framework completo para exploração         {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} 2. {C.VERDE}Nmap Advanced{C.RESET} - 0.001 BTC             {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}    Scanner de rede com scripts customizados  {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} 3. {C.VERDE}Wireshark Pro{C.RESET} - 0.0015 BTC           {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}    Analisador de pacotes com filtros        {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET} 4. {C.VERDE}John the Ripper{C.RESET} - 0.0008 BTC         {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}│{C.RESET}    Quebrador de senhas avançado              {C.ROXO}│{C.RESET}")
    print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

def simular_transacao_bitcoin(state, valor, descricao):
    """Simula uma transação bitcoin"""
    print(f"\n{C.AMARELO}┌─ TRANSAÇÃO BITCOIN ─────────────────────────────┐{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} Descrição: {descricao}                       {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} Valor: {C.VERDE}{valor:.4f} BTC{C.RESET}                        {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} Saldo atual: {C.VERDE}{state.bitcoin_wallet:.4f} BTC{C.RESET}           {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}│{C.RESET} Saldo após: {C.VERDE}{(state.bitcoin_wallet - valor):.4f} BTC{C.RESET}         {C.AMARELO}│{C.RESET}")
    print(f"{C.AMARELO}└─────────────────────────────────────────────────┘{C.RESET}")

    if state.gastar_bitcoin(valor):
        print(f"\n{C.VERDE}✓ Transação confirmada!{C.RESET}")
        return True
    else:
        print(f"\n{C.VERMELHO}✗ Saldo insuficiente!{C.RESET}")
        return False

# ========== CAPÍTULO 4: SEQUÊNCIA PRINCIPAL ==========

def iniciar(dados_jogador, arquivo_save=None):
    """
    Função principal do Capítulo 4
    """
    state = GameState(dados_jogador)

    try:
        # Introdução dramática
        exibir_header()

        digitar("ShadowBroker_89 me deu uma dica valiosa.", delay=0.05, cor=C.CIANO)
        time.sleep(1)
        digitar("'Se você quer ferramentas reais, vá ao mercado negro'.", delay=0.05, cor=C.CIANO)
        digitar("É hora de comprar minhas primeiras ferramentas reais.", delay=0.05, cor=C.CIANO)
        digitar("Mas tudo tem um preço... em bitcoin.", delay=0.05, cor=C.CIANO)

        mostrar_pensamentos_mercado(state)
        print(f"\n{C.CINZA}{'─' * 73}{C.RESET}")
        time.sleep(1)

        # Tutorial mercado negro
        tutorial_mercado_negro()

        if not state.missoes.get('acessar_mercado', False):
            # MISSÃO 1: Acessar mercado negro
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 1/6: ACESSO AO MERCADO NEGRO{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] ShadowBroker me deu o link para o Dark Market.", delay=0.03, cor=C.VERDE)
            digitar("# darkmarketx7z.onion - um dos maiores mercados.", delay=0.03, cor=C.CINZA)
            digitar("# Vou acessar através do Tor.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: torsocks lynx https://darkmarketx7z.onion", delay=0.03, cor=C.CINZA)

            if prompt_simples("torsocks lynx https://darkmarketx7z.onion", "Acessar mercado negro", state):
                state.completar_missao('acessar_mercado')
                state.mercados_visitados.append('Dark Market')
                print(f"\n{C.ROXO}🏪 Bem-vindo ao Dark Market!{C.RESET}")
                print(f"{C.ROXO}📦 1.247 vendedores ativos | 💰 Volume: 2.3 BTC/dia{C.RESET}")
                sucesso("Mercado acessado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'mercado_acessado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 1 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('avaliar_vendedor', False):
            # MISSÃO 2: Avaliar vendedor
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 2/6: AVALIAÇÃO DE VENDEDOR{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora preciso avaliar um vendedor confiável.", delay=0.03, cor=C.VERDE)
            digitar("# Vou procurar o vendedor 'CyberTools_Pro'.", delay=0.03, cor=C.CINZA)
            digitar("# Preciso verificar sua reputação.", delay=0.03, cor=C.CINZA)

            print(f"\n{C.ROXO}┌─ PERFIL VENDEDOR: CyberTools_Pro ───────────────┐{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} 📊 Estatísticas:                               {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • Vendas realizadas: 1.247                  {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • Avaliação média: 4.8/5                    {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • Tempo de resposta: < 1 hora                {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • Membro desde: 2020                        {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET}                                               {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} 💬 Reviews recentes:                         {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • 'Entrega rápida e discreta'               {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • 'Ferramentas funcionam perfeitamente'      {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} • 'Recomendo para todos'                     {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

            digitar("# Vou verificar se há reclamações.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: grep -i 'cybertools' reviews.txt", delay=0.03, cor=C.CINZA)

            if prompt_simples("grep -i 'cybertools' reviews.txt", "Verificar reviews do vendedor", state):
                state.completar_missao('avaliar_vendedor')
                print(f"\n{C.VERDE}✓ Avaliação concluída: Vendedor confiável!{C.RESET}")
                sucesso("Vendedor avaliado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'vendedor_avaliado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 2 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('comprar_ferramenta', False):
            # MISSÃO 3: Comprar ferramenta
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 3/6: COMPRA DE FERRAMENTA{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora vou comprar minha primeira ferramenta.", delay=0.03, cor=C.VERDE)
            digitar("# Vou escolher o Metasploit Framework.", delay=0.03, cor=C.CINZA)
            digitar("# É uma ferramenta essencial para exploração.", delay=0.03, cor=C.CINZA)

            exibir_catalogo_mercado()

            print(f"\n{C.ROXO}💰 QUAL FERRAMENTA DESEJA COMPRAR? (1-4):{C.RESET}")
            escolha = input(f"{C.VERDE}Escolha: {C.RESET}").strip()

            ferramentas = {
                '1': ('Metasploit Framework', 0.002),
                '2': ('Nmap Advanced', 0.001),
                '3': ('Wireshark Pro', 0.0015),
                '4': ('John the Ripper', 0.0008)
            }

            if escolha not in ferramentas:
                erro("Escolha inválida!")
                state.registrar_falha(10)
                return state.to_dict()

            ferramenta, preco = ferramentas[escolha]

            if simular_transacao_bitcoin(state, preco, f"Compra de {ferramenta}"):
                state.completar_missao('comprar_ferramenta')
                state.ferramentas_compradas.append(ferramenta)
                sucesso(f"{ferramenta} comprada com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'ferramenta_comprada')
            else:
                erro("Compra falhou - saldo insuficiente!")
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 3 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('verificar_pagamento', False):
            # MISSÃO 4: Verificar pagamento
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 4/6: VERIFICAÇÃO DE PAGAMENTO{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora preciso verificar se o pagamento foi processado.", delay=0.03, cor=C.VERDE)
            digitar("# Vou verificar no blockchain.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: bitcoin-cli gettransaction <txid>", delay=0.03, cor=C.CINZA)

            if prompt_simples("bitcoin-cli gettransaction <txid>", "Verificar transação bitcoin", state):
                state.completar_missao('verificar_pagamento')
                print(f"\n{C.VERDE}✓ Transação confirmada no blockchain!{C.RESET}")
                print(f"{C.VERDE}✓ Confirmações: 6/6 | Status: FINALIZADO{C.RESET}")
                sucesso("Pagamento verificado com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'pagamento_verificado')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 4 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('receber_entrega', False):
            # MISSÃO 5: Receber entrega
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 5/6: RECEBIMENTO DA ENTREGA{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora espero pela entrega da ferramenta.", delay=0.03, cor=C.VERDE)
            digitar("# O vendedor vai enviar por um link onion.", delay=0.03, cor=C.CINZA)
            time.sleep(3)

            print(f"\n{C.ROXO}📦 MENSAGEM DO VENDEDOR:{C.RESET}")
            print(f"{C.ROXO}┌─────────────────────────────────────────────────┐{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} CyberTools_Pro: Pagamento recebido!           {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Link de download: download123.onion/dl/msf    {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}│{C.RESET} Senha: H4ck3rP0w3r2024                       {C.ROXO}│{C.RESET}")
            print(f"{C.ROXO}└─────────────────────────────────────────────────┘{C.RESET}")

            digitar("# Vou baixar a ferramenta.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: wget --user=anon --password=H4ck3rP0w3r2024 https://download123.onion/dl/msf", delay=0.03, cor=C.CINZA)

            if prompt_simples("wget --user=anon --password=H4ck3rP0w3r2024 https://download123.onion/dl/msf", "Baixar ferramenta comprada", state):
                state.completar_missao('receber_entrega')
                sucesso("Ferramenta recebida com sucesso!")
                salvar_checkpoint(state, arquivo_save, 'entrega_recebida')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 5 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        exibir_status(state)
        time.sleep(2)

        if not state.missoes.get('testar_ferramenta', False):
            # MISSÃO 6: Testar ferramenta
            print(f"\n{C.ROXO}{'═' * 60}{C.RESET}")
            print(f"{C.ROXO}🎯 MISSÃO 6/6: TESTE DA FERRAMENTA{C.RESET}")
            print(f"{C.ROXO}{'═' * 60}{C.RESET}")

            digitar("\n[*] Agora vou testar a ferramenta que comprei.", delay=0.03, cor=C.VERDE)
            digitar("# Vou verificar se o Metasploit está funcionando.", delay=0.03, cor=C.CINZA)
            digitar("# Comando: msfconsole --version", delay=0.03, cor=C.CINZA)

            if prompt_simples("msfconsole --version", "Testar ferramenta Metasploit", state):
                state.completar_missao('testar_ferramenta')
                print(f"\n{C.VERDE}✓ Metasploit Framework v6.3.1 - FUNCIONANDO!{C.RESET}")
                print(f"{C.VERDE}✓ Módulos carregados: 2.847{C.RESET}")
                print(f"{C.VERDE}✓ Exploits disponíveis: 1.234{C.RESET}")
                sucesso("Ferramenta testada e funcionando!")
                salvar_checkpoint(state, arquivo_save, 'ferramenta_testada')
            else:
                return state.to_dict()
        else:
            print(f"\n{C.AMARELO}Missão 6 já concluída. Continuando...{C.RESET}")
            time.sleep(1)

        # FINAL DO CAPÍTULO
        exibir_status(state)

        # Momento de reflexão
        mostrar_pensamentos_mercado(state)

        digitar("\nA ferramenta está funcionando perfeitamente.", delay=0.05, cor=C.CIANO)
        digitar("Paguei com bitcoin, recebi anonimamente.", delay=0.05, cor=C.CIANO)
        digitar("O mercado negro é eficiente... e perigoso.", delay=0.05, cor=C.CIANO)
        digitar("Mas agora tenho poder real nas mãos.", delay=0.05, cor=C.CIANO)

        state.capitulo_concluido = True
        state.operacao_sucesso = True
        salvar_checkpoint(state, arquivo_save, 'capitulo_concluido')

        # Resumo final
        completas, total = state.verificar_progresso()
        print(f"\n{C.VERDE}{'═' * 60}{C.RESET}")
        print(f"{C.VERDE}✓ CAPÍTULO 4 CONCLUÍDO!{C.RESET}")
        print(f"{C.CIANO}Missões completadas: {completas}/{total}{C.RESET}")
        print(f"{C.CIANO}Score final: {state.score}{C.RESET}")
        print(f"{C.CIANO}Ferramentas compradas: {len(state.ferramentas_compradas)}{C.RESET}")
        print(f"{C.CIANO}Bitcoin gasto: {state.bitcoin_gasto:.4f}{C.RESET}")
        print(f"{C.VERDE}{'═' * 60}{C.RESET}")

        input(f"\n{C.CINZA}[ENTER para continuar para o próximo capítulo]{C.RESET}")

        return state.to_dict()

    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}Capítulo interrompido pelo usuário.{C.RESET}")
        return state.to_dict()
    except Exception as e:
        erro(f"Erro inesperado no capítulo: {e}")
        return state.to_dict()
