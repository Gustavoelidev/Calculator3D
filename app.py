import streamlit as st

st.set_page_config(page_title="Calculadora de Custo 3D", layout="centered")
st.title("Calculadora de Custo de Impressão 3D - GamaStudio")

st.header("1. Dados do Modelo")
modelo = st.text_input("Nome do modelo:")
tempo_horas = st.number_input("Tempo de impressão - Horas:", min_value=0, format="%d")
tempo_minutos = st.number_input("Tempo de impressão - Minutos:", min_value=0, max_value=59, format="%d")
tempo_total_horas = tempo_horas + (tempo_minutos / 60)

peso = st.number_input("Peso da peça (gramas):", min_value=0.0, format="%.2f")

st.header("2. Custos Variáveis")
preco_filamento_kg = st.number_input("Preço do filamento (R$/kg):", min_value=0.0, value=130.0, format="%.2f")
potencia_impressora = st.number_input("Potência da impressora (Watts):", min_value=0.0, value=150.0, format="%.0f")
tarifa_energia = st.number_input("Tarifa de energia (R$/kWh):", min_value=0.0, value=0.85, format="%.2f")

st.header("3. Custos Fixos e Precificação")
markup = st.number_input("Markup (multiplicador):", min_value=1.0, value=2.0, format="%.2f")
imposto_percentual = st.number_input("Imposto (%):", min_value=0.0, value=0.0, format="%.2f")
taxa_cartao_percentual = st.number_input("Taxa de cartão (%):", min_value=0.0, value=5.0, format="%.2f")
custo_anuncio = st.number_input("Custo de anúncio (R$):", min_value=0.0, value=0.25, format="%.2f")

# Conversão de percentuais
imposto = imposto_percentual / 100
taxa_cartao = taxa_cartao_percentual / 100

st.divider()

# Cálculos corretos
custo_filamento = (peso / 1000) * preco_filamento_kg
custo_energia = (potencia_impressora / 1000) * tempo_total_horas * tarifa_energia
custo_variavel_total = custo_filamento + custo_energia
custo_total = custo_variavel_total + custo_anuncio

# Preço base com markup
preco_base = custo_total * markup

# Cálculo dos encargos sobre o preco_base
valor_taxa_cartao = preco_base * taxa_cartao
valor_imposto = preco_base * imposto
preco_final = preco_base + valor_taxa_cartao + valor_imposto

lucro_bruto = preco_final - custo_total
lucro_liquido = lucro_bruto - valor_taxa_cartao - valor_imposto

# Resultados
st.header("Resumo do Cálculo")
st.write(f"**Modelo:** {modelo if modelo else '---'}")
st.write(f"Custo com filamento: R$ {custo_filamento:.2f}")
st.write(f"Custo com energia: R$ {custo_energia:.2f}")
st.write(f"Custo de anúncio: R$ {custo_anuncio:.2f}")
st.write(f"**Custo total de produção:** R$ {custo_total:.2f}")
st.write(f"**Preço de venda sugerido:** R$ {preco_final:.2f}")
st.write(f"Lucro bruto: R$ {lucro_bruto:.2f}")
st.success(f"Lucro líquido: R$ {lucro_liquido:.2f}")