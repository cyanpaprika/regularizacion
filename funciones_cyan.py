from prettytable import PrettyTable
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm




def informacion_df(df, orden="Tipo de Dato"):    
    print(f'Numero de filas:  {df.shape[0]}')
    print(f'Numero de columnas:  {df.shape[1]}')
    x = PrettyTable()
    x.field_names = ["Columnas", "Valores unicos", "Valores Nulos","Moda","Moda %", "Tipo de Dato", "Valores"]
    for col in df.columns:
        x.add_row([col, len(df[col].unique()), f'{(((df[col].isnull().sum()) /len(df))*100).round(1)}%'
        , f'{df[col].value_counts().index[0]}'
        , f'{((df[col].value_counts().iloc[0]/len(df))*100).round(1)}%'
        , df[col].dtype, df[col].unique()[0:2]])
    x.sortby = orden
    print(x)   


def getc_nulas(df,pctje):
    lista= []
    for col in df.columns:
        if (((df[col].isnull().sum()) /len(df)))>pctje:
            lista.append(col)
    return lista  

def getc_saturadas(df,pctje):
    lista= []
    for col in df.columns:
        if ((df[col].value_counts().iloc[0]/len(df)))>pctje:
            lista.append(col)
    return lista  


def busca_y_muestra_lineas(nombre_archivo, texto_a_buscar, n=5):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

        for indice, linea in enumerate(lineas):
            if texto_a_buscar in linea:
                print(f"Texto encontrado en la línea {indice + 1}. Mostrando las siguientes {n} líneas:\n")
                for linea_extra in lineas[indice: indice + n + 1]:  # +1 para incluir la línea de la coincidencia.
                    print(linea_extra, end='')
                print("\n" + "-"*40)  # Separador
                return 
        
        print("Texto no encontrado.")
        return 
#getc_numericas
def getc_numericas(df):
    return df.select_dtypes(include=['float64', 'int64']).columns

#getc_cadenas
def getc_cadenas(df):
    return df.select_dtypes(include=['object']).columns

#getc_dummies
def getc_dummies(df):
    return df.select_dtypes(include=['uint8']).columns

#Graficos

def gboxplot(df, columnas,ncol=5):
    # Calcular el número de filas que se necesitan para mostrar todos los gráficos en 5 columnas
    num_filas = -(-len(columnas) // ncol)  # Es igual a ceil(len / 5)

    # Configurar el diseño de la figura para mostrar los boxplots
    plt.figure(figsize=(5*ncol, ncol * num_filas))  # Ajustar el ancho para 5 columnas

    # Iterar a través de las columnas numéricas y crear boxplots
    for i, columna in enumerate(columnas):
        plt.subplot(num_filas, ncol, i+1)  # Cambiar el número de columnas a 5
        plt.boxplot(df[columna].dropna(), vert=True, patch_artist=True)  # Añadir .dropna() para evitar errores con NaN
        plt.title(f'Boxplot de {columna}')
        plt.ylabel(columna)

    # Ajustar el diseño y mostrar los boxplots
    plt.tight_layout()
    plt.show()


def gbarras(df, columnas, ncol=5):
    # Calcular el número de filas que se necesitan para mostrar todos los gráficos en 5 columnas
    num_filas = -(-len(columnas) // ncol)  # Es igual a ceil(len / 5)

    # Configurar el diseño de la figura para mostrar los countplots
    plt.figure(figsize=(5*ncol, ncol * num_filas))

    # Iterar a través de las columnas categóricas y crear countplots
    for i, col in enumerate(columnas):
        plt.subplot(num_filas, ncol, i+1)  # Cambiar el número de columnas a 5
        sns.countplot(data=df, x=col, order=df[col].value_counts().index)  # Usamos value_counts().index para ordenar
        plt.title(f'Countplot de {col}')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=90)  # Girar las etiquetas del eje x para mejor visibilidad

    # Ajustar el diseño y mostrar los countplots
    plt.tight_layout()
    plt.show()


def ghistograma(df, columnas, ncol=5):
    # Calcular el número de filas que se necesitan para mostrar todos los gráficos en 5 columnas
    num_filas = -(-len(columnas) // ncol)  # Es igual a ceil(len / 5)

    # Configurar el diseño de la figura para mostrar los histogramas
    plt.figure(figsize=(4*ncol, ncol * num_filas))  # Ajustar el ancho a 20 para 5 columnas

    # Iterar a través de las columnas numéricas y crear histogramas
    for i, col in enumerate(columnas, 1):
        plt.subplot(num_filas, ncol, i)
        plt.hist(df[col].dropna(), bins=20, edgecolor='k')  # Añadir .dropna() para evitar errores con NaN
        plt.title(f'Histograma de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')

    # Ajustar el diseño y mostrar los histogramas
    plt.tight_layout()
    plt.show()

def ghistogramahue(df, target ,columnas, ncol=5):
    # Calcular el número de filas que se necesitan para mostrar todos los gráficos en 5 columnas
    num_filas = -(-len(columnas) // 5)  # Es igual a ceil(len / 5)

    # Configurar el diseño de la figura
    plt.figure(figsize=(4*ncol, ncol * num_filas))  # Ajustar el ancho a 20 para 5 columnas

    # Iterar a través de las columnas categóricas y crear histogramas
    for i, col in enumerate(columnas):
        plt.subplot(num_filas, ncol, i+1)  # Cambia el 3 a 5 aquí
        sns.histplot(data=df, x=target, hue=col)
        plt.title(f'Histograma con {col}')
        plt.xlabel(target)

    # Ajustar el diseño y mostrar los gráficos
    plt.tight_layout()
    plt.show()

def gscatterhue(df, target ,columnas, ncol=5):
    # Calcular el número de filas para un diseño de 5 columnas
    num_filas = -(-len(columnas) // ncol)  # Es igual a ceil(len / 5)

    # Configurar el diseño de la figura
    plt.figure(figsize=(5*ncol, ncol * num_filas))  # Ajustar el ancho para 5 columnas

    # Iterar a través de las columnas numéricas
    for i, col in enumerate(columnas):
        plt.subplot(num_filas, ncol, i+1)
        
        # Hacer regplot
        sns.regplot(data=df, x=col, y=target, scatter_kws={'s':10, 'alpha':0.3}, line_kws={'color':'red'})

        # Realizar regresión lineal usando statsmodels
        X = df[col].dropna()
        y = df[target].loc[X.index]
        X = sm.add_constant(X) # añadir constante para intercepto
        model = sm.OLS(y, X).fit()

        # Obtener el valor p de la pendiente
        p_value = model.pvalues[col]
        
        # Verificar si la pendiente es significativa
        significativo = "Sí" if p_value < 0.05 else "No"
        
        # Mostrar la función y si la pendiente es significativa
        plt.title(f'{col}\nSalePrice = {model.params.const:.2f} + {model.params[col]:.2f}*{col}\nPendiente significativa: {significativo}')
        #plt.title(f'{col}\nSalePrice = {model.params.const:.2f} + {model.params[col]:.2f}*{col}\nPendiente significativa: {p_value}')
    plt.tight_layout()
    plt.show()

