# =============================================================================
# TALLER #4: Herramientas Avanzadas y Dashboards
# Curso: Herramientas y Visualización - ADM-3083
# =============================================================================

# 1. IMPORTACIÓN DE LIBRERÍAS
import streamlit as st
import plotly.express as px
import pandas as pd

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Foodie's Place Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# 3. CARGA DE DATOS
# El dataset tips viene integrado en Plotly Express (244 registros)
tips = px.data.tips()

# 4. ENCABEZADO PRINCIPAL
st.title("🍽️ Foodie's Place — Dashboard de Propinas")
st.markdown(
    "Análisis exploratorio para validar si **la cena genera más propinas que el almuerzo** "
    "y si **los fines de semana superan a los días laborables**."
)
st.divider()

# 5. SIDEBAR — FILTROS INTERACTIVOS
st.sidebar.title("🔍 Filtros")

# Filtro por día (todos seleccionados por defecto)
dias_disponibles = tips["day"].unique().tolist()
dias_seleccionados = st.sidebar.multiselect(
    label="Selecciona el Día",
    options=dias_disponibles,
    default=dias_disponibles
)

# Filtro por momento del día (todos seleccionados por defecto)
momentos_disponibles = tips["time"].unique().tolist()
momentos_seleccionados = st.sidebar.multiselect(
    label="Selecciona el Momento",
    options=momentos_disponibles,
    default=momentos_disponibles
)

st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Fuente:** Dataset `tips` — Plotly Express")

# 6. FILTRADO DEL DATAFRAME
# Se aplican los filtros del sidebar al dataframe original
df_filtrado = tips[
    (tips["day"].isin(dias_seleccionados)) &
    (tips["time"].isin(momentos_seleccionados))
]

# Aviso si no hay datos con los filtros aplicados
if df_filtrado.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados.")
    st.stop()

# 7. KPIs — MÉTRICAS CLAVE
st.subheader("📌 Métricas Clave")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    total_facturado = df_filtrado["total_bill"].sum()
    st.metric(label="💵 Total Facturado", value=f"${total_facturado:,.2f}")

with col_kpi2:
    total_propinas = df_filtrado["tip"].sum()
    st.metric(label="💰 Total Propinas", value=f"${total_propinas:,.2f}")

with col_kpi3:
    propina_promedio = df_filtrado["tip"].mean()
    st.metric(label="📈 Propina Promedio", value=f"${propina_promedio:,.2f}")

st.divider()

# 8. VISUALIZACIONES — DOS COLUMNAS
st.subheader("📊 Visualizaciones")

col_izq, col_der = st.columns(2)

# Columna izquierda: Total de Propinas por Momento del Día
with col_izq:
    st.markdown("**¿Se gana más en la Cena o en el Almuerzo?**")

    propinas_por_momento = (
        df_filtrado.groupby("time", as_index=False)["tip"]
        .sum()
        .rename(columns={"tip": "Total Propinas", "time": "Momento"})
    )

    fig_bar = px.bar(
        propinas_por_momento,
        x="Momento",
        y="Total Propinas",
        color="Momento",
        text_auto=".2f",
        color_discrete_map={"Dinner": "#E07B39", "Lunch": "#4A90D9"},
        title="Total de Propinas por Momento del Día",
        labels={"Total Propinas": "Total ($)", "Momento": "Momento del Día"}
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

# Columna derecha: Scatter Plot Total Cuenta vs Propina
with col_der:
    st.markdown("**¿A mayor consumo, mayor propina?**")

    fig_scatter = px.scatter(
        df_filtrado,
        x="total_bill",
        y="tip",
        color="time",
        symbol="day",
        size="size",
        hover_data=["sex", "day", "time", "size"],
        color_discrete_map={"Dinner": "#E07B39", "Lunch": "#4A90D9"},
        trendline="ols",
        title="Total Cuenta vs. Propina",
        labels={
            "total_bill": "Total Cuenta ($)",
            "tip": "Propina ($)",
            "time": "Momento",
            "day": "Día"
        }
    )
    fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

# 9. INSIGHT FINAL — CONCLUSIÓN DE NEGOCIO
st.divider()
st.subheader("💡 Conclusión de Negocio")

st.success(
    "✅ **Los datos respaldan la teoría del gerente:**\n\n"
    "- 🌙 **La cena supera al almuerzo** en propinas totales.\n\n"
    "- 📅 **El fin de semana (Sat & Sun) concentra la mayor actividad** y mayores propinas acumuladas.\n\n"
    "- 📈 **Existe una correlación positiva** entre el total de la cuenta y la propina.\n\n"
    "**Recomendación:** Reforzar el personal en cenas de fin de semana e incentivar upselling."
)
