
# ============================================================
# BIOPRODATA
# BioProcess & Biofactory Data Analytics
# ============================================================

import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="BIOPRODATA",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# IDENTIDAD VISUAL
# ============================================================

VERDE_OSCURO = "#164E46"
VERDE_MEDIO = "#527C70"
VERDE_SALVIA = "#DCE9E2"
VERDE_CLARO = "#EDF3EF"
FONDO = "#F7FAF8"
AZUL = "#17365D"
TEXTO = "#263B35"
BLANCO = "#FFFFFF"
BORDE = "#D2E1D8"


# ============================================================
# ESTILOS CSS
# ============================================================

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background-color: #F7FAF8;
    color: #263B35;
}

/* Área principal: espacio superior para evitar que la navegación quede cortada */
.block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 3.25rem !important;
    padding-bottom: 3rem !important;
    max-width: 1450px;
}

/* Evita que el contenedor principal pegue la navegación al borde superior */
[data-testid="stAppViewContainer"] section.main > div {
    padding-top: 0.5rem;
}

/* Navegación superior: color verde también en los estados internos de Streamlit */
div[data-testid="stSegmentedControl"] {
    margin: 0.35rem 0 1rem 0 !important;
    padding-top: 0.15rem;
}
div[data-testid="stSegmentedControl"] button,
div[data-testid="stSegmentedControl"] [role="tab"],
div[data-testid="stSegmentedControl"] [role="radio"] {
    border-color: #C6D9CE !important;
}
div[data-testid="stSegmentedControl"] button[aria-pressed="true"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] button[data-selected="true"],
div[data-testid="stSegmentedControl"] [aria-selected="true"],
div[data-testid="stSegmentedControl"] [data-state="active"] {
    background: #164E46 !important;
    color: #FFFFFF !important;
    border-color: #164E46 !important;
    box-shadow: none !important;
}

/* Respaldo para versiones que dibujan el selector como pestañas BaseWeb */
[role="tablist"] [role="tab"][aria-selected="true"],
[role="tablist"] button[aria-selected="true"] {
    color: #164E46 !important;
    border-bottom-color: #164E46 !important;
    box-shadow: inset 0 -2px 0 #164E46 !important;
}
[role="tablist"] [role="tab"]:hover,
[role="tablist"] button:hover {
    color: #164E46 !important;
}

/* Barra lateral */
[data-testid="stSidebar"] {
    background-color: #E8F0EB;
    border-right: 1px solid #D2E1D8;
}

/* Navegación superior: pestañas compactas, sin círculos de radio */
div[data-testid="stSegmentedControl"] {
    margin: 0.15rem 0 0.8rem 0;
}
div[data-testid="stSegmentedControl"] button {
    border: 1px solid #C6D9CE !important;
    border-radius: 7px !important;
    background: #E8F0EB !important;
    color: #164E46 !important;
    min-height: 2.1rem;
}
div[data-testid="stSegmentedControl"] button[aria-pressed="true"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] button[data-selected="true"] {
    background: #164E46 !important;
    color: #FFFFFF !important;
    border-color: #164E46 !important;
    box-shadow: none !important;
}

div[data-testid="stSegmentedControl"] button:hover {
    background: #DCE9E2 !important;
    color: #164E46 !important;
    border-color: #527C70 !important;
}

/* Evita que el color de selección predeterminado del tema se vea naranja */
div[data-testid="stSegmentedControl"] button:focus,
div[data-testid="stSegmentedControl"] button:focus-visible {
    outline: 2px solid #527C70 !important;
    outline-offset: 1px !important;
}

/* Títulos */
h1, h2, h3 {
    color: #17365D !important;
    font-weight: 650;
}

/* Texto */
p, label {
    color: #263B35;
}

/* Indicadores */
[data-testid="stMetric"] {
    background-color: #EDF3EF;
    border: 1px solid #D2E1D8;
    padding: 18px;
    border-radius: 14px;
}

/* Valor de indicadores */
[data-testid="stMetricValue"] {
    color: #164E46;
    font-weight: 700;
}

/* Paneles desplegables */
[data-testid="stExpander"] {
    background-color: #E8F0EB;
    border: 1px solid #C6D9CE;
    border-radius: 12px;
}

/* Encabezado de paneles */
[data-testid="stExpander"] summary {
    background-color: #DCE9E2;
    color: #164E46;
    font-weight: 600;
    border-radius: 12px;
}

/* Botones */
.stButton button,
.stDownloadButton button {
    background-color: #527C70;
    color: white;
    border: 1px solid #527C70;
    border-radius: 9px;
    font-weight: 600;
    transition: 0.2s;
}

/* Efecto al pasar el cursor */
.stButton button:hover,
.stDownloadButton button:hover {
    background-color: #164E46;
    color: white;
    border-color: #164E46;
}

/* Selecciones múltiples */
[data-baseweb="tag"] {
    background-color: #527C70 !important;
    color: white !important;
    border-radius: 7px !important;
}

[data-baseweb="tag"] span {
    color: white !important;
}

/* Controles desplegables */
[data-baseweb="select"] > div {
    border-color: #C6D9CE !important;
    border-radius: 9px !important;
}

/* Opciones seleccionadas */
[aria-selected="true"] {
    background-color: #DCE9E2 !important;
    color: #164E46 !important;
}

/* Casillas y controles */
input, textarea {
    accent-color: #527C70;
}

/* Separadores */
hr {
    border-color: #D2E1D8;
}

/* Mensajes informativos */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Etiquetas secundarias */
small {
    color: #527C70;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DICCIONARIO DE VARIABLES
# Basado en la Tabla 1 de Oyetunde et al. (2019)
# ============================================================

DICCIONARIO = {

    # IDENTIFICACIÓN

    "paper_number": (
        "Identificación",
        "Identificador del artículo científico de origen.",
        "No especificada"
    ),

    "no_of_designs": (
        "Identificación",
        "Número de diseños experimentales registrados.",
        "Conteo"
    ),

    # FUENTES DE CARBONO

    "cs1": (
        "Fuentes de carbono",
        "Primera fuente de carbono utilizada.",
        "Código o categoría"
    ),

    "cs2": (
        "Fuentes de carbono",
        "Segunda fuente de carbono utilizada.",
        "Código o categoría"
    ),

    "cs3": (
        "Fuentes de carbono",
        "Tercera fuente de carbono utilizada.",
        "Código o categoría"
    ),

    "cs1_mw": (
        "Fuentes de carbono",
        "Peso molecular de la primera fuente de carbono.",
        "No especificada"
    ),

    "cs2_mw": (
        "Fuentes de carbono",
        "Peso molecular de la segunda fuente de carbono.",
        "No especificada"
    ),

    "cs3_mw": (
        "Fuentes de carbono",
        "Peso molecular de la tercera fuente de carbono.",
        "No especificada"
    ),

    "cs_conc1": (
        "Fuentes de carbono",
        "Concentración de la primera fuente de carbono.",
        "mM"
    ),

    "cs_conc2": (
        "Fuentes de carbono",
        "Concentración de la segunda fuente de carbono.",
        "mM"
    ),

    "cs_conc3": (
        "Fuentes de carbono",
        "Concentración de la tercera fuente de carbono.",
        "mM"
    ),

    "CS_C1": (
        "Fuentes de carbono",
        "Moles de carbono en la primera fuente de carbono.",
        "mol C"
    ),

    "CS_H1": (
        "Fuentes de carbono",
        "Moles de hidrógeno en la primera fuente de carbono.",
        "mol H"
    ),

    "CS_O1": (
        "Fuentes de carbono",
        "Moles de oxígeno en la primera fuente de carbono.",
        "mol O"
    ),

    "CS_C2": (
        "Fuentes de carbono",
        "Moles de carbono en la segunda fuente de carbono.",
        "mol C"
    ),

    "CS_H2": (
        "Fuentes de carbono",
        "Moles de hidrógeno en la segunda fuente de carbono.",
        "mol H"
    ),

    "CS_O2": (
        "Fuentes de carbono",
        "Moles de oxígeno en la segunda fuente de carbono.",
        "mol O"
    ),

    "CS_C3": (
        "Fuentes de carbono",
        "Moles de carbono en la tercera fuente de carbono.",
        "mol C"
    ),

    "CS_H3": (
        "Fuentes de carbono",
        "Moles de hidrógeno en la tercera fuente de carbono.",
        "mol H"
    ),

    "CS_O3": (
        "Fuentes de carbono",
        "Moles de oxígeno en la tercera fuente de carbono.",
        "mol O"
    ),

    # CONDICIONES DEL BIOPROCESO

    "reactor_type": (
        "Condiciones del bioproceso",
        "Tipo de reactor: continuo, batch o fed-batch.",
        "Código categórico"
    ),

    "rxt_volume": (
        "Condiciones del bioproceso",
        "Volumen de trabajo del reactor.",
        "L"
    ),

    "media": (
        "Condiciones del bioproceso",
        "Medio utilizado para la fermentación.",
        "Categórica"
    ),

    "temp": (
        "Condiciones del bioproceso",
        "Temperatura del medio durante la fermentación.",
        "°C"
    ),

    "time": (
        "Condiciones del bioproceso",
        "Tiempo total de fermentación.",
        "h"
    ),

    "fermentation_time": (
        "Condiciones del bioproceso",
        "Tiempo de fermentación. Equivalencia con time pendiente de verificar.",
        "h"
    ),

    "oxygen": (
        "Condiciones del bioproceso",
        "Condición de oxígeno del reactor.",
        "Código categórico"
    ),

    # INFORMACIÓN GENÉTICA

    "strain_background": (
        "Modificaciones genéticas",
        "Cepa de referencia utilizada en el estudio.",
        "Categórica"
    ),

    "strain_background_genotype": (
        "Modificaciones genéticas",
        "Información del genotipo de la cepa de referencia.",
        "Texto"
    ),

    "strain_background_genotype_modification": (
        "Modificaciones genéticas",
        "Información sobre modificaciones del genotipo de referencia.",
        "Pendiente de verificar"
    ),

    "genes_modified": (
        "Modificaciones genéticas",
        "Genes modificados en la cepa estudiada.",
        "Lista o texto"
    ),

    "gene_deletion": (
        "Modificaciones genéticas",
        "Indica si se realizaron eliminaciones de genes.",
        "Vector binario"
    ),

    "gene_overexpression": (
        "Modificaciones genéticas",
        "Indica si se realizó sobreexpresión de genes.",
        "Vector binario"
    ),

    "heterologous_gene": (
        "Modificaciones genéticas",
        "Indica si se incorporaron genes heterólogos.",
        "Vector binario"
    ),

    "replication_origin": (
        "Modificaciones genéticas",
        "Número de copias del plásmido.",
        "Conteo o vector"
    ),

    "codon_optimization": (
        "Modificaciones genéticas",
        "Indica si se realizó optimización de codones.",
        "Binaria o vector"
    ),

    "sensor_regulator": (
        "Modificaciones genéticas",
        "Indica si se utilizó un regulador sensor.",
        "Binaria o vector"
    ),

    "enzyme_redesign_evolution": (
        "Modificaciones genéticas",
        "Indica si se realizó rediseño o evolución de enzimas.",
        "Binaria o vector"
    ),

    "protein_scaffold": (
        "Modificaciones genéticas",
        "Indica si se utilizó un andamiaje proteico.",
        "Binaria o vector"
    ),

    "dir_evo": (
        "Modificaciones genéticas",
        "Indica si se realizó evolución dirigida.",
        "Binaria"
    ),

    "Mod_path_opt": (
        "Modificaciones genéticas",
        "Indica si se realizó optimización modular de rutas metabólicas.",
        "Binaria"
    ),

    # PRODUCTO

    "product_name": (
        "Caracterización del producto",
        "Nombre del producto obtenido.",
        "Categórica"
    ),

    "no_C": (
        "Caracterización del producto",
        "Número de moles de carbono en el producto.",
        "mol C"
    ),

    "no_H": (
        "Caracterización del producto",
        "Número de moles de hidrógeno en el producto.",
        "mol H"
    ),

    "no_O": (
        "Caracterización del producto",
        "Número de moles de oxígeno en el producto.",
        "mol O"
    ),

    "no_N": (
        "Caracterización del producto",
        "Número de moles de nitrógeno en el producto.",
        "mol N"
    ),

    "mw": (
        "Caracterización del producto",
        "Peso molecular del producto.",
        "No especificada"
    ),

    # CARACTERÍSTICAS METABÓLICAS

    "precursor": (
        "Características metabólicas",
        "Precursor del producto proveniente del metabolismo central.",
        "Código o categoría"
    ),

    "enzyme_steps": (
        "Características metabólicas",
        "Número de pasos enzimáticos desde el precursor hasta el producto.",
        "Conteo"
    ),

    "atp_cost": (
        "Características metabólicas",
        "Número de moléculas de ATP necesarias desde el precursor hasta el producto.",
        "Moléculas"
    ),

    "nadh_nadph_cost": (
        "Características metabólicas",
        "Número de moléculas de NADH/NADPH necesarias desde el precursor hasta el producto.",
        "Moléculas"
    ),

    "na_cost": (
        "Características metabólicas",
        "Posible variable relacionada con el costo de NADH/NADPH. Correspondencia pendiente de verificar.",
        "Pendiente de verificar"
    ),

    # MÉTRICAS DE PRODUCCIÓN

    "yield_1": (
        "Métricas de producción",
        "Rendimiento en gramos de producto por gramo de fuente de carbono alimentada.",
        "g/g"
    ),

    "yield_2": (
        "Métricas de producción",
        "Rendimiento en gramos de producto por gramo de fuente de carbono consumida.",
        "g/g"
    ),

    "yield_3": (
        "Métricas de producción",
        "Rendimiento en gramos de producto por gramo de biomasa.",
        "g/g"
    ),

    # La base Bioprocesses data.xlsx contiene estas tres columnas.
    # Se mantienen como métricas distintas. Su correspondencia exacta con
    # yield_1/yield_2/yield_3 debe verificarse contra el diccionario original.
    "yield": (
        "Métricas de producción",
        "Indicador de rendimiento reportado en la columna original 'yield'. "
        "Se presenta por separado para no confundirlo con las otras métricas "
        "de rendimiento. Consultar la definición metodológica del registro de origen.",
        "Según la fuente original; revisar unidad antes de comparar"
    ),
    "yield_o": (
        "Métricas de producción",
        "Indicador de rendimiento reportado en la columna original 'yield_o'. "
        "Su significado específico no se infiere del nombre de la columna; "
        "se mantiene separado de las demás métricas.",
        "Según la fuente original; revisar unidad antes de comparar"
    ),
    "yield2": (
        "Métricas de producción",
        "Segundo indicador de rendimiento reportado en la columna original 'yield2'. "
        "Se mantiene separado de 'yield' y 'yield_o'; confirmar su definición "
        "en la documentación de origen antes de interpretarlo.",
        "Según la fuente original; revisar unidad antes de comparar"
    ),

    "titer": (
        "Métricas de producción",
        "Concentración del producto.",
        "g/L"
    ),

    "rate": (
        "Métricas de producción",
        "Productividad máxima.",
        "g producto/L/h"
    ),

    "bio_titre": (
        "Métricas de producción",
        "Concentración de biomasa.",
        "g/L"
    ),

    "bio_grw_rate": (
        "Métricas de producción",
        "Velocidad de crecimiento de biomasa durante la fase exponencial.",
        "h⁻¹"
    ),

    "bio_growth_rate": (
        "Métricas de producción",
        "Velocidad de crecimiento de biomasa durante la fase exponencial.",
        "h⁻¹"
    ),

    # INFORMACIÓN COMPLEMENTARIA

    "gen_info": (
        "Información complementaria",
        "Indica si las modificaciones genéticas del estudio están representadas por las categorías registradas.",
        "Sí / No"
    ),

    "env_info": (
        "Información complementaria",
        "Indica si las condiciones del reactor están representadas por las categorías registradas.",
        "Sí / No"
    ),

    "good": (
        "Información complementaria",
        "Definición no especificada inequívocamente en la tabla consultada.",
        "Pendiente de verificar"
    )
}


# ============================================================
# FUNCIONES GENERALES
# ============================================================

def obtener_info(variable):

    if variable in DICCIONARIO:
        return DICCIONARIO[variable]

    return (
        "Sin clasificar",
        "Definición pendiente de verificar en la fuente científica.",
        "No especificada"
    )


def convertir_numerico(serie):

    return pd.to_numeric(
        serie,
        errors="coerce"
    )


def cargar_excel(archivo):

    if archivo is not None:
        return pd.read_excel(archivo)

    posibles_rutas = [
        Path(__file__).parent / "data" / "Bioprocesses data.xlsx",
        Path("data/Bioprocesses data.xlsx"),
        Path("Bioprocesses data.xlsx")
    ]

    for ruta in posibles_rutas:

        if ruta.exists():
            return pd.read_excel(ruta)

    return None


def exportar_excel(hojas):

    archivo = io.BytesIO()

    with pd.ExcelWriter(
        archivo,
        engine="openpyxl"
    ) as writer:

        for nombre, tabla in hojas.items():

            tabla.to_excel(
                writer,
                sheet_name=nombre[:31],
                index=False
            )

    archivo.seek(0)

    return archivo.getvalue()


def mostrar_descripcion(variable, etiqueta="ℹ️"):
    """Muestra la definición en un popover compacto, sin alargar la página."""
    categoria, descripcion, unidad = obtener_info(variable)
    with st.popover(etiqueta, help=f"Consultar información de {nombre_visible(variable)}"):
        st.markdown(f"**{nombre_visible(variable)}**")
        st.caption(categoria)
        st.write(descripcion)
        st.caption(f"Unidad o tipo: {unidad}")


def selector_con_info(etiqueta, opciones, variable_info, key):
    """Selector compacto con icono ℹ️ en la misma línea del título."""
    col_label, col_info = st.columns([0.90, 0.10], vertical_alignment="center")
    with col_label:
        st.markdown(f"**{etiqueta}**")
    with col_info:
        mostrar_descripcion(variable_info)

    # Se resuelve en tiempo de ejecución porque nombre_visible se define
    # más abajo en el archivo. Así evitamos pasar None como format_func.
    return st.selectbox(
        etiqueta,
        opciones,
        format_func=lambda valor: nombre_visible(valor),
        key=key,
        label_visibility="collapsed"
    )


# NAVEGACIÓN PRINCIPAL
# ============================================================

secciones = [
    "Inicio",
    "Datos experimentales",
    "Calidad de datos y EDA",
    "Distribuciones",
    "Relaciones",
    "Análisis y comparación"
]

seccion = st.segmented_control(
    "Navegación principal",
    options=secciones,
    default="Inicio",
    selection_mode="single",
    label_visibility="collapsed",
    key="navegacion_principal"
)

if seccion is None:
    seccion = "Inicio"


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div style="
        background:linear-gradient(110deg,#164E46,#527C70);
        padding:24px 28px;
        border-radius:16px;
        margin-bottom:22px;
        color:white;
    ">
        <div style="font-size:30px;font-weight:750;color:white;">
            🦠 BIOPRODATA
        </div>
        <div style="font-size:15px;color:#EDF3EF;margin-top:5px;">
            BioProcess & Biofactory Data Analytics
        </div>
        <div style="font-size:12px;color:#DCE9E2;margin-top:9px;">
            Exploring Biofactories and Bioprocesses Through Data
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CARGA DEL ARCHIVO
# ============================================================

with st.expander(
    "📂 Base de datos experimental",
    expanded=(seccion == "Inicio")
):

    st.write(
        "Carga el archivo Excel para comenzar a explorar "
        "los registros experimentales."
    )

    archivo_subido = st.file_uploader(
        "Seleccionar archivo Excel",
        type=["xlsx", "xls"],
        help="Archivo esperado: Bioprocesses data.xlsx",
        key="archivo_bioprodata"
    )

    st.caption(
        "También puedes guardar el archivo en la carpeta "
        "BIOPRODATA/data para que se cargue automáticamente."
    )


# ============================================================
# CARGA Y VALIDACIÓN DE DATOS
# ============================================================

try:

    df_original = cargar_excel(archivo_subido)

except Exception as error:

    st.error(
        f"No se pudo leer el archivo. Detalle: {error}"
    )

    st.stop()


if df_original is None:

    st.markdown(
        """
        <div style="
            background:#E8F0EB;
            border:1px solid #C6D9CE;
            border-radius:15px;
            padding:28px;
            text-align:center;
        ">
            <div style="font-size:42px;">🧫</div>
            <h3 style="color:#164E46;">Bienvenido a BIOPRODATA</h3>
            <p>
                Para comenzar, carga tu base de datos experimental
                en el apartado superior.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


df = df_original.copy()

df.columns = [
    str(col).strip()
    for col in df.columns
]


# ============================================================
# NOMBRES AMIGABLES PARA LA INTERFAZ
# ============================================================

NOMBRES_VARIABLES = {

    "paper_number": "Artículo científico",
    "no_of_designs": "Número de diseños",
    "product_name": "Producto",
    "strain_background": "Cepa de referencia",
    "media": "Medio de cultivo",
    "reactor_type": "Tipo de reactor",
    "rxt_volume": "Volumen del reactor (L)",
    "temp": "Temperatura (°C)",
    "time": "Tiempo de fermentación (h)",
    "fermentation_time": "Tiempo de fermentación (h)",
    "oxygen": "Condición de oxígeno",
    "cs1": "Primera fuente de carbono",
    "cs2": "Segunda fuente de carbono",
    "cs3": "Tercera fuente de carbono",
    "cs_conc1": "Concentración de fuente de carbono 1 (mM)",
    "cs_conc2": "Concentración de fuente de carbono 2 (mM)",
    "cs_conc3": "Concentración de fuente de carbono 3 (mM)",
    "cs1_mM": "Concentración de fuente de carbono 1 (mM)",
    "cs2_mM": "Concentración de fuente de carbono 2 (mM)",
    "cs3_mM": "Concentración de fuente de carbono 3 (mM)",
    "cs_C1": "Carbono en la primera fuente de carbono (mol C)",
    "cs_H1": "Hidrógeno en la primera fuente de carbono (mol H)",
    "cs_O1": "Oxígeno en la primera fuente de carbono (mol O)",
    "genes_modified": "Genes modificados",
    "gene_deletion": "Eliminación de genes",
    "gene_overexpression": "Sobreexpresión de genes",
    "heterologous_gene": "Genes heterólogos",
    "precursor": "Precursor metabólico",
    "enzyme_steps": "Pasos enzimáticos",
    "atp_cost": "Costo de ATP",
    "nadh_nadph_cost": "Costo de NADH/NADPH",
    "yield": "Rendimiento (yield)",
    "yield_o": "Rendimiento (yield_o)",
    "yield2": "Rendimiento (yield2)",
    "yield_1": "Rendimiento sobre carbono alimentado (yield_1)",
    "yield_2": "Rendimiento sobre carbono consumido (yield_2)",
    "yield_3": "Rendimiento sobre biomasa (yield_3)",
    "titer": "Concentración de producto (titer, g/L)",
    "rate": "Productividad (rate, g/L/h)",
    "bio_titre": "Concentración de biomasa (bio_titre, g/L)",
    "bio_growth_rate": "Velocidad de crecimiento de biomasa (bio_growth_rate)",
    "bio_grw_rate": "Velocidad de crecimiento de biomasa (bio_grw_rate)",
    "rxt_type": "Tipo de reactor (rxt_type)",
    "obj_set": "Conjunto de objetivos genéticos (obj_set)",
    "expr_gen": "Genes expresados (expr_gen)",
    "gen_mod": "Modificaciones genéticas (gen_mod)",
    "gene_del": "Genes eliminados (gene_del)",
    "gene_ov": "Genes sobreexpresados (gene_ov)",
    "protein_scaffold": "Ensamblaje de proteínas (protein_scaffold)",
    "dir_evo": "Evolución dirigida (dir_evo)",
    "enzyme_redesign": "Rediseño enzimático (enzyme_redesign)",
    "mw": "Peso molecular del producto (mw)",
    "precursor": "Precursor metabólico (precursor)",
    "atp_cost": "Costo de ATP (atp_cost)",
    "nadh_nadph_cost": "Costo de NADH/NADPH (nadh_nadph_cost)",
    "time": "Tiempo de fermentación (time, h)"
}


def nombre_visible(variable):

    return NOMBRES_VARIABLES.get(
        variable,
        variable.replace("_", " ").capitalize()
    )


# Métricas de producción que pueden existir en distintas versiones del Excel.
# Las columnas legacy (yield, yield_o, yield2) se conservan separadas de
# yield_1/yield_2/yield_3: no se presupone equivalencia entre sus nombres.
METRICAS_PRODUCCION = [
    "titer", "rate", "yield", "yield_o", "yield2",
    "yield_1", "yield_2", "yield_3"
]


def opciones_columna(datos, columna):

    return sorted(
        datos[columna]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


# ============================================================
# SECCIÓN: INICIO
# ============================================================

if seccion == "Inicio":

    st.title("Panel general")

    st.write(
        """
        Explora información experimental de biofábricas
        y bioprocesos de *Escherichia coli*.

        BIOPRODATA integra datos de fuentes de carbono,
        modificaciones genéticas, condiciones de cultivo,
        características metabólicas y resultados de producción.
        """
    )

    st.markdown("### Resumen de la base de datos")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Registros experimentales",
            f"{len(df):,}"
        )

    with col2:

        st.metric(
            "Variables disponibles",
            f"{len(df.columns):,}"
        )

    with col3:

        if "product_name" in df.columns:

            total_productos = df["product_name"].nunique()

        else:

            total_productos = 0

        st.metric(
            "Productos registrados",
            f"{total_productos:,}"
        )

    with col4:

        total_nulos = int(df.isna().sum().sum())

        st.metric(
            "Valores faltantes",
            f"{total_nulos:,}"
        )

    st.markdown("---")

    st.subheader("Explora BIOPRODATA")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div style="
                background:#E8F0EB;
                border-radius:13px;
                padding:20px;
                min-height:160px;
            ">
                <div style="font-size:30px;">🔬</div>
                <h4 style="color:#164E46;">Explorar experimentos</h4>
                <p style="font-size:14px;">
                    Busca productos, consulta estudios y examina
                    sus condiciones experimentales.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div style="
                background:#E8F0EB;
                border-radius:13px;
                padding:20px;
                min-height:160px;
            ">
                <div style="font-size:30px;">📊</div>
                <h4 style="color:#164E46;">Analizar datos</h4>
                <p style="font-size:14px;">
                    Examina la calidad, las distribuciones
                    y las relaciones entre variables.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div style="
                background:#E8F0EB;
                border-radius:13px;
                padding:20px;
                min-height:160px;
            ">
                <div style="font-size:30px;">🧪</div>
                <h4 style="color:#164E46;">Comparar diseños</h4>
                <p style="font-size:14px;">
                    Compara características experimentales
                    y resultados de producción.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("Productos registrados")

    if "product_name" in df.columns:

        productos = (
            df["product_name"]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .rename_axis("Producto")
            .reset_index(name="Experimentos")
        )

        fig_productos = px.bar(
            productos.sort_values("Experimentos", ascending=True),
            x="Experimentos",
            y="Producto",
            orientation="h",
            title="Productos con mayor número de registros",
            color_discrete_sequence=[VERDE_MEDIO]
        )

        fig_productos.update_layout(
            plot_bgcolor=BLANCO,
            paper_bgcolor=BLANCO,
            font_color=TEXTO,
            xaxis_title="Experimentos",
            yaxis_title="Producto",
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=25, r=20, t=55, b=35)
        )

        st.plotly_chart(
            fig_productos,
            use_container_width=True
        )

    st.caption(
        "Fuente: Oyetunde et al. (2019). "
        "Machine learning framework for assessment "
        "of microbial factory performance."
    )


# ============================================================
# SECCIÓN: DATOS EXPERIMENTALES
# ============================================================

elif seccion == "Datos experimentales":

    st.title("Explorador de experimentos")

    st.write(
        """
        Consulta los diseños experimentales registrados.
        Puedes comenzar seleccionando un producto y después
        personalizar la búsqueda con filtros adicionales.
        """
    )

    # --------------------------------------------------------
    # FILTRO PRINCIPAL: PRODUCTO
    # --------------------------------------------------------

    st.markdown("### 1. Selecciona un producto")

    if "product_name" in df.columns:

        productos = opciones_columna(
            df,
            "product_name"
        )

        producto_seleccionado = st.selectbox(
            "¿Qué producto quieres investigar?",
            ["Todos los productos"] + productos,
            help="Selecciona un producto para consultar sus experimentos."
        )

    else:

        producto_seleccionado = "Todos los productos"

        st.warning(
            "No se encontró la columna product_name."
        )


    # Copia de los datos para aplicar filtros

    datos_filtrados = df.copy()


    if (
        producto_seleccionado != "Todos los productos"
        and "product_name" in datos_filtrados.columns
    ):

        datos_filtrados = datos_filtrados[
            datos_filtrados["product_name"].astype(str)
            == producto_seleccionado
        ]


    # --------------------------------------------------------
    # FILTROS AVANZADOS
    # --------------------------------------------------------

    st.markdown("### 2. Personaliza tu búsqueda")

    with st.expander(
        "⚙️ Mostrar filtros adicionales",
        expanded=False
    ):

        st.caption(
            "Puedes combinar varios filtros. "
            "Si dejas una opción vacía, no se aplicará ese filtro."
        )

        filtros = [

            ("paper_number", "Artículo científico"),

            ("strain_background", "Cepa de referencia"),

            ("media", "Medio de cultivo"),

            ("reactor_type", "Tipo de reactor"),

            ("oxygen", "Condición de oxígeno"),

            ("cs1", "Primera fuente de carbono"),

            ("cs2", "Segunda fuente de carbono"),

            ("cs3", "Tercera fuente de carbono")

        ]

        columnas_filtros = st.columns(2)

        for i, (columna, etiqueta) in enumerate(filtros):

            if columna in datos_filtrados.columns:

                opciones = opciones_columna(
                    datos_filtrados,
                    columna
                )

                seleccion = columnas_filtros[
                    i % 2
                ].multiselect(
                    etiqueta,
                    opciones,
                    key=f"nuevo_filtro_{columna}"
                )

                if seleccion:

                    datos_filtrados = datos_filtrados[
                        datos_filtrados[columna]
                        .astype(str)
                        .isin(seleccion)
                    ]


    # --------------------------------------------------------
    # RESULTADOS DE BÚSQUEDA
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 3. Resultados de la búsqueda")

    cantidad_registros = len(datos_filtrados)

    cantidad_publicaciones = (
        datos_filtrados["paper_number"].nunique()
        if "paper_number" in datos_filtrados.columns
        else 0
    )

    metricas_produccion = [
        columna
        for columna in METRICAS_PRODUCCION
        if columna in datos_filtrados.columns
        and datos_filtrados[columna].notna().any()
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Experimentos encontrados",
        f"{cantidad_registros:,}"
    )

    col2.metric(
        "Publicaciones",
        f"{cantidad_publicaciones:,}"
    )

    col3.metric(
        "Métricas de producción disponibles",
        f"{len(metricas_produccion)}"
    )

    if cantidad_registros == 0:

        st.warning(
            "No se encontraron experimentos con los filtros seleccionados. "
            "Prueba eliminando alguno de los filtros."
        )

    else:

        # Columnas principales para una vista más sencilla

        columnas_principales = [

            "paper_number",
            "product_name",
            "strain_background",
            "media",
            "reactor_type",
            "temp",
            "oxygen",
            "cs1",
            "cs_conc1",
            "titer",
            "rate"

        ]

        columnas_visibles = [
            c for c in columnas_principales
            if c in datos_filtrados.columns
        ]

        tabla_resumen = datos_filtrados[
            columnas_visibles
        ].copy()

        tabla_resumen = tabla_resumen.rename(
            columns={
                c: nombre_visible(c)
                for c in tabla_resumen.columns
            }
        )

        st.dataframe(
            tabla_resumen,
            use_container_width=True,
            hide_index=True,
            height=350
        )

        # Vista completa de las variables

        with st.expander(
            "Consultar todas las variables de los registros"
        ):

            st.caption(
                "Esta vista incluye las columnas originales "
                "de la base de datos."
            )

            st.dataframe(
                datos_filtrados,
                use_container_width=True,
                height=400
            )

        # Descargar resultados

        st.download_button(
            "📥 Descargar resultados filtrados",

            data=datos_filtrados.to_csv(
                index=False
            ).encode("utf-8-sig"),

            file_name="BIOPRODATA_experimentos.csv",

            mime="text/csv"
        )


    # --------------------------------------------------------
    # DICCIONARIO DE VARIABLES INTEGRADO
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📖 Diccionario de variables")

    st.write(
        """
        ¿No sabes qué significa una variable de la base de datos?
        Búscala aquí para consultar su descripción y unidad.
        """
    )

    filas_diccionario = []

    for columna in df.columns:

        categoria, descripcion, unidad = obtener_info(
            columna
        )

        filas_diccionario.append({

            "Variable original": columna,

            "Nombre descriptivo": nombre_visible(columna),

            "Categoría": categoria,

            "Descripción": descripcion,

            "Unidad o tipo": unidad

        })

    tabla_diccionario = pd.DataFrame(
        filas_diccionario
    )

    busqueda_variable = st.text_input(
        "Buscar una variable",

        placeholder="Ejemplo: cs1, ATP, temperatura, titer..."
    )

    if busqueda_variable:

        coincidencias = (
            tabla_diccionario.astype(str)
            .apply(
                lambda columna:
                columna.str.contains(
                    busqueda_variable,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        )

        tabla_diccionario = tabla_diccionario[
            coincidencias
        ]

    st.dataframe(
        tabla_diccionario,
        use_container_width=True,
        hide_index=True,
        height=350
    )

    st.caption(
        "Las definiciones pendientes de verificar se identifican "
        "para evitar atribuir significados no confirmados."
    )
    # ============================================================
# SECCIÓN: CALIDAD DE DATOS Y EDA
# ============================================================

elif seccion == "Calidad de datos y EDA":

    st.title("Calidad de datos y análisis exploratorio")

    st.write(
        """
        Examina la integridad de la base de datos,
        identifica valores faltantes y duplicados,
        y calcula estadísticas descriptivas de las variables.
        """
    )

    # --------------------------------------------------------
    # INDICADORES DE CALIDAD
    # --------------------------------------------------------

    total_filas = len(df)
    total_columnas = len(df.columns)
    total_nulos = int(df.isna().sum().sum())
    total_duplicados = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Registros", f"{total_filas:,}")
    col2.metric("Variables", f"{total_columnas:,}")
    col3.metric("Valores faltantes", f"{total_nulos:,}")
    col4.metric("Filas duplicadas", f"{total_duplicados:,}")

    st.markdown("---")

    # --------------------------------------------------------
    # ANÁLISIS DE VALORES FALTANTES
    # --------------------------------------------------------

    st.subheader("Valores faltantes por variable")

    calidad = pd.DataFrame({

        "Variable": df.columns,

        "Valores faltantes": df.isna().sum().values,

        "Porcentaje de faltantes (%)": (
            df.isna().mean().values * 100
        ).round(2),

        "Tipo de dato": [
            str(df[col].dtype)
            for col in df.columns
        ],

        "Valores únicos": [
            df[col].nunique(dropna=True)
            for col in df.columns
        ]

    })

    calidad = calidad.sort_values(
        "Porcentaje de faltantes (%)",
        ascending=False
    )

    st.dataframe(
        calidad,
        use_container_width=True,
        hide_index=True
    )

    # Gráfico de faltantes

    faltantes = calidad[
        calidad["Valores faltantes"] > 0
    ].head(20)

    if not faltantes.empty:

        fig_faltantes = px.bar(
            faltantes.sort_values(
                "Porcentaje de faltantes (%)"
            ),
            x="Porcentaje de faltantes (%)",
            y="Variable",
            orientation="h",
            title="Variables con mayor porcentaje de valores faltantes",
            color_discrete_sequence=[VERDE_MEDIO]
        )

        fig_faltantes.update_layout(
            plot_bgcolor=BLANCO,
            paper_bgcolor=BLANCO
        )

        st.plotly_chart(
            fig_faltantes,
            use_container_width=True
        )

    else:

        st.success(
            "No se encontraron valores faltantes."
        )

    st.markdown("---")

    # --------------------------------------------------------
    # DUPLICADOS
    # --------------------------------------------------------

    st.subheader("Registros duplicados")

    if total_duplicados > 0:

        st.warning(
            f"Se encontraron {total_duplicados} filas duplicadas."
        )

        if st.checkbox(
            "Mostrar registros duplicados"
        ):

            duplicados = df[
                df.duplicated(keep=False)
            ]

            st.dataframe(
                duplicados,
                use_container_width=True
            )

    else:

        st.success(
            "No se encontraron filas completamente duplicadas."
        )

    st.markdown("---")

    # --------------------------------------------------------
    # SELECCIÓN DE VARIABLES PARA EDA
    # --------------------------------------------------------

    st.subheader("Análisis exploratorio de variables")

    st.write(
        """
        Selecciona hasta 50 variables para calcular
        estadísticas descriptivas. Todas las columnas
        permanecen disponibles en las demás secciones.
        """
    )

    variables_eda = st.multiselect(
        "Seleccionar variables",
        options=list(df.columns),
        default=list(
            df.columns[:min(10, len(df.columns))]
        ),
        max_selections=50
    )

    if variables_eda:

        resultados_eda = []

        for variable in variables_eda:

            serie = df[variable]

            valores_numericos = convertir_numerico(
                serie
            )

            cantidad_numerica = (
                valores_numericos.notna().sum()
            )

            # Se considera numérica cuando la columna
            # es numérica o al menos 80% de sus valores
            # no nulos se pueden convertir.

            proporcion_numerica = (
                cantidad_numerica / max(serie.notna().sum(), 1)
            )

            es_numerica = (
                pd.api.types.is_numeric_dtype(serie)
                or (
                    cantidad_numerica > 0
                    and proporcion_numerica >= 0.80
                )
            )

            categoria, descripcion, unidad = (
                obtener_info(variable)
            )

            if es_numerica:

                valores = valores_numericos.dropna()

                maximo = valores.max() if not valores.empty else "N/A"
                minimo = valores.min() if not valores.empty else "N/A"
                promedio = valores.mean() if not valores.empty else "N/A"
                desviacion = valores.std() if not valores.empty else "N/A"
                mediana = valores.median() if not valores.empty else "N/A"
                q1 = valores.quantile(0.25) if not valores.empty else "N/A"
                q3 = valores.quantile(0.75) if not valores.empty else "N/A"

                tipo = "Numérica"

                categorias = "N/A"

            else:

                maximo = "N/A"
                minimo = "N/A"
                promedio = "N/A"
                desviacion = "N/A"
                mediana = "N/A"
                q1 = "N/A"
                q3 = "N/A"

                tipo = (
                    "Categórica"
                    if serie.nunique(dropna=True) <= 50
                    else "Texto / alta cardinalidad"
                )

                categorias = ", ".join(
                    map(
                        str,
                        serie.dropna().unique()[:10]
                    )
                )

            resultados_eda.append({

                "Nombre de columna": variable,

                "Ubicación": (
                    f"Columna {df.columns.get_loc(variable) + 1}"
                ),

                "Tipo de dato": tipo,

                "Máximo": maximo,

                "Mínimo": minimo,

                "Promedio": promedio,

                "DS": desviacion,

                "Mediana": mediana,

                "Q1": q1,

                "Q3": q3,

                "Conteo": serie.nunique(dropna=True),

                "Categorías": categorias,

                "Nulos": int(serie.isna().sum())

            })

        tabla_eda = pd.DataFrame(
            resultados_eda
        )

        st.dataframe(
            tabla_eda,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ----------------------------------------------------
        # EXPORTACIÓN A EXCEL
        # ----------------------------------------------------

        st.subheader("Exportar resultados")

        archivo_excel = exportar_excel({

            "Datos originales": df_original,

            "EDA": tabla_eda,

            "Calidad de datos": calidad

        })

        st.download_button(

            "📥 Descargar informe EDA en Excel",

            data=archivo_excel,

            file_name="BIOPRODATA_informe_EDA.xlsx",

            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )

        )

    else:

        st.info(
            "Selecciona al menos una variable para realizar el EDA."
        )

    st.markdown("---")

    st.info(
        """
        **Criterio de procesamiento:** esta sección no reemplaza
        valores faltantes por cero ni elimina automáticamente
        registros o valores atípicos. Los datos originales
        se conservan para evitar modificaciones injustificadas.
        """
    )


# ============================================================
# SECCIÓN: DISTRIBUCIONES
# ============================================================

elif seccion == "Distribuciones":

    st.title("Distribuciones de variables")
    st.write("Explora la frecuencia de condiciones categóricas y la distribución de variables numéricas.")

    # Solo variables numéricas de significado bioprocesal; excluye IDs y códigos categóricos.
    numericas = [
        c for c in [
            "temp", "rxt_volume", "fermentation_time",
            "cs_conc1", "cs_conc2", "cs_conc3",
            "titer", "rate", "yield", "yield_o", "yield2",
            "yield_1", "yield_2", "yield_3", "bio_titre", "bio_growth_rate", "mw",
            "atp_cost", "nadh_nadph_cost"
        ]
        if c in df.columns
        and convertir_numerico(df[c]).notna().sum() >= 2
        and convertir_numerico(df[c]).nunique(dropna=True) > 1
    ]

    st.subheader("Distribución de variables numéricas")
    if numericas:
        variable_previa = st.session_state.get("dist_num_final", numericas[0])
        variable = selector_con_info(
            "Seleccionar variable numérica", numericas,
            variable_previa if variable_previa in numericas else numericas[0],
            "dist_num_final"
        )
        valores = convertir_numerico(df[variable]).dropna()

        if len(valores) >= 1:
            col_hist, col_stats = st.columns([1.65, 1])
            with col_hist:
                fig_hist = px.histogram(
                    x=valores, nbins=30,
                    title=f"Histograma de {nombre_visible(variable)}",
                    labels={"x": nombre_visible(variable), "count": "Frecuencia"},
                    color_discrete_sequence=[VERDE_MEDIO]
                )
                fig_hist.update_layout(
                    plot_bgcolor=BLANCO, paper_bgcolor=BLANCO,
                    xaxis_title=nombre_visible(variable), yaxis_title="Frecuencia"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            with col_stats:
                st.markdown("**Estadísticas descriptivas**")
                stats = valores.describe().rename({
                    "count": "n", "mean": "Promedio", "std": "Desv. estándar",
                    "min": "Mínimo", "25%": "Q1", "50%": "Mediana",
                    "75%": "Q3", "max": "Máximo"
                }).to_frame("Valor")
                st.dataframe(stats.round(4), use_container_width=True, height=330)
                st.caption(f"{len(valores):,} observaciones con dato de {len(df):,} registros.")

            with st.expander("📦 Consultar diagrama de caja y bigotes (boxplot)", expanded=False):
                st.write(
                    "Resume la mediana, los cuartiles, la dispersión y los valores atípicos. "
                    "No indica por sí solo cuál valor fue el más frecuente."
                )
                fig_box = px.box(
                    y=valores, points="outliers",
                    title=f"Diagrama de caja de {nombre_visible(variable)}",
                    labels={"y": nombre_visible(variable)},
                    color_discrete_sequence=[VERDE_MEDIO]
                )
                fig_box.update_layout(plot_bgcolor=BLANCO, paper_bgcolor=BLANCO)
                st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No hay observaciones numéricas disponibles.")
    else:
        st.warning("No se encontraron variables numéricas adecuadas.")

    st.markdown("---")
    st.subheader("Frecuencia de variables categóricas")
    categoricas = [
        c for c in ["media", "strain_background", "reactor_type", "oxygen",
                    "cs1", "cs2", "cs3", "product_name", "paper_number"]
        if c in df.columns and df[c].nunique(dropna=True) > 1
    ]
    if categoricas:
        categoria_previa = st.session_state.get("dist_cat_final", categoricas[0])
        var_cat = selector_con_info(
            "Seleccionar variable categórica", categoricas,
            categoria_previa if categoria_previa in categoricas else categoricas[0],
            "dist_cat_final"
        )
        frecuencias = (
            df[var_cat].fillna("Sin dato").astype(str).value_counts().head(25)
            .rename_axis(nombre_visible(var_cat)).reset_index(name="Frecuencia")
        )
        cchart, ctable = st.columns([1.8, 1])
        with cchart:
            fig_cat = px.bar(
                frecuencias.sort_values("Frecuencia", ascending=True),
                x="Frecuencia", y=nombre_visible(var_cat), orientation="h",
                title=f"Frecuencia de {nombre_visible(var_cat)}",
                color_discrete_sequence=[VERDE_MEDIO]
            )
            fig_cat.update_layout(
                plot_bgcolor=BLANCO, paper_bgcolor=BLANCO,
                xaxis_title="Número de registros",
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        with ctable:
            st.markdown("**Frecuencias**")
            st.dataframe(frecuencias, use_container_width=True, hide_index=True, height=330)
        st.caption(
            "La frecuencia corresponde a filas de la base de datos, no necesariamente a artículos únicos "
            "ni ensayos independientes."
        )
    else:
        st.warning("No se encontraron variables categóricas.")


# ============================================================

# SECCIÓN: RELACIONES ENTRE VARIABLES
# ============================================================

elif seccion == "Relaciones":

    st.title("Relaciones entre variables")
    st.write(
        "Explora asociaciones entre condiciones experimentales y resultados productivos. "
        "Estas relaciones son exploratorias y no demuestran causalidad."
    )

    numericas_rel = [
        c for c in [
            "temp", "rxt_volume", "fermentation_time",
            "cs_conc1", "cs_conc2", "cs_conc3",
            "titer", "rate", "yield", "yield_o", "yield2",
            "yield_1", "yield_2", "yield_3", "bio_titre", "bio_growth_rate", "mw"
        ]
        if c in df.columns
        and convertir_numerico(df[c]).notna().sum() >= 3
        and convertir_numerico(df[c]).nunique(dropna=True) > 1
    ]

    if len(numericas_rel) >= 2:
        st.subheader("Relación entre dos variables")
        c1, c2 = st.columns(2)
        x_def = "temp" if "temp" in numericas_rel else numericas_rel[0]
        y_def = "rate" if "rate" in numericas_rel else ("titer" if "titer" in numericas_rel else numericas_rel[1])

        with c1:
            vx_previo = st.session_state.get("rel_x_v3", x_def)
            vx = selector_con_info(
                "Variable del eje X", numericas_rel,
                vx_previo if vx_previo in numericas_rel else x_def,
                "rel_x_v3"
            )
        ys = [c for c in numericas_rel if c != vx]
        with c2:
            vy_previo = st.session_state.get("rel_y_v3", y_def)
            vy = selector_con_info(
                "Variable del eje Y", ys,
                vy_previo if vy_previo in ys else (y_def if y_def in ys else ys[0]),
                "rel_y_v3"
            )
        tendencia = st.checkbox("Mostrar línea de tendencia lineal", value=True, key="rel_tend_v3")

        data_rel = df.copy()
        data_rel["_x"] = convertir_numerico(data_rel[vx])
        data_rel["_y"] = convertir_numerico(data_rel[vy])
        data_rel = data_rel.dropna(subset=["_x", "_y"])

        # Filtros opcionales de contexto para no mezclar todos los estudios sin control.
        filtros_rel = [c for c in ["product_name", "paper_number", "strain_background"] if c in data_rel.columns]
        fcols = st.columns(len(filtros_rel)) if filtros_rel else []
        for ix, col in enumerate(filtros_rel):
            vals = opciones_columna(data_rel, col)
            with fcols[ix]:
                selected = st.selectbox(
                    f"Filtrar {nombre_visible(col)}", ["Todos"] + vals,
                    key=f"rel_ctx_{col}_v3"
                )
            if selected != "Todos":
                data_rel = data_rel[data_rel[col].astype(str) == selected]

        if len(data_rel) >= 3 and data_rel["_x"].nunique() > 1 and data_rel["_y"].nunique() > 1:
            fig_rel = px.scatter(
                data_rel, x="_x", y="_y",
                hover_data=filtros_rel,
                opacity=0.55,
                labels={"_x": nombre_visible(vx), "_y": nombre_visible(vy)},
                title=f"{nombre_visible(vy)} en función de {nombre_visible(vx)}",
                color_discrete_sequence=[VERDE_MEDIO]
            )
            if tendencia:
                coef = np.polyfit(data_rel["_x"], data_rel["_y"], 1)
                xline = np.linspace(data_rel["_x"].min(), data_rel["_x"].max(), 100)
                fig_rel.add_trace(go.Scatter(
                    x=xline, y=coef[0] * xline + coef[1],
                    mode="lines", name="Tendencia lineal",
                    line=dict(color=AZUL, width=2)
                ))
            fig_rel.update_layout(plot_bgcolor=BLANCO, paper_bgcolor=BLANCO)
            st.plotly_chart(fig_rel, use_container_width=True)

            pares = data_rel[["_x", "_y"]]
            r = pares.corr(method="pearson").iloc[0, 1]
            rho = pares.corr(method="spearman").iloc[0, 1]
            m1, m2, m3 = st.columns(3)
            m1.metric("Pares completos (n)", f"{len(pares):,}")
            m2.metric("Pearson (r)", f"{r:.3f}")
            m3.metric("Spearman (ρ)", f"{rho:.3f}")
            st.caption(
                "Pearson evalúa asociación lineal; Spearman evalúa asociación monotónica por rangos. "
                "La mezcla de artículos y condiciones puede influir en ambas medidas."
            )
        else:
            st.warning("No hay suficientes pares completos y variación en ambas variables para calcular correlaciones.")

        st.markdown("---")
        st.subheader("Mapa de calor de correlaciones")
        st.write(
            "Resume las asociaciones monotónicas entre las variables numéricas seleccionadas. "
            "No incluye variables categóricas ni códigos numéricos de categorías."
        )
        heat_vars = st.multiselect(
            "Variables para el mapa de calor",
            options=numericas_rel,
            default=[c for c in ["temp", "fermentation_time", "titer", "rate", "yield", "yield_o", "yield2", "yield_1", "yield_2", "yield_3"] if c in numericas_rel][:7],
            format_func=nombre_visible,
            max_selections=12,
            key="heatmap_v3"
        )
        if len(heat_vars) >= 2:
            hdata = pd.DataFrame({c: convertir_numerico(df[c]) for c in heat_vars})
            hcorr = hdata.corr(method="spearman", min_periods=5)
            fig_heat = px.imshow(
                hcorr, text_auto=".2f", zmin=-1, zmax=1,
                color_continuous_scale="RdYlGn", aspect="auto",
                title="Correlación de Spearman"
            )
            fig_heat.update_layout(paper_bgcolor=BLANCO, plot_bgcolor=BLANCO)
            st.plotly_chart(fig_heat, use_container_width=True)
            with st.expander("Ver número de observaciones utilizado en cada correlación"):
                n_pairs = hdata.notna().astype(int).T.dot(hdata.notna().astype(int))
                st.dataframe(n_pairs, use_container_width=True)
        else:
            st.info("Selecciona al menos dos variables para generar el mapa de calor.")
    else:
        st.warning("Se necesitan al menos dos variables numéricas adecuadas.")


# ============================================================

# SECCIÓN: ANÁLISIS Y COMPARACIÓN
# ============================================================

elif seccion == "Análisis y comparación":

    st.title("Análisis y comparación de diseños")
    st.write(
        "Compara las características de diseños experimentales y explora "
        "cómo las condiciones reportadas se relacionan con los resultados productivos."
    )

    if "product_name" not in df.columns:
        st.warning("No se encontró la columna product_name.")
    else:
        productos = opciones_columna(df, "product_name")
        producto = st.selectbox("Seleccionar producto", productos, key="producto_comparacion_v3")
        dp = df[df["product_name"].astype(str) == producto].copy()
        metricas = [
            c for c in METRICAS_PRODUCCION
            if c in dp.columns and convertir_numerico(dp[c]).notna().sum() >= 1
        ]
        n_papers = dp["paper_number"].nunique() if "paper_number" in dp.columns else 0

        st.subheader("Resumen del producto")
        a, b, c = st.columns(3)
        a.metric("Registros", f"{len(dp):,}")
        b.metric("Artículos", f"{n_papers:,}")
        c.metric("Métricas productivas disponibles", f"{len(metricas)}")
        st.caption(
            "Los registros son filas de la base y no necesariamente artículos o réplicas independientes. "
            "Una métrica que no aparece para este producto puede no haber sido reportada; no equivale a cero."
        )
        metricas_ausentes = [m for m in METRICAS_PRODUCCION if m in dp.columns and convertir_numerico(dp[m]).notna().sum() == 0]
        if metricas_ausentes:
            st.caption("Sin valores reportados para este producto: " + ", ".join(nombre_visible(m) for m in metricas_ausentes) + ".")

        st.markdown("---")
        st.subheader("Comparar diseños experimentales")
        st.write("Selecciona de dos a cinco registros del producto para comparar sus características y resultados.")
        dp = dp.reset_index(drop=True)
        dp["_id"] = dp.index
        dp["_label"] = dp.apply(
            lambda r: f"Registro {int(r['_id'])+1} · Artículo {r.get('paper_number','s/d')} · Cepa {str(r.get('strain_background','s/d'))[:35]}",
            axis=1
        )
        selected_ids = st.multiselect(
            "Diseños/experimentos", dp["_id"].tolist(),
            format_func=lambda k: dp.loc[k, "_label"],
            max_selections=5, key="designs_select_v3"
        )
        cols_exp = [
            "paper_number", "strain_background", "genes_modified", "gene_deletion",
            "gene_overexpression", "heterologous_gene", "cs1", "cs2", "cs3",
            "cs_conc1", "cs_conc2", "cs_conc3", "media", "temp", "oxygen",
            "reactor_type", "rxt_volume", "fermentation_time", "precursor",
            "enzyme_steps"
        ]
        cols_table = [c for c in cols_exp + metricas if c in dp.columns]
        if len(selected_ids) >= 2:
            chosen = dp[dp["_id"].isin(selected_ids)].copy()
            display = chosen[["_label"] + cols_table].rename(
                columns={"_label": "Diseño experimental", **{c: nombre_visible(c) for c in cols_table}}
            )
            st.dataframe(display, use_container_width=True, hide_index=True)
            metrics_chart = [m for m in metricas if convertir_numerico(chosen[m]).notna().sum() >= 2]
            if metrics_chart:
                met = st.selectbox("Resultado productivo para comparar", metrics_chart,
                                   format_func=nombre_visible, key="design_metric_v3")
                chart_data = chosen[["_label", met]].copy()
                chart_data[met] = convertir_numerico(chart_data[met])
                chart_data = chart_data.dropna(subset=[met])
                fig = px.bar(
                    chart_data, x="_label", y=met,
                    labels={"_label": "Diseño experimental", met: nombre_visible(met)},
                    title=f"Comparación de {nombre_visible(met)}",
                    color_discrete_sequence=[VERDE_MEDIO]
                )
                fig.update_layout(plot_bgcolor=BLANCO, paper_bgcolor=BLANCO, xaxis_tickangle=-25)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Los registros seleccionados no comparten suficientes valores para graficar una métrica.")
        else:
            st.info("Selecciona al menos dos registros para activar la comparación.")

        st.markdown("---")
        resumen_titulo, resumen_info = st.columns([0.92, 0.08], vertical_alignment="center")
        with resumen_titulo:
            st.subheader("Resumen de resultados productivos")
        with resumen_info:
            yields_disponibles = [m for m in metricas if m.startswith("yield")]
            if yields_disponibles:
                with st.popover("ℹ️", help="Consultar definiciones de las métricas de rendimiento"):
                    st.markdown("**Definiciones de rendimiento**")
                    for met in yields_disponibles:
                        _, descripcion, unidad = obtener_info(met)
                        st.markdown(f"**{nombre_visible(met)}**")
                        st.write(descripcion)
                        st.caption(f"Unidad o tipo: {unidad}")
        st.write(
            "Estadísticas de las métricas disponibles para el producto seleccionado. "
            "Para explorar la forma de una distribución, utiliza la pestaña Distribuciones."
        )
        resumen_metricas = []
        for met in metricas:
            vals = convertir_numerico(dp[met]).dropna()
            if not vals.empty:
                categoria, descripcion, unidad = obtener_info(met)
                resumen_metricas.append({
                    "Métrica": nombre_visible(met),
                    "n": int(vals.size),
                    "Promedio": vals.mean(),
                    "Mediana": vals.median(),
                    "Desv. estándar": vals.std() if vals.size > 1 else np.nan,
                    "Unidad / nota": unidad
                })
        if resumen_metricas:
            st.dataframe(
                pd.DataFrame(resumen_metricas).round(4),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No hay resultados productivos numéricos para este producto.")

        st.markdown("---")
        st.subheader("Condiciones experimentales frente a resultados productivos")
        st.write(
            "Compara la distribución de una métrica productiva entre las condiciones observadas. "
            "Se trata de una comparación descriptiva: no permite atribuir causalidad a una sola condición."
        )
        conditions = [
            c for c in [
                "temp", "media", "strain_background", "reactor_type",
                "oxygen", "cs1", "cs2", "cs3", "fermentation_time"
            ]
            if c in dp.columns and dp[c].nunique(dropna=True) >= 2 and dp[c].notna().sum() >= 4
        ]
        if conditions and metricas:
            c1, c2 = st.columns(2)
            with c1:
                condition_actual = st.session_state.get("condition_v4", conditions[0])
                condition = selector_con_info(
                    "Condición experimental", conditions,
                    condition_actual if condition_actual in conditions else conditions[0],
                    "condition_v4"
                )
            with c2:
                outcome_actual = st.session_state.get("outcome_v4", metricas[0])
                outcome = selector_con_info(
                    "Resultado productivo", metricas,
                    outcome_actual if outcome_actual in metricas else metricas[0],
                    "outcome_v4"
                )

            # Permite revisar el conjunto completo o aislar un artículo concreto.
            if "paper_number" in dp.columns:
                paper_options = ["Todos los artículos"] + opciones_columna(dp, "paper_number")
                paper_filter = st.selectbox(
                    "Filtrar por artículo (opcional)",
                    paper_options,
                    key="condition_paper_filter_v3"
                )
                if paper_filter != "Todos los artículos":
                    dp_condition = dp[dp["paper_number"].astype(str) == paper_filter].copy()
                else:
                    dp_condition = dp.copy()
            else:
                dp_condition = dp.copy()

            grouped = dp_condition[[condition, outcome]].copy()
            grouped["_outcome"] = convertir_numerico(grouped[outcome])
            grouped = grouped.dropna(subset=[condition, "_outcome"])
            grouped["_category"] = grouped[condition].astype(str).str.strip()

            # Categorías numéricas discretas como temperatura quedan agrupadas por valor exacto.
            if condition in ["temp", "rxt_volume", "fermentation_time"]:
                grouped["_category"] = grouped[condition].map(
                    lambda x: f"{float(x):g}" if pd.notna(x) else "Sin dato"
                )
            counts = grouped["_category"].value_counts()
            keep = counts[counts >= 2].head(15).index.tolist()
            grouped = grouped[grouped["_category"].isin(keep)]

            if grouped["_category"].nunique() >= 2:
                # Gráfico vertical de puntos agrupados (strip/beeswarm-like).
                # Es preferible al violín cuando hay grupos pequeños o desiguales:
                # no estima una densidad que podría resultar engañosa.
                orden_categorias = (
                    grouped.groupby("_category")["_outcome"]
                    .size().sort_values(ascending=False).index.tolist()
                )
                etiquetas_n = {
                    categoria: f"{categoria} (n={int((grouped['_category'] == categoria).sum())})"
                    for categoria in orden_categorias
                }
                grouped["_category_label"] = grouped["_category"].map(etiquetas_n)

                fig_cond = px.strip(
                    grouped,
                    x="_category_label",
                    y="_outcome",
                    hover_data={"_category": True, "_outcome": ":.4f"},
                    labels={
                        "_category_label": nombre_visible(condition),
                        "_outcome": nombre_visible(outcome)
                    },
                    title=f"{nombre_visible(outcome)} según {nombre_visible(condition)}",
                    category_orders={"_category_label": [etiquetas_n[x] for x in orden_categorias]},
                    color_discrete_sequence=[VERDE_MEDIO]
                )
                fig_cond.update_traces(
                    jitter=0.32,
                    pointpos=0,
                    marker={"size": 7, "opacity": 0.62, "line": {"width": 0.35, "color": "white"}},
                    name="Observaciones"
                )

                # Mediana por categoría, mostrada como diamante.
                medianas = (
                    grouped.groupby("_category_label", sort=False)["_outcome"]
                    .median().reindex([etiquetas_n[x] for x in orden_categorias])
                )
                fig_cond.add_trace(go.Scatter(
                    x=medianas.index.tolist(),
                    y=medianas.values.tolist(),
                    mode="markers",
                    name="Mediana",
                    marker={"symbol": "diamond", "size": 11, "color": AZUL,
                            "line": {"width": 1, "color": "white"}},
                    hovertemplate="Mediana: %{y:.4g}<extra></extra>"
                ))
                fig_cond.update_layout(
                    plot_bgcolor=BLANCO,
                    paper_bgcolor=BLANCO,
                    xaxis_tickangle=-25,
                    yaxis_title=nombre_visible(outcome),
                    xaxis_title=nombre_visible(condition),
                    legend_title_text=""
                )
                st.plotly_chart(fig_cond, use_container_width=True)
                summary = (
                    grouped.groupby("_category")["_outcome"]
                    .agg(n="count", promedio="mean", mediana="median", desviacion="std")
                    .reset_index()
                    .rename(columns={
                        "_category": nombre_visible(condition),
                        "promedio": "Promedio", "mediana": "Mediana",
                        "desviacion": "Desv. estándar"
                    })
                )
                st.dataframe(summary.round(4), use_container_width=True, hide_index=True)
                st.caption(
                    "Se muestran categorías con al menos dos registros. Las diferencias entre artículos, "
                    "cepas, medios y otros factores pueden explicar parte de la variación."
                )
            else:
                st.info("No hay al menos dos categorías con dos observaciones cada una para comparar distribuciones.")
        else:
            st.info("No hay suficientes condiciones y resultados para realizar esta comparación.")

        st.markdown("---")
        st.subheader("Comparación de resultados por artículo")
        if "paper_number" in dp.columns and metricas:
            metric_paper = st.selectbox(
                "Métrica productiva",
                metricas,
                format_func=nombre_visible,
                key="paper_metric_v4"
            )

            per_paper = dp[["paper_number", metric_paper]].copy()
            per_paper["_value"] = convertir_numerico(per_paper[metric_paper])
            per_paper = per_paper.dropna(subset=["paper_number", "_value"]).copy()

            # Los identificadores de artículos son categorías, no una escala numérica.
            per_paper["Artículo"] = per_paper["paper_number"].astype(str).str.strip()
            per_paper = per_paper[per_paper["Artículo"] != ""].copy()

            if not per_paper.empty:
                conteos = per_paper["Artículo"].value_counts()

                # Se muestran hasta 15 artículos con más observaciones.
                articulos_seleccionados = conteos.head(15).index.tolist()
                per_paper = per_paper[
                    per_paper["Artículo"].isin(articulos_seleccionados)
                ].copy()

                # Orden natural para identificadores numéricos; alfabético para los demás.
                def clave_orden_articulo(valor):
                    texto = str(valor)
                    if texto.isdigit():
                        return (0, int(texto))
                    return (1, texto.casefold())

                orden_ids = sorted(
                    per_paper["Artículo"].unique().tolist(),
                    key=clave_orden_articulo
                )

                conteos_visibles = per_paper["Artículo"].value_counts()
                etiquetas_articulos = {
                    articulo: (
                        f"Artículo {articulo} "
                        f"(n={int(conteos_visibles[articulo])})"
                    )
                    for articulo in orden_ids
                }

                per_paper["Artículo visible"] = per_paper["Artículo"].map(
                    etiquetas_articulos
                )

                orden_etiquetas = [
                    etiquetas_articulos[articulo] for articulo in orden_ids
                ]

                # Con n >= 4 se muestra boxplot; con n < 4 se muestran
                # únicamente los puntos individuales para no sugerir una
                # distribución robusta con muy pocas observaciones.
                conteos_por_articulo = per_paper["Artículo"].value_counts()
                ids_box = conteos_por_articulo[
                    conteos_por_articulo >= 4
                ].index.tolist()

                datos_box = per_paper[
                    per_paper["Artículo"].isin(ids_box)
                ].copy()

                datos_puntos = per_paper[
                    ~per_paper["Artículo"].isin(ids_box)
                ].copy()

                fig_paper = None

                if not datos_box.empty:
                    fig_paper = px.box(
                        datos_box,
                        x="Artículo visible",
                        y="_value",
                        points="all",
                        category_orders={
                            "Artículo visible": orden_etiquetas
                        },
                        title=(
                            f"Distribución de {nombre_visible(metric_paper)} "
                            "por artículo"
                        ),
                        labels={
                            "_value": nombre_visible(metric_paper),
                            "Artículo visible": "Artículo científico"
                        },
                        color_discrete_sequence=[VERDE_MEDIO]
                    )

                if not datos_puntos.empty:
                    fig_puntos = px.strip(
                        datos_puntos,
                        x="Artículo visible",
                        y="_value",
                        category_orders={
                            "Artículo visible": orden_etiquetas
                        },
                        labels={
                            "_value": nombre_visible(metric_paper),
                            "Artículo visible": "Artículo científico"
                        },
                        color_discrete_sequence=[AZUL]
                    )
                    fig_puntos.update_traces(
                        jitter=0.18,
                        pointpos=0,
                        marker={"size": 8, "opacity": 0.8},
                        name="Pocos registros (n < 4)"
                    )

                    if fig_paper is None:
                        fig_paper = fig_puntos
                    else:
                        fig_paper.add_traces(fig_puntos.data)

                if fig_paper is not None:
                    fig_paper.update_layout(
                        plot_bgcolor=BLANCO,
                        paper_bgcolor=BLANCO,
                        xaxis={
                            "type": "category",
                            "categoryorder": "array",
                            "categoryarray": orden_etiquetas,
                            "tickangle": -30,
                            "title": "Artículo científico"
                        },
                        yaxis_title=nombre_visible(metric_paper),
                        legend_title_text=""
                    )
                    st.plotly_chart(
                        fig_paper,
                        use_container_width=True
                    )

                    st.caption(
                        "Se muestran hasta 15 artículos con datos disponibles. "
                        "Los artículos con 4 o más observaciones se representan "
                        "con diagramas de caja y puntos individuales; los que "
                        "tienen menos de 4 se muestran solo como puntos. "
                        "Las etiquetas indican el número de registros (n)."
                    )
                else:
                    st.info(
                        "No hay observaciones suficientes para representar "
                        "esta métrica por artículo."
                    )
            else:
                st.info(
                    "No hay datos disponibles para la métrica seleccionada "
                    "en los artículos."
                )
        else:
            st.info(
                "No hay identificador de artículo o métricas productivas disponibles."
            )


# PIE DE PÁGINA
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#527C70;
        padding:10px;
        font-size:12px;
    ">
        BIOPRODATA | BioProcess & Biofactory Data Analytics
        <br>
        Análisis exploratorio y descriptivo de bioprocesos.
    </div>
    """,
    unsafe_allow_html=True
)
