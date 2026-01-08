#!/usr/bin/env python3
"""
CHAPTER_02.PY - "O Vazio entre os Bits"
Três semanas após os eventos do Capítulo 1.
O apartamento está um caos. Garrafas vazias, tela do laptop a única luz.

Foco: Autoaprendizado, Criptografia, Esteganografia
Habilidade: zip2john, steghide
"""

import os
import sys
import time
import random
import json
import shutil
from datetime import datetime
from pathlib import Path

# Tentativa de importar utils
try:
    from utils.terminal_kali import C, digitar, fim_digitar, limpa_tela
except ImportError:
    # Fallback
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
        KALI_AZUL = '\033[34m'
        
    def digitar(texto, delay=0.03, cor=C.BRANCO, fim="\n"):
        print(f"{cor}{texto}{C.RESET}", end=fim)
        time.sleep(len(texto) * delay)

    def limpa_tela():
        os.system('cls' if os.name == 'nt' else 'clear')


# ========== ESTADO DO JOGO ==========

class GameStateChapter2:
    def __init__(self, dados_anteriores):
        self.player_name = dados_anteriores.get('player_name', 'Neo')
        self.codinome = dados_anteriores.get('codiname', 'SHADOW_00')
        self.privacy_level = dados_anteriores.get('privacy_level', 80)
        self.reputation = dados_anteriores.get('reputation', 0)
        self.score = dados_anteriores.get('score', 0)
        self.inventory = dados_anteriores.get('inventory', [])
        
        # Histórico do Cap 1
        self.cap1_resultado = dados_anteriores.get('capitulo_1_resultado', 'exfiltrar') # exfiltrar ou destruir
        
        # Estado local
        self.erros = 0
        self.game_over = False
        self.saindo_para_menu = False # Flag para voltar ao menu

    def registrar_falha(self, penalidade=10):
        self.erros += 1
        self.privacy_level = max(0, self.privacy_level - penalidade)

    def registrar_sucesso(self, pontos):
        self.score += pontos
        self.reputation += 2

    def to_dict(self):
        # Retorna dados atualizados para o main loop
            'capitulo_1_resultado': self.capit1_resultado,
            'last_seen': datetime.now().isoformat(),
            'saindo_para_menu': self.saindo_para_menu,
            'completed': getattr(self, 'capitulo_concluido', True) # Assumindo true se chegou aqui sem sair
        }

# ========== FERRAMENTAS SIMULADAS ==========

def prompt_kali(codinome):
    return f"{C.KALI_AZUL}┌──({C.VERDE}{codinome}{C.KALI_AZUL}㉿kali)-[{C.BRANCO}~/learning/crypto{C.KALI_AZUL}]\n└─{C.ROXO}#{C.RESET} "

def header_kali_v2(titulo="CAPÍTULO 2: O VAZIO ENTRE OS BITS"):
    """Cabeçalho padronizado"""
    limpa_tela()
    largura = 100
    try:
        largura = shutil.get_terminal_size().columns
    except:
        pass
    
    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print(f"{C.CIANO}{C.NEGRITO}{f'[{titulo}]':^{largura}}{C.RESET}")
    print(f"{C.CINZA}{'Brasília - Asa Norte | Apartamento Provisório':^{largura}}{C.RESET}")
    print(f"{C.VERDE}{'═' * largura}{C.RESET}")
    print()
    print(f"{C.AMARELO}💡 DICA: Digite {C.RESET}{C.VERMELHO}'menu'{C.RESET}{C.AMARELO} para retornar ao menu do jogo a qualquer momento.{C.RESET}")
    print(f"{C.AMARELO}📖 Acesse{C.RESET}{C.VERMELHO}'manual'{C.RESET}{C.AMARELO}para consultar o Manual de Hacking durante o jogo.{C.RESET}")
    print(f"{C.VERDE}{'═' * largura}{C.RESET}\n")

def check_comandos_globais(cmd, state, arquivo_save):
    """Verifica comandos globais como 'menu' e 'manual'"""
    if cmd.lower() == 'menu':
        print(f"\n{C.AMARELO}[*] Salvando checkpoint e retornando ao menu...{C.RESET}")
        state.saindo_para_menu = True
        return "MENU"
        
    if cmd.lower() in ['manual', 'help', '?']:
        try:
            from manual_hacking import exibir_banner
            # Importar dinamicamente para evitar problemas circulares ou de path
            exibir_banner()
        except ImportError:
             print(f"{C.CINZA}Manual não disponível neste contexto.{C.RESET}")
        return "MANUAL"
    
    return None

def pensamento(texto):
    """Exibe um pensamento do personagem (texto azul/ciano com itálico se possível)"""
    print(f"\n{C.CIANO}{C.NEGRITO}>> {texto}{C.RESET}")
    time.sleep(1.5)

def narracao(texto, delay=0.04):
    """Exibe texto narrativo"""
    digitar(texto, delay=delay, cor=C.BRANCO)
    time.sleep(0.5)

def drama_pause(segundos=1):
    time.sleep(segundos)

# ========== SIMULAÇÕES TÉCNICAS ==========

def simular_john(target):
    print(f"\n{C.CINZA}[*] Iniciando John The Ripper jumbo-1...{C.RESET}")
    time.sleep(1)
    print(f"{C.CINZA}[*] Loaded 1 password hash ({target}){C.RESET}")
    print(f"{C.CINZA}[*] Will run 8 OpenMP threads{C.RESET}")
    time.sleep(2)
    
    print(f"\n{C.AMARELO}Proceeding with wordlist: /usr/share/wordlists/rockyou.txt{C.RESET}")
    chars = ["|", "/", "-", "\\"]
    for i in range(20):
        sys.stdout.write(f"\r{C.BRANCO}Cracking... {chars[i % 4]} {i*5}%{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.2)
    
    senha = "nobile123"
    print(f"\n\n{C.VERDE}[+] Session completed. Password found: {C.NEGRITO}{senha}{C.RESET}")
    return senha

def simular_steghide_extract(arquivo, senha):
    print(f"\n{C.CINZA}[*] Tentando extrair dados de {arquivo}...{C.RESET}")
    time.sleep(1)
    
    if senha == "rex":
        print(f"{C.VERDE}[+] Wrote extracted data to 'backup_link.txt'.{C.RESET}")
        return True
    else:
        print(f"{C.VERMELHO}steghide: could not extract any data with that passphrase!{C.RESET}")
        return False

# ========== CENAS ==========

def cena_abertura(state):
    header_kali_v2()
    print("\n" * 2)
    drama_pause(1)
    
    digitar(f"{C.CINZA}Três semanas.{C.RESET}", delay=0.1)
    drama_pause(1)
    digitar(f"{C.CINZA}Vinte e um dias desde que saí daquele apartamento.{C.RESET}", delay=0.06)
    drama_pause(1)
    
    header_kali_v2()
    drama_pause(2)
    
    narracao("O quarto cheira a pizza velha e energéticos quentes.")
    narracao("A luz do sol tenta entrar pela persiana quebrada, mas a única iluminação real vem dos monitores.")
    drama_pause(1)
    
    pensamento("Eu não durmo direito há dias. Toda vez que fecho os olhos, vejo o rosto dela.")
    pensamento("Ela mentiu. Olhando nos meus olhos, ela mentiu.")
    drama_pause(1)
    
    narracao("Você olha para as suas mãos. Elas tremem levemente sobre o teclado mecânico.")
    narracao("Mas quando você digita... o tremor para.")
    drama_pause(1)
    
    pensamento("O código não mente. O código é lógico. Se há um erro, é sintaxe. É corrigível.")
    pensamento("Vida real não tem compilador. Vida real é... quebrada.") 
    
    drama_pause(2)

def rota_exfiltracao(state, arquivo_save):
    """Rota para quem salvou os dados (Final exfiltrar)"""
    narracao("\nNo seu Desktop, o arquivo criptografado brilha como um troféu maldito.")
    print(f"\n{C.VERMELHO}📄 fotos_reserva_dupla.zip{C.RESET}")
    drama_pause(1)
    
    pensamento("Eu tenho as provas. Eu sei que tenho. Mas a senha...")
    pensamento("Eu tentei datas, nomes... nada. Preciso pensar como um hacker. Não como o namorado traído.")
    
    narracao("Você abre o terminal. O cursor piscando é a única coisa que faz sentido agora.")
    
    print(f"\n{C.AMARELO}MISSÃO: Quebrar a criptografia do arquivo ZIP.{C.RESET}")
    print(f"{C.CINZA}DICA: Use 'zip2john' para extrair o hash da senha, depois use 'john' para quebrá-la.{C.RESET}\n")
    
    # Parte 1: zip2john
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return False

        # Check global commands
        status_global = check_comandos_globais(cmd, state, arquivo_save)
        if status_global == "MENU": return False
        if status_global == "MANUAL": continue
        
        if cmd == "ls":
            print("fotos_reserva_dupla.zip   wordlist.txt")
        elif "zip2john" in cmd and "fotos_reserva_dupla.zip" in cmd:
            if ">" in cmd:
                print(f"{C.VERDE}[+] Hash extraído com sucesso!{C.RESET}")
                break
            else:
                print(f"{C.AMARELO}Dica: Redirecione a saída para um arquivo (ex: > hash.txt){C.RESET}")
        else:
            print(f"{C.VERMELHO}Comando não reconhecido ou incorreto para esta etapa.{C.RESET}")
            state.registrar_falha(2)

    pensamento("O hash... a impressão digital da senha. Agora é força bruta.")
    pensamento("Não importa o quão complexa seja a mentira, a verdade é apenas uma sequência de caracteres.")
    
    # Parte 2: John
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return False
            
        status_global = check_comandos_globais(cmd, state, arquivo_save)
        if status_global == "MENU": return False
        if status_global == "MANUAL": continue
        
        if cmd.startswith("john"):
            simular_john("zip")
            break
        else:
            print(f"{C.VERMELHO}Use o comando 'john' seguido do arquivo de hash.{C.RESET}")
            state.registrar_falha(2)

    drama_pause(1)
    narracao("\n'nobile123'.")
    drama_pause(1)
    pensamento("O nome do hotel. Sério? Ela nem tentou esconder. A arrogância dela...")
    
    narracao("Você descompacta o arquivo. As fotos aparecem na tela.")
    narracao("São inegáveis. Datas, horários, rostos.")
    
    drama_pause(2)
    pensamento("Eu deveria sentir vitória. Mas só sinto... vazio.")
    pensamento("Mas espere... o que é isso no metadado da terceira foto?")
    
    digitar(f"\n{C.VERDE}>> Nova habilidade desbloqueada: CRIPTOGRAFIA AVANÇADA <<{C.RESET}", delay=0.05)
    return True

def rota_destruicao(state, arquivo_save):
    """Rota para quem destruiu os dados (Final destruir)"""
    narracao("\nVocê olha para a tela vazia. Você apagou tudo naquela noite.")
    narracao("O medo te dominou. Você destruiu as evidências para salvar a relação.")
    drama_pause(1)
    
    pensamento("E adivinhe? Não adiantou nada. Ela foi embora dois dias depois.")
    pensamento("Agora eu não tenho a garota, e não tenho as provas.")
    pensamento("Sou um covarde. Um idiota.")
    
    drama_pause(2)
    narracao("Mas a obsessão não dorme. Você passou os últimos dias vasculhando a vida digital dela (o que restou).")
    narracao("Você encontrou uma foto antiga no perfil social público dela. Uma foto 'inocente' do cachorro, Rex.")
    
    print(f"\n{C.CIANO}🖼️ perfil_social.jpg{C.RESET}")
    drama_pause(1)
    
    pensamento("Há algo estranho nessa imagem. O tamanho do arquivo... é grande demais para um JPEG comprimido.")
    pensamento("Esteganografia. Esconder dados à vista de todos.")
    
    print(f"\n{C.AMARELO}MISSÃO: Extrair dados ocultos da imagem.{C.RESET}")
    print(f"{C.CINZA}DICA: Use 'steghide info' para verificar e 'steghide extract' para extrair.{C.RESET}\n")

    # Parte 1: Info
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return False
            
        status_global = check_comandos_globais(cmd, state, arquivo_save)
        if status_global == "MENU": return False
        if status_global == "MANUAL": continue
        
        if "steghide info" in cmd and "perfil_social.jpg" in cmd:
            print(f"{C.CINZA}[*] Probing 'perfil_social.jpg'...{C.RESET}")
            time.sleep(1)
            print(f"{C.VERDE}[+] Found embedded data: 'backup_link.txt'{C.RESET}")
            break
        elif cmd == "ls":
            print("perfil_social.jpg")
        else:
            print(f"{C.VERMELHO}Verifique o arquivo com 'steghide info'.{C.RESET}")

    pensamento("Eu sabia. Ela sempre foi paranoica com backups. Onde há fumaça digital...")
    pensamento("Preciso de uma senha. Algo que ela nunca esqueceria. O nome daquele maldito cachorro.")

    # Parte 2: Extract
    while True:
        try:
            cmd = input(prompt_kali(state.codinome)).strip()
        except (KeyboardInterrupt, EOFError):
            state.saindo_para_menu = True
            return False
            
        status_global = check_comandos_globais(cmd, state, arquivo_save)
        if status_global == "MENU": return False
        if status_global == "MANUAL": continue
        
        if "steghide extract" in cmd:
            senha = input(f"{C.AMARELO}Enter passphrase: {C.RESET}")
            if simular_steghide_extract("perfil_social.jpg", senha):
                break
            else:
                state.registrar_falha(3)
        else:
            print(f"{C.VERMELHO}Use 'steghide extract -sf perfil_social.jpg'.{C.RESET}")
            
    drama_pause(1)
    narracao("\nUm arquivo de texto se extrai das entranhas digitais da imagem.")
    print(f"\n{C.BRANCO}CONTENT: cloud-backup.secure/recover?id=juliana_reserva_nobile{C.RESET}")
    
    drama_pause(2)
    pensamento("Um link de recuperação. Eu não perdi tudo.")
    pensamento("Ainda posso provar quem ela é.")
    
    digitar(f"\n{C.VERDE}>> Nova habilidade desbloqueada: ESTEGANOGRAFIA <<{C.RESET}", delay=0.05)
    return True

def cena_final(state):
    drama_pause(2)
    header_kali_v2()
    
    narracao("A adrenalina corre nas suas veias. Pela primeira vez em semanas, você não sente dor.")
    narracao("Você sente... poder.")
    
    pensamento("Eles acham que deletar é o fim. Que criptografar é seguro.")
    pensamento("Eles não entendem. Nada nunca é realmente deletado.")
    
    drama_pause(1)
    digitar(f"\n{C.CINZA}* Notificação no navegador *{C.RESET}")
    print(f"{C.ROXO}[Fórum Underground] Nova mensagem privada de: V0id_Walker{C.RESET}")
    
    drama_pause(2)
    pensamento("Quem é V0id_Walker? Como ele me achou nesse fórum?")
    
    digitar(f"\n{C.BRANCO}Mensagem: 'Vimos o que você fez com o servidor Nobile. Impressionante para um amador.'{C.RESET}", delay=0.05)
    drama_pause(1)
    digitar(f"{C.BRANCO}Mensagem: 'Temos um objetivo em comum. Procure por fsociety.br'{C.RESET}", delay=0.05)
    
    drama_pause(2)
    pensamento("Isso não é mais sobre a Juliana.")
    pensamento("Isso acabou de se tornar algo muito maior.")
    
    digitar(f"\n{C.VERDE}CAPÍTULO 2 CONCLUÍDO.{C.RESET}")
    state.registrar_sucesso(100)
    time.sleep(3)


# ========== MAIN ==========

def iniciar(dados_jogador, arquivo_save=None):
    # Inicializa estado
    state = GameStateChapter2(dados_jogador)
    
    try:
        cena_abertura(state)
        
        resultado = False
        if state.cap1_resultado == "exfiltrar":
            resultado = rota_exfiltracao(state, arquivo_save)
        else:
            resultado = rota_destruicao(state, arquivo_save)
            
        if state.saindo_para_menu:
            return state.to_dict()

        if resultado:
            cena_final(state)
            return state.to_dict()
            
    except KeyboardInterrupt:
        print(f"\n{C.VERMELHO}JOGO INTERROMPIDO.{C.RESET}")
        return None

if __name__ == "__main__":
    # Teste rápido
    dados = {'player_name': 'Tester', 'capitulo_1_resultado': 'exfiltrar'}
    iniciar(dados)
