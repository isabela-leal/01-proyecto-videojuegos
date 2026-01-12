"""
Utilidades para cargar y procesar datos
"""


def load_data():
    """
    Carga el dataset de videojuegos desde un archivo CSV limpio.
    
    Esta función localiza el archivo 'vgsales_clean.csv' en el directorio de datos
    del proyecto y lo carga en un DataFrame de pandas. Asegura que la columna 'Year'
    tenga el tipo de dato correcto (entero) para evitar problemas en análisis posteriores.

    Returns:
        pd.DataFrame: Dataset de videojuegos con todas las columnas disponibles,
                        incluyendo información de ventas por región, plataforma, género,
                        publisher y año de lanzamiento.
    """
    # Ruta al archivo de datos - navega desde el directorio actual hasta /data/
    data_path = Path(__file__).parent.parent.parent.parent / 'data' / 'vgsales_clean.csv'

    # Cargar datos desde el archivo CSV
    df = pd.read_csv(data_path)

    # Asegurar tipos de datos correctos - convertir Year a entero si existe
    if 'Year' in df.columns:
        df['Year'] = df['Year'].astype(int)

    return df

def get_data_info(df):
    """
    Obtiene información estadística básica y agregada del dataset de videojuegos.
    
    Calcula métricas importantes como totales, promedios y rangos que proporcionan
    una visión general del dataset completo.

    Args:
        df (pd.DataFrame): Dataset de videojuegos que debe contener las columnas:
                            'Global_Sales', 'Platform', 'Genre', 'Publisher', 'Year',
                            'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'

    Returns:
        dict: Diccionario con las siguientes claves:
                - total_games (int): Número total de juegos en el dataset
                - total_sales (float): Suma total de ventas globales en millones
                - avg_sales (float): Promedio de ventas por juego en millones
                - total_platforms (int): Número de plataformas únicas
                - total_genres (int): Número de géneros únicos
                - total_publishers (int): Número de publishers únicos
                - year_range (tuple): Tupla con (año_mínimo, año_máximo)
                - na_sales (float): Total de ventas en Norteamérica en millones
                - eu_sales (float): Total de ventas en Europa en millones
                - jp_sales (float): Total de ventas en Japón en millones
                - other_sales (float): Total de ventas en otras regiones en millones
    """
    info = {
        'total_games': len(df),
        'total_sales': df['Global_Sales'].sum(),
        'avg_sales': df['Global_Sales'].mean(),
        'total_platforms': df['Platform'].nunique(),
        'total_genres': df['Genre'].nunique(),
        'total_publishers': df['Publisher'].nunique(),
        'year_range': (int(df['Year'].min()), int(df['Year'].max())),
        'na_sales': df['NA_Sales'].sum(),
        'eu_sales': df['EU_Sales'].sum(),
        'jp_sales': df['JP_Sales'].sum(),
        'other_sales': df['Other_Sales'].sum()
    }

    return info

def filter_data(df, filters):
    """
    Filtra el dataset de videojuegos según múltiples criterios especificados.
    
    Aplica filtros de manera secuencial sobre una copia del dataset original,
    permitiendo combinaciones de diferentes criterios de filtrado.

    Args:
        df (pd.DataFrame): Dataset original de videojuegos sin modificar
        filters (dict): Diccionario con criterios de filtrado. Claves opcionales:
                        - 'year_range' (tuple): (año_min, año_max) para filtrar por rango de años
                        - 'genres' (list): Lista de géneros a incluir (ej: ['Action', 'Sports'])
                        - 'platforms' (list): Lista de plataformas a incluir (ej: ['PS4', 'Xbox'])
                        - 'publishers' (list): Lista de publishers a incluir
                        - 'regions' (list): Lista de regiones dominantes a incluir
                        - 'sales_categories' (list): Lista de categorías de ventas a incluir

    Returns:
        pd.DataFrame: Dataset filtrado que cumple con todos los criterios especificados.
                        Si no hay filtros, retorna una copia del dataset original.
    """
    # Crear copia para no modificar el DataFrame original
    filtered_df = df.copy()

    # Filtro por años - mantiene solo registros dentro del rango especificado
    if 'year_range' in filters and filters['year_range']:
        min_year, max_year = filters['year_range']
        filtered_df = filtered_df[
            (filtered_df['Year'] >= min_year) &
            (filtered_df['Year'] <= max_year)
        ]

    # Filtro por géneros - mantiene solo los géneros seleccionados
    if 'genres' in filters and filters['genres']:
        filtered_df = filtered_df[filtered_df['Genre'].isin(filters['genres'])]

    # Filtro por plataformas - mantiene solo las plataformas seleccionadas
    if 'platforms' in filters and filters['platforms']:
        filtered_df = filtered_df[filtered_df['Platform'].isin(filters['platforms'])]

    # Filtro por publishers - mantiene solo los publishers seleccionados
    if 'publishers' in filters and filters['publishers']:
        filtered_df = filtered_df[filtered_df['Publisher'].isin(filters['publishers'])]

    # Filtro por región dominante - región con mayores ventas para cada juego
    if 'regions' in filters and filters['regions']:
        filtered_df = filtered_df[filtered_df['Dominant_Region'].isin(filters['regions'])]

    # Filtro por categoría de ventas - clasificación según volumen de ventas
    if 'sales_categories' in filters and filters['sales_categories']:
        filtered_df = filtered_df[filtered_df['Sales_Category'].isin(filters['sales_categories'])]

    return filtered_df

def get_top_n(df, column, n=10, agg_column='Global_Sales', agg_func='sum'):
    """
    Obtiene los top N elementos de una columna basado en una función de agregación.
    
    Agrupa el dataset por la columna especificada y calcula el ranking de los
    mejores N elementos según la función de agregación elegida.

    Args:
        df (pd.DataFrame): Dataset de videojuegos a analizar
        column (str): Nombre de la columna por la cual agrupar los datos
                        (ej: 'Platform', 'Genre', 'Publisher')
        n (int, optional): Número de elementos top a retornar. Por defecto 10
        agg_column (str, optional): Columna sobre la cual aplicar la agregación.
                                    Por defecto 'Global_Sales'
        agg_func (str, optional): Función de agregación a aplicar. Opciones:
                                    - 'sum': Suma total de valores
                                    - 'mean': Promedio de valores
                                    - 'count': Conteo de ocurrencias
                                    Por defecto 'sum'

    Returns:
        pd.DataFrame: DataFrame con los top N elementos ordenados de mayor a menor.
                        Columnas: [column, agg_column] o [column, 'count'] si agg_func='count'
    """
    # Suma total de valores y obtiene los N mayores
    if agg_func == 'sum':
        result = df.groupby(column)[agg_column].sum().nlargest(n).reset_index()
    # Promedio de valores y obtiene los N mayores
    elif agg_func == 'mean':
        result = df.groupby(column)[agg_column].mean().nlargest(n).reset_index()
    # Conteo de ocurrencias y obtiene los N más frecuentes
    elif agg_func == 'count':
        result = df[column].value_counts().head(n).reset_index()
        result.columns = [column, 'count']

    return result

def calculate_regional_percentage(df):
    """
    Calcula el porcentaje de ventas que representa cada región respecto al total global.
    
    Útil para visualizar la distribución geográfica de las ventas y determinar
    qué regiones tienen mayor peso en el mercado de videojuegos.

    Args:
        df (pd.DataFrame): Dataset de videojuegos que debe contener las columnas:
                            'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'

    Returns:
        dict: Diccionario con los porcentajes de ventas por región:
                - 'Norteamérica' (float): Porcentaje de ventas en Norteamérica (0-100)
                - 'Europa' (float): Porcentaje de ventas en Europa (0-100)
                - 'Japón' (float): Porcentaje de ventas en Japón (0-100)
                - 'Otros' (float): Porcentaje de ventas en otras regiones (0-100)
                La suma de todos los porcentajes debe ser aproximadamente 100%
    """
    # Calcular total de ventas globales para el cálculo de porcentajes
    total = df['Global_Sales'].sum()

    # Calcular porcentaje de cada región respecto al total
    percentages = {
        'Norteamérica': (df['NA_Sales'].sum() / total * 100),
        'Europa': (df['EU_Sales'].sum() / total * 100),
        'Japón': (df['JP_Sales'].sum() / total * 100),
        'Otros': (df['Other_Sales'].sum() / total * 100)
    }

    return percentages
