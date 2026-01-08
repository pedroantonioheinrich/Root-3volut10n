
import sys
import os

# Adiciona diretório atual ao path
sys.path.append(os.getcwd())

try:
    print("Testing imports...")
    import root_evolution_main
    from bitcoin_and_market import BitcoinSystem
    print("Imports successful.")

    print("Testing BitcoinSystem instantiation...")
    # Mock menu interface
    class MockMenu:
        term_width = 80
        def _limpar_tela(self): pass
        def _salvar_jogo(self, d, f): pass

    menu = MockMenu()
    btc_sys = BitcoinSystem(menu)
    print("BitcoinSystem instantiated successfully.")
    
    # Test method existence
    assert hasattr(btc_sys, 'mostrar_carteira')
    assert hasattr(btc_sys, 'mercado_negro')
    print("Methods verified.")

except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
