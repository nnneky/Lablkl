# Laboratorio de bioseñales
This repository is dedicated to the statistical analysis of a biological signal extracted from PhysioNet, using Python to calculate descriptive metrics, visualize data and study the signal-to-noise ratio (SNR).

## Introducción:
Las señales fisiológicas son de vital importancia en el ámbito de la biomedicina, ya que permiten comprender y monitorear el funcionamiento del cuerpo humano. En este caso, se analizó una señal ECG con el objetivo de calcular sus estadísticos descriptivos y observar cómo diferentes tipos de ruido pueden afectarla. Este análisis se realizó utilizando la interfaz de Python, aplicando los conocimientos adquiridos en la materia de Procesamiento Digital de Señales, como parte de la primera práctica de laboratorio.

## Requirements
- Interfaz de python (para este caso 3.12)
- Numpy
-  Matplotlib
-  Scipy.io
-  Scipy.interpolate

## Importar la señal 
Se eligió la señal ECG "00ed2097-cd14-4f03-ab33-853da5be5550m" de la derivación aVR en PhysioNet, y se descargaron los archivos .info y .mat para su análisis. Esta señal forma parte de un estudio sobre los efectos de los medicamentos Dofetilide, Moxifloxacin, y sus combinaciones con Mexiletine, Lidocaine y Diltiazem en el corazón. Se espera que el ECG muestre cambios en el ritmo y la forma de las ondas, especialmente en la duración de los intervalos y en cómo se recupera el corazón después de cada latido, debido al efecto de estos medicamentos.

A continuación se muestran las librerias y el código implementado para la adecuación de la señal basado en los parametro sdescritos en el archivo .info descargado
```bash
import matplotlib.pyplot as plt ## Crear gráficos y visualizaciones
import numpy as np  ## Manejo de arreglos y cálculos numéricos
from scipy.io import loadmat  ## Cargar archivos .mat 
from scipy.interpolate import make_interp_spline ## Interpolación y suavización de curvas

x=loadmat('00ed2097-cd14-4f03-ab33-853da5be5550m.mat') ## carga el archivo .mat descargado 

ecg=(x['val']-22430)/66154.2  ## ajuste de los valores segun el archivo .info
ecg=np.transpose(ecg) ## transpone el vector de columnas a filas
fs=1000  ## frecuencia de muestreo 
tm=1/fs ## tiempo entre muestras

t=np.linspace(0,np.size(ecg),np.size(ecg))*tm ## vector tiempo para gráficar (valores del eje x)
```
## Gráfico de la señal:
Mediante el uso de matplotlib se realizó el gráfico del ecg:
``` bash
plt.figure(figsize=(12, 8)) ## tamaño de la figura (determinado por los desarrolladores)
plt.show()  ## muestra la figura

plt.plot(ecg, label="Señal Original", color='darkslategray') ## dibuja la señal ecg , se define el título  y el color deseado
plt.xlabel("Tiempo [ms]", color='navy') ## define el nombre y las unidades del eje x de la gráfica, tambien el color
plt.ylabel("Voltaje [mv]", color='navy') ## define el nombre y las unidades del eje y de la gráfica, tambien el color
plt.title("Señal origninal", color='navy') ## muestra el título y define su color
plt.show()  ## muestra la señal,los ejes y el título  
```
![image](https://github.com/user-attachments/assets/f7cd8bc3-0f6c-4a18-b041-37a789844f7f)

La gráfica de la señal demuestra un ritmo cárdiaco regular.

## Cálculo de los estadísticos descriptivos:
En el marco de la práctica, se calcularon la media aritmética, la desviación estándar y el coeficiente de variación de la señal ECG. Para ello, se implementaron dos métodos diferentes, cuya ejecución se llevó a cabo de la siguiente manera:
```bash
# Calcular la media aritmética manualmente
n = ecg.size ## se obtiene el número total de los datos del arreglo (una variableque guarda cuantos datos tiene el archivo)
if n > 1:    ## el cálculo se ejecutará si n almacena más de un dato
    suma = 0.0
    for x in ecg:  ## se recorré el arreglo almacenando cada dato (x) en la variable suma 
        suma += x
    media = suma / n ## se divide la suma total de los datos en el número de datos del arreglo
# Calcular la desviación estándar manualmente
    suma1 = 0.0
    for x in ecg:    ## se recorre el arreglo, en donde a cada dato se le resta la media aritmética y se eleva al cuadrado, luego se guarda en un sumador (suma 1)
        suma1 += (x - media) ** 2
    desvi = (suma1 / (n - 1)) ** 0.5   ## se cálcula la desviación estandar empleando la formula de la misma, suma1 se divide en el número total de datos menos 1 y se eleva a la 1/2
else:
    media = float('error al calcular')
    desvi = float('error al calcular')
# Estadísticos calculados por medio de funciones
mediac = np.mean(ecg) ## función para la media 
desviacionc = np.std(ecg, ddof=1)  ## función para la desviación , ddof=1 significa que al número total de datos se le resta uno
## coeficiente de variación calculado
coefi= desvi/media  ## se toman los datos cálculados y se realiza una división para obtener el valor 
## coeficiente de variación con los valores de las funciones (numpy no posee una función que lo realice automáticamente)
coefi1= desviacionc/mediac
```
![image](https://github.com/user-attachments/assets/d6f5e305-d2c6-468d-ad3d-a08a6ceebe1c)

La imagen anterior muestra los resultados de 3 de los estádisticos descriptivos,se puede observar que ambos métodos proporcionaron resultados iguales, lo que indica una correcta ejecución del código.

## Implementar el ruido 
La señal inicial de la derivación AVR fue contaminada manualmente por ruido: Gaussiano, Artefacto e Impulso los cuales fueron implementados de la siguiente forma:
```bash
r_gauss=np.random.normal(0,0.1, size=ecg.shape) #donde el [0.1] controla la amplitud del ruido el cúal se ve de manera gráfica.
s_gauss= (ecg+r_gauss) #se crea la señal juntando el ruido Gaussiano con la señal ECG original.

r_artefacto=0.2*np.sin(2*np.pi*50*np.linspace(0, 1, len(ecg))) # Este crea un vector de tiempo que va de 0 a 1 segundo con largo de las muestras, asegurando una frecuencia de muestreo correcta y alcula la frecuencia angular de 50 Hz en radianes
s_artefacto= (ecg+r_artefacto) #se crea la señal juntando el ruido Artefacto con la señal ECG original.

impulso=np.zeros_like(ecg) #Crea un array del mismo tamaño que ecg, pero lleno de ceros
p_impulso=np.random.choice(range(len(ecg)),size=100, replace=False) #Selecciona 100 posiciones aleatorias dentro de la señal ECG
impulso[p_impulso] = np.random.choice([-1, 1], size=1) * 0.5  #Elige aleatoriamente entre -1 o 1 y regula el impulso para que tenga amplitud 0.5
s_impulso=(ecg+impulso)  #se crea la señal juntando el ruido Impulso con la señal ECG original.
```
