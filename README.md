# Laboratorio de bioseñales
This repository is dedicated to the statistical analysis of a biological signal extracted from PhysioNet, using Python to calculate descriptive metrics, visualize data and study the signal-to-noise ratio (SNR).

## Introducción:
Las señales fisiológicas son de vital importancia en el ámbito de la biomedicina, ya que permiten comprender y monitorear el funcionamiento del cuerpo humano. En este caso, se analizó una señal ECG con el objetivo de calcular sus estadísticos descriptivos y observar cómo diferentes tipos de ruido pueden afectarla. Este análisis se realizó utilizando la interfaz de Python, aplicando los conocimientos adquiridos en la materia de Procesamiento Digital de Señales, como parte de la primera práctica de laboratorio.

## Requirements
- interfaz de python (para este caso 3.12)
- numpy
-  matplotlib
-  scipy.io
-  scipy.interpolate

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
## Implementar el ruido 
La señal inicial de la derivación AVR fue contaminada manualmente por ruido: Gaussiano, Artefacto e Impulso
