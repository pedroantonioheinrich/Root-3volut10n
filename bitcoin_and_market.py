
import time
import sys

# Tentar importar utils para cores
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
        RESET = '\033[0m'

class BitcoinSystem:
    def __init__(self, menu_interface):
        """
        Inicializa o sistema de Bitcoin e Mercado.
        :param menu_interface: Instância da classe IntroMenu (para acessar métodos de UI e Save)
        """
        self.menu = menu_interface
        self.term_width = getattr(menu_interface, 'term_width', 100)

    def _limpar_tela(self):
        if hasattr(self.menu, '_limpar_tela'):
            self.menu._limpar_tela()
        else:
            print("\n" * 50)

    def _mostrar_erro(self, msg):
        print(f"\n{' ' * ((self.term_width - 30) // 2)}{C.VERMELHO}{msg}{C.RESET}")
        time.sleep(1.5)

    def mostrar_carteira(self, dados_jogador, arquivo_save):
        """Mostra a carteira de Bitcoin e Mercado Negro"""
        while True:
            self._limpar_tela()
            
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.AMARELO}╔══════════════════════════════════════╗")
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.AMARELO}║        CARTEIRA & MERCADO            ║")
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.AMARELO}╚══════════════════════════════════════╝{C.RESET}\n")
            
            btc = dados_jogador.get('bitcoin_wallet', 0.005)
            # Valor fictício do BTC para imersão
            valor_usd = btc * 45000  
            
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.CIANO}Saldo: {C.VERDE}{btc:.6f} BTC")
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.CIANO}Valor est.: {C.VERDE}US$ {valor_usd:.2f}{C.RESET}")
            
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.CINZA}{'─' * 36}{C.RESET}")
            
            # Opções
            print(f"\n{' ' * ((self.term_width - 35) // 2)}{C.BRANCO}[1] {C.CINZA}Transferir Bitcoin")
            print(f"{' ' * ((self.term_width - 35) // 2)}{C.BRANCO}[2] {C.ROXO}ACESSAR MERCADO NEGRO (Darknet)")
            print(f"{' ' * ((self.term_width - 35) // 2)}{C.BRANCO}[3] {C.CINZA}Ver Histórico")
            print(f"{' ' * ((self.term_width - 35) // 2)}{C.BRANCO}[0] {C.CINZA}Voltar{C.RESET}")
            
            try:
                escolha = input(f"\n{' ' * ((self.term_width - 20) // 2)}{C.BRANCO}> {C.RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                break
            
            if escolha == "1":
                self.transferir_bitcoin(dados_jogador, arquivo_save)
            elif escolha == "2":
                self.mercado_negro(dados_jogador, arquivo_save)
            elif escolha == "3":
                self.ver_historico(dados_jogador)
            elif escolha == "0":
                break

    def mercado_negro(self, dados_jogador, arquivo_save):
        """Implementação do Mercado Negro"""
        # Itens disponíveis
        itens = [
            {"id": "vpn_plus", "nome": "VPN Duplo Hop (Privacidade +10)", "custo": 0.002},
            {"id": "brute_force", "nome": "Script BruteForce v2.0", "custo": 0.005},
            {"id": "proxies", "nome": "Lista de Proxies Elite", "custo": 0.003},
            {"id": "exploit_db", "nome": "Acesso ExploitDB Premium", "custo": 0.010}
        ]
        
        while True:
            self._limpar_tela()
            print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.ROXO}╔══════════════════════════════════════╗")
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.ROXO}║         DARKNET MARKETPLACE          ║")
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.ROXO}╚══════════════════════════════════════╝{C.RESET}\n")
            
            print(f"{' ' * ((self.term_width - 40) // 2)}{C.CIANO}Seu Saldo: {C.VERDE}{dados_jogador.get('bitcoin_wallet', 0):.6f} BTC{C.RESET}\n")
            
            print(f"{' ' * ((self.term_width - 50) // 2)}{C.CINZA}ITENS DISPONÍVEIS:{C.RESET}")
            
            for i, item in enumerate(itens, 1):
                # Verificar se já possui
                possuido = item['id'] in dados_jogador.get('inventory', [])
                status_str = f"{C.VERDE}[COMPRADO]" if possuido else f"{C.AMARELO}{item['custo']:.4f} BTC"
                cor_item = C.CINZA if possuido else C.BRANCO
                
                espacamento = " " * ((self.term_width - 60) // 2)
                print(f"{espacamento}{cor_item}[{i}] {item['nome']:<30} {status_str}{C.RESET}")
                
            print(f"\n{' ' * ((self.term_width - 35) // 2)}{C.BRANCO}[0] {C.CINZA}Voltar{C.RESET}")
            
            try:
                escolha = input(f"\n{' ' * ((self.term_width - 20) // 2)}{C.BRANCO}COMPRAR > {C.RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                break
            
            if escolha == "0":
                break
            
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(itens):
                    item = itens[idx]
                    
                    # Verificar se já tem
                    if item['id'] in dados_jogador.get('inventory', []):
                        self._mostrar_erro("Você já possui este item!")
                        continue
                        
                    # Verificar saldo
                    saldo = dados_jogador.get('bitcoin_wallet', 0)
                    if saldo >= item['custo']:
                        # Comprar
                        print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.AMARELO}Processando transação na Blockchain...{C.RESET}")
                        time.sleep(1.5)
                        
                        dados_jogador['bitcoin_wallet'] = saldo - item['custo']
                        dados_jogador.setdefault('inventory', []).append(item['id'])
                        
                        # Efeito se for item de privacidade
                        if "Privacidade" in item['nome']:
                            dados_jogador['privacy_level'] = min(100, dados_jogador.get('privacy_level', 50) + 10)
                            
                        # Salvar através do menu principal
                        if hasattr(self.menu, '_salvar_jogo'):
                            self.menu._salvar_jogo(dados_jogador, arquivo_save)
                        
                        print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.VERDE}COMPRA REALIZADA COM SUCESSO!{C.RESET}")
                        time.sleep(1)
                    else:
                        self._mostrar_erro("Saldo insuficiente!")
                else:
                    pass
            except ValueError:
                pass

    def transferir_bitcoin(self, dados_jogador, arquivo_save):
        """Simula transferência de Bitcoin"""
        print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.VERDE}Funcionalidade em desenvolvimento...{C.RESET}")
        time.sleep(1.5)
    
    def ver_historico(self, dados_jogador):
        """Mostra histórico de transações"""
        print(f"\n{' ' * ((self.term_width - 40) // 2)}{C.VERDE}Histórico de transações:{C.RESET}")
        print(f"{' ' * ((self.term_width - 50) // 2)}{C.CINZA}Nenhuma transação encontrada.{C.RESET}")
        input(f"\n{' ' * ((self.term_width - 25) // 2)}{C.CINZA}[ENTER PARA VOLTAR]{C.RESET}")
