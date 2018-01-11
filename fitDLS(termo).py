import math
import matplotlib.pyplot as plt
import scipy.optimize as sp
import lmfit as lm
import numpy as np
import fitDLS as fit
import tkinter.filedialog as tk
import natsort
import os
from lomnikol import *


def f(x, y0, jd, A, f1, f2, s1, s2):
    return y0 + (1 + jd * ((A * np.exp(-pow(f1 * x, s1))) + ((1 - A) * np.exp(-pow(f2 * x, s2))) - 1)) ** 2

def poimenovanje(lista):
	vzorec = []
	if 'vzorec.txt' in lista:
	a = open(pot + '/vzorec.txt', 'r')
	for b in a:
		print(b)
		vzorec.append(b.strip())
	print(vzorec)

	if 'vzorec.txt' not in lista:
		a = open(pot + '/vzorec.txt', 'w')
		vzorec.append(input('Vnesi ime vzorca: '))
		a.write(str(vzorec[0]) + '\n')
		vzorec.append(input('Vnesi koncentracijo oligonukleotida v mM: '))
		a.write(str(vzorec[1]) + '\n')
		vzorec.append(input('Vnesi koncentracijo soli v mM: '))
		a.write(str(vzorec[2]) + '\n')
		vzorec.append(input('Vnesi koncentracijo pufra v mM: '))
		a.write(str(vzorec[3]) + '\n')
		vzorec.append(input('Vnesi datum sinteze: '))
		a.write(str(vzorec[4]) + '\n')
		vzorec.append((input('Vnesi datum meritve: ')))
		a.write(str(vzorec[5]) + '\n')
		vzorec.append(input('Vnesi temperaturo: '))
		a.write(str(vzorec[6]) + '\n')
	a.close()
	return vzorec

def grafi(x, y, spodnja, zgornja, para, temp, metoda, ime, vzorc, ylow = [], yup = []):
	fig, ax = plt.subplots(1)
	plt.plot(x, y, 'bo', label='meritev')
	if metoda == 'scipy':
		plt.plot(xdata[spodnja:zgornja], f(xdata[spodnja:zgornja], para[0], para[1], para[2], para[3], para[4], para[5], para[6]), 'r')
		text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$\n$scipy$' \
	  	% (float(param[0]), float(param[1]), float(param[2]), float(param[3]),
		float(param[4]), float(param[5]), float(param[6]))
		if ylow != [] and yup != []:
			ax.fill_between(x, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
	if metoda == 'limfit':
		plt.plot(xdata[spod:zgor], final, 'r', linewidth=2)
		text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$\n$limfit$' \
					% (float(para[1][0]), float(para[2][0]), float(para[0][0]), float(para[3][0]),
					float(para[4][0]), float(para[5][0]), float(para[6][0]))		
		if ylow != [] and yup != []:
			ax.fill_between(x, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
	plt.xscale('log')
	plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
	plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
	plt.title('$' + vzorc[0] + '$' + ' $T={0:4.2f}$'.format(temp)

	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
	ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
	    verticalalignment='top', bbox=props)

	plt.savefig(pot + '/' + ime +'fitano.jpg')
	plt.clf()

if __name__ == '__main__':

	root = tk.Tk()
    root.withdraw()

	pot = tk.askdirectory(initialdir='/home/vid/IJS/Meritve')
	seznam = os.listdir(pot)
	seznam = natsort.natsorted(seznam)
    pot1 = tk.askopenfilename(initialdir=pot)  # odpremo datoteko s temperaturo

	podatki  = poimenovanje(seznam)

	with open(pot1, 'r') as file:
		try:
			for line in file:
				temp.append(float(line.split(' ')[0]))  # Odpre datoteko s temperaturami, uporabljeno za izpis grafov
			for i in range(4):
				next(file)
		except StopIteration:
			pass

	dat = open(pot + '/parametri.txt', 'w')
	fji = []
	fjierr = []
	serije = {}
	paramstr = ['y0', 'jd', 'A', 'f1', 'f2', 's1', 's2']
	values = [1, 1, 0.7, 30, 1.5, 1, 1]
	spod, zgor = [16, 180]
	dat.write('Začetni parametri:\n' + str(values) + '\n' 
			  + 'Spodnja in zgornja meja:\n' + str(spod) + ', ' 
			  + str(zgor) + '\n')


