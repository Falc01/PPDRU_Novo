import pandas as pd
import streamlit as st
import plotly.express as px

def graficos_pop(bairro_selecionado, file_path):
    # Carregar os dados da planilha
    df = pd.read_excel(file_path)

    # Converter colunas de decimal para porcentagem
    colunas_percentuais = ["PROP_LIXO/DOM", "PROP_SANEAMENTO/DOM", "PROP_AGUA/DOM"]
    for coluna in colunas_percentuais:
        if coluna in df.columns:
            df[coluna] = df[coluna] * 100
            df[coluna] = df[coluna].map(lambda x: f"{x:.2f}%")

    # Arredondar colunas específicas
    if "GRAU_ENVELHECIMENTO" in df.columns:
        df["GRAU_ENVELHECIMENTO"] = df["GRAU_ENVELHECIMENTO"].round().astype(int)

    if "DENSIDADE" in df.columns:
        df["DENSIDADE"] = df["DENSIDADE"].round().astype(int)

    st.title("📊 Projeto de Disponibilidade de Dados")

    df_bairro_selecionado = df[df["NOME_BAIRRO"] == bairro_selecionado]

    st.sidebar.header("🔽 Selecione os gráficos")
    mostrar_pop_total = st.sidebar.checkbox("População por sexo", True)
    mostrar_pop_total_bairro = st.sidebar.checkbox("População por bairros", True)
    mostrar_faixa_etaria = st.sidebar.checkbox("População por grupos de idade", True)
    mostrar_grau = st.sidebar.checkbox("Grau de envelhecimento", True)
    mostrar_cor = st.sidebar.checkbox("População por cor/raça", True)
    mostrar_densidade = st.sidebar.checkbox("Densidade demográfica", True)
    mostrar_analfabetismo = st.sidebar.checkbox("População não alfabetizada", True)

    if mostrar_pop_total:
        valores_bairro = {
            "Homens": df_bairro_selecionado["POP_TOTAL_HOMEM"].iloc[0],
            "Mulheres": df_bairro_selecionado["POP_TOTAL_MULHER"].iloc[0]
        }
        st.write("### 📊 Distribuição percentual da população residente, por sexo, segundo os bairros de Salvador, 2010")
        st.write(f"##### {bairro_selecionado}")
        fig_pizza = px.pie(
            names=list(valores_bairro.keys()), 
            values=list(valores_bairro.values()),
            color=list(valores_bairro.keys()),
            color_discrete_map={"Homens": "blue", "Mulheres": "pink"}
        )
        st.plotly_chart(fig_pizza)
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_pop_total_bairro:
        st.write('### 📊 População residente segundo os bairros de Salvador, 2010')
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao_pop = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Residente (Crescente)": ("POP_TOTAL_RESIDENTE", True),
            "Residente (Decrescente)": ("POP_TOTAL_RESIDENTE", False),
        }   
        criterio_ordenacao_pop = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao_pop.keys()))
        coluna_ordenacao_pop, ordem_crescente = opcoes_ordenacao_pop[criterio_ordenacao_pop]
        df_ordenado = df.sort_values(by=coluna_ordenacao_pop, ascending=ordem_crescente)
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()
        fig_pop_total = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="POP_TOTAL_RESIDENTE", 
            labels={'POP_TOTAL_RESIDENTE': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}
        )
        fig_pop_total.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        st.plotly_chart(fig_pop_total)
        pop_total_bairro = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
        pop_total_geral = df["POP_TOTAL_RESIDENTE"].sum()
        percentual_bairro = (pop_total_bairro / pop_total_geral) * 100
        st.markdown(f"📌 **Nota:** A população residente deste bairro representa {percentual_bairro:.2f}% da população de Salvador.")
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_faixa_etaria:
        idade_cols = [col for col in df.columns if "IDADE_" in col]
        if idade_cols:
            faixa_etaria = {
                "Entre 0 a 6 Anos": df_bairro_selecionado["IDADE_0_6_ANOS"].iloc[0],
                "Entre 7 a 14 Anos": df_bairro_selecionado["IDADE_7_14_ANOS"].iloc[0],
                "Entre 15 a 18 Anos": df_bairro_selecionado["IDADE_15_18_ANOS"].iloc[0],
                "Entre 19 a 24 Anos": df_bairro_selecionado["IDADE_19_24_ANOS"].iloc[0],
                "Entre 25 a 49 Anos": df_bairro_selecionado["IDADE_25_49_ANOS"].iloc[0],
                "Entre 50 a 64 Anos": df_bairro_selecionado["IDADE_50_64_ANOS"].iloc[0],
                "Entre 65 ou mais Anos": df_bairro_selecionado["IDADE_65_MAIS"].iloc[0],
            }
            st.write("### 📊 Distribuição da população residente, por grupos de idade, segundo os bairros de Salvador, 2010")
            st.write(f"##### {bairro_selecionado}")
            fig_barras = px.bar(
                x=list(faixa_etaria.keys()), 
                y=list(faixa_etaria.values()),
                labels= {"x" : "Grupos de idade", 'y' : ' '},
                text_auto=True
            )
            fig_barras.update_traces(textposition="outside")
            fig_barras.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
            st.plotly_chart(fig_barras)
            st.write(" ")
            st.write(" ")
            st.write(" ")

    if mostrar_grau:
        st.write('### 📊 Grau de envelhecimento da população residente segundo os bairros de Salvador, 2010')
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao_grau = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Salvador (Crescente)": ('GRAU_ENVELHECIMENTO', True),
            "Salvador (Decrescente)": ('GRAU_ENVELHECIMENTO', False),
        }   
        criterio_ordenacao_grau = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao_grau.keys()))
        coluna_ordenacao_grau, ordem_crescente = opcoes_ordenacao_grau[criterio_ordenacao_grau]
        df_ordenado = df.sort_values(by=coluna_ordenacao_grau, ascending=ordem_crescente)
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()
        fig_grau = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y='GRAU_ENVELHECIMENTO', 
            labels={'GRAU_ENVELHECIMENTO': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}
        )
        fig_grau.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        st.plotly_chart(fig_grau)
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_cor:
        cor_cols = [col for col in df.columns if "COR_" in col]
        if cor_cols:
            cor_values = {
                "Parda": df_bairro_selecionado["COR_PARDA"].iloc[0],
                "Preta": df_bairro_selecionado["COR_PRETA"].iloc[0],
                "Branca": df_bairro_selecionado["COR_BRANCA"].iloc[0],
                "Amarela": df_bairro_selecionado["COR_AMARELA"].iloc[0],
                "Indigena": df_bairro_selecionado["COR_INDIGENA"].iloc[0],
            }
            st.write(f'### 📊 Distribuição percentual da população residente, por cor/raça, segundo os bairros de Salvador, 2010')
            st.write(f'##### {bairro_selecionado}')
            fig_cor = px.pie(
                names=list(cor_values.keys()), 
                values=list(cor_values.values()),
                color=list(cor_values.keys()),
                color_discrete_map={"Parda": "brown", "Preta": "black", "Branca": "white", 'Amarela': 'yellow', 'Indigena': 'Green'}
            )
            st.plotly_chart(fig_cor)
            st.write(" ")
            st.write(" ")
            st.write(" ")

    if mostrar_densidade:
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        st.write('### 📊 Densidade demográfica segundo os bairros de Salvador, 2010')
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Densidade (Crescente)": ("DENSIDADE", True),
            "Densidade (Decrescente)": ("DENSIDADE", False),
        }   
        criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))
        coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
        df_ordenado = df.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()
        fig_densidade = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="DENSIDADE", 
            labels={'DENSIDADE': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}
        )
        fig_densidade.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        st.plotly_chart(fig_densidade)
        st.markdown("📌 **Nota:** Densidade demográfica - Habitantes/Km²")
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_analfabetismo:
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        st.write('### 📊 População residente acima de 15 anos não alfabetizada segundo os bairros de Salvador, 2010')
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Taxa de Analfabetismo (Crescente)": ("EDUC_ANALFABETISMO", True),
            "Taxa de Analfabetismo (Decrescente)": ("EDUC_ANALFABETISMO", False),
        }
        criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))
        coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
        df_ordenado = df.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()
        fig_analfabetismo = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="EDUC_ANALFABETISMO", 
            labels={'EDUC_ANALFABETISMO': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}
        )
        fig_analfabetismo.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        st.plotly_chart(fig_analfabetismo)

def graficos_dom(bairro_selecionado, file_path):
    df = pd.read_excel(file_path)

    # Converter colunas de decimal para porcentagem
    colunas_percentuais = ["PROP_LIXO/DOM", "PROP_SANEAMENTO/DOM", "PROP_AGUA/DOM"]
    for coluna in colunas_percentuais:
        if coluna in df.columns:
            df[coluna] = df[coluna] * 100
            df[coluna] = df[coluna].map(lambda x: f"{x:.2f}%")

    # Arredondar colunas específicas
    if "GRAU_ENVELHECIMENTO" in df.columns:
        df["GRAU_ENVELHECIMENTO"] = df["GRAU_ENVELHECIMENTO"].round().astype(int)
    if "DENSIDADE" in df.columns:
        df["DENSIDADE"] = df["DENSIDADE"].round().astype(int)

    st.title("📊 Projeto de Disponibilidade de Dados")

    df_bairro_selecionado = df[df["NOME_BAIRRO"] == bairro_selecionado]

    st.sidebar.header("🔽 Selecione os gráficos")
    mostrar_domicilios = st.sidebar.checkbox("Domicílios por tipo", True)
    mostrar_moradores  = st.sidebar.checkbox("Domicílios por número de moradores", True)
    mostrar_proporcao = st.sidebar.checkbox("Domicílios por tipo de infraestrutura urbana", True)
    mostrar_renda_sexo = st.sidebar.checkbox("Rendimento médio dos responsáveis por sexo", True)
    mostrar_salario = st.sidebar.checkbox("Rendimento em salários mínimos dos responsáveis", True)
    mostrar_renda = st.sidebar.checkbox("Rendimento médio dos responsáveis", True)

    if mostrar_domicilios:
        dom_values = {
            "Casa": df_bairro_selecionado["DOM_PART_PERM_CASA"].iloc[0],
            "Casa em vilas": df_bairro_selecionado["DOM_PART_PERM_CASA_VILA"].iloc[0],
            "Apartamentos": df_bairro_selecionado["DOM_PART_PERM_CASA_APART"].iloc[0],
        }
        st.write(f'### 📊 Total de domicílios particulares permanentes, por tipo, segundo os bairros de Salvador, 2010')
        st.write(f'##### {bairro_selecionado}')
        fig_dom = px.bar(
            x=list(dom_values.keys()), 
            y=list(dom_values.values()),
            labels={"x": "Tipo de domicílio", "y": " "},
            text_auto=True
        )
        fig_dom.update_traces(textposition="outside")
        fig_dom.update_layout(
            yaxis_showticklabels=False, 
            showlegend=False, 
            yaxis_showgrid=False, 
            yaxis_tickformat="."
        )
        st.plotly_chart(fig_dom)
        dom_totais = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
        st.markdown(f"📌 **Nota:** Total de domicilios no bairro de {bairro_selecionado}: {dom_totais}")
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_moradores:
        dom_pizza_values = {
            "1 morador": df_bairro_selecionado["DOM_1_MORADOR"].iloc[0],
            "2 a 4 moradores": df_bairro_selecionado["DOM_2_4_MORADORES"].iloc[0],
            "5 a 6 moradores": df_bairro_selecionado["DOM_5_6_MORADORES"].iloc[0],
            "7 ou mais moradores": df_bairro_selecionado["DOM_ACIMA_7_MORADORES"].iloc[0],
        }
        st.write(f'### 📊 Distribuição percentual dos domicílios particulares permanentes, por número de moradores, segundo os bairros de Salvador, 2010')
        st.write(f'##### {bairro_selecionado}')
        df_pizza = pd.DataFrame({
            "Categoria": list(dom_pizza_values.keys()),
            "Valor": list(dom_pizza_values.values())
        })
        ordem_categorias = [
            "1 morador",
            "2 a 4 moradores",
            "5 a 6 moradores",
            "7 ou mais moradores"
        ]
        df_pizza["Categoria"] = pd.Categorical(df_pizza["Categoria"], categories=ordem_categorias, ordered=True)
        df_pizza = df_pizza.sort_values("Categoria", ascending=True)
        fig_dom_pizza = px.pie(
            df_pizza,
            names="Categoria", 
            values="Valor",
        )
        fig_dom_pizza.update_traces(sort=False)
        fig_dom_pizza.update_layout(
            legend=dict(traceorder="normal")
        )
        st.plotly_chart(fig_dom_pizza)

    if mostrar_proporcao:
        prop_values = {
            "Lixo coletado": df_bairro_selecionado["PROP_LIXO/DOM"].iloc[0],
            "Esgotamento sanitário ligado a rede geral": df_bairro_selecionado["PROP_SANEAMENTO/DOM"].iloc[0],
            "Abastecimento de água ligado a rede geral": df_bairro_selecionado["PROP_AGUA/DOM"].iloc[0],
        }
        st.write(f'### 📊 Distribuição percentual dos domicílios particulares permanentes, por tipo de infraestrutura urbada segundo os bairros de Salvador, 2010')
        st.write(f'##### {bairro_selecionado}')
        fig_prop = px.bar(
            x=list(prop_values.keys()), 
            y=list(prop_values.values()),
            labels={'x' : 'Tipo de infraestrutura urbana', 'y' : ' '}
        )
        fig_prop.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        st.plotly_chart(fig_prop)
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_renda_sexo:
        if "RESP_RENDA_MEDIA_HOMEM" in df.columns and "RESP_RENDA_MEDIA_MULHER" in df.columns:
            df_bairro = df[df["NOME_BAIRRO"] == bairro_selecionado]
            st.write(f'### 📊 Rendimento médio dos responsáveis pelos domicílios particulares permanentes, por sexo, segundo os bairros de Salvador, 2010 ')
            st.write(f'##### {bairro_selecionado}')
            df_renda_genero = pd.DataFrame({
                "Gênero": ["Homens", "Mulheres"],
                "Renda Média": [df_bairro["RESP_RENDA_MEDIA_HOMEM"].values[0], df_bairro["RESP_RENDA_MEDIA_MULHER"].values[0]]
            })
            fig_renda_genero = px.bar(
                df_renda_genero, 
                x="Gênero", 
                y="Renda Média", 
                labels={"Renda Média": " ", "Gênero": "Sexo"},
                color="Gênero", 
                color_discrete_map={"Homens": "blue", "Mulheres": "pink"},
                text_auto=True,
            )
            fig_renda_genero.update_traces(textposition="outside")
            fig_renda_genero.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
            st.plotly_chart(fig_renda_genero)
            st.write(" ")
            st.write(" ")
            st.write(" ")

    if mostrar_salario:
        resp_pizza_values = {
            "0 a 2 Salários mínimos": df_bairro_selecionado["RESP_RENDA_0_2_SM"].iloc[0],
            "mais de 2 a 5 Salários mínimos": df_bairro_selecionado["RESP_RENDA_2_5_SM"].iloc[0],
            "mais de 5 a 10 Salários mínimos": df_bairro_selecionado["RESP_RENDA_5_10_SM"].iloc[0],
            "mais de 10 a 20 Salários mínimos": df_bairro_selecionado["RESP_RENDA_10_20_SM"].iloc[0],
            "mais de 20 Salários mínimos": df_bairro_selecionado["RESP_RENDA_20_MAIS_SM"].iloc[0],
            "Sem rendimento": df_bairro_selecionado["RESP_SEM_RENDIMENTO"].iloc[0],
        }
        st.write(f'### 📊 Rendimento em salários mínimos dos responsáveis pelos domicílios particulares permanentes segundo os bairros de Salvador, 2010')
        st.write(f'##### {bairro_selecionado}')
        fig_resp_pizza = px.pie(
            names=list(resp_pizza_values.keys()),
            values=list(resp_pizza_values.values()),
            category_orders={"names": [
                "0 a 2 Salários mínimos",
                "mais de 2 a 5 Salários mínimos",
                "mais de 5 a 10 Salários mínimos",
                "mais de 10 a 20 Salários mínimos",
                "mais de 20 Salários mínimos",
                'Sem rendimento',
            ]}
        )
        st.plotly_chart(fig_resp_pizza)
        resp_total_bairro = df_bairro_selecionado["RESP_TOTAL"].iloc[0]
        st.write(f"##### População Total de Responsaveis no Bairro {bairro_selecionado}: {resp_total_bairro}")
        st.write(" ")
        st.write(" ")
        st.write(" ")

    if mostrar_renda:
        df["cor"] = df["NOME_BAIRRO"].apply(lambda x: "red" if x == bairro_selecionado else "blue")
        st.write('### 📊 Rendimento médio dos responsáveis por domicílios particulares permanentes segundo os bairros de Salvador, 2010')
        st.write("##### 🔽 Ordenação dos Dados")
        opcoes_ordenacao = {
            "Alfabética": ("NOME_BAIRRO", True),
            "Renda Média (Crescente)": ("RESP_RENDA_MEDIA", True),
            "Renda Média (Decrescente)": ("RESP_RENDA_MEDIA", False),
        }
        criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))
        coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
        df_ordenado = df.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)
        categoria_ordem = df_ordenado["NOME_BAIRRO"].tolist()
        fig_renda = px.bar(
            df_ordenado, 
            x="NOME_BAIRRO", 
            y="RESP_RENDA_MEDIA", 
            labels={'RESP_RENDA_MEDIA': ' ', 'NOME_BAIRRO' : 'Bairros de Salvador'}, 
            color="cor", 
            color_discrete_map={"red": "red", "blue": "lightblue"},
            category_orders={"NOME_BAIRRO": categoria_ordem}
        )
        fig_renda.update_layout(yaxis_showticklabels=False, showlegend=False, yaxis_showgrid=False, yaxis_tickformat=".")
        st.plotly_chart(fig_renda)