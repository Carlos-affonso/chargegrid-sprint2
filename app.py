import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ChargeGrid Intelligence",
    layout="wide"
)

st.title("ChargeGrid Intelligence")
st.subheader("Simulador simples de recarga inteligente para condomínios")

st.write(
    "Este simulador representa uma prova de conceito do sistema ChargeGrid. "
    "A ideia é mostrar como um condomínio poderia controlar carregadores de veículos elétricos, "
    "autenticar usuários por RFID e dividir a energia disponível entre os carros conectados."
)

# -----------------------------
# Dados fixos da simulação
# -----------------------------

limite_condominio = 30
limite_carregador = 7.4

usuarios = [
    "Carlos Eduardo",
    "Temitope Kuku",
    "Igor Massone",
    "Gabriel Oliveira",
    "Gabrieli Pettena",
    "Murillo Kamei"
]

# -----------------------------
# Guardando informações
# -----------------------------

if "carros" not in st.session_state:
    st.session_state.carros = 0

if "mensagem" not in st.session_state:
    st.session_state.mensagem = "Sistema iniciado."

# -----------------------------
# Escolha do cenário
# -----------------------------

st.sidebar.header("Controle da simulação")

cenario = st.sidebar.selectbox(
    "Escolha o cenário:",
    [
        "Pico solar",
        "Transição",
        "Pico tarifário",
        "Off-peak"
    ]
)

if cenario == "Pico solar":
    energia_solar = 22
    energia_bateria = 4
    energia_rede = 4
    tarifa = 0.65

elif cenario == "Transição":
    energia_solar = 12
    energia_bateria = 10
    energia_rede = 8
    tarifa = 0.82

elif cenario == "Pico tarifário":
    energia_solar = 2
    energia_bateria = 16
    energia_rede = 12
    tarifa = 1.15

else:
    energia_solar = 0
    energia_bateria = 6
    energia_rede = 24
    tarifa = 0.55

# -----------------------------
# Botões
# -----------------------------

if st.sidebar.button("Passar RFID autorizado"):
    if st.session_state.carros < len(usuarios):
        st.session_state.carros = st.session_state.carros + 1
        st.session_state.mensagem = "RFID autorizado. Veículo adicionado."
    else:
        st.session_state.mensagem = "Todos os carregadores simulados já estão em uso."

if st.sidebar.button("Passar RFID inválido"):
    st.session_state.mensagem = "RFID inválido. Recarga bloqueada."

if st.sidebar.button("Remover veículo"):
    if st.session_state.carros > 0:
        st.session_state.carros = st.session_state.carros - 1
        st.session_state.mensagem = "Veículo removido e sessão encerrada."
    else:
        st.session_state.mensagem = "Não há veículos conectados."

if st.sidebar.button("Resetar"):
    st.session_state.carros = 0
    st.session_state.mensagem = "Simulação reiniciada."

st.sidebar.info(st.session_state.mensagem)

# -----------------------------
# Cálculos principais
# -----------------------------

energia_total = energia_solar + energia_bateria + energia_rede

if energia_total > limite_condominio:
    energia_total = limite_condominio

if st.session_state.carros > 0:
    potencia_por_carro = energia_total / st.session_state.carros

    if potencia_por_carro > limite_carregador:
        potencia_por_carro = limite_carregador
else:
    potencia_por_carro = 0

energia_renovavel = energia_solar + energia_bateria

if energia_total > 0:
    porcentagem_renovavel = (energia_renovavel / energia_total) * 100
else:
    porcentagem_renovavel = 0

consumo_por_carro = potencia_por_carro * 0.5
custo_por_carro = consumo_por_carro * tarifa

consumo_total = consumo_por_carro * st.session_state.carros
custo_total = custo_por_carro * st.session_state.carros

co2_evitado = consumo_total * (porcentagem_renovavel / 100) * 0.45

# -----------------------------
# Métricas principais
# -----------------------------

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Limite do condomínio", f"{limite_condominio} kW")
col2.metric("Veículos conectados", st.session_state.carros)
col3.metric("Potência por veículo", f"{potencia_por_carro:.2f} kW")
col4.metric("Cenário", cenario)

# -----------------------------
# Fontes de energia
# -----------------------------

st.divider()

st.header("Fontes de energia")

col_a, col_b, col_c = st.columns(3)

col_a.metric("Energia solar", f"{energia_solar} kW")
col_b.metric("Bateria", f"{energia_bateria} kW")
col_c.metric("Rede elétrica", f"{energia_rede} kW")

dados_fontes = pd.DataFrame({
    "Fonte": ["Solar", "Bateria", "Rede"],
    "Potência": [energia_solar, energia_bateria, energia_rede]
})

st.bar_chart(dados_fontes, x="Fonte", y="Potência")

# -----------------------------
# Tabela de sessões
# -----------------------------

st.divider()

st.header("Sessões de recarga")

lista_carros = []

for i in range(st.session_state.carros):
    lista_carros.append({
        "Carregador": f"HCA G2-{i + 1}",
        "Usuário": usuarios[i],
        "RFID": f"RFID-00{i + 1}",
        "Status": "Ativo",
        "Potência": f"{potencia_por_carro:.2f} kW",
        "Consumo estimado": f"{consumo_por_carro:.2f} kWh",
        "Custo estimado": f"R$ {custo_por_carro:.2f}",
        "Energia renovável": f"{porcentagem_renovavel:.0f}%"
    })

if st.session_state.carros == 0:
    st.warning("Nenhum veículo conectado.")
else:
    tabela = pd.DataFrame(lista_carros)
    st.dataframe(tabela, use_container_width=True)

# -----------------------------
# Resultados
# -----------------------------

st.divider()

st.header("Resultados da simulação")

r1, r2, r3 = st.columns(3)

r1.metric("Consumo total estimado", f"{consumo_total:.2f} kWh")
r2.metric("Custo total estimado", f"R$ {custo_total:.2f}")
r3.metric("CO₂ evitado", f"{co2_evitado:.2f} kg")

# -----------------------------
# Explicação
# -----------------------------

st.divider()

st.header("Explicação da lógica")

st.write(
    "O sistema soma a energia disponível da geração solar, da bateria e da rede elétrica. "
    "Depois, verifica se esse valor ultrapassa o limite máximo do condomínio. "
    "Se ultrapassar, o sistema usa apenas o limite permitido."
)

st.write(
    "Em seguida, a potência disponível é dividida pela quantidade de veículos conectados. "
    "Isso representa o balanceamento dinâmico de carga, também chamado de DLM."
)

st.write(
    "A autenticação RFID foi simulada pelos botões. Quando o RFID é autorizado, "
    "um veículo entra na sessão de recarga. Quando o RFID é inválido, a recarga é bloqueada."
)