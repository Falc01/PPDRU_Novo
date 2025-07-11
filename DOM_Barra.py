import sys
import os
import streamlit as st from streamlit_js_eval 
import streamlit_js_eval
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modulo_graficos import graficos_dom

result = streamlit_js_eval(js_expressions="window.location.hostname", key="get_hostname")

if result:
    hostname = result
    subdominio = hostname.split(".")[0]  # barra-populacao
    entre_barra_e_traco = subdominio.split("-")[0]  # "barra"

graficos_dom(bairro_selecionado=entre_barra_e_traco, file_path="\\dados_agrupados_unido.xlsx")
