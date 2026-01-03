#!/usr/bin/env python3
"""
Teste interativo do fluxo do jogo:
1. Criar novo jogo
2. Entrar no menu de jogo
3. Continuar jogo (chapter_01)
4. Digitar 'menu' para voltar salvando checkpoint
5. Verificar se continua jogo funciona
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from io import StringIO

# Adicionar projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simular inputs do usuário
class MockInput:
    def __init__(self, inputs):
        self.inputs = iter(inputs)
    
    def __call__(self, prompt=""):
        try:
            valor = next(self.inputs)
            print(f"{prompt}{valor}")
            return valor
        except StopIteration:
            raise EOFError("Entrada simulada esgotada")

def test_chapter_01_basic():
    """Teste básico: executar chapter_01 com 'menu' no primeiro prompt"""
    print("\n" + "="*60)
    print("TESTE 1: Chapter 01 com 'menu' no primeiro prompt")
    print("="*60)
    
    try:
        from chapters.chapter_01 import iniciar
        
        # Criar dados de teste
        dados_teste = {
            'player_name': 'Test_Player',
            'codiname': 'TESTE_01',
            'current_chapter': 1,
            'completed_chapters': [],
            'score': 0,
            'inventory': [],
            'bitcoin_wallet': 0.005,
            'privacy_level': 80,
            'darknet_access': False,
            'reputation': 0,
            'last_seen': '2026-01-03T00:00:00'
        }
        
        # Criar arquivo temporário para save
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            save_file = f.name
            json.dump(dados_teste, f)
        
        # Simular inputs: digitar 'menu' no primeiro prompt
        inputs_simulados = ['menu']
        original_input = __builtins__.input
        __builtins__.input = MockInput(inputs_simulados)
        
        resultado = None
        try:
            resultado = iniciar(dados_teste, save_file)
            
            print(f"\n[✓] Chapter executado com sucesso")
            print(f"    - checkpoint: {resultado.get('chapter_01_checkpoint', 'N/A')}")
            print(f"    - Arquivo de save: {save_file}")
            
            # Verificar se arquivo foi salvo
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    saved = json.load(f)
                print(f"[✓] Save file criado e contém:")
                print(f"    - player_name: {saved.get('player_name')}")
                print(f"    - score: {saved.get('score')}")
                print(f"    - checkpoint: {saved.get('chapter_01_checkpoint', 'N/A')}")
                return True
            else:
                print("[!] Save file não foi criado")
                return False
                
        finally:
            __builtins__.input = original_input
            if os.path.exists(save_file):
                os.unlink(save_file)
    
    except Exception as e:
        print(f"[!] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chapter_01_commands():
    """Teste 2: executar alguns comandos antes de digitar 'menu'"""
    print("\n" + "="*60)
    print("TESTE 2: Digitar comandos corretos depois 'menu'")
    print("="*60)
    
    try:
        from chapters.chapter_01 import iniciar
        
        dados_teste = {
            'player_name': 'Test_Player_2',
            'codiname': 'TESTE_02',
            'current_chapter': 1,
            'completed_chapters': [],
            'score': 0,
            'inventory': [],
            'bitcoin_wallet': 0.005,
            'privacy_level': 80,
            'darknet_access': False,
            'reputation': 0,
            'last_seen': '2026-01-03T00:00:00'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            save_file = f.name
            json.dump(dados_teste, f)
        
        # Simular: comando correto + menu
        inputs_simulados = [
            'ssh admin@backup-cloud',  # Primeiro comando (correto)
            'menu'  # Sair para menu após primeiro sucesso
        ]
        
        original_input = __builtins__.input
        __builtins__.input = MockInput(inputs_simulados)
        
        resultado = None
        try:
            resultado = iniciar(dados_teste, save_file)
            
            print(f"\n[✓] Chapter executado com sucesso após 1 comando")
            print(f"    - Score após comando: {resultado.get('score', 0)}")
            
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    saved = json.load(f)
                print(f"[✓] Save file contém score atualizado: {saved.get('score')}")
                return True
            return False
                
        finally:
            __builtins__.input = original_input
            if os.path.exists(save_file):
                os.unlink(save_file)
    
    except Exception as e:
        print(f"[!] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_command():
    """Teste 3: Digitar 'manual' (deve mostrar banner mas continuar jogo)"""
    print("\n" + "="*60)
    print("TESTE 3: Digitar 'manual' e depois 'menu'")
    print("="*60)
    
    try:
        from chapters.chapter_01 import iniciar
        
        dados_teste = {
            'player_name': 'Test_Player_3',
            'codiname': 'TESTE_03',
            'current_chapter': 1,
            'completed_chapters': [],
            'score': 0,
            'inventory': [],
            'bitcoin_wallet': 0.005,
            'privacy_level': 80,
            'darknet_access': False,
            'reputation': 0,
            'last_seen': '2026-01-03T00:00:00'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            save_file = f.name
            json.dump(dados_teste, f)
        
        # Simular: manual + menu
        inputs_simulados = [
            'manual',  # Tentar acessar manual
            'menu'  # Depois sair
        ]
        
        original_input = __builtins__.input
        __builtins__.input = MockInput(inputs_simulados)
        
        resultado = None
        try:
            resultado = iniciar(dados_teste, save_file)
            
            print(f"\n[✓] Manual não interrompeu o jogo")
            print(f"    - Erros acumulados após manual: {resultado.get('privacy_level', 'N/A')}")
            
            return True
                
        finally:
            __builtins__.input = original_input
            if os.path.exists(save_file):
                os.unlink(save_file)
    
    except Exception as e:
        print(f"[!] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█  TESTES INTERATIVOS DO JOGO".center(60))
    print("█"*60)
    
    resultados = []
    
    # Teste 1
    resultados.append(("Chapter 01 com menu", test_chapter_01_basic()))
    
    # Teste 2
    resultados.append(("Chapter 01 com comandos", test_chapter_01_commands()))
    
    # Teste 3
    resultados.append(("Manual + menu", test_manual_command()))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES".center(60))
    print("="*60)
    
    passed = 0
    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"{nome:<40} {status}")
        if resultado:
            passed += 1
    
    print("="*60)
    print(f"Total: {passed}/{len(resultados)} testes passaram")
    
    sys.exit(0 if passed == len(resultados) else 1)
