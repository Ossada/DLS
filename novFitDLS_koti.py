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


def premica(x, D):
    return D*x

def f(x, y0, jd, A, f1, f2, s1, s2):
    return y0 + (1 + jd * ((A * np.exp(-pow(f1 * x, s1))) + ((1 - A) * np.exp(-pow(f2 * x, s2))) - 1)) ** 2

def f1(x,y0,f1,s1,A):
	return y0 + A*np.exp(-pow(f1*x, s1))

def norm(d, T):
	return d*(298/(T+273))*(visk(T)/visk(25))

def risanje2(seznamk, seznamf, seznamfer, ime, vzor, napaka, izpis=True):
	koti = np.array(seznamk)
	fji = np.array(seznamf)
	fjierr = np.array(seznamfer)
	para, error = sp.curve_fit(premica, koti, fji, sigma=fjierr, absolute_sigma=True)
	para1, error1 = sp.curve_fit(premica, koti, fji)
	par = para[0] * 10 ** 3
	par1 = para1[0] * 10 **3
	t = np.linspace(0, 9e14, 100)
	print(para, np.sqrt(error))
	eror = np.sqrt(error[0][0])/1e-13
	eror1 = np.sqrt(error1[0][0])/1e-13
	Dnorm = norm(par, float(vzor[6]))
	DnormD2O = normalizacijaD2O(par, float(vzor[6]), 0.9, 0.1)
	fig, ax = plt.subplots(1)
	plt.plot(koti, fji, 'bo', alpha=0.8)
	if napaka == True:
		ax.errorbar(koti, fji, yerr=fjierr, fmt='bo')
	plt.plot(t, premica(t, para),  'r')
	#	plt.plot(t, premica(t, para1), 'g--')
	plt.xlabel('$q^{2}$ $[m^{2}/s]$', fontsize=14)
	plt.ylabel('$f_{1}$ $kHz$', fontsize=14)
	plt.title(vzor[0])
	plt.xlim(xmin=0)
	plt.ylim(ymin=0)
	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
	if izpis == True:
		
		v = '${0}$\n${1}mM$ $oligo$\n${2} mM$ $NaCl$\n${3} mM$ $NaPi$\n$Datum:$ ${4}$\n$Merjeno:$ ${5}$ \n$T={6}^o C$'.format(vzor[0], vzor[1], vzor[2], vzor[3], vzor[4], vzor[5], vzor[6])
		ax.text(0.05, 0.95, v, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
		tex = ('$D={:0=.5f}$'.format(par/1e-10) + '$\\pm{:0=.4f}$'.format(eror) + '$\\times 10^{-10}$' + ' $m^{2}/s$' +
				#'\n' + '$D={:0=.5f}$'.format(par1/1e-10) + '$\\pm{:0=.4f}$'.format(eror1) + '$\\times 10^{-10}$' + 
				#'\n' + '$D_{{25}}={:0=.5f}$'.format(Dnorm/1e-10) + ' $m^{2}/s$')+
				'\n' + '$D_{{25}}={:0=.5f}$'.format(DnormD2O/1e-10) + ' $m^{2}/s$')
		
		ax.text(0.4, 0.3, tex, transform=ax.transAxes, fontsize=14,
		verticalalignment='top', bbox=props)
	if izpis == False:
		tex = ('$D={:0=.5f}$'.format(par/1e-10) + '$\\pm{:0=.4f}$'.format(eror) + '$\\times 10^{-10}$' + ' $m^{2}/s$' +
				#'\n' + '$D={:0=.5f}$'.format(par1/1e-10) + '$\\pm{:0=.4f}$'.format(eror1) + '$\\times 10^{-10}$' + 
				'\n' + '$D_{{25}}={:0=.5f}$'.format(Dnorm/1e-10) + ' $m^{2}/s$')# +
				#'\n' + '$D_{{25}}={:0=.5f}$'.format(DnormD2O/1e-10) + ' $m^{2}/s$')
		
		ax.text(0.2, 0.8, tex, transform=ax.transAxes, fontsize=14,
		verticalalignment='top', bbox=props)
	plt.savefig(ime + '.png')
	plt.close()

	return Dnorm, eror # vrne samo normalizacijo in napako, ni deljeno in ni za tezko vodo!

def beri2(pot):
	f1 = []
	with open(pot) as file:
		for line in file:
			if 'f1' in line:
				f1.append(line.split(' ')[1:])
	return f1

def origin(kot_sez, fji_sez, fjierr_sez, poti):
	file = open(poti + '/origin_premica.csv', 'w')
	for i in range(len(kot_sez)):
		file.write(str(kot_sez[i]) + ',' + str(fji_sez[i]) + ',' + str(fjierr_sez[i]) + '\n')
	file.close()

pot = tk.askdirectory(initialdir='/home/vid/MEGA/Meritve DLS/G4C2/ponovno staranje/')
seznam = os.listdir(pot)
seznam = natsort.natsorted(seznam)
vzorec = []
if 'vzorec.txt' in seznam:
	a = open(pot + '/vzorec.txt', 'r')
	for b in a:
		print(b)
		vzorec.append(b.strip())
	print(vzorec)

if 'vzorec.txt' not in seznam:
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




dat = open(pot + '/parametri.txt', 'w')  # V datoteko zapišmo fitane parametre vseh datotek

koti = []
fji = []
fjierr = []
serije = {}
paramstr = ['y0', 'jd', 'A', 'f1', 'f2', 's1', 's2']
values = [1, 1, 0.1, 10, 1, 1, 1]
spod, zgor = [3, 160]
dat.write('Začetni parametri:\n' + str(values) + '\n' + 'Spodnja in zgornja meja:\n' + str(spod) + ', ' + str(zgor) + '\n')
Origin = True  # Če True, se izpišejo vrednosti fjev za fit premice v csv datoteko, ki jo lahko uvozimo v origin
n = True  # napaka, ce so meritve cudne jih ne narise, da ni graf potem premajhen
D20 = False

for a in seznam:  # Začetek glevne zanke, kjer se izvede fit za vse datoteke
	if a[-4:] == '.ASC':
		key = a[:-4]
		kot = float(a.split('_')[0])  # Za datoteke, poimenovane kot_vzorec.asc (primer: 60_Seq4Amod3.ASC)
		xdata, ydata, time = fit.beri2(pot + '/' + a)
		error = fit.berierr2(pot + '/' + a)
		print('xdata: ' + str(len(xdata)))
		print('err: ' + str(len(error)))
		yup = []
		ylow = []
		vekt = fit.q2(kot)

		try: 

			for i in range(len(ydata)):  # Za prikaz napake v meritvi
				yup.append(ydata[i] + error[i])
				ylow.append(ydata[i] - error[i])
		except IndexError:
			print('Ni izmerjenih napak v datotekah, fitam brez uporabe napak!')

		
		try:
			
			try:
				param_bounds = ([-np.inf, 0, 0, 0, -np.inf, 0, 0], [np.inf, 10, 2, np.inf, np.inf, 1, 1])  # tuple dveh seznamov, prvi seznam ima spodnjo mejo paramterov, drugi zgornjo
				param, e = sp.curve_fit(f, xdata[spod:zgor], ydata[spod:zgor], p0=values, bounds=param_bounds, sigma=error[spod:zgor], absolute_sigma=True)
				
				if param[3] < 3: 
					paramstr1 = ['y0', 'f1','s1','A']
					values1 = [0, 10, 1, 1]
					param_bounds1 = ([-np.inf, 0, 0, 0], [np.inf, np.inf, 1, np.inf])
					param1, e1 = sp.curve_fit(f1, xdata[spod:zgor], ydata[spod:zgor], p0=values1, bounds=param_bounds1, sigma=error[spod:zgor])
					
					dat.write(a + '\n' + str(kot) + '\n' + str(vekt) + '\n')
					for i in range(len(param1)):
						dat.write(str(paramstr1[i]) + '  ' + str(param1[i]) + ' ' + str(np.sqrt(e1[i][i])) + '\n')
					fig, ax = plt.subplots(1)
					plt.plot(xdata, ydata, 'bo', label='meritev')
					plt.plot(xdata[spod:zgor], f1(xdata[spod:zgor], param1[0], param1[1], param1[2], param1[3]), 'r')
					ax.fill_between(xdata, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
					plt.xscale('log')
					plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
					plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
					plt.ylim(0, 1.2)
					plt.title(key)
					text = '$y_{0}=%.4f$\n$f_{1}=%.4f$\n$s_{1}=%.4f$\n$A=%.4f$' \
					  % (float(param1[0]), float(param1[1]), float(param1[2]), float(param1[3]))
					props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
					ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
					    verticalalignment='top', bbox=props)

					plt.savefig(pot + '/' + key +'1exp_scipy.png')
					plt.clf()
					values1 = param1
				
				dat.write(a + '\n' + str(kot) + '\n' + str(vekt) + '\n')
				for i in range(len(param)):
					dat.write(str(paramstr[i]) + '  ' + str(param[i]) + ' ' + str(np.sqrt(e[i][i])) + '\n')

				if key in serije:
					if param[3] > param[4]:
						serije[key].append([vekt, param[3], np.sqrt(e[3][3])])
					else:
						serije[key].append([vekt, param[4], np.sqrt(e[4][4])])
				else:
					if param[3] > param[4]:
						serije[key] = [[vekt, param[3], np.sqrt(e[3][3])]]
					else:
						serije[key] = [[vekt, param[4], np.sqrt(e[4][4])]]

				fig, ax = plt.subplots(1)
				plt.plot(xdata, ydata, 'bo', label='meritev')
				plt.plot(xdata[spod:zgor], f(xdata[spod:zgor], param[0], param[1], param[2], param[3], param[4], param[5], param[6]), 'r')
				ax.fill_between(xdata, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
				plt.xscale('log')
				plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
				plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
				plt.ylim(0, 1.2)
				plt.title(key)
				text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$' \
				  % (float(param[0]), float(param[1]), float(param[2]), float(param[3]),
				     float(param[4]), float(param[5]), float(param[6]))
				props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
				ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
				    verticalalignment='top', bbox=props)

				plt.savefig(pot + '/' + key +'scipy.png')
				plt.clf()
				values = param

			except Exception as e:
				print(e)
				
				param_bounds = ([-np.inf, 0, 0, 0, -np.inf, 0, 0], [np.inf, 10, 2, np.inf, np.inf, 1, 1])  # tuple dveh seznamov, prvi seznam ima spodnjo mejo paramterov, drugi zgornjo
				param, e = sp.curve_fit(f, xdata[spod:zgor], ydata[spod:zgor], p0=values, bounds=param_bounds)
				
				
				dat.write(a + '\n' + str(kot) + '\n' + str(vekt) + '\n')
				for i in range(len(param)):
					dat.write(str(paramstr[i]) + '  ' + str(param[i]) + ' ' + str(np.sqrt(e[i][i])) + '\n')

				if key in serije:
					if param[3] > param[4]:
						serije[key].append([vekt, param[3], np.sqrt(e[3][3])])
					else:
						serije[key].append([vekt, param[4], np.sqrt(e[4][4])])
				else:
					if param[3] > param[4]:
						serije[key] = [[vekt, param[3], np.sqrt(e[3][3])]]
					else:
						serije[key] = [[vekt, param[4], np.sqrt(e[4][4])]]

				fig, ax = plt.subplots(1)
				plt.plot(xdata, ydata, 'bo', label='meritev')
				plt.plot(xdata[spod:zgor], f(xdata[spod:zgor], param[0], param[1], param[2], param[3], param[4], param[5], param[6]), 'r')
				plt.xscale('log')
				plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
				plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
				plt.ylim(0, 1.2)
				plt.title(key)
				text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$' \
				  % (float(param[0]), float(param[1]), float(param[2]), float(param[3]),
				     float(param[4]), float(param[5]), float(param[6]))
				props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
				ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
				    verticalalignment='top', bbox=props)

				plt.savefig(pot + '/' + key +'scipy.png')
				plt.clf()
				values = param
		except RuntimeError:
			print('Z ' + key + ' je neki narobe. Poskušam z drugo metodo!')

			try:

				params = lm.Parameters()
				params.add('A', value=values[0])
				params.add('y0', value=values[1])
				params.add('jd', value=values[2], min=0, max=10)
				params.add('f1', value=values[3], min=0)
				params.add('f2', value=values[4])
				params.add('s1', value=values[5], min=0, max=1)
				params.add('s2', value=values[6], min=0.99, max=1)
				result = lm.minimize(fit.slowfastmode, params, args=(xdata[spod:zgor], ydata[spod:zgor]))
				final = ydata[spod:zgor] + result.residual
				tem = fit.parametri(result.params)
				lm.report_fit(result.params, show_correl=False)

				dat.write(a + '\n' +  str(kot) + '\n' + str(vekt) + '\n')
				fit.zapis(tem, dat)

				if key in serije:
					if tem[3][0] > tem[4][0]:
						serije[key].append([vekt, float(tem[3][0]), float(tem[3][1])])
					else:
						serije[key].append([vekt, float(tem[4][0]), float(tem[4][1])])
				else:
					if tem[3][0] > tem[4][0]:
						serije[key] = [[vekt, float(tem[3][0]), float(tem[3][1])]]
					else:
						serije[key] = [[vekt, float(tem[4][0]), float(tem[4][1])]]

				fig, ax = plt.subplots(1)
				plt.plot(xdata, ydata, 'bo')
				plt.plot(xdata[spod:zgor], final, 'r', linewidth=2)
				try:
					ax.fill_between(xdata, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
				except:
					continue
				plt.xscale('log')
				plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
				plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
				#plt.ylim(0, 1.2)				# plt.ylim(0, 1.1)
				plt.title(key)
				text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$' \
						% (float(tem[1][0]), float(tem[2][0]), float(tem[0][0]), float(tem[3][0]),
						float(tem[4][0]), float(tem[5][0]), float(tem[6][0]))
				props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
				ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
						verticalalignment='top', bbox=props)
				plt.savefig(pot + '/' + key +'scipyFailed.png')
				plt.close()
			except Exception as e:
				print('Napaka je: ' + str(e))
				plt.plot(xdata, ydata, 'bo')
				plt.xscale('log')
				plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
				plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
				plt.title(key)
				plt.savefig(pot + '/' + key +'FAIL.png')
				plt.close()
dat.close()
print(serije)
koti = []
fji = []
fjierr = []
for i in serije:
	print(i)


	koti.append(serije[i][0][0])
	fji.append(serije[i][0][1])
	fjierr.append(serije[i][0][2])

	# for j in range(len(serije[i])):  # Če imamo več serij meritev (staranje)
	# 	koti.append(serije[i][j][0])
	# 	fji.append(serije[i][j][1])
	# 	fjierr.append(serije[i][j][2])
	# 	print

text = pot + '/skupno'
print(fji)
D, E = risanje2(koti, fji, fjierr, text, vzorec, n, D20)
with open(pot + '/parametri.txt', 'a') as f:
	f.write('\nDnorm ' + str(D/1e-10) + '\nError ' + str(E) )

if Origin:
	origin(koti, fji,fjierr, pot)



# j = beri2('parametri.txt')
# file = open('fji.txt', 'w')
# for i in range(len(j)):
# 	for k in range(len(j[i])):
# 		file.write(str(j[i][k]) + ' ')
# file.close()

# koti = [60, 90, 100, 110]
# Q2 = []
# fji = [35.3985, 68.3022, 75.0742, 80.2132]
# for a in koti:
# 	Q2.append(q2(a))

# param, err = sp.curve_fit(premica, Q2, fji)
# print(param)
# fig, ax = plt.subplots(1)
# par = param * 10 ** 3
# t = np.linspace(0, 7e14, 100)
# plt.plot(Q2, fji, 'bo')
# plt.plot(t, premica(t, param))
# plt.xlabel('$q^{2}$ $[m^{2}/s]$', fontsize=14)
# plt.ylabel('$f_{1}$ $kHz$', fontsize=14)
# plt.xlim(xmin=0)
# par = par /10e-11
# tex = '$D={:f}$'.format(par[0]) + '$\\times 10^{-10}$' + ' $m^{2}/s$'
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# ax.text(0.60, 0.50, tex, transform=ax.transAxes, fontsize=14,
#         verticalalignment='top', bbox=props)
# plt.savefig('/media/vid/SILICON 16G/seq4A_21.11.png')
# plt.show()