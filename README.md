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
![image](https://github.com/user-attachments/assets/f2340035-531a-47f7-b76f-4cfeade83041)


La imagen anterior muestra los resultados de 3 de los estádisticos descriptivos,se puede observar que ambos métodos proporcionaron resultados iguales, lo que indica una correcta ejecución del código.

## Histogramas  y funciones de probabilidad:El primer histograma se realizó de forma automática por medio de funciones:

El primer histograma se realizó de forma automática por medio de funciones:

```bash
# Histograma 
plt.figure(figsize=(10, 8)) ## se crea una figura 
count, bins, ignored = plt.hist(ecg, bins=50, color='purple', edgecolor='black', alpha=0.4) ##se definen los parametros del histograma, en los cuales se realizara de la señal ecg, con 50 barras de color morado con delineado engro, con un nivel de opacidad de 0.4, count= array que almacena los datos en frecuencias, bins= array con intervalo de los bordes 

# Calcular puntos medios de los intervalos
bin_centers = (bins[:-1] + bins[1:]) / 2  ## cálcula el centro del bing (borde izquierdo + el derecho dividido en 2) para ubicar el punto en el centro

# Crear una interpolación suavizada
x_smooth = np.linspace(bin_centers.min(), bin_centers.max(), 300) ##crea una serie de 300 puntos a igual distancia el uno del otro entre el valor mínimo y máximo de bin_centers.(valores del eje x)
y_smooth = make_interp_spline(bin_centers, count)(x_smooth) ## mediante la libreria scipy.interpolate se crea una interpolación entre los centros de los bins y las frecuencias (parametro count) así se obtendran los valores de y suavizados

# Dibujar línea de tendencia suavizada
plt.plot(x_smooth, y_smooth, linestyle='-', color='blue', label='Línea de Tendencia')

plt.xlabel("Voltaje (mV)", color='blue') ## titulo y color del eje x
plt.ylabel("Frecuencia", color='blue') ## titulo y color del eje x
plt.title("Histograma de la Señal ECG", color='blue') ## titulo y color del titulo del histograma 
plt.legend() ## muestra la leyenda de la curva suavizada
plt.show()

print(f"\nEl histograma muestra una función de probablidad sesgada hacia la izquierda\n") ## función de probabilidad en base al hitograma
```

En la imagen se muestra el histograma generado por funciones, se observa un sesgo hacia la izquierda o negativo lo cual indica que la mayoría de los valores en la distribución están concentrados en el lado derecho del gráfico.

![image](https://github.com/user-attachments/assets/d5185dd0-1169-46c4-a79e-4aa6c91b7e01)

Segundo histograma fue realizado de manera manual:

```bash
# histograma manual 
num_bins = 50  # Número de intervalos en los que se dividira el histograma
min_val = np.min(ecg) ## encuentra el valor minimo de la señal
max_val = np.max(ecg) ## encuentra el valor máximo de la señal
bin_width = (max_val - min_val) / num_bins    ## se cálcula el ancho de cada intervalo (rango total de los datos dividido el número de divisiones del histograma)

# Inicializar contadores de frecuencia
bin_edges = np.linspace(min_val, max_val, num_bins + 1) ## se crean los bordes de los bins +1 ya que serán 51 bordes 
bin_counts = np.zeros(num_bins) ## se crea un arreglo para guardar las frecuencias de cada intervalo

# Contar la cantidad de valores en cada intervalo
for value in ecg:   ## Recorrer todos los valores de la señal 
    for i in range(num_bins):  ## Recorrer cada intervalo (bin)
        if bin_edges[i] <= value < bin_edges[i + 1]:  # Verificar si el valor está en el intervalo de algun bin
            bin_counts[i] += 1 ## se aumenta la cuenta del bin correspondiente
            break

# Calcular los centros de los bins
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2  ## borde izquierdo mas el derecho dividido entre dos

# Crear una interpolación suavizada
x_smooth = np.linspace(bin_centers.min(), bin_centers.max(), 300) ## de la misma manera que en el anterior histograma 
y_smooth = make_interp_spline(bin_centers, bin_counts)(x_smooth)

# Graficar el histograma manual
plt.figure(figsize=(10, 8)) ## se crea una figura del tamaño deseado
plt.bar(bin_centers, bin_counts, width=bin_width, color='purple', edgecolor='black', alpha=0.4, label='Histograma Manual') ## dibujas las barras del histograma con los criterios de numeros de barras y los centros de las mismas, se define el color nombre, titulo y opacidad de las barras 
plt.plot(x_smooth, y_smooth, linestyle='-', color='blue', label='Línea de Tendencia') ## dibuja la linea de tendencia suavizada

plt.xlabel("Voltaje (mV)", color='blue') ## unidades y color del eje x
plt.ylabel("Frecuencia", color='blue')## unidades y color del eje y
plt.title("Histograma Manual de la Señal ECG", color='blue') ## titulo y color del histograma 
plt.legend() # leyenda de la curva de tendencia 
plt.show()
print(f"\nEl histograma muestra una función de probablidad sesgada hacia la izquierda\n") ## función de probabilidad 
```
En la imagen se muestra el histograma generado manualmente, se observa un sesgo hacia la izquierda o negativo lo cual indica que la mayoría de los valores en la distribución están concentrados en el lado derecho del gráfico.

![image](https://github.com/user-attachments/assets/f3bed24f-df56-45da-8dc7-3005463529ff)


## Implementar el ruido 
La señal inicial de la derivación AVR fue contaminada manualmente por ruido: Gaussiano, Artefacto e Impulso los cuales fueron implementados de la siguiente forma:
```bash
r_gauss=np.random.normal(0,0.1, size=ecg.shape) #donde el [0.1] controla la amplitud del ruido el cúal se ve de manera gráfica.
s_gauss= (ecg+r_gauss) #se crea la señal juntando el ruido Gaussiano con la señal ECG original.

r_artefacto=0.2*np.sin(2*np.pi*50*np.linspace(0, 1, len(ecg))) # Este crea un vector de tiempo que va de 0 a 1 segundo con largo de las muestras, asegurando una frecuencia de muestreo correcta y cálcula la frecuencia angular de 50 Hz en radianes
s_artefacto= (ecg+r_artefacto) #se crea la señal juntando el ruido Artefacto con la señal ECG original.

impulso=np.zeros_like(ecg) #Crea un array del mismo tamaño que ecg, pero lleno de ceros
p_impulso=np.random.choice(range(len(ecg)),size=100, replace=False) #Selecciona 100 posiciones aleatorias dentro de la señal ECG
impulso[p_impulso] = np.random.choice([-1, 1], size=1) * 0.5  #Elige aleatoriamente entre -1 o 1 y regula el impulso para que tenga amplitud 0.5
s_impulso=(ecg+impulso)  #se crea la señal juntando el ruido Impulso con la señal ECG original.
```
Las señales tanto la original como las que se contaminaron con ruido se gráficaron de la siguiente manera:
```bash
plt.figure(figsize=(12, 8))
plt.show()

plt.plot(ecg, label="Señal Original", color='darkslategray')
plt.xlabel("Tiempo [ms]", color='navy')
plt.ylabel("Voltaje [mv]", color='navy')
plt.title("Señal origninal", color='navy')
plt.show()

plt.plot(s_gauss, label=f"Ruido Gaussiano",color ='darkslategray')
plt.xlabel("Tiempo [ms]", color='navy')
plt.ylabel("Voltaje [mv]", color='navy')
plt.title("Señal con Ruido Gaussiano", color='navy')
plt.show()


plt.plot(s_artefacto, label=f"Ruido Artefacto ")
plt.xlabel("Tiempo [ms]", color='navy')
plt.ylabel("Voltaje [mv]", color='navy')
plt.title("Señal con Ruido artefacto", color='navy')
plt.show()


plt.plot(s_impulso, label=f"Ruido IMPULSO ",color ='darkslategray')
plt.xlabel("Tiempo [ms]", color='navy')
plt.ylabel("Voltaje [mv]", color='navy')
plt.title("Señal con ruido impulso", color='navy')
plt.show()
```

## Gráfica de la señal original:

![image](https://github.com/user-attachments/assets/39136c2a-8f57-4f89-b985-8239589b378d)

## Gráficas de la señal contaminada con los diferentes tipos de ruido: 

Señal contaminada con el ruido Gaussiano

![image](https://github.com/user-attachments/assets/e1021cc1-0057-4400-8ac7-90c2e2d818d8)

Señal contaminada con el ruido Artefacto


![image](https://github.com/user-attachments/assets/e972fbf9-f3f9-4888-b535-980f57ae6ca4)

Señal contaminada con el ruido Impulso


![image](https://github.com/user-attachments/assets/8c99f109-1a3d-4690-b392-2aa872c1d243)

## Implementación del SNR a las señales contaminadas:

El SNR (Signal-to-Noise Ratio) es la relación entre la potencia de la señal y la potencia del ruido, expresada en decibeles (dB). Se calcula como:

![image](https://github.com/user-attachments/assets/b32d218e-1143-48e6-8a7c-aceed7b2eaa7)  (imagen 1.1)

Un SNR alto indica una señal clara con poco ruido, mientras que un SNR bajo significa que el ruido domina la señal.

En el caso de python lo implementamos de la siguiente manera:
```bash
def snr(signal,noise):
    pseñal=np.mean(signal**2) #Potencia media de la señal 
    pruido=np.mean(noise**2)  #Potencia media el ruido
    return 10* np.log10(pseñal/pruido)  #Se convierte el valor a [dB]
```
Para calcularlo dentro de cada ruido se aplico de la siguiente manera:
 ```bash
snr_gauss=snr(ecg,r_gauss) #SNR ruido Gaussiano relacionando la señal original y el ruido. 
snr_artefacto = snr(ecg,r_artefacto) #SNR ruido Artefacto relacionando la señal original y el ruido.
snr_impulso=snr(ecg,impulso) #SNR ruido Impulso relacionando la señal original y el ruido.
```
Los resultados del SNR en las 6 señales con ruidos de párametros diferentes fueron:

![image](https://github.com/user-attachments/assets/34d875b7-113d-47b6-8ea9-89b2093fea6a)

En los valores de SNR de muestras iniciales podemos encontrar que los valores dentro de cada ruido varían en cúanto a la degradación de la señal teniendo el ruido impulso con una degradación mínima gracias a su alto valor de SNR a comparación con los demás ruidos, lo cual significa que este tuvo menor impacto en cuanto a la señal original, sin embargo en la segunda tanda de SNRs creados manualmente, se graduaron los parametros para que los ruidos tuvieran mayor impacto con respecto a la señal original, lo cual se implementó correctamente al ver los valores de SNR más cercanos a 0 o incluso en términos negativos lo cúal índica que el ruido tiene mayor predominación con respecto a la señal electrocaridiográfica original.

## Bibliografía:
- La totalidad de las imagenes mostradas en este repositorio son de propia autoria, exeptuando la imagen 1.1 la cual fue extraida de https://es.slideshare.net/gluzardo/sesion-05-estadistica-en-senales
- la señal en la cual se baso este repositorio fue obtenida del banco de señales biológicas physionet.org
- SciPy Developers (2023). SciPy Interpolation Module.https://numpy.org/doc/
- SciPy Developers (2023). SciPy Interpolation Module. https://docs.scipy.org/doc/scipy/reference/interpolate.html
- GRUPO BIOMEDICO. (2020, 22 septiembre). Graficar señal DE PHYSIONET EN PYTHON  - señal de prueba ecg [Vídeo]. YouTube. https://www.youtube.com/watch?v=auZ0jB8jYt8


