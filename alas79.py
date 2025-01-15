import pandas as pd

# Ruta del archivo Excel
input_file = r"C:\Users\FEN\Downloads\CALIDAD DE VIDA (2).xlsx"

# Diccionario de mapeo de identificadores de regiones a números de región
region_identifiers = {
    1: ['arap', '1'],
    2: ['antof', '2'],
    3: ['acama', '3'],
    4: ['quimbo', '4'],
    5: ['alpara', '5'],
    6: ['ernado', '6'],
    7: ['aule', '7'],
    8: ['iob', '8'],
    9: ['raucan', '9'],
    10: ['ago', '10'],
    11: ['sen', '11'],
    12: ['agall', '12'],
    13: ['antiag', '13'],
    14: ['osR', 'osr', '14'],
    15: ['icay', '15'],
    16: ['ubl', '16']
}

# Función para identificar el número de región basado en fragmentos de texto o números
def identify_region(region_name):
    if pd.isna(region_name):
        return None  # Si la región es NaN, devolver None
    region_name = str(region_name).strip().lower()
    for region_number, fragments in region_identifiers.items():
        if any(fragment in region_name for fragment in fragments):
            return region_number
    return None  # Si no se encuentra un match, devolver None

# Función para encontrar la primera fila con datos
def find_first_non_empty_row(df):
    # Encuentra la primera fila que no esté completamente vacía
    for i, row in df.iterrows():
        if not row.isnull().all():
            return i
    return None

# Leer todas las hojas del archivo Excel
all_sheets = pd.ExcelFile(input_file).sheet_names

# Lista para almacenar los DataFrames reestructurados de cada hoja
all_data_reshaped = []

# Procesar cada hoja
for sheet_name in all_sheets:
    # Leer la hoja para encontrar la primera fila con datos
    df_preview = pd.read_excel(input_file, sheet_name=sheet_name, header=None)
    first_row_with_data = find_first_non_empty_row(df_preview)
    
    if first_row_with_data is not None:
        # Leer los datos a partir de la primera fila con datos
        df = pd.read_excel(input_file, sheet_name=sheet_name, header=None, skiprows=first_row_with_data)
        
        # La primera fila (0) contiene los años
        years = df.iloc[0, 1:].values  # Obtener años desde la segunda columna
        
        # Filtrar solo las columnas que correspondan a los años válidos
        years_str = []
        valid_years = [str(year) for year in range(2014, 2023)]  # Años válidos: 2014 a 2022
        
        for year in years:
            try:
                year_str = str(int(year))
                if year_str in valid_years:
                    years_str.append(year_str)
                else:
                    years_str.append('')
            except ValueError:
                # Si no se puede convertir a entero, agregar una cadena vacía
                years_str.append('')
        
        year_columns = [i+1 for i, year in enumerate(years_str) if year]
        
        if not year_columns:
            # Si no hay datos válidos, añadir una columna vacía con el nombre de la hoja
            empty_df = pd.DataFrame(columns=['Región', 'Año', sheet_name])
            empty_df['Región'] = []
            empty_df['Año'] = []
            empty_df[sheet_name] = []
            all_data_reshaped.append(empty_df)
            continue

        # Filtrar y reestructurar los datos
        filtered_df = df.iloc[1:, [0] + year_columns]  # Seleccionar la columna de región y las columnas de años válidos
        
        # Reestructurar el DataFrame para cada hoja
        reshaped_data = []
        for region_index in range(len(filtered_df)):
            if region_index >= 17:  # Detener en la fila 17 (index 16)
                break

            region = filtered_df.iloc[region_index, 0]  # Región de la primera columna (A)
            region_number = identify_region(region)
            
            if region_number is None:
                print(f"Advertencia: No se pudo mapear la región '{region}' en la hoja '{sheet_name}'")
                continue

            for year_index, col_index in enumerate(year_columns):
                year = years_str[col_index - 1]  # Año como cadena
                value = filtered_df.iloc[region_index, year_index + 1]  # Obtener el valor correspondiente
                reshaped_data.append([region_number, year, value])  # Añadir la fila reestructurada
        
        # Convertir la lista de filas en un DataFrame para la hoja actual
        df_reshaped = pd.DataFrame(reshaped_data, columns=['Región', 'Año', sheet_name])
        
        # Añadir el DataFrame de la hoja actual a la lista
        all_data_reshaped.append(df_reshaped)
    else:
        print(f"No se encontró ninguna fila con datos en la hoja '{sheet_name}'")

# Concatenar todos los DataFrames en uno solo
df_final = pd.concat(all_data_reshaped, axis=0, ignore_index=True)

# Guardar el DataFrame final en un nuevo archivo Excel
output_file = r'C:\Users\FEN\Desktop\tabla_reestructurada_multiple.xlsx'  # Ruta del archivo de salida
df_final.to_excel(output_file, index=False)

print(f"\nArchivo reestructurado guardado como {output_file}")
