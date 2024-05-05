import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio 
import pandas as pd
class manejo_archivo: 
    def __init__(self) :
        self.archivo_mat = {}
        self.archivo_csv = {}
    def leer_mat(self, ruta, llave):
        try:
            data = sio.loadmat(ruta)
            self.archivo_mat[llave] = data
        except Exception as e:
            return e
            print(f"Error al leer el archivo .mat: {e}")
    def leer_csv(self, ruta_archivo, llave):
        try:
            data = pd.read_csv(ruta_archivo)
            self.archivo_csv[llave] = data
        except Exception as e:
            print(f"Error al leer el archivo .csv: {e}")
    def obtener_datos(self,llave):
        if llave in self.archivo_mat:
            return self.archivo_mat[llave]["val"]
        elif llave in self.archivo_csv:
            return self.archivo_csv[llave]
        else:
            print("los datos asociados a la clave no existen o la clave es incorrecta")
            return None
class graficadora(manejo_archivo):
    
    def __init__(self, ma):
        super().__init__()
        self.ma = ma
    def crear_boxplot(self,data, indice_fila,ax):
        fil=int(indice_fila)
        data = data
        fila = data[fil, ]
        fig, ax = plt.subplots()
        ax.boxplot(fila)
        ax.set_title(f'Boxplot de la fila {indice_fila}')
        ax.set_xlabel('Puntos de datos')
        ax.set_ylabel('Valores')
        
    def graficar_promedio(self, data, inicio_columna, fin_columna,ax):
        ic=int(inicio_columna)
        iff=int(fin_columna)
        data = data
        promedios = []
        for i in range(data.shape[0]):
            fila = data[i, ic:iff]
            promedio = np.mean(fila)
            promedios.append(promedio)

        fig, ax = plt.subplots()
        ax.plot(promedios)
        ax.set_title('Promedio de canales en los puntos seleccionados')
        ax.set_xlabel('canales')
        ax.set_ylabel('Promedio')
    def obtener_forma_matriz(self, clave):
        data = self.ma.obtener_datos(clave)
        if data is not None:
            forma_matriz = data.shape
            print(f"La forma de la matriz asociada a la clave {clave} es: {forma_matriz}")
            return forma_matriz
        else:
            print("No se encontraron datos asociados")
            return None

        
    def graficar_sensores_con_ruido(self, data, sensor1, sensor2, punto_inicio, punto_fin,ax):
        data = data
        s1=int(sensor1)
        s2=int(sensor2)
        pi=int(punto_inicio)
        pf=int(punto_fin)
        if data is not None:
            datos_sensor1 = data[s1, pi:pf]
            datos_sensor2= data[s2, pi:pf]
            suma_sensores = datos_sensor1 + datos_sensor2
            ruido = np.random.normal(0, 0.1, len(suma_sensores))
            suma_con_ruido = suma_sensores + ruido
            tiempo_milisegundos = np.arange(len(suma_con_ruido)) * 0.1  
            fig, ax = plt.subplots()
            ax.plot(tiempo_milisegundos, suma_con_ruido)
            ax.set_title('Suma de filas con ruido')
            ax.set_xlabel('Tiempo (ms)')
            ax.set_ylabel('Suma con ruido')
            
    def obtener_nombres_columnas(self, llave):
        data = self.ma.obtener_datos(llave)
        if data is not None:
            nombres_columnas = data.columns.tolist()
            print("Los nombres de las columnas son: ")
            for nombre_columna in nombres_columnas:
                print(nombre_columna)
            return None
        else:
            print("No se encontraron datos asociados")
            return None

    def histograma_columna(self, llave, columna):
        columna = self.ma.obtener_datos(llave)[columna]
        plt.hist(columna.dropna())
        plt.title(f'Histograma de "{columna}"')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
    def boxplot_columna_multiplicacion(self, llave, C1, C2,NnuevaC):
        data = self.ma.obtener_datos(llave)
        if C1 in data.columns and C2 in data.columns:
            columna_nueva = data[C1] * data[C2]
            data[NnuevaC] = columna_nueva

            
            plt.boxplot(data[NnuevaC].dropna())
            plt.title(f'Boxplot de la  columna {NnuevaC}')
            plt.ylabel('Valores')
            plt.show()
        else:
            print("revisa los datos")
