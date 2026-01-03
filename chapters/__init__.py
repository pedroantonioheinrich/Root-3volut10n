#!/usr/bin/env python3
"""
Pacote CHAPTERS - Módulos dos capítulos do jogo ROOT EVOLUTION

Este arquivo transforma o diretório 'chapters' em um pacote Python válido
e facilita a importação dos capítulos.

Capítulos Disponíveis:
- chapter_01: O Protocolo da Traição
- chapter_02: O Vazio entre os Bits (em desenvolvimento)
- chapter_03: O Primeiro Chamado (em desenvolvimento)
- chapter_04: A Mentira Benevolente (em desenvolvimento)
- chapter_05: Rootkit na Realidade (em desenvolvimento)
"""

import os
import sys
import importlib
import json
from pathlib import Path
from datetime import datetime

# Adiciona o diretório pai ao path para facilitar imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Versão do pacote
__version__ = '1.0.0'
__author__ = 'Root Evolution Team'
__description__ = 'Capítulos do jogo de hacking ROOT EVOLUTION'

# Cores para output
try:
    from utils.terminal_kali import C
except ImportError:
    class C:
        VERDE = '\033[92m'
        VERMELHO = '\033[91m'
        CINZA = '\033[90m'
        CIANO = '\033[96m'
        RESET = '\033[0m'


# ========== FUNÇÕES UTILITÁRIAS ==========

def listar_capitulos():
    """Lista todos os capítulos disponíveis no pacote."""
    capitulos = []
    
    # Procura por arquivos chapter_*.py no diretório
    diretorio = os.path.dirname(__file__)
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith('chapter_') and arquivo.endswith('.py'):
            nome = arquivo[:-3]  # Remove .py
            numero = int(nome.split('_')[1])
            capitulos.append((numero, nome))
    
    return sorted(capitulos, key=lambda x: x[0])


def carregar_capitulo(numero):
    """
    Carrega um capítulo específico dinamicamente.
    
    Args:
        numero: Número do capítulo (ex: 1 para chapter_01)
    
    Returns:
        Módulo do capítulo ou None se não encontrado
    """
    nome_capitulo = f'chapter_{numero:02d}'
    
    try:
        # Tentar importar o capítulo
        modulo = importlib.import_module(f'.{nome_capitulo}', package=__name__)
        return modulo
    except ImportError as e:
        print(f"{C.VERMELHO}[!] Capítulo {numero} não encontrado: {e}{C.RESET}")
        return None


def executar_capitulo(numero, dados_jogador, arquivo_save):
    """
    Executa um capítulo específico.
    
    Args:
        numero: Número do capítulo
        dados_jogador: Dicionário com dados do personagem
        arquivo_save: Caminho do arquivo de save
    
    Returns:
        Dicionário com dados atualizados do jogador ou None se erro
    """
    modulo = carregar_capitulo(numero)
    
    if modulo is None:
        return None
    
    if not hasattr(modulo, 'iniciar'):
        print(f"{C.VERMELHO}[!] Capítulo {numero} não possui função 'iniciar'{C.RESET}")
        return None
    
    try:
        resultado = modulo.iniciar(dados_jogador, arquivo_save)
        return resultado
    except Exception as e:
        print(f"{C.VERMELHO}[!] Erro ao executar capítulo {numero}: {e}{C.RESET}")
        return None


def obter_proximo_capitulo(dados_jogador):
    """
    Determina qual é o próximo capítulo a ser jogado.
    
    Args:
        dados_jogador: Dicionário com dados do personagem
    
    Returns:
        Número do próximo capítulo
    """
    capitulos_completados = dados_jogador.get('completed_chapters', [])
    capitulo_atual = dados_jogador.get('current_chapter', 1)
    
    # Se completou capítulos, pega o próximo
    if capitulos_completados:
        return max(capitulos_completados) + 1
    
    # Caso contrário, retorna o capítulo atual
    return capitulo_atual


def obter_ultimo_capitulo_jogado(dados_jogador):
    """Retorna qual foi o último capítulo jogado."""
    capitulos_completados = dados_jogador.get('completed_chapters', [])
    
    if capitulos_completados:
        return max(capitulos_completados)
    
    return 0


# ========== IMPORTAÇÕES FACILITADAS ==========

def importar_capitulo_1():
    """Importa o capítulo 1"""
    try:
        from . import chapter_01
        return chapter_01
    except ImportError:
        print(f"{C.VERMELHO}[!] Capítulo 1 não encontrado{C.RESET}")
        return None


# ========== INFORMAÇÕES DOS CAPÍTULOS ==========

CAPITULOS_INFO = {
    1: {
        'nome': 'O Protocolo da Traição',
        'descricao': 'Brasília, 02:47 AM. Descubra a traição de Juliana hackando seu servidor.',
        'dificuldade': 'Fácil',
        'foco': 'SSH, manipulação de arquivos',
        'arquivo': 'chapter_01.py',
        'ativo': True
    },
    2: {
        'nome': 'O Vazio entre os Bits',
        'descricao': 'Três semanas depois. A depressão consome, mas o código faz sentido.',
        'dificuldade': 'Médio',
        'foco': 'Criptografia básica, anonimato digital',
        'arquivo': 'chapter_02.py',
        'ativo': False
    },
    3: {
        'nome': 'O Primeiro Chamado',
        'descricao': 'Uma mensagem misteriosa: "Vimos seu trabalho. Procure por fsociety.br"',
        'dificuldade': 'Médio',
        'foco': 'SQL Injection, bypass de autenticação',
        'arquivo': 'chapter_03.py',
        'ativo': False
    },
    4: {
        'nome': 'A Mentira Benevolente',
        'descricao': 'Seis meses com os Anônimos. As missões ficam mais complexas.',
        'dificuldade': 'Difícil',
        'foco': 'Análise forense, data mining',
        'arquivo': 'chapter_04.py',
        'ativo': False
    },
    5: {
        'nome': 'Rootkit na Realidade',
        'descricao': 'Os Anônimos preparam "Operação Raiz". Você escolhe seu caminho.',
        'dificuldade': 'Muito Difícil',
        'foco': 'Todas as habilidades anteriores',
        'arquivo': 'chapter_05.py',
        'ativo': False
    }
}


def obter_info_capitulo(numero):
    """Retorna informações sobre um capítulo específico."""
    return CAPITULOS_INFO.get(numero, None)


def listar_info_capitulos():
    """Lista informações sobre todos os capítulos."""
    return CAPITULOS_INFO


# ========== VALIDAÇÃO DE CAPÍTULOS ==========

def validar_capitulos():
    """Valida quais capítulos estão disponíveis."""
    diretorio = Path(__file__).parent
    
    print(f"{C.CIANO}Validando capítulos...{C.RESET}\n")
    
    capitulos_encontrados = []
    
    for numero, info in CAPITULOS_INFO.items():
        arquivo = diretorio / info['arquivo']
        
        if arquivo.exists():
            print(f"{C.VERDE}[✓]{C.RESET} Capítulo {numero}: {info['nome']}")
            capitulos_encontrados.append(numero)
        else:
            print(f"{C.CINZA}[○]{C.RESET} Capítulo {numero}: {info['nome']} (não encontrado)")
    
    print(f"\n{C.CIANO}Total: {len(capitulos_encontrados)} capítulos disponíveis{C.RESET}")
    
    return capitulos_encontrados


# Exportar funções principais
__all__ = [
    'listar_capitulos',
    'carregar_capitulo',
    'executar_capitulo',
    'obter_proximo_capitulo',
    'obter_ultimo_capitulo_jogado',
    'importar_capitulo_1',
    'obter_info_capitulo',
    'listar_info_capitulos',
    'validar_capitulos',
    'CAPITULOS_INFO'
]


if __name__ == "__main__":
    # Validar capítulos quando executado diretamente
    validar_capitulos()
    
    print(f"\n=== Pacote CHAPTERS v{__version__} ===")
    print(f"Descrição: {__description__}")
    print(f"Autor: {__author__}")
    print(f"\nCapítulos disponíveis: {listar_capitulos()}")
    print(f"\nIntegridade:")
    
    # Verificar integridade dos capítulos
    integridade = verificar_integridade()
    for cap_tuple, info in integridade.items():
        numero, nome = cap_tuple
        status = info['status']
        print(f"  {nome}: {status}")
        if status == 'ERRO':
            print(f"    Erro: {info.get('erro', 'Desconhecido')}")