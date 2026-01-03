#!/usr/bin/env python3
"""
Pacote CHAPTERS - Módulos dos capítulos do jogo ROOT EVOLUTION

Este arquivo transforma o diretório 'chapters' em um pacote Python válido
e facilita a importação dos capítulos.
"""

import os
import sys

# Adiciona o diretório pai ao path para facilitar imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Lista todos os capítulos disponíveis
__all__ = ['chapter_01', 'chapter_02']  # Adicione mais capítulos conforme criar

# Versão do pacote
__version__ = '1.0.0'
__author__ = 'Root Evolution Team'
__description__ = 'Capítulos do jogo de hacking ROOT EVOLUTION'

# Importações facilitadas
try:
    from ..backup_chapters.chapter_01 import iniciar as iniciar_capitulo_1
    __all__.append('iniciar_capitulo_1')
except ImportError as e:
    print(f"[WARNING] Não foi possível importar chapter_01: {e}")

try:
    from ..backup_chapters.chapter_02 import iniciar as iniciar_capitulo_2
    __all__.append('iniciar_capitulo_2')
except ImportError:
    pass  # chapter_02 pode não existir ainda

# Função utilitária para listar capítulos disponíveis
def listar_capitulos():
    """Lista todos os capítulos disponíveis no pacote."""
    capitulos = []
    
    # Procura por arquivos chapter_*.py no diretório
    for arquivo in os.listdir(os.path.dirname(__file__)):
        if arquivo.startswith('chapter_') and arquivo.endswith('.py'):
            nome = arquivo[:-3]  # Remove .py
            capitulos.append(nome)
    
    return sorted(capitulos)

# Função para carregar um capítulo específico
def carregar_capitulo(numero):
    """
    Carrega e retorna a função 'iniciar' de um capítulo específico.
    
    Args:
        numero (int ou str): Número do capítulo (ex: 1, 2, "01", "02")
    
    Returns:
        function: Função 'iniciar' do capítulo
    
    Raises:
        ImportError: Se o capítulo não existir
    """
    # Normaliza o número do capítulo
    if isinstance(numero, int):
        numero = f"{numero:02d}"
    else:
        numero = str(numero).zfill(2)
    
    nome_modulo = f"chapter_{numero}"
    
    if nome_modulo not in __all__:
        raise ImportError(f"Capítulo {numero} não encontrado")
    
    # Importação dinâmica
    modulo = __import__(f".{nome_modulo}", fromlist=['iniciar'], level=1)
    
    if not hasattr(modulo, 'iniciar'):
        raise AttributeError(f"Módulo {nome_modulo} não tem função 'iniciar'")
    
    return modulo.iniciar

# Função para verificar a integridade dos capítulos
def verificar_integridade():
    """Verifica se todos os capítulos estão funcionando corretamente."""
    resultados = {}
    
    for cap in listar_capitulos():
        try:
            # Tenta importar o módulo
            modulo = __import__(f".{cap}", fromlist=['iniciar'], level=1)
            
            # Verifica se tem a função 'iniciar'
            if hasattr(modulo, 'iniciar'):
                resultados[cap] = {
                    'status': 'OK',
                    'tem_iniciar': True
                }
            else:
                resultados[cap] = {
                    'status': 'ERRO',
                    'tem_iniciar': False,
                    'erro': 'Função "iniciar" não encontrada'
                }
                
        except Exception as e:
            resultados[cap] = {
                'status': 'ERRO',
                'erro': str(e)
            }
    
    return resultados

# Informações de debug quando executado diretamente
if __name__ == "__main__":
    print(f"=== Pacote CHAPTERS v{__version__} ===")
    print(f"Descrição: {__description__}")
    print(f"Autor: {__author__}")
    print(f"\nCapítulos disponíveis: {listar_capitulos()}")
    print(f"\nIntegridade:")
    for cap, info in verificar_integridade().items():
        status = info['status']
        print(f"  {cap}: {status}")
        if status == 'ERRO':
            print(f"    Erro: {info.get('erro', 'Desconhecido')}")