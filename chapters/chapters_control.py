#!/usr/bin/env python3
"""
CHAPTERS_CONTROL.PY
Controlador central para o progresso dos capítulos.
Gerencia a transição, salvamento e estado dos capítulos.
"""

class ChapterController:
    def __init__(self):
        self.max_chapters = 14

    def processar_resultado(self, dados_jogador, resultado_capitulo):
        """
        Processa o resultado retornado por um capítulo e atualiza os dados do jogador.
        
        Args:
            dados_jogador (dict): Dados atuais do jogador.
            resultado_capitulo (dict): Dados retornados pelo capítulo (iniciar()).
            
        Returns:
            dict: Dados do jogador atualizados.
        """
        if not resultado_capitulo:
            return dados_jogador

        # Atualiza dados básicos (inventário, score, etc)
        # Preservamos os dados do jogador antes de mesclar o resultado do capítulo.
        dados_atualizados = dados_jogador.copy()
        dados_atualizados.update(resultado_capitulo)

        # Lógica de Controle de Capítulo
        capitulo_atual = dados_jogador.get('current_chapter', 1)

        saindo_menu = dados_atualizados.get('saindo_para_menu', False)
        completo = dados_atualizados.get('completed', False)

        # Se saiu para o menu, NÃO avança. Mantém o capítulo atual.
        if saindo_menu:
            dados_atualizados['current_chapter'] = capitulo_atual
            # Não adiciona aos completados se saiu antes
            return dados_atualizados

        # Se completou com sucesso
        if completo:
            # Adiciona à lista de completados se não estiver lá
            completed_list = dados_jogador.get('completed_chapters', [])
            if capitulo_atual not in completed_list:
                completed_list.append(capitulo_atual)
                completed_list.sort()  # Manter organizado
            
            dados_atualizados['completed_chapters'] = completed_list
            
            # ERRO CORRIGIDO: Código duplicado removido
            # Avança para o próximo capítulo (se houver)
            if capitulo_atual < self.max_chapters:
                dados_atualizados['current_chapter'] = capitulo_atual + 1
            else:
                # Fim do jogo ou limite alcançado
                dados_atualizados['current_chapter'] = capitulo_atual
        else:
            # Se não completou e não saiu pro menu (Game Over ou falha crítica)
            # Mantém no mesmo capítulo para tentar de novo
            dados_atualizados['current_chapter'] = capitulo_atual

        return dados_atualizados

    def verificar_conclusao_capitulo(self, numero_capitulo, dados_jogador):
        """
        Verifica se um capítulo específico foi concluído com sucesso.
        
        Args:
            numero_capitulo (int): Número do capítulo a verificar.
            dados_jogador (dict): Dados atuais do jogador.
            
        Returns:
            bool: True se o capítulo foi concluído com sucesso.
        """
        completed_chapters = dados_jogador.get('completed_chapters', [])
        return numero_capitulo in completed_chapters

    def verificar_missoes_capitulo(self, numero_capitulo, dados_jogador):
        """
        Verifica o status detalhado das missões de um capítulo específico.
        
        Args:
            numero_capitulo (int): Número do capítulo.
            dados_jogador (dict): Dados do jogador.
            
        Returns:
            dict: Status detalhado das missões do capítulo.
        """
        status_base = {
            'capitulo_completo': self.verificar_conclusao_capitulo(numero_capitulo, dados_jogador),
            'missoes': {},
            'progresso': 0.0,
            'total_missoes': 0
        }
        
        # Verificações específicas por capítulo
        if numero_capitulo == 1:
            return self._verificar_missoes_capitulo_01(dados_jogador, status_base)
        elif numero_capitulo == 2:
            return self._verificar_missoes_capitulo_02(dados_jogador, status_base)
        elif numero_capitulo == 3:
            return self._verificar_missoes_capitulo_03(dados_jogador, status_base)
        elif numero_capitulo == 4:
            return self._verificar_missoes_capitulo_04(dados_jogador, status_base)
        elif numero_capitulo == 5:
            return self._verificar_missoes_capitulo_05(dados_jogador, status_base)
        elif numero_capitulo == 6:
            return self._verificar_missoes_capitulo_06(dados_jogador, status_base)
        elif numero_capitulo == 7:
            return self._verificar_missoes_capitulo_07(dados_jogador, status_base)
        elif numero_capitulo == 8:
            return self._verificar_missoes_capitulo_08(dados_jogador, status_base)
        elif numero_capitulo == 9:
            return self._verificar_missoes_capitulo_09(dados_jogador, status_base)
        elif numero_capitulo == 10:
            return self._verificar_missoes_capitulo_10(dados_jogador, status_base)
        elif numero_capitulo == 11:
            return self._verificar_missoes_capitulo_11(dados_jogador, status_base)
        elif numero_capitulo == 12:
            return self._verificar_missoes_capitulo_12(dados_jogador, status_base)
        elif numero_capitulo == 13:
            return self._verificar_missoes_capitulo_13(dados_jogador, status_base)
        elif numero_capitulo == 14:
            return self._verificar_missoes_capitulo_14(dados_jogador, status_base)
        else:
            # Para capítulos não implementados ainda
            return status_base

    def _verificar_missoes_capitulo_01(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 1: Protocolo da Traição"""
        missoes = {
            'conexao_ssh': dados_jogador.get('capitulo_1_conexao_ssh', False),
            'navegacao_private': dados_jogador.get('capitulo_1_navegacao_private', False), 
            'listagem_arquivos': dados_jogador.get('capitulo_1_listagem_arquivos', False),
            'decisao_critica': dados_jogador.get('capitulo_1_decisao_critica', False),
            'operacao_final': dados_jogador.get('capitulo_1_operacao_sucesso', False)
        }
        
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        
        # Verificação adicional: se o capítulo está marcado como completo
        if dados_jogador.get('capitulo_1_operacao_sucesso', False):
            status_base['capitulo_completo'] = True
            
        return status_base

    def _verificar_missoes_capitulo_02(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 2"""
        # Implementar quando o capítulo 2 for criado
        missoes = {
            'missao_1': False,  # Placeholder
            'missao_2': False,  # Placeholder
        }
        
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        
        return status_base

    def _verificar_missoes_capitulo_03(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 3"""
        # Implementar quando o capítulo 3 for criado
        missoes = {
            'missao_1': False,  # Placeholder
            'missao_2': False,  # Placeholder
        }
        
        status_base['missoes'] = missoes
        # ERRO CORRIGIDO: Removido 'if missoes' desnecessário (missoes sempre existe)
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        
        return status_base

    def _verificar_missoes_capitulo_04(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 4"""
        # Implementar quando o capítulo 4 for criado
        missoes = {
            'missao_1': False,  # Placeholder
            'missao_2': False,  # Placeholder
        }
        
        status_base['missoes'] = missoes
        # ERRO CORRIGIDO: Removido 'if missoes' desnecessário (missoes sempre existe)
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        
        return status_base

    def debug_status_capitulos(self, dados_jogador):
        """
        Função de debug para mostrar o status de todos os capítulos.
        
        Args:
            dados_jogador (dict): Dados do jogador.
            
        Returns:
            str: Relatório de debug formatado.
        """
        relatorio = []
        relatorio.append("=== DEBUG STATUS DOS CAPÍTULOS ===")
        relatorio.append(f"Capítulo Atual: {dados_jogador.get('current_chapter', 1)}")
        relatorio.append(f"Capítulos Completados: {dados_jogador.get('completed_chapters', [])}")
        relatorio.append("")
        
        for cap in range(1, 5):  # Verificar primeiros 4 capítulos
            status = self.verificar_missoes_capitulo(cap, dados_jogador)
            relatorio.append(f"Capítulo {cap}: {'✓ COMPLETO' if status['capitulo_completo'] else '✗ INCOMPLETO'}")
            relatorio.append(f"  Progresso: {status['progresso']:.1%} ({sum(status['missoes'].values())}/{status['total_missoes']} missões)")
            
            if status['missoes']:
                for missao, completa in status['missoes'].items():
                    relatorio.append(f"    {missao}: {'✓' if completa else '✗'}")
            relatorio.append("")
        
        return "\n".join(relatorio)

    def _verificar_missoes_capitulo_05(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 5: Investigação Digital"""
        missoes = dados_jogador.get('missoes_capitulo_5', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_5_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_06(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 6: Networking Underground"""
        missoes = dados_jogador.get('missoes_capitulo_6', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_6_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_07(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 7: Inteligência Social"""
        missoes = dados_jogador.get('missoes_capitulo_7', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_7_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_08(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 8: Revelações"""
        missoes = dados_jogador.get('missoes_capitulo_8', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_8_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_09(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 9: Infiltração Governamental"""
        missoes = dados_jogador.get('missoes_capitulo_9', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_9_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_10(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 10: A Caçada"""
        missoes = dados_jogador.get('missoes_capitulo_10', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_10_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_11(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 11: Alianças Perigosas"""
        missoes = dados_jogador.get('missoes_capitulo_11', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_11_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_12(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 12: O Confronto Final"""
        missoes = dados_jogador.get('missoes_capitulo_12', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_12_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_13(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 13: Justiça ou Vingança"""
        missoes = dados_jogador.get('missoes_capitulo_13', {})
        status_base['missoes'] = missoes
        status_base['total_missoes'] = len(missoes)
        status_base['progresso'] = sum(missoes.values()) / len(missoes) if missoes else 0.0
        status_base['capitulo_completo'] = dados_jogador.get('capitulo_13_operacao_sucesso', False)
        return status_base

    def _verificar_missoes_capitulo_14(self, dados_jogador, status_base):
        """Verifica missões específicas do Capítulo 14: O Novo Amanhecer"""
        status_base['capitulo_completo'] = dados_jogador.get('jogo_concluido', False)
        status_base['missoes'] = {'jogo_concluido': status_base['capitulo_completo']}
        status_base['total_missoes'] = 1
        status_base['progresso'] = 1.0 if status_base['capitulo_completo'] else 0.0
        return status_base