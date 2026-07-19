"""
CyberSentinel AI - Pacote Central da Aplicação

Este módulo inicializa o pacote principal do agente CyberSentinel AI,
definindo os metadados do nível de pacote e gerenciando o namespace público
para a arquitetura do Copilot de SOC.
"""

__version__ = "0.1.0"
__author__ = "Desenvolvedor CyberSentinel AI"
__description__ = "Assistente de Cyber Threat Intelligence e Suporte a SOC"

# A lista __all__ define a interface pública ao utilizar 'from src import *'
__all__ = [
    "__version__",
    "__author__",
    "__description__",
]

# Nota para futura expansão da arquitetura:
# À medida que componentes como CyberSentinelAgent ou VectorRetriever se encontrarem consolidados,
# eles poderão ser importados aqui para simplificar as importações de alto nível.
# Exemplo:
# from src.interfaces.agent import CyberSentinelAgent
# __all__.append("CyberSentinelAgent")