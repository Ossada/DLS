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
import collections
import time


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
		vzorec.append(input('Kot merjenja: '))
		a.write(str(vzorec[7]) + '\n')
	a.close()
	return vzorec

def verbose(para, err, parstring):
	print('Fit report:')
	for k in range(len(para)):
		num = err[k]/para[k]
		print(str(parstring[k]) +  ' = ' + str(para[k]) + ' (1 +- ' + '{0:.4f})'.format(num) + '({0:.4f}%)'.format(num*100))

def grafi(x, y, spodnja, zgornja, para, temp, metoda, ime, vzorc, mapa, ylow = [], yup = [], final=[]):
	fig, ax = plt.subplots(1)
	plt.plot(x, y, 'bo', label='meritev')
	if metoda == 'scipy':
		plt.plot(xdata[spodnja:zgornja], f(xdata[spodnja:zgornja], para[0], para[1], para[2], para[3], para[4], para[5], para[6]), 'r')
		text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$\n$scipy$' \
	  	% (float(param[0]), float(param[1]), float(param[2]), float(param[3]),
		float(param[4]), float(param[5]), float(param[6]))
		if ylow != [] and yup != []:
			ax.fill_between(x, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
	if metoda == 'lmfit':
		plt.plot(xdata[spodnja:zgornja], final, 'r', linewidth=2)
		text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$\n$lmfit$' \
					% (float(para[1][0]), float(para[2][0]), float(para[0][0]), float(para[3][0]),
					float(para[4][0]), float(para[5][0]), float(para[6][0]))		
		if ylow != [] and yup != []:
			ax.fill_between(x, yup, ylow, interpolate=True, facecolor='green', alpha=0.4)
	plt.xscale('log')
	plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
	plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
	plt.title('$' + vzorc[0] + '$' + ' $T={0:4.2f}$'.format(temp))
	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
	ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
	    verticalalignment='top', bbox=props)
	
	plt.savefig(mapa + '/' + ime +'fitanoDin.jpg')
	plt.clf()
	plt.close('all')

def branjepar(pots):
	temper = []
	with open(pots + '/parametri.txt', 'r') as file:

		for i in range(4):
			next(file)
		for line in file:
			temp = line.strip().split(' ')
			temper.append(temp)
	return temper

def assign(sez):
	fy0 = []
	fjd = []
	fA = []
	ff1 = []
	ff2 = []
	fs1 = []
	fs2 = []
	try:
		for i in te:
			# print(i)
			if 'mod' in i:
				continue
			if 'y0' in i:
				fy0.append([float(i[1]), float(i[2])])
				continue
			if 'jd' in i:
				fjd.append([float(i[1]), float(i[2])])
				continue
			if 'A' in i:
				fA.append([float(i[1]), float(i[2])])
				continue
			if 'f1' in i:
				ff1.append([float(i[1]), float(i[2])])
				continue
			if 'f2' in i:
				ff2.append([float(i[1]), float(i[2])])
				continue
			if 's1' in i:
				fs1.append([float(i[1]), float(i[2])])
				continue
			if 's2' in i:
				fs2.append([float(i[1]), float(i[2])])
				continue
	except ValueError:
		print(i)
	return fy0, fjd, fA, ff1, ff2, fs1, fs2


if __name__ == '__main__':

	root = tk.Tk()
	root.withdraw()

	pot = tk.askdirectory(initialdir='/home/vid/IJS/Meritve')
	seznam = os.listdir(pot)
	seznam = natsort.natsorted(seznam)
	pot1 = tk.askopenfilename(initialdir=pot)  # odpremo datoteko s temperaturo

	podatki  = poimenovanje(seznam)
	indeks = -1
	tempera = []
	dinamicno = True  # Poskuša se izogniti oscilacijam pri fitu
	mapa = time.strftime('%c')
	os.mkdir(pot + '/' + mapa)
	novapot = pot + '/' + mapa


	with open(pot1, 'r') as file:
		try:
			for line in file:
				tempera.append(float(line.split(' ')[0]))  # Odpre datoteko s temperaturami, uporabljeno za izpis grafov
				for i in range(4):
					next(file)
		except StopIteration:
			pass
	
	for o in range(len(tempera)):
		if tempera[o+1] < tempera[o]:
			prvi = o
			break

	for o in range(prvi, len(tempera)):
		if tempera[o+1] > tempera[o]:
			drugi = o
			break

	y0 = []
	jd = []
	A = []
	f1 = []
	f2 = []
	s1 = []
	s2 = []
	# print(tempera[:prvi])
	# print(tempera[prvi:drugi])
	if 'parametri.txt' in seznam:
		te = branjepar(pot)
		y0, jd, A, f1, f2, s1, s2 = assign(te)

	else:

		dat = open(novapot + '/parametri.txt', 'w')
		fji = []
		fjierr = []
		serije = {}
		paramstr = ['y0', 'jd', 'A', 'f1', 'f2', 's1', 's2']
		values = [1, 1, 0.7, 16, 1.5, 1, 1]
		spod, zgor = [20, 160]
		zgor1 = zgor
		eps = 0
		dat.write('Začetni parametri:\n' + str(values) + '\n' 
				  + 'Spodnja in zgornja meja:\n' + str(spod) + ', ' 
				  + str(zgor) + '\n')


		for i in seznam:
			if i[-4:] == '.ASC':
				xdata, ydata = fit.beri(pot + '/' + i)
				error = fit.berierr(pot + '/' + i)
				yupp = []
				yloww = []
				indeks += 1
				key = i[:-4]
				eps = 0

				if len(ydata) == len(error):
					for j in range(len(ydata)):
						yupp.append(ydata[j] + error[j])
						yloww.append(ydata[j] - error[j])

				if dinamicno:
					for p in range(130, 180):
						if ydata[p-1] < (ydata[p] - 0.001):
							if p < zgor1:
								zgor1 = p
							eps += 0.1
					if eps > 0.6:
						print('Zaznana stopnica pri mestu: ' + str(zgor1) + ', moč: ' + str(eps))
						zgor = zgor1
				
				print('Fit ' + str(i))
				try:	
					try:
						meth = 'scipy'
						param_bounds = ([-np.inf, 0, 0, 0, -np.inf, 0, 0], [np.inf, 10, np.inf, np.inf, np.inf, 1, 1])  # tuple dveh seznamov, prvi seznam ima spodnjo mejo paramterov, drugi zgornjo
						
						param, e = sp.curve_fit(f, xdata[spod:zgor], ydata[spod:zgor], p0=values, bounds=param_bounds, sigma=error[spod:zgor], absolute_sigma=True)
						
						erro = np.sqrt(np.diag(e))
						dat.write(str(i) + '\n')
						for neki in range(len(param)):
							dat.write(str(paramstr[neki]) + ' ' + str(param[neki]) + ' ' + str(erro[neki]) + '\n')
						grafi(xdata, ydata, spod, zgor, param, tempera[indeks], meth, i, podatki, novapot, yupp, yloww)
						verbose(param, erro, paramstr)
						serije[key] = [param, erro]
						# print(param)
						values = list(param)
					except ValueError:
						meth = 'scipy'
						param_bounds = ([-np.inf, 0, 0, 0, -np.inf, 0, 0], [np.inf, 10, np.inf, np.inf, np.inf, 1, 1])
						param, e = sp.curve_fit(f, xdata[spod:zgor], ydata[spod:zgor], p0=values, bounds=param_bounds)
						
						erro = np.sqrt(np.diag(e))
						dat.write(str(i) + '\n')
						for neki in range(len(param)):
							dat.write(str(paramstr[neki]) + ' ' + str(param[neki]) + ' ' + str(erro[neki]) + '\n')
						grafi(xdata, ydata, spod, zgor, param, tempera[indeks], meth, i, podatki, novapot, yupp, yloww)
						verbose(param, erro, paramstr)
						serije[key] = [param, erro]
						values = list(param)
				except Exception as e:
					print(e)
					print('Z ' + key + ' je neki narobe. Fitam z drugo metodo!')
					try:
						meth = 'lmfit'
						params = lm.Parameters()
						params.add('A', value=values[0])
						params.add('y0', value=values[1])
						params.add('jd', value=values[2], min=0, max=10)
						params.add('f1', value=values[3], min=0)
						params.add('f2', value=values[4])
						params.add('s1', value=values[5], min=0, max=1)
						params.add('s2', value=values[6], min=0, max=1)
						result = lm.minimize(fit.slowfastmode, params, args=(xdata[spod:zgor], ydata[spod:zgor]))
						final = ydata[spod:zgor] + result.residual
						lm.report_fit(result.params, show_correl=False)
						tem = fit.parametri(result.params)
						dat.write(str(i) + '\n')
						for neki in range(len(tem)):
							dat.write(str(paramstr[neki]) + ' ' + str(tem[neki][0]) + ' ' + str(tem[neki][1]) + '\n')
						grafi(xdata, ydata, spod, zgor, tem, tempera[indeks], meth, i, podatki, novapot, yupp, yloww, final)
						serije[key] = tem
						
					except Exception as er:
						print(er)
				zgor = 160
		dat.close()
		te = branjepar(novapot)
		y0, jd, A, f1, f2, s1, s2 = assign(te)


	f1y, f1s = [*zip(*f1)]

	Ay, As = [*zip(*A)]
	konc = len(Ay)
	print(type(f1y), type(Ay))
	print('f1y: ' +str(len(f1y)))
	print('f1s: ' + str(len(f1s)))
	print('Ay: ' + str(len(Ay)))
	print('As: ' + str(len(As)))
	print(prvi)
	print(tempera[0:prvi])
	print(len(Ay[0:prvi]))

	try:


		fig, axs = plt.subplots(nrows=2, ncols=2)
		fig.suptitle('A')
		ax = axs[0,0]
		ax.errorbar(tempera[:prvi], Ay[:prvi], yerr=As[:prvi], color='r')
		ax.errorbar(tempera[prvi:drugi], Ay[prvi:drugi],yerr=As[prvi:drugi], color='b')
		ax.errorbar(tempera[drugi:konc], Ay[drugi:],yerr=As[drugi:], color='#ff3300')
		# ax.set_ylim(0,1)
		ax.set_title('Celotno območje')

		ax = axs[0,1]
		ax.errorbar(tempera[2:prvi], Ay[2:prvi],yerr=As[2:prvi], color='r')
		ax.set_title('Prvo segrevanje')

		ax = axs[1,0]
		ax.errorbar(tempera[prvi:drugi], Ay[prvi:drugi],yerr=As[prvi:drugi])
		ax.set_title('Ohlajanje')

		ax = axs[1,1]
		ax.errorbar(tempera[drugi:konc], Ay[drugi:],yerr=As[drugi:], color='#ff3300')
		ax.set_title('Drugo segrevanje')
		# plt.ylim(0, 1)
		plt.savefig(novapot + '/Aji.jpg')
	except AssertionError:
		fig, axs = plt.subplots(nrows=2, ncols=2)
		fig.suptitle('A')
		ax = axs[0,0]
		ax.plot(tempera[:prvi], Ay[:prvi], color='r')
		ax.plot(tempera[prvi:drugi], Ay[prvi:drugi], color='b')
		ax.plot(tempera[drugi:konc], Ay[drugi:], color='#ff3300')
		# ax.set_ylim(0,1)
		ax.set_title('Celotno območje')

		ax = axs[0,1]
		ax.errorbar(tempera[2:prvi], Ay[2:prvi], color='r')
		ax.set_title('Prvo segrevanje')

		ax = axs[1,0]
		ax.errorbar(tempera[prvi:drugi], Ay[prvi:drugi])
		ax.set_title('Ohlajanje')

		ax = axs[1,1]
		ax.errorbar(tempera[drugi:konc], Ay[drugi:], color='#ff3300')
		ax.set_title('Drugo segrevanje')
		# plt.ylim(0, 1)
		plt.savefig(novapot + '/Aji.jpg')



	fig, axs = plt.subplots(nrows=2, ncols=2)
	fig.suptitle('f1')
	ax = axs[0,0]
	ax.errorbar(tempera[2:prvi], f1y[2:prvi],yerr=f1s[2:prvi], color='r')
	ax.errorbar(tempera[prvi:drugi], f1y[prvi:drugi],yerr=f1s[prvi:drugi])
	ax.errorbar(tempera[drugi:konc], f1y[drugi:],yerr=f1s[drugi:], color='#ff3300')
	# ax.set_ylim(0,1)
	ax.set_title('Celotno območje')

	ax = axs[0,1]
	ax.errorbar(tempera[2:prvi], f1y[2:prvi],yerr=f1s[2:prvi], color='r')
	ax.set_title('Prvo segrevanje')

	ax = axs[1,0]
	ax.errorbar(tempera[prvi:drugi], f1y[prvi:drugi],yerr=f1s[prvi:drugi])
	ax.set_title('Ohlajanje')

	ax = axs[1,1]
	ax.errorbar(tempera[drugi:konc], f1y[drugi:],yerr=f1s[drugi:], color='#ff3300')
	ax.set_title('Drugo segrevanje')
	# plt.ylim(0, 1)
	plt.savefig(novapot + '/f1ji.jpg')

	f2y, f2s = [*zip(*f2)]

	fig, axs = plt.subplots(nrows=2, ncols=2)
	fig.suptitle('f2')
	ax = axs[0,0]
	ax.errorbar(tempera[2:prvi], f2y[2:prvi],yerr=f2s[2:prvi], color='r')
	ax.errorbar(tempera[prvi:drugi], f2y[prvi:drugi],yerr=f2s[prvi:drugi])
	ax.errorbar(tempera[drugi:konc], f2y[drugi:],yerr=f2s[drugi:], color='#ff3300')
	# ax.set_ylim(0,1)
	ax.set_title('Celotno območje')

	ax = axs[0,1]
	ax.errorbar(tempera[2:prvi], f2y[2:prvi],yerr=f2s[2:prvi], color='r')
	ax.set_title('Prvo segrevanje')

	ax = axs[1,0]
	ax.errorbar(tempera[prvi:drugi], f2y[prvi:drugi],yerr=f2s[prvi:drugi])
	ax.set_title('Ohlajanje')

	ax = axs[1,1]
	ax.errorbar(tempera[drugi:konc], f2y[drugi:],yerr=f2s[drugi:], color='#ff3300')
	ax.set_title('Drugo segrevanje')
	# plt.ylim(0, 1)
	plt.savefig(novapot + '/f2ji.jpg')

	s1y, s1s = [*zip(*s1)]

	fig, axs = plt.subplots(nrows=2, ncols=2)
	fig.suptitle('s1')
	ax = axs[0,0]
	ax.errorbar(tempera[2:prvi], s1y[2:prvi],yerr=s1s[2:prvi], color='r')
	ax.errorbar(tempera[prvi:drugi], s1y[prvi:drugi],yerr=s1s[prvi:drugi])
	ax.errorbar(tempera[drugi:konc], s1y[drugi:],yerr=s1s[drugi:], color='#ff3300')
	# ax.set_ylim(0,1)
	ax.set_title('Celotno območje')

	ax = axs[0,1]
	ax.errorbar(tempera[2:prvi], s1y[2:prvi],yerr=s1s[2:prvi], color='r')
	ax.set_title('Prvo segrevanje')

	ax = axs[1,0]
	ax.errorbar(tempera[prvi:drugi], s1y[prvi:drugi],yerr=s1s[prvi:drugi])
	ax.set_title('Ohlajanje')

	ax = axs[1,1]
	ax.errorbar(tempera[drugi:konc], s1y[drugi:],yerr=s1s[drugi:], color='#ff3300')
	ax.set_title('Drugo segrevanje')
	# plt.ylim(0, 1)
	plt.savefig(novapot + '/es1ji.jpg')

	s2y, s2s = [*zip(*s2)]

	fig, axs = plt.subplots(nrows=2, ncols=2)
	fig.suptitle('s2')
	ax = axs[0,0]
	ax.errorbar(tempera[2:prvi], s2y[2:prvi],yerr=s2s[2:prvi], color='r')
	ax.errorbar(tempera[prvi:drugi], s2y[prvi:drugi],yerr=s2s[prvi:drugi])
	ax.errorbar(tempera[drugi:konc], s2y[drugi:],yerr=s2s[drugi:], color='#ff3300')
	# ax.set_ylim(0,1)
	ax.set_title('Celotno območje')

	ax = axs[0,1]
	ax.errorbar(tempera[2:prvi], s2y[2:prvi],yerr=s2s[2:prvi], color='r')
	ax.set_title('Prvo segrevanje')

	ax = axs[1,0]
	ax.errorbar(tempera[prvi:drugi], s2y[prvi:drugi],yerr=s2s[prvi:drugi])
	ax.set_title('Ohlajanje')

	ax = axs[1,1]
	ax.errorbar(tempera[drugi:konc], s2y[drugi:],yerr=s2s[drugi:], color='#ff3300')
	ax.set_title('Drugo segrevanje')
	# plt.ylim(0, 1)
	plt.savefig(novapot + '/es2ji.jpg')

	jdy, jds = [*zip(*jd)]

	fig, axs = plt.subplots(nrows=2, ncols=2)
	fig.suptitle('jd')
	ax = axs[0,0]
	ax.errorbar(tempera[2:prvi], jdy[2:prvi],yerr=jds[2:prvi], color='r')
	ax.errorbar(tempera[prvi:drugi], jdy[prvi:drugi],yerr=jds[prvi:drugi])
	ax.errorbar(tempera[drugi:konc], jdy[drugi:],yerr=jds[drugi:], color='#ff3300')
	# ax.set_ylim(0,1)
	ax.set_title('Celotno območje')

	ax = axs[0,1]
	ax.errorbar(tempera[2:prvi], jdy[2:prvi],yerr=jds[2:prvi], color='r')
	ax.set_title('Prvo segrevanje')

	ax = axs[1,0]
	ax.errorbar(tempera[prvi:drugi], jdy[prvi:drugi],yerr=jds[prvi:drugi])
	ax.set_title('Ohlajanje')

	ax = axs[1,1]
	ax.errorbar(tempera[drugi:konc], jdy[drugi:],yerr=jds[drugi:], color='#ff3300')
	ax.set_title('Drugo segrevanje')
	# plt.ylim(0, 1)
	plt.savefig(novapot + '/jdji.jpg')
	fig.clf()

	kot = fit.q2(float(podatki[7]))
	Dji = []
	Djinorm = []

	for ii in f1y:
		Dji.append(ii/kot)
	print(len(Dji))
	print(len(tempera))
	for jj in range(len(tempera[:konc])):
		Djinorm.append(normalizacija(Dji[jj], tempera[jj], 0.9, 0.1))

	plt.clf()
	fig, axs = plt.subplots(nrows = 3, ncols=1)
	ax = axs[0]
	ax.plot(tempera[:prvi], Djinorm[:prvi], color='r')
	ax.set_title('Prvo segrevanje')
	# ax.get_ylabel('$D [\\times 10^{-10} m^{2}/s]$')
	ax = axs[1]
	ax.plot(tempera[prvi:drugi], Djinorm[prvi:drugi], color='b')
	ax.set_title('Ohlajanje')
	# ax.get_ylabel('$D [\\times 10^{-10} m^{2}/s]$')
	ax = axs[2]
	ax.plot(tempera[drugi:konc], Djinorm[drugi:], color='#ff3300')
	ax.set_title('Drugo segrevanje')
	# ax.get_ylabel('$D [\\times 10^{-10} m^{2}/s]$')
	plt.savefig(novapot + '/test.jpg')