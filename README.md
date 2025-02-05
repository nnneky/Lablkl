# Lab_Procesamiento.
## Introducción:
El uso de señales fisiologicas en entornos biomédicos ayuda al correcto entendimiento del tema al igual que la implementación en diferentes campos al igual es esencial para el diagnóstico, monitoreo y tratamiento de enfermedades, ya que permiten evaluar el estado funcional del cuerpo en tiempo real. Estas señales, como ECG, EEG y EMG, son clave para detectar patologías, supervisar pacientes en entornos críticos, optimizar dispositivos médicos como prótesis y marcapasos. 

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
