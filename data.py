import pandas as pd
import os
from datetime import datetime
import requests

# ===============================
# CONFIGURACIÓN
# ===============================
API_URL = "https://desafio.somosait.com/api/upload/"
OUTPUT_DIR = "downloads"

# Fecha actual para nombre de archivos
FECHA_HOY = datetime.now().strftime("%Y%m%d")


# ===============================
# FUNCIONES AUXILIARES
# ===============================
def limpiar_precio(valor):
    """Convierte precio a número válido con punto decimal y sin separador de miles."""
    try:
        # Eliminar comas o puntos de miles
        valor = str(valor).replace(",", "").replace(" ", "")
        return float(valor)
    except:
        return None


def limitar_descripcion(desc):
    """Limita a 100 caracteres la descripción."""
    if pd.isna(desc):
        return ""
    return str(desc)[:100]


def guardar_archivo(df, proveedor):
    """Guarda el DataFrame en formato estandarizado .xlsx"""
    filename = f"{proveedor}_{FECHA_HOY}.xlsx"
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_excel(filepath, index=False)
    return filepath


def subir_api(filepath):
    """Sube el archivo a la API en form-data"""
    with open(filepath, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
    print("Respuesta API:", response.status_code, response.text)


# ===============================
# PROCESAMIENTO AUTOFiX
# ===============================
def procesar_autofix(filepath):
    """Procesa Autofix con múltiples hojas (una por marca)"""
    xls = pd.ExcelFile(filepath)
    all_data = []

    for hoja in xls.sheet_names:
        df = pd.read_excel(filepath, sheet_name=hoja)

        # Estandarización
        df_estandar = pd.DataFrame()
        df_estandar["CODIGO"] = df["CODIGO"]
        df_estandar["DESCRIPCION"] = df["DESCR"].astype(str).apply(limitar_descripcion)
        df_estandar["MARCA"] = hoja  # nombre de la hoja = marca
        df_estandar["PRECIO"] = df["PRECIO"].apply(limpiar_precio)

        all_data.append(df_estandar)

    df_final = pd.concat(all_data, ignore_index=True)
    filepath = guardar_archivo(df_final, "Autofix")
    print(f"1 Archivo guardado en: {filepath}")
    subir_api(filepath)


# ===============================
# PROCESAMIENTO AUTO REPUESTOS EXPRESS (XLSX)
# ===============================
def procesar_express_xlsx(filepath):
    df = pd.read_excel(filepath, sheet_name=0, skiprows=10)  # datos arrancan en fila 11

    df_estandar = pd.DataFrame()
    df_estandar["CODIGO"] = df["CODIGO PROVEEDOR"]
    df_estandar["DESCRIPCION"] = (
        df["DESCRIPCION"].astype(str) + " " + df["RUBRO"].astype(str)
    ).apply(limitar_descripcion)
    df_estandar["MARCA"] = df["MARCA"]
    df_estandar["PRECIO"] = df["PRECIO DE LISTA"].apply(limpiar_precio)

    filepath = guardar_archivo(df_estandar, "AutoRepuestosExpressXLSX")
    print(f"2 Archivo guardado en: {filepath}")
    subir_api(filepath)


# ===============================
# PROCESAMIENTO AUTO REPUESTOS EXPRESS (CSV)
# ===============================
def procesar_express_csv(filepath):
    print(f"===> Leyendo archivo CSV: {filepath}")
    df = pd.read_csv(filepath, sep=";", encoding="utf-8")

    # Normalizar columnas a minúsculas sin espacios ni tildes
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(".", "", regex=False)
        .str.replace("ó", "o")
        .str.replace("í", "i")
    )
    if "cod_articulo" in df.columns:
        codigo_col = "cod_articulo"
    elif "cod" in df.columns:
        codigo_col = "cod"
    else:
        raise KeyError("No se encontró la columna de código ('cod_articulo' o 'cod') en el CSV.")

    df_estandar = pd.DataFrame()
    df_estandar["CODIGO"] = df[codigo_col]
    df_estandar["DESCRIPCION"] = (
        df["descripcion"].astype(str) + " " + df["rubro"].astype(str)
    ).apply(limitar_descripcion)
    df_estandar["MARCA"] = df["marca"]
    df_estandar["PRECIO"] = df["importe"].apply(limpiar_precio)

    filepath = guardar_archivo(df_estandar, "AutoRepuestosExpressCSV")
    print(f"3 Archivo guardado en: {filepath}")
    subir_api(filepath)


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    # Rutas a los archivos descargados
    autofix_file = os.path.join(OUTPUT_DIR, "AutoFix Repuestos.xlsx")
    express_xlsx_file = os.path.join(OUTPUT_DIR, "AutoRepuestos Express.xlsx")
    express_csv_file = os.path.join(OUTPUT_DIR, "AutoRepuestos Express Lista de Precios.csv")

    # Procesar cada uno
    if os.path.exists(autofix_file):
        procesar_autofix(autofix_file)

    if os.path.exists(express_xlsx_file):
        procesar_express_xlsx(express_xlsx_file)

    if os.path.exists(express_csv_file):
        procesar_express_csv(express_csv_file)
