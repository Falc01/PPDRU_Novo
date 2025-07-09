import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modulo_graficos import graficos_dom

graficos_dom(bairro_selecionado="Stella Maris", file_path="..\\dados_agrupados_unido.xlsx")