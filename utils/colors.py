#!/usr/bin/env python3
"""Paleta de cores compartilhada para o projeto"""

class CoresKali:
    """Classe de cores para terminal Kali Linux"""

    # Cores principais do Kali
    KALI_AZUL = '\033[38;5;39m'
    KALI_ROXO = '\033[38;5;135m'
    KALI_VERDE = '\033[38;5;82m'
    KALI_VERMELHO = '\033[38;5;196m'
    KALI_AMARELO = '\033[38;5;226m'
    KALI_CIANO = '\033[38;5;51m'
    KALI_BRANCO = '\033[38;5;255m'
    KALI_CINZA = '\033[38;5;244m'

    # Cores padrão ANSI (fallback)
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    CINZA = '\033[90m'
    ROXO = '\033[95m'
    MAGENTA = '\033[35m'

    # Estilos
    RESET = '\033[0m'
    NEGRITO = '\033[1m'
    ITALICO = '\033[3m'
    SUBLINHADO = '\033[4m'
    INVERTIDO = '\033[7m'

    # Efeitos especiais
    PISCANDO = '\033[5m'
    RAPIDO = '\033[6m'


# Instância exportada para conveniência
C = CoresKali()

# Alias para compatibilidade com código existente
Cores = CoresKali
