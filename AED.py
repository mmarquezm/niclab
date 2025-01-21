# -*- coding: utf-8 -*-
"""
@author: Moira Márquez
#ASUNTO: NIC LABS

#I. ANÁLISIS EXPLORATORIO DE LAS VARIABLES

¿Qué tenemos?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general de gráficos
plt.style.use('ggplot')
sns.set_theme()

# 1. CARGA DE DATOS
ruta_csv_clientes = 'C:/Users/FEN/Desktop/NIC LABS/ventas_DocumentoIdentidad_202409042235.csv'

try:
    clientes_df = pd.read_csv(ruta_csv_clientes, encoding='utf-8', sep=None, engine='python')
    print("Archivo cargado correctamente con codificación UTF-8.")
except UnicodeDecodeError:
    clientes_df = pd.read_csv(ruta_csv_clientes, encoding='latin1', sep=None, engine='python')
    print("Archivo cargado correctamente con codificación Latin-1.")
except Exception as e:
    print(f"Error al cargar el archivo: {e}")

# 2. FUNCIÓN PARA CORREGIR CARACTERES ESPECIALES Y ESTANDARIZAR 'ÑUÑOA'
def corregir_caracteres(texto):
    if pd.isnull(texto):
        return texto
    reemplazos = {
        'Ã‘': 'Ñ', 'Ã±': 'ñ',
        'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'ÃÁ': 'Á', 'Ã‰': 'É', 'ÃÍ': 'Í', 'Ã“': 'Ó', 'Ãš': 'Ú',
        'Ã¼': 'ü', 'Ãœ': 'Ü'
    }
    for mal, bien in reemplazos.items():
        texto = str(texto).replace(mal, bien)
    # Estandarizar 'Ñuñoa'
    if 'Ñuñoa' in texto or 'Ã±uÃ±oa' in texto or 'NuÃ±oa' in texto:
        return 'Ñuñoa'
    return texto

columnas_a_corregir = ['Comuna', 'Nombre o razon social', 'Pais', 'Tipo persona']
for col in columnas_a_corregir:
    clientes_df[col] = clientes_df[col].apply(corregir_caracteres)

print("\nCorrección de caracteres especiales realizada. Comuna 'Ñuñoa' estandarizada.")

# Identificar columnas con valores nulos y su cantidad
nulos_por_columna = clientes_df.isnull().sum()
print("\nColumnas con valores nulos y su cantidad:")
display(nulos_por_columna[nulos_por_columna > 0].sort_values(ascending=False))

# 3. EXPLORACIÓN ORDENADA POR COLUMNA

# 1. Fecha de Pago
display("\n#1. Fecha de Pago")
if clientes_df['Fecha pago'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Fecha pago'].isnull()])
else:
    display("No hay valores nulos.")

plt.figure(figsize=(10, 5))
clientes_df['Fecha pago'] = pd.to_datetime(clientes_df['Fecha pago'], errors='coerce', dayfirst=True)
clientes_df['Fecha pago'].dt.year.value_counts().sort_index().plot(kind='bar')
plt.title('Distribución de Pagos por Año')
plt.xlabel('Año')
plt.ylabel('Cantidad de Pagos')
plt.show()

# 2. Nombre o Razón Social
display("\n#2. Nombre o Razón Social")
duplicados_rut = clientes_df.groupby('Documento identidad')['Nombre o razon social'].nunique()
display("RUT asociados a más de un nombre o razón social:")
display(duplicados_rut[duplicados_rut > 1])

if clientes_df['Nombre o razon social'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Nombre o razon social'].isnull()])
else:
    display("No hay valores nulos.")

# 3. Tipo de Persona
display("\n#3. Tipo de Persona")
display("Valores únicos:")
display(sorted(clientes_df['Tipo persona'].dropna().unique()))

if clientes_df['Tipo persona'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Tipo persona'].isnull()])
else:
    display("No hay valores nulos.")

plt.figure(figsize=(6, 4))
clientes_df['Tipo persona'].value_counts().plot(kind='bar')
plt.title('Distribución por Tipo de Persona')
plt.xlabel('Tipo de Persona')
plt.ylabel('Cantidad')
plt.show()

# 4. País
display("\n#4. País")
display("Valores únicos:")
display(sorted(clientes_df['Pais'].dropna().unique()))

if clientes_df['Pais'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Pais'].isnull()])
else:
    display("No hay valores nulos.")

plt.figure(figsize=(10, 5))
clientes_df['Pais'].value_counts().plot(kind='bar')
plt.title('Distribución de Países')
plt.xlabel('País')
plt.ylabel('Cantidad')
plt.show()

# 5. Tipo Documento Identidad
display("\n#5. Tipo Documento Identidad")
display("Valores únicos:")
display(sorted(clientes_df['Tipo documento identidad'].dropna().unique()))

if clientes_df['Tipo documento identidad'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Tipo documento identidad'].isnull()])
else:
    display("No hay valores nulos.")

# 6. Documento Identidad
display("\n#6. Documento Identidad")
if clientes_df['Documento identidad'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Documento identidad'].isnull()])
else:
    display("No hay valores nulos.")

# 7. País Documento Identidad
display("\n#7. País Documento Identidad")
display("Valores únicos:")
display(sorted(clientes_df['Pais documento identidad'].dropna().unique()))

if clientes_df['Pais documento identidad'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Pais documento identidad'].isnull()])
else:
    display("No hay valores nulos.")

plt.figure(figsize=(10, 5))
clientes_df['Pais documento identidad'].value_counts().plot(kind='bar')
plt.title('Distribución de País Documento Identidad')
plt.xlabel('País Documento Identidad')
plt.ylabel('Cantidad')
plt.show()

# 8. Región
display("\n#8. Región")
display("Valores únicos:")
display(sorted(clientes_df['Region'].dropna().unique()))

if clientes_df['Region'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Region'].isnull()])
else:
    display("No hay valores nulos.")

# 9. Comuna
display("\n#9. Comuna")
display("Top 20 comunas:")
display(clientes_df['Comuna'].value_counts().head(20))

if clientes_df['Comuna'].isnull().any():
    display("Valores nulos:")
    display(clientes_df[clientes_df['Comuna'].isnull()])
else:
    display("No hay valores nulos.")

# 10. Moneda
display("\n#10. Moneda")
display("Valores únicos:")
display(sorted(clientes_df['Moneda'].dropna().unique()))

# 11. Dominio
display("\n#11. Dominio")
display("Top 10 dominios:")
display(clientes_df['Dominio'].value_counts().head(10))

# 12. Monto
display("\n#12. Monto")
display("Resumen estadístico de montos:")
display(clientes_df['Monto'].describe())

# Identificación de outliers en monto
plt.figure(figsize=(8, 5))
sns.boxplot(x=clientes_df['Monto'])
plt.title('Outliers en Monto')
plt.xlabel('Monto')
plt.show()

# 13. Tarifa
display("\n#13. Tarifa")
display("Valores únicos:")
display(sorted(clientes_df['Tarifa'].dropna().unique()))

# Identificación de duplicados
display("\nDuplicados en Documento identidad y Fecha pago:")
duplicados = clientes_df.duplicated(subset=['Documento identidad', 'Fecha pago'], keep=False)
display(clientes_df[duplicados])

# GUARDAR DATASET PROCESADO
ruta_guardado = 'C:/Users/FEN/Desktop/NIC LABS/ventas_aed.csv'
clientes_df.to_csv(ruta_guardado, index=False, encoding='utf-8')
print(f"Dataset guardado exitosamente en {ruta_guardado}.")

# Región - Numérica discreta
plt.figure(figsize=(8, 5))
clientes_df['Region'] = clientes_df['Region'].astype('Int64')
clientes_df['Region'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribución de Clientes por Región')
plt.xlabel('Región')
plt.ylabel('Cantidad')
plt.show()

# Comuna - Categórica
plt.figure(figsize=(10, 5))
clientes_df['Comuna'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Comunas con más Clientes')
plt.xlabel('Comuna')
plt.ylabel('Cantidad')
plt.show()

# Moneda - Categórica
plt.figure(figsize=(6, 4))
clientes_df['Moneda'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribución de Moneda')
plt.ylabel('')
plt.show()

# Monto - Numérica continua
plt.figure(figsize=(8, 5))
sns.histplot(clientes_df['Monto'], bins=30, kde=True)
plt.title('Distribución de Montos de Pago')
plt.xlabel('Monto')
plt.ylabel('Frecuencia')
plt.show()

# Tarifa - Numérica discreta
plt.figure(figsize=(8, 5))
clientes_df['Tarifa'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribución de Tarifas')
plt.xlabel('Tarifa')
plt.ylabel('Cantidad')
plt.show()

# Dominio - Categórica (Top 10 más frecuentes)
plt.figure(figsize=(10, 5))
clientes_df['Dominio'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Dominios más Frecuentes')
plt.xlabel('Dominio')
plt.ylabel('Cantidad')
plt.show()

