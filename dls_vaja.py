import tkinter.filedialog as tk
import scipy.optimize as sp
import natsort
import os
import matplotlib.pyplot as plt
import numpy as np


def beri(poti):
    lagtime = []
    corr = []
    with open(poti, encoding='windows-1250') as file:
        for i in range(33):
            next(file)
        for line in file:
            temp = line.strip().split('\t')
            if '' in temp:
                break
            lagtime.append(float(temp[0]))
            corr.append(float(temp[1]))

    return np.array(lagtime), np.array(corr)


def fun(x, f1, A, y0):
    return A * np.exp(-x * f1) + y0


def q2(fi):
    return ((4*np.pi*1.33*np.sin(fi*np.pi/360))/(532*10**(-9)))**2


def risanje(ime):
    fig, ax = plt.subplots(1)
    plt.plot(xdata, ydata, 'bo', alpha=0.8)
    plt.plot(xdata, fun(xdata, para[0], para[1], para[2]), 'r')
    # plt.plot(xdata, fl(xdata, latp[0], latp[1], latp[2]), 'r', linewidth=2.0)
    plt.title(str(ime))
    plt.xscale('log')
    plt.xlabel('$Time$ $[ms]$', fontsize=14)
    plt.ylabel('$g(2)-1$', fontsize=14)
    plt.ylim(0, 1.1)
    text = '$f_{1}=%.4f$\n$A=%.4f$\n$y_{0}=%.4f$' \
          % (para[0], para[1], para[2])
    # text = '$f_{3}={0}$\n$A={1}$\n$y_{4}={2}$'.format(round(latp[0], 4), round(latp[1], 4), round(latp[2], 4), "{1}", "{0}")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    # plt.show()
    plt.savefig(pot + '/' + str(a) + '.jpg')
    plt.close()

### MAIN ##

pot = tk.askdirectory(initialdir='/home/vid/Faks/2.stopnja/Fizikalni eksperimenti/DLS/')
seznam = natsort.natsorted(os.listdir(pot))

# print(seznam)
file = open(pot + '/parametri.txt', 'w')  # Pisanje fitanih parametrov
slovar = {}
for a in seznam:
    if a[-4:] == '.ASC':
        xdata, ydata = beri(pot + '/' +a)  # Prebere podatke
        file.write(str(a) + '\n')
        try:
            para, err = sp.curve_fit(fun, xdata, ydata)  # Fita eksponent (definiran zgoraj)
            file.write(str(para) + '\n' + str(err) + '\n')
        except Exception as e:  # Če je kaj narobe, pove kaj
            print(e)
        try:
            kot = a.split('_')[1].split('.')[0]  # razdeli ime datoteke na 3 dele (za ločilo uporabi _ ) in določi drugi element za kot
        except IndexError:
            kot = 90
        try:
            kot = float(kot)
            vekt = q2(kot)  # izračuna valovni vektor glede na kot
            file.write(str(vekt) + '\n \n')
        except Exception as E:
            print(E)
        risanje(a)

file.close()

