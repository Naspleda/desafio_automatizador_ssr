import argparse
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # ajustar si en tu docker-compose usas otra pass
        database="boxer_db"
    )

def export_to_csv(df, filename, output_dir):
    path = f"{output_dir}/{filename}.csv"
    df.to_csv(path, index=False)
    print(f"✅ CSV generado: {path}")

def main(output_dir):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Repuestos Autofix no actualizados en el último mes
    query1 = """
        SELECT r.codigo, r.descripcion, m.nombre AS marca, r.precio, p.nombre AS proveedor, a.fecha AS ultima_actualizacion
        FROM Repuesto r
        JOIN Marca m ON r.id_marca = m.id
        JOIN Proveedor p ON r.proveedor_id = p.id
        JOIN Actualizacion a ON r.id_ultima_actualizacion = a.id
        WHERE p.nombre = 'Autofix'
        AND a.fecha < CURDATE() - INTERVAL 1 MONTH;
    """
    df1 = pd.read_sql(query1, conn)
    export_to_csv(df1, "autofix_no_actualizados", output_dir)

    # 2. Incremento 15% en marcas específicas
    query2 = """
        SELECT r.codigo, r.descripcion, m.nombre AS marca, r.precio,
               ROUND(r.precio * 1.15, 2) AS nuevo_precio
        FROM Repuesto r
        JOIN Marca m ON r.id_marca = m.id
        WHERE m.nombre IN ('ELEXA', 'BERU', 'SH', 'MASTERFILT', 'RN');
    """
    df2 = pd.read_sql(query2, conn)
    export_to_csv(df2, "incremento_15_marcas", output_dir)

    # 3. Recargo 30% para AutoRepuestos Express y Automax con precio entre 50k y 100k
    query3 = """
        SELECT r.codigo, r.descripcion, m.nombre AS marca, r.precio, p.nombre AS proveedor,
               ROUND(r.precio * 1.30, 2) AS precio_recargo
        FROM Repuesto r
        JOIN Marca m ON r.id_marca = m.id
        JOIN Proveedor p ON r.proveedor_id = p.id
        WHERE p.nombre IN ('AutoRepuestos Express', 'Automax')
        AND r.precio > 50000 AND r.precio < 100000;
    """
    df3 = pd.read_sql(query3, conn)
    export_to_csv(df3, "recargo_30_express_automax", output_dir)

    # 4. Resumen por proveedor
    query4 = """
        SELECT p.nombre AS proveedor,
               COUNT(r.id) AS total_repuestos,
               SUM(CASE WHEN (r.descripcion IS NULL OR r.descripcion = '') THEN 1 ELSE 0 END) AS sin_descripcion,
               MAX(r.precio) AS repuesto_mas_caro
        FROM Repuesto r
        JOIN Proveedor p ON r.proveedor_id = p.id
        GROUP BY p.id;
    """
    df4 = pd.read_sql(query4, conn)

    # 4.2 Promedio por marca
    query5 = """
        SELECT m.nombre AS marca, ROUND(AVG(r.precio), 2) AS promedio_precio
        FROM Repuesto r
        JOIN Marca m ON r.id_marca = m.id
        GROUP BY m.id;
    """
    df5 = pd.read_sql(query5, conn)

    export_to_csv(df4, "resumen_por_proveedor", output_dir)
    export_to_csv(df5, "promedio_por_marca", output_dir)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL para listas de precios")
    parser.add_argument("--output", required=True, help="Carpeta de salida para los CSVs")
    args = parser.parse_args()

    main(args.output)
