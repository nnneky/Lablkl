import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.interpolate import make_interp_spline
#Cargamos los datos de phyisionet al código.
x=loadmat('nombre del archivo.mat')

ecg=(x['val']-22430)/66154.2 ## ajustar según tu archivo .info
ecg=np.transpose(ecg)
fs=1000 ## segun archivo .info
tm=1/fs

t=np.linspace(0,np.size(ecg),np.size(ecg))*tm

#definimos la variable de SNR y creamos el cálculo para este.
def snr(signal,noise):
    pseñal=np.mean(signal**2)
    pruido=np.mean(noise**2)
    return 10* np.log10(pseñal/pruido)

#Se crea el ruido Gaussiano 1 manualmente
r_gauss=np.random.normal(0,0.1, size=ecg.shape)
s_gauss= (ecg+r_gauss)
snr_gauss=snr(ecg,r_gauss)

#Se crea el ruido Gaussiano 2 manualmente
r_gauss2=np.random.normal(0,0.5, size=ecg.shape)
s_gauss2= (ecg+r_gauss2)
snr_gauss2=snr(ecg,r_gauss2)

#Se crea el ruido Artefacto 1 manualmente
r_artefacto=0.2*np.sin(2*np.pi*50*np.linspace(0, 1, len(ecg)))
s_artefacto= (ecg+r_artefacto)
snr_artefacto = snr(ecg,r_artefacto)

#Se crea el ruido Artefacto 2 manualmente
r_artefacto2=0.5*np.sin(3*np.pi*50*np.linspace(0, 5, len(ecg)))
s_artefacto2= (ecg+r_artefacto2)
snr_artefacto2 = snr(ecg,r_artefacto2)

#Se crea el ruido Impulso 2 manualmente
impulso2=np.zeros_like(ecg)
p_impulso2=np.random.choice(range(len(ecg)),size=50, replace=False)
impulso2[p_impulso2] = np.random.choice([-1, 1], size=1) * 0.5  
s_impulso2=(ecg+impulso2)
snr_impulso2=snr(ecg,impulso2)

#Se crea el ruido Impulso  manualmente
impulso=np.zeros_like(ecg)
p_impulso=np.random.choice(range(len(ecg)),size=100, replace=False)
impulso[p_impulso] = np.random.choice([-1, 1], size=1) * 0.5  
s_impulso=(ecg+impulso)
snr_impulso=snr(ecg,impulso)


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

# Calcular la media aritmética manualmente
n = ecg.size

if n > 1:
    suma = 0.0
    for x in ecg:
        suma += x
    media = suma / n

# Calcular la desviación estándar manualmente
    suma1 = 0.0
    for x in ecg:
        suma1 += (x - media) ** 2
    desvi = (suma1 / (n - 1)) ** 0.5  
else:
    media = float('error al calcular')
    desvi = float('error al calcular')

# Estadísticos calculados por medio de funciones
mediac = np.mean(ecg)
desviacionc = np.std(ecg, ddof=1) 

## coeficiente de variación calculado

coefi= desvi/media 

## coeficiente de variación con los valores de las funciones

coefi1= desviacionc/mediac

print(f"\nMedia calculada: {media}\n")
print(f"Desviación estándar calculada: {desvi}\n")
print(f"coeficiente de variación calculado: {coefi}\n")
print(f"Media por funciones: {mediac}\n")
print(f"Desviación estándar por funciones: {desviacionc}\n")
print(f"coeficiente de variación con valores de las funciones: {coefi1}\n")
print(f"\nSNR de Señal con ruido Gaussiano: {snr_gauss}dB\n ")
print(f"\nSNR de Señal con ruido Artefacto: {snr_artefacto}dB\n ")
print(f"\nSNR de Señal con ruido Impulso: {snr_impulso}dB\n ")
print(f"\nSNR de Señal con ruido Gaussiano 2: {snr_gauss2}dB\n ")
print(f"\nSNR de Señal con ruido Artefacto 2: {snr_artefacto2}dB\n ")
print(f"\nSNR de Señal con ruido Impulso 2: {snr_impulso2}dB\n ")

# Histograma 
plt.figure(figsize=(10, 8))
count, bins, ignored = plt.hist(ecg, bins=50, color='purple', edgecolor='black', alpha=0.4)

# Calcular puntos medios de los intervalos
bin_centers = (bins[:-1] + bins[1:]) / 2

# Crear una interpolación suavizada
x_smooth = np.linspace(bin_centers.min(), bin_centers.max(), 300)
y_smooth = make_interp_spline(bin_centers, count)(x_smooth)

# Dibujar línea de tendencia suavizada
plt.plot(x_smooth, y_smooth, linestyle='-', color='blue', label='Línea de Tendencia')

plt.xlabel("Voltaje (mV)", color='blue')
plt.ylabel("Frecuencia", color='blue')
plt.title("Histograma de la Señal ECG", color='blue')
plt.legend()
plt.show()

print(f"\nEl histograma muestra una función de probablidad sesgada hacia la izquierda\n")
