#!/usr/bin/env python3
"""
AUDITORIA_ROOT_EVOLUTION.py - Sistema de Testes e Logs Completo
Versão melhorada: Melhor organização, tratamento de erros e novas funcionalidades
"""

import os
import sys
import time
import json
import shutil
import logging
import traceback
import tempfile
import subprocess
import threading
import concurrent.futures
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Callable
from enum import Enum
import io
from contextlib import redirect_stdout, redirect_stderr

# Configurar logging global
LOG_DIR = Path(__file__).parent / "logs_auditoria"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILENAME = f"auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG_FILE = LOG_DIR / LOG_FILENAME

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

class ColorFormatter(logging.Formatter):
    """Formatação colorida para logs no console"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Ciano
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Amarelo
        'ERROR': '\033[31m',     # Vermelho
        'CRITICAL': '\033[41m',  # Vermelho com fundo
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['INFO'])
        message = super().format(record)
        return f"{log_color}{message}{self.COLORS['RESET']}"

def setup_logging():
    """Configura sistema de logging avançado"""
    logger = logging.getLogger('AuditoriaRoot')
    logger.setLevel(logging.DEBUG)
    
    # Remover handlers existentes
    logger.handlers.clear()
    
    # Handler para arquivo com rotação
    file_handler = logging.FileHandler(
        LOG_FILE, 
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Formato detalhado para arquivo
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Handler para console com cores
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = ColorFormatter(
        '%(asctime)s - %(levelname)-8s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Suprimir logs de bibliotecas externas
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logger

logger = setup_logging()

class TestResult:
    """Classe para armazenar resultados de testes"""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = time.time()
        self.end_time = None
        self.success = False
        self.error = None
        self.details = {}
        self.duration = 0.0
    
    def finish(self, success: bool, error: str = None, **details):
        """Finaliza o teste com resultados"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.success = success
        self.error = error
        self.details.update(details)
        return self
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'name': self.name,
            'success': self.success,
            'error': self.error,
            'duration': round(self.duration, 3),
            'details': self.details,
            'timestamp': datetime.fromtimestamp(self.start_time).isoformat()
        }

class FileValidator:
    """Validador de arquivos e diretórios"""
    
    REQUIRED_FILES = {
        'essential': [
            ('run.py', 1000, "Script principal"),
            ('intro_menu.py', 500, "Menu inicial"),
            ('game_state.py', 300, "Sistema de save/load"),
            ('manual_hacking.py', 500, "Manual completo"),
            ('main.py', 200, "Jogo principal"),
        ],
        'utils': [
            ('utils/terminal_kali.py', 50, "Sistema de cores"),
            ('utils/__init__.py', 0, "Pacote utils"),
        ],
        'chapters': [
            ('chapters/__init__.py', 10, "Pacote capítulos"),
            ('chapters/chapter_01.py', 100, "Capítulo 1"),
        ],
        'directories': [
            ('saves/', None, "Salvamentos"),
            ('utils/', None, "Utilitários"),
            ('chapters/', None, "Capítulos"),
        ]
    }
    
    @staticmethod
    def validate_python_syntax(filepath: str) -> Tuple[bool, str]:
        """Valida sintaxe Python de um arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, filepath, 'exec')
            return True, "Sintaxe válida"
        except SyntaxError as e:
            return False, f"Erro de sintaxe: {e}"
        except UnicodeDecodeError:
            # Tentar outras codificações
            for encoding in ['latin-1', 'cp1252', 'utf-16']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                    compile(content, filepath, 'exec')
                    return True, f"Sintaxe válida (encoding: {encoding})"
                except:
                    continue
            return False, "Erro de encoding - não foi possível ler o arquivo"
        except Exception as e:
            return False, f"Erro na validação: {e}"
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """Verifica dependências do sistema"""
        dependencies = {
            'python_version': sys.version_info >= (3, 7),
            'json_module': True,  # Incluído no Python
            'pathlib': True,      # Incluído no Python 3.4+
        }
        
        # Verificar módulos opcionais
        optional_deps = ['psutil', 'rich', 'colorama']
        for dep in optional_deps:
            try:
                __import__(dep)
                dependencies[dep] = True
            except ImportError:
                dependencies[dep] = False
        
        return dependencies

class Auditoria:
    """Classe principal de auditoria com logging detalhado"""
    
    def __init__(self):
        """Inicializa auditoria"""
        self.start_time = time.time()
        self.test_results: List[TestResult] = []
        self.problems: List[str] = []
        self.stats = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'warnings': 0
        }
        
        self.resultados = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'auditoria_version': '2.0.0',
                'log_file': str(LOG_FILE),
            },
            'system_info': self._capturar_info_sistema(),
            'test_results': {},
            'problems': [],
            'summary': self.stats
        }
        
        logger.info("=" * 80)
        logger.info("🔍 AUDITORIA ROOT EVOLUTION v2.0")
        logger.info("=" * 80)
        logger.info(f"📁 Log: {LOG_FILE}")
        logger.info(f"📊 Python: {sys.version}")
    
    def _capturar_info_sistema(self) -> Dict[str, Any]:
        """Captura informações detalhadas do sistema"""
        info = {
            'python': {
                'version': sys.version,
                'executable': sys.executable,
                'path': sys.path,
            },
            'system': {
                'platform': sys.platform,
                'cwd': os.getcwd(),
                'user': os.environ.get('USER', os.environ.get('USERNAME', 'Desconhecido')),
                'pid': os.getpid(),
            },
            'environment': {
                'encoding': sys.getdefaultencoding(),
                'filesystem_encoding': sys.getfilesystemencoding(),
            }
        }
        
        # Informações adicionais da plataforma
        try:
            import platform
            info['platform_details'] = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
            }
        except:
            info['platform_details'] = 'Não disponível'
        
        # Informações de diretório
        info['directories'] = {
            'script_dir': str(Path(__file__).parent),
            'home_dir': str(Path.home()),
            'temp_dir': tempfile.gettempdir(),
        }
        
        return info
    
    def log_sistema_info(self):
        """Loga informações do sistema formatadas"""
        logger.info("📊 INFORMAÇÕES DO SISTEMA:")
        logger.info("─" * 40)
        
        # Python info
        py_info = self.resultados['system_info']['python']
        logger.info(f"🐍 Python {py_info['version'].split()[0]}")
        logger.info(f"   Executável: {py_info['executable']}")
        
        # System info
        sys_info = self.resultados['system_info']['system']
        logger.info(f"💻 Sistema: {sys_info['platform']}")
        logger.info(f"   Usuário: {sys_info['user']}")
        logger.info(f"   PID: {sys_info['pid']}")
        logger.info(f"   Diretório: {sys_info['cwd']}")
        
        logger.info("")
    
    def _run_test(self, test_func: Callable, test_name: str, **kwargs) -> TestResult:
        """Executa um teste com tratamento de erros padronizado"""
        result = TestResult(test_name)
        self.stats['total'] += 1
        
        try:
            logger.info(f"▶️  Executando: {test_name}")
            logger.debug("─" * 40)
            
            test_result = test_func(**kwargs)
            
            if isinstance(test_result, TestResult):
                result = test_result
            elif isinstance(test_result, dict):
                if test_result.get('status') in ['sucesso', 'success', True]:
                    result.finish(True, **test_result)
                    self.stats['passed'] += 1
                    logger.info(f"✅ {test_name} - OK ({result.duration:.2f}s)")
                else:
                    error = test_result.get('error', 'Erro desconhecido')
                    result.finish(False, error, **test_result)
                    self.stats['failed'] += 1
                    logger.error(f"❌ {test_name} - FALHA: {error}")
            else:
                result.finish(True)
                self.stats['passed'] += 1
                logger.info(f"✅ {test_name} - OK ({result.duration:.2f}s)")
                
        except KeyboardInterrupt:
            result.finish(False, "Interrompido pelo usuário")
            self.stats['errors'] += 1
            logger.warning(f"⏸️  {test_name} - INTERROMPIDO")
            raise
            
        except Exception as e:
            result.finish(False, str(e), traceback=traceback.format_exc())
            self.stats['errors'] += 1
            logger.error(f"💥 {test_name} - ERRO: {e}")
            logger.debug(traceback.format_exc())
            
            if not isinstance(e, (ImportError, FileNotFoundError)):
                self.problems.append(f"{test_name}: {e}")
        
        self.test_results.append(result)
        return result
    
    def verificar_arquivos(self) -> TestResult:
        """Verifica se todos os arquivos necessários existem"""
        result = TestResult("Verificação de Arquivos")
        
        logger.info("📁 VERIFICAÇÃO DE ARQUIVOS:")
        logger.info("─" * 40)
        
        problems = []
        missing_files = []
        syntax_errors = []
        
        validator = FileValidator()
        
        # Verificar categorias
        for category, files in validator.REQUIRED_FILES.items():
            logger.info(f"\n📂 {category.upper()}:")
            
            for (path, min_size, description) in files:
                if path.endswith('/'):
                    # É diretório
                    if os.path.exists(path) and os.path.isdir(path):
                        logger.info(f"   ✅ {path:<30} {description}")
                    else:
                        logger.error(f"   ❌ {path:<30} {description} - DIRETÓRIO FALTANDO")
                        missing_files.append(path)
                else:
                    # É arquivo
                    if not os.path.exists(path):
                        logger.error(f"   ❌ {path:<30} {description} - ARQUIVO FALTANDO")
                        missing_files.append(path)
                        continue
                    
                    try:
                        size = os.path.getsize(path)
                        size_status = "OK"
                        
                        if min_size and size < min_size:
                            size_status = f"PEQUENO ({size} < {min_size})"
                            problems.append(f"{path}: Tamanho insuficiente")
                            logger.warning(f"   ⚠️  {path:<30} {size_status}")
                        else:
                            logger.info(f"   ✅ {path:<30} {size:>6} bytes")
                        
                        # Validar sintaxe para arquivos Python
                        if path.endswith('.py'):
                            syntax_ok, syntax_msg = validator.validate_python_syntax(path)
                            if syntax_ok:
                                logger.debug(f"      ✓ {syntax_msg}")
                            else:
                                logger.error(f"      ✗ {syntax_msg}")
                                syntax_errors.append(f"{path}: {syntax_msg}")
                                problems.append(f"{path}: Erro de sintaxe")
                    
                    except Exception as e:
                        logger.error(f"   ❌ {path} - ERRO: {e}")
                        problems.append(f"{path}: {e}")
        
        # Verificar dependências
        logger.info("\n🔧 DEPENDÊNCIAS:")
        deps = validator.check_dependencies()
        for dep, available in deps.items():
            status = "✅" if available else "❌"
            logger.info(f"   {status} {dep:<20} {'Disponível' if available else 'Faltando'}")
            if not available and dep not in ['psutil', 'rich', 'colorama']:
                problems.append(f"Dependência faltando: {dep}")
        
        # Resultado
        if not missing_files and not syntax_errors and not problems:
            result.finish(True, 
                         files_checked=sum(len(files) for files in validator.REQUIRED_FILES.values()),
                         dependencies_checked=len(deps))
            logger.info(f"\n🎉 Todos os arquivos verificados com sucesso!")
        else:
            result.finish(False, 
                         error="Problemas encontrados",
                         missing_files=missing_files,
                         syntax_errors=syntax_errors,
                         problems=problems,
                         files_checked=sum(len(files) for files in validator.REQUIRED_FILES.values()))
            logger.error(f"\n🚨 Problemas encontrados:")
            if missing_files:
                logger.error(f"   • Arquivos/diretórios faltando: {len(missing_files)}")
            if syntax_errors:
                logger.error(f"   • Erros de sintaxe: {len(syntax_errors)}")
            if problems:
                logger.error(f"   • Outros problemas: {len(problems)}")
        
        return result
    
    def testar_importacoes(self) -> TestResult:
        """Testa importação de todos os módulos"""
        result = TestResult("Teste de Importações")
        
        logger.info("\n📦 TESTE DE IMPORTAÇÕES:")
        logger.info("─" * 40)
        
        modulos = [
            ('game_state', 'Sistema de save/load'),
            ('manual_hacking', 'Manual de hacking'),
            ('intro_menu', 'Menu inicial'),
            ('utils.terminal_kali', 'Sistema de cores'),
            ('chapters.chapter_01', 'Capítulo 1'),
        ]
        
        resultados = {}
        import_errors = []
        
        for modulo_nome, descricao in modulos:
            try:
                inicio = time.time()
                modulo = __import__(modulo_nome)
                
                # Para módulos com ponto, importar completamente
                if '.' in modulo_nome:
                    parts = modulo_nome.split('.')
                    for part in parts[1:]:
                        modulo = getattr(modulo, part)
                
                tempo = time.time() - inicio
                
                status = '✅' if tempo < 0.5 else '⚠️'
                logger.info(f"{status} {modulo_nome:<25} {tempo:>6.3f}s - {descricao}")
                
                resultados[modulo_nome] = {
                    'status': 'sucesso',
                    'tempo': tempo,
                    'module': str(type(modulo))
                }
                
            except ImportError as e:
                logger.error(f"❌ {modulo_nome:<25} - ImportError: {e}")
                import_errors.append(f"{modulo_nome}: {e}")
                resultados[modulo_nome] = {
                    'status': 'erro',
                    'erro': str(e)
                }
                
            except Exception as e:
                logger.error(f"❌ {modulo_nome:<25} - Erro: {e}")
                import_errors.append(f"{modulo_nome}: {e}")
                resultados[modulo_nome] = {
                    'status': 'erro',
                    'erro': str(e)
                }
        
        if not import_errors:
            result.finish(True, 
                         modules_tested=len(modulos),
                         results=resultados)
            logger.info(f"\n✅ Todas importações bem sucedidas")
        else:
            result.finish(False,
                         error=f"{len(import_errors)} erros de importação",
                         import_errors=import_errors,
                         results=resultados)
            logger.error(f"\n🚨 {len(import_errors)} erro(s) de importação")
        
        return result
    
    def testar_game_state_basico(self) -> TestResult:
        """Testa funcionalidades básicas do GameState"""
        result = TestResult("Teste GameState")
        
        logger.info("\n🎮 TESTE GAMESTATE:")
        logger.info("─" * 40)
        
        test_dir = None
        resultados = {}
        
        try:
            # 1. Importar GameState
            from game_state import GameState
            
            # 2. Criar diretório temporário
            test_dir = tempfile.mkdtemp(prefix='audit_gamestate_')
            original_saves_dir = GameState.SAVES_DIR
            GameState.SAVES_DIR = os.path.join(test_dir, 'saves')
            os.makedirs(GameState.SAVES_DIR, exist_ok=True)
            
            logger.info(f"📁 Diretório de teste: {test_dir}")
            
            # 3. Testar criação
            logger.info("\n1. Testando criação...")
            estado = GameState("JogadorTeste", "AUDIT_01")
            logger.info(f"   ✅ Criado: {estado.codinome}")
            logger.info(f"      Nome: {estado.nome_jogador}")
            logger.info(f"      Capítulo: {estado.capitulo_atual}")
            resultados['criacao'] = {'sucesso': True, 'codinome': estado.codinome}
            
            # 4. Testar salvamento
            logger.info("\n2. Testando salvamento...")
            arquivo_save = estado.salvar()
            size = os.path.getsize(arquivo_save)
            logger.info(f"   ✅ Salvo: {os.path.basename(arquivo_save)} ({size} bytes)")
            resultados['salvamento'] = {'sucesso': True, 'arquivo': arquivo_save, 'tamanho': size}
            
            # 5. Testar carregamento
            logger.info("\n3. Testando carregamento...")
            estado_carregado = GameState.carregar(arquivo_save)
            logger.info(f"   ✅ Carregado: {estado_carregado.codinome}")
            
            # Verificar integridade
            integro = estado.codinome == estado_carregado.codinome
            resultados['carregamento'] = {
                'sucesso': True,
                'integro': integro,
                'codinome_original': estado.codinome,
                'codinome_carregado': estado_carregado.codinome
            }
            
            if integro:
                logger.info(f"      ✓ Integridade verificada")
            else:
                logger.error(f"      ✗ Problema de integridade")
            
            # 6. Testar atualizações
            logger.info("\n4. Testando atualizações...")
            estado.atualizar_progresso(2)
            estado.adicionar_bitcoin(0.5)
            estado.atualizar_anonimato(-10)
            logger.info(f"   ✅ Atualizações aplicadas")
            logger.info(f"      Capítulo: {estado.capitulo_atual}")
            logger.info(f"      Bitcoin: {estado.bitcoin}")
            logger.info(f"      Anonimato: {estado.anonimato}%")
            resultados['atualizacoes'] = {
                'sucesso': True,
                'capitulo': estado.capitulo_atual,
                'bitcoin': estado.bitcoin,
                'anonimato': estado.anonimato
            }
            
            # 7. Testar listagem
            logger.info("\n5. Testando listagem...")
            saves = GameState.listar_saves_disponiveis()
            logger.info(f"   ✅ {len(saves)} save(s) listado(s)")
            resultados['listagem'] = {
                'sucesso': True,
                'quantidade': len(saves)
            }
            
            # 8. Restaurar configuração
            GameState.SAVES_DIR = original_saves_dir
            
            result.finish(True, resultados=resultados)
            logger.info(f"\n🎉 Todos os testes do GameState passaram!")
            
        except ImportError as e:
            result.finish(False, f"ImportError: {e}")
            logger.error(f"❌ Não foi possível importar game_state: {e}")
            
        except Exception as e:
            result.finish(False, str(e), traceback=traceback.format_exc())
            logger.error(f"❌ Erro no teste GameState: {e}")
            
        finally:
            # Limpar diretório temporário
            if test_dir and os.path.exists(test_dir):
                try:
                    shutil.rmtree(test_dir)
                    logger.debug(f"📁 Diretório temporário removido")
                except:
                    logger.warning(f"⚠️  Não foi possível remover diretório: {test_dir}")
        
        return result
    
    def testar_sistema_cores(self) -> TestResult:
        """Testa sistema de cores"""
        result = TestResult("Teste Sistema de Cores")
        
        logger.info("\n🎨 TESTE SISTEMA DE CORES:")
        logger.info("─" * 40)
        
        try:
            from utils.terminal_kali import Cores
            
            C = Cores()
            
            # Lista de cores esperadas
            cores_esperadas = ['VERDE', 'VERMELHO', 'AMARELO', 'CIANO', 'AZUL', 'ROXO', 'RESET']
            cores_encontradas = []
            cores_faltando = []
            
            for cor in cores_esperadas:
                if hasattr(C, cor):
                    valor = getattr(C, cor)
                    cores_encontradas.append(cor)
                    logger.debug(f"   {cor:<10}: {repr(valor)}")
                else:
                    cores_faltando.append(cor)
            
            # Exibir demo de cores
            logger.info("\n   Demonstração de cores:")
            if hasattr(C, 'VERDE'):
                logger.info(f"      {C.VERDE}● Texto verde{C.RESET}")
            if hasattr(C, 'VERMELHO'):
                logger.info(f"      {C.VERMELHO}● Texto vermelho{C.RESET}")
            if hasattr(C, 'AMARELO'):
                logger.info(f"      {C.AMARELO}● Texto amarelo{C.RESET}")
            if hasattr(C, 'CIANO'):
                logger.info(f"      {C.CIANO}● Texto ciano{C.RESET}")
            
            if not cores_faltando:
                result.finish(True, 
                             cores_encontradas=cores_encontradas,
                             total_cores=len(cores_encontradas))
                logger.info(f"\n✅ Sistema de cores OK ({len(cores_encontradas)} cores)")
            else:
                result.finish(False,
                             error=f"{len(cores_faltando)} cores faltando",
                             cores_faltando=cores_faltando,
                             cores_encontradas=cores_encontradas)
                logger.error(f"\n❌ {len(cores_faltando)} cor(es) faltando: {', '.join(cores_faltando)}")
                
        except Exception as e:
            result.finish(False, str(e), traceback=traceback.format_exc())
            logger.error(f"❌ Erro no sistema de cores: {e}")
        
        return result
    
    def testar_performance(self) -> TestResult:
        """Testa performance básica"""
        result = TestResult("Teste de Performance")
        
        logger.info("\n⚡ TESTE DE PERFORMANCE:")
        logger.info("─" * 40)
        
        resultados = {}
        
        # Teste 1: Tempos de importação
        logger.info("1. Tempos de importação:")
        modulos = ['game_state', 'manual_hacking', 'intro_menu', 'utils.terminal_kali']
        tempos = {}
        
        for modulo in modulos:
            try:
                start = time.perf_counter()
                __import__(modulo)
                elapsed = time.perf_counter() - start
                tempos[modulo] = elapsed
                
                status = '✓' if elapsed < 0.1 else '⚠️'
                logger.info(f"   {status} {modulo:<20} {elapsed:>7.3f}s")
                
                if elapsed >= 0.1:
                    logger.warning(f"      ⚠️  Importação lenta")
                    
            except Exception as e:
                logger.error(f"   ✗ {modulo:<20} ERRO: {e}")
        
        resultados['tempos_importacao'] = tempos
        
        # Teste 2: GameState performance
        logger.info("\n2. Performance GameState:")
        try:
            from game_state import GameState
            
            # Criar diretório temporário
            test_dir = tempfile.mkdtemp(prefix='audit_perf_')
            original_saves_dir = GameState.SAVES_DIR
            GameState.SAVES_DIR = os.path.join(test_dir, 'saves')
            os.makedirs(GameState.SAVES_DIR, exist_ok=True)
            
            # Teste de criação
            start = time.perf_counter()
            estado = GameState("PerfTest", "PERF_01")
            create_time = time.perf_counter() - start
            
            # Teste de salvamento
            start = time.perf_counter()
            save_file = estado.salvar()
            save_time = time.perf_counter() - start
            
            # Teste de carregamento
            start = time.perf_counter()
            GameState.carregar(save_file)
            load_time = time.perf_counter() - start
            
            logger.info(f"   ✓ Criação:   {create_time:>7.3f}s")
            logger.info(f"   ✓ Salvamento: {save_time:>7.3f}s")
            logger.info(f"   ✓ Carregamento: {load_time:>7.3f}s")
            
            resultados['gamestate_tempos'] = {
                'criacao': create_time,
                'salvamento': save_time,
                'carregamento': load_time
            }
            
            # Restaurar
            GameState.SAVES_DIR = original_saves_dir
            shutil.rmtree(test_dir)
            
        except Exception as e:
            logger.error(f"   ✗ Erro nos testes de performance: {e}")
        
        # Análise de resultados
        tempos_altos = [t for t in tempos.values() if t and t > 0.1]
        if not tempos_altos:
            result.finish(True, resultados=resultados)
            logger.info(f"\n✅ Performance dentro dos limites aceitáveis")
        else:
            result.finish(True, 
                         warning="Algumas importações estão lentas",
                         slow_imports=len(tempos_altos),
                         resultados=resultados)
            logger.warning(f"\n⚠️  {len(tempos_altos)} importação(ões) lenta(s)")
        
        return result
    
    def testar_execucao_rapida(self) -> TestResult:
        """Testa execução rápida dos principais componentes"""
        result = TestResult("Teste de Execução Rápida")
        
        logger.info("\n🚀 TESTE DE EXECUÇÃO RÁPIDA:")
        logger.info("─" * 40)
        
        testes = []
        
        def testar_menu_intro():
            """Testa execução do menu intro"""
            try:
                from root_evolution_main import IntroMenu
                menu = IntroMenu()
                # Simular execução rápida
                if hasattr(menu, 'run'):
                    return True, "IntroMenu OK"
                return False, "Método run não encontrado"
            except Exception as e:
                return False, str(e)
        
        def testar_manual():
            """Testa execução do manual"""
            try:
                import manual_hacking
                if hasattr(manual_hacking, 'exibir_manual'):
                    # Mock input para sair rapidamente
                    import builtins
                    original_input = builtins.input
                    builtins.input = lambda _: '0'
                    
                    try:
                        # Executar em thread com timeout
                        def run_manual():
                            try:
                                manual_hacking.exibir_manual()
                                return True, "Manual executado"
                            except Exception as e:
                                return False, str(e)
                        
                        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(run_manual)
                            try:
                                resultado = future.result(timeout=2)
                                return resultado
                            except concurrent.futures.TimeoutError:
                                future.cancel()
                                return False, "Timeout - manual demorou muito"
                    finally:
                        builtins.input = original_input
                return False, "Função exibir_manual não encontrada"
            except Exception as e:
                return False, str(e)
        
        # Executar testes
        logger.info("Executando testes rápidos...")
        
        # Teste 1: Menu Intro
        logger.info("\n1. IntroMenu:")
        sucesso1, msg1 = testar_menu_intro()
        if sucesso1:
            logger.info(f"   ✅ {msg1}")
        else:
            logger.error(f"   ❌ {msg1}")
        testes.append(('IntroMenu', sucesso1, msg1))
        
        # Teste 2: Manual
        logger.info("\n2. Manual de Hacking:")
        sucesso2, msg2 = testar_manual()
        if sucesso2:
            logger.info(f"   ✅ {msg2}")
        else:
            logger.error(f"   ❌ {msg2}")
        testes.append(('ManualHacking', sucesso2, msg2))
        
        # Resultado
        sucessos = sum(1 for _, s, _ in testes if s)
        total = len(testes)
        
        if sucessos == total:
            result.finish(True, testes=testes)
            logger.info(f"\n✅ Todos os testes de execução passaram ({sucessos}/{total})")
        else:
            result.finish(False,
                         error=f"{total - sucessos} teste(s) falharam",
                         testes=testes,
                         sucessos=sucessos,
                         total=total)
            logger.error(f"\n❌ {total - sucessos} teste(s) de execução falharam")
        
        return result
    
    def executar_todos_testes(self):
        """Executa todos os testes"""
        logger.info("\n" + "=" * 80)
        logger.info("🏃 EXECUTANDO SUITE DE TESTES COMPLETA")
        logger.info("=" * 80 + "\n")
        
        # Logar informações do sistema
        self.log_sistema_info()
        
        # Executar testes em sequência
        testes = [
            ('verificar_arquivos', self.verificar_arquivos),
            ('testar_importacoes', self.testar_importacoes),
            ('testar_sistema_cores', self.testar_sistema_cores),
            ('testar_game_state', self.testar_game_state_basico),
            ('testar_performance', self.testar_performance),
            ('testar_execucao_rapida', self.testar_execucao_rapida),
        ]
        
        for nome, teste_func in testes:
            result = self._run_test(teste_func, nome)
            self.resultados['test_results'][nome] = result.to_dict()
        
        # Atualizar estatísticas
        self._atualizar_estatisticas()
    
    def _atualizar_estatisticas(self):
        """Atualiza estatísticas baseadas nos resultados"""
        self.stats['total'] = len(self.test_results)
        self.stats['passed'] = sum(1 for r in self.test_results if r.success and not r.error)
        self.stats['failed'] = sum(1 for r in self.test_results if not r.success and r.error)
        self.stats['errors'] = sum(1 for r in self.test_results if not r.success)
        self.stats['warnings'] = sum(1 for r in self.test_results if r.success and 'warning' in r.details)
        
        self.resultados['summary'] = self.stats
        self.resultados['problems'] = self.problems
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        tempo_total = time.time() - self.start_time
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 RELATÓRIO FINAL")
        logger.info("=" * 80)
        
        # Estatísticas
        total = self.stats['total']
        passed = self.stats['passed']
        failed = self.stats['failed']
        errors = self.stats['errors']
        
        logger.info(f"\n⏱️  Tempo total: {tempo_total:.2f} segundos")
        logger.info(f"📈 Estatísticas:")
        logger.info(f"   Testes realizados: {total}")
        logger.info(f"   ✅ Sucessos: {passed}")
        logger.info(f"   ❌ Falhas: {failed}")
        logger.info(f"   💥 Erros: {errors}")
        
        if total > 0:
            taxa_sucesso = (passed / total) * 100
            logger.info(f"   📊 Taxa de sucesso: {taxa_sucesso:.1f}%")
            
            # Tempo médio por teste
            tempo_medio = tempo_total / total
            logger.info(f"   🐌 Tempo médio por teste: {tempo_medio:.2f}s")
        
        # Problemas encontrados
        if self.problems:
            logger.info(f"\n🚨 PROBLEMAS ENCONTRADOS ({len(self.problems)}):")
            for i, problema in enumerate(self.problems[:10], 1):  # Limitar a 10
                logger.info(f"   {i:2d}. {problema}")
            if len(self.problems) > 10:
                logger.info(f"   ... e mais {len(self.problems) - 10} problema(s)")
        else:
            logger.info("\n🎉 NENHUM PROBLEMA ENCONTRADO!")
        
        # Testes que falharam
        testes_falhos = [r for r in self.test_results if not r.success]
        if testes_falhos:
            logger.info(f"\n🔴 TESTES QUE FALHARAM ({len(testes_falhos)}):")
            for teste in testes_falhos:
                logger.info(f"   • {teste.name}: {teste.error}")
        
        # Salvar resultados
        self._salvar_resultados()
        
        # Resumo final
        logger.info("\n" + "=" * 80)
        if failed == 0 and errors == 0:
            logger.info("✅ AUDITORIA CONCLUÍDA COM SUCESSO!")
            return_code = 0
        else:
            logger.info("⚠️  AUDITORIA CONCLUÍDA COM PROBLEMAS")
            return_code = 1
        logger.info("=" * 80)
        
        return return_code
    
    def _salvar_resultados(self):
        """Salva resultados em arquivos"""
        # Salvar JSON completo
        json_file = LOG_FILE.with_suffix('.json')
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"💾 JSON detalhado: {json_file.name}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar JSON: {e}")
        
        # Salvar relatório resumido
        resumo_file = LOG_FILE.with_name(f"resumo_{LOG_FILE.name}")
        try:
            with open(resumo_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("AUDITORIA ROOT EVOLUTION - RELATÓRIO RESUMO\n")
                f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"TEMPO TOTAL: {time.time() - self.start_time:.2f}s\n")
                f.write(f"TESTES: {self.stats['total']}\n")
                f.write(f"SUCESSOS: {self.stats['passed']}\n")
                f.write(f"FALHAS: {self.stats['failed']}\n")
                f.write(f"ERROS: {self.stats['errors']}\n\n")
                
                if self.problems:
                    f.write("PROBLEMAS ENCONTRADOS:\n")
                    for problema in self.problems:
                        f.write(f"• {problema}\n")
                else:
                    f.write("NENHUM PROBLEMA ENCONTRADO\n")
                
                f.write(f"\nLog completo: {LOG_FILE.name}\n")
                f.write(f"JSON detalhado: {json_file.name}\n")
            
            logger.info(f"📝 Resumo salvo: {resumo_file.name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resumo: {e}")

def executar_auditoria_completa():
    """Executa auditoria completa"""
    logger.info("🔍 Iniciando auditoria completa...")
    
    auditoria = Auditoria()
    
    try:
        auditoria.executar_todos_testes()
        return_code = auditoria.gerar_relatorio()
        
        # Mostrar arquivos gerados
        logger.info("\n📁 ARQUIVOS GERADOS:")
        logger.info(f"   • {LOG_FILE.name} - Log completo")
        logger.info(f"   • {LOG_FILE.stem}.json - Dados estruturados")
        logger.info(f"   • resumo_{LOG_FILE.name} - Resumo executivo")
        
        return return_code
        
    except KeyboardInterrupt:
        logger.error("\n⏹️  Auditoria interrompida pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"\n💥 ERRO FATAL: {e}")
        logger.error(traceback.format_exc())
        return 1

def executar_teste_especifico(teste_nome: str):
    """Executa um teste específico"""
    logger.info(f"🎯 Executando teste específico: {teste_nome}")
    
    auditoria = Auditoria()
    
    testes = {
        'arquivos': auditoria.verificar_arquivos,
        'importacoes': auditoria.testar_importacoes,
        'cores': auditoria.testar_sistema_cores,
        'gamestate': auditoria.testar_game_state_basico,
        'performance': auditoria.testar_performance,
        'execucao': auditoria.testar_execucao_rapida,
    }
    
    if teste_nome in testes:
        resultado = auditoria._run_test(testes[teste_nome], teste_nome)
        auditoria._atualizar_estatisticas()
        auditoria._salvar_resultados()
        
        if resultado.success:
            logger.info(f"✅ Teste '{teste_nome}' concluído com sucesso")
            return 0
        else:
            logger.error(f"❌ Teste '{teste_nome}' falhou: {resultado.error}")
            return 1
    else:
        logger.error(f"❌ Teste '{teste_nome}' não encontrado")
        logger.info("Testes disponíveis: " + ", ".join(testes.keys()))
        return 2

def mostrar_ajuda():
    """Mostra ajuda do sistema"""
    print("""
🔍 AUDITORIA ROOT EVOLUTION v2.0
──────────────────────────────────────────────────────

USO: python auditoria_root.py [OPÇÃO]

OPÇÕES:
  --completo, -c      Executa auditoria completa (padrão)
  --teste NOME        Executa teste específico
  --help, -h          Mostra esta ajuda
  --version, -v       Mostra versão

TESTES DISPONÍVEIS:
  arquivos      Verifica arquivos e diretórios
  importacoes   Testa importação de módulos
  cores         Testa sistema de cores
  gamestate     Testa GameState (save/load)
  performance   Testes de performance
  execucao      Teste rápido de execução

EXEMPLOS:
  python auditoria_root.py --completo
  python auditoria_root.py --teste gamestate
  python auditoria_root.py --teste performance
  python auditoria_root.py -h

SAÍDA:
  • logs_auditoria/auditoria_YYYYMMDD_HHMMSS.log
  • logs_auditoria/auditoria_YYYYMMDD_HHMMSS.json
  • logs_auditoria/resumo_auditoria_YYYYMMDD_HHMMSS.log
    """)

def main():
    """Função principal"""
    
    # Banner
    print("\n" + "=" * 80)
    print("🔍 AUDITORIA ROOT EVOLUTION v2.0")
    print("=" * 80)
    print(f"📁 Logs serão salvos em: {LOG_DIR}/")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print("=" * 80 + "\n")
    
    # Processar argumentos
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h']:
            mostrar_ajuda()
            return 0
            
        elif arg in ['--version', '-v']:
            print("Auditoria Root Evolution v2.0")
            return 0
            
        elif arg in ['--completo', '-c'] or len(sys.argv) == 1:
            return executar_auditoria_completa()
            
        elif arg == '--teste' and len(sys.argv) > 2:
            teste_nome = sys.argv[2].lower()
            return executar_teste_especifico(teste_nome)
            
        else:
            print(f"❌ Opção desconhecida: {arg}")
            print("Use --help para ver opções disponíveis")
            return 1
    else:
        # Executar completo por padrão
        return executar_auditoria_completa()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Auditoria interrompida pelo usuário")
        print(f"📁 Log parcial salvo em: {LOG_FILE}")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 ERRO FATAL: {e}")
        traceback.print_exc()
        print(f"\n📁 Log de erro salvo em: {LOG_FILE}")
        sys.exit(1)