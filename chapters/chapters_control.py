#!/usr/bin/env python3
"""
CHAPTERS_CONTROL.PY
Controlador central para o progresso dos capítulos.
Gerencia a transição, salvamento e estado dos capítulos.
"""

class ChapterController:
    def __init__(self):
        self.max_chapters = 50

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
        # Preservamos o que veio do capítulo, exceto a lógica de 'current_chapter' que será decidida aqui
        dados_atualizados = resultado_capitulo.copy()
        
        # Lógica de Controle de Capítulo
        capitulo_atual = dados_jogador.get('current_chapter', 1)
        
        saindo_menu = resultado_capitulo.get('saindo_para_menu', False)
        completo = resultado_capitulo.get('completed', False)

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
                completed_list.sort() # Manter organizado
            
            dados_atualizados['completed_chapters'] = completed_list
            
            # Avança para o próximo capítulo (se houver)
            if capitulo_atual < self.max_chapters:
                dados_atualizados['current_chapter'] = capitulo_atual + 1
            else:
                # Fim do jogo ou limite alcançado
                pass
        else:
            # Se não completou e não saiu pro menu (Game Over ou falha crítica)
            # Mantém no mesmo capítulo para tentar de novo
            dados_atualizados['current_chapter'] = capitulo_atual

        return dados_atualizados
