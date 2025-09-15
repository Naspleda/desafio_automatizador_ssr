#!/bin/bash
# Ejecuta el ETL y guarda los resultados en la carpeta "respuestas/parte2"
OUTPUT_DIR="respuestas/parte2"

mkdir -p $OUTPUT_DIR

# Ejecutar el script de python con la carpeta de salida como argumento
# python3 main.py --output $OUTPUT_DIR
./venv/bin/python main.py --output $OUTPUT_DIR