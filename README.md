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
PhysioNet es una plataforma que proporciona acceso a bases de datos de señales fisiológicas, herramientas de análisis y software para investigación biomédica. Es  utilizada en el desarrollo de algoritmos para el análisis de ECG, EEG y otras señales médicas. Al realizar la busqueda de una señal fisiológica en Physionet se escogió la señal "00ed2097-cd14-4f03-ab33-853da5be5550m" Una señal Electrocardiográfica de la derivación AVR así descargando los archivos [.info]en el cual podemos encontrar la información en cuanto a la señal fisiologica que está analizando, luego el  [.mat] este archivo contenía todos los datos enteros de la señal fisológica, gracias a esta descarga se pudo importar la señal al código de python al igual que graficarla para su clara visualización.

Así se importó la señal haciendo uso de los valores de fracuencia y ganancia especificados en el archivo [.info] Al igual usando la librería WFDB la cual permite cargar, procesar, visualizar y analizar señales fisiológicas, especialmente de bases de datos, usando esto  pudímos importar la señal desde physionet.

```bash
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.interpolate import make_interp_spline

x=loadmat('00ed2097-cd14-4f03-ab33-853da5be5550m.mat')

ecg=(x['val']-22430)/66154.2
ecg=np.transpose(ecg)
fs=1000
tm=1/fs

t=np.linspace(0,np.size(ecg),np.size(ecg))*tm
```
## Implementar el ruido 
La señal inicial de la derivación AVR fue contaminada manualmente por ruido: Gaussiano, Artefacto e Impulso
