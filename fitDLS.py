__author__ = 'vid'
import os
import numpy as np
import lmfit as lm
import matplotlib.pyplot as plt
from matplotlib.patches import *
import natsort
import tkinter.filedialog as tk
from lomnikol import *


def beri(poti):
    lagtime = []
    corr = []
    with open(poti, encoding='windows-1250') as file:
    # with open(poti) as file:
        for i in range(33):
            next(file)
        for line in file:
            temp = line.strip().split('\t')
            if '' in temp:
                break
            lagtime.append(float(temp[0]))
            corr.append(float(temp[1]))

    return np.array(lagtime), np.array(corr)

def beri2(poti):
    lagtime = []
    corr = []
    with open(poti, encoding='windows-1250') as file:
    # with open(poti) as file:
        next(file)
        temporary = file.readline().strip().split('\"')[1]
        temporary2 = file.readline().strip().split('\"')[1]
        time = str(temporary2) + ' ' + str(temporary)
        print(time)
        for i in range(28):
            next(file)
        for line in file:
            temp = line.strip().split('\t')
            if '' in temp:
                break
            lagtime.append(float(temp[0]))
            corr.append(float(temp[1]))

    return np.array(lagtime), np.array(corr), time

def berierr(poti):
    err = []
    with open(poti, encoding='windows-1250') as file:
        for line in file:
            if '"StandardDeviation"' in line:
                for i  in range(8):
                    next(file)
                for line in file:
                    temp = line.strip().split('\t')
                    if '' in temp:
                        break
                    err.append(float(temp[1]))
    return np.array(err)

def berierr2(poti):
    err = []
    with open(poti, encoding='windows-1250') as file:
        for line in file:
            if '"StandardDeviation"' in line:
                next(file)
                for line in file:
                    temp = line.strip().split('\t')
                    if '' in temp:
                        break
                    err.append(float(temp[1]))
    return np.array(err)

def slowfastmode(params, xdata, ydata):
    A = params['A'].value
    y0 = params['y0'].value
    jd = params['jd'].value
    f1 = params['f1'].value
    f2 = params['f2'].value
    s1 = params['s1'].value
    s2 = params['s2'].value

    model = y0 + (1 + jd * ((A * np.exp(-pow(f1 * xdata, s1))) +
                            ((1 - A) * np.exp(-pow(f2 * xdata, s2))) - 1)) ** 2
    return model - ydata


def q2(fi):
    return ((4*math.pi*1.33*math.sin(fi*math.pi/360))/(532*10**(-9)))**2


def parametri(slovar):
    temp = []
    for i in slovar:
        temp.append(((str(slovar[i]).split(',')[1]).split('=')[1]).split('+/-'))
    return temp


def zapis(sez, file):
    for i in sez:
        val, err = i
        file.write(val + ' ' + err + '\n')
    file.write('\n')


def risanje(i, b):
    fig, ax = plt.subplots(1)
    plt.plot(xdata, ydata, 'bo', alpha=0.8)
    plt.plot(xdata[spod:zgor], final, 'r', linewidth=2)
    plt.xscale('log')
    plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
    plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
    plt.ylim(0, 1.1)
    D = (float(tem[3][0])/q2(b))/1e-13 
    D = normalizacija(D, 24.4) ## SPREMENI KOT!!!!
    #plt.title('$0.5mM$' + ' ' + '$Seq4A,$' + '$T={0:4.2f}$'.format(temp[i]))
    text = '$y_{0}=%.4f$\n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$\n$D_{25}=%.5f$' \
          % (float(tem[1][0]), float(tem[2][0]), float(tem[0][0]), float(tem[3][0]),
             float(tem[4][0]), float(tem[5][0]), float(tem[6][0]), D)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.savefig(pot + '/' + str(j) + '.png')
    plt.close()

def risanje2(st):
    barve = ['k', 'b', 'g', 'm', 'r', 'y']

    if st%10 == 0:
        k += 1
        fig, ax = plt.subplots(1)
        plt.xscale('log')
        plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
        plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
        plt.ylim(0, 1.1)
        plt.plot(xdata, ydata, barve[k])

if __name__ == '__main__':

    root = tk.Tk()
    root.withdraw()
    pot = tk.askdirectory(initialdir='/home/vid/MEGA')  # odpremo datoteke za fit
    seznam = os.listdir(pot)
    seznam = natsort.natsorted(seznam)
    fji = []
    fjierr = []
    serije = {}
    temp = []   
    indeks = -1
    values = [-0.1, 0.1, 0.1, 10, 0.1, 0.5, 0.5]
    spod = 2
    zgor = 175
    pot1 = tk.askopenfilename(initialdir=pot)  # odpremo datoteko s temperaturo
    print(pot1)
    k=-1  #test

    with open(pot1, 'r') as file:
        try:
            for line in file:
                temp.append(float(line.split(' ')[0]))  # Odpre datoteko s temperaturami, uporabljeno za izpis grafov
                for i in range(3):
                    next(file)
        except StopIteration:
            pass

    file = open(pot + '/parametri.txt', 'w')

    a = input('Vnesi začetno daoteko (0 za fitanje od začetka): ')
    a = int(a)
    ko = int(input('Kot meritve: '))
    for j in seznam[a:]:
        if j[-4:] == '.ASC':
            xdata, ydata, timestr = beri2(pot + '/' + j)

            try:
                params = lm.Parameters()
                params.add('A', value=values[0])
                params.add('y0', value=values[1])
                params.add('jd', value=values[2])#,# min=0, max=10)
                params.add('f1', value=values[3])#, min=0)
                params.add('f2', value=values[4])
                params.add('s1', value=values[5], min=0, max=1)
                params.add('s2', value=values[6], min=0, max=1)
                indeks += 1
                result = lm.minimize(slowfastmode, params, args=(xdata[spod:zgor], ydata[spod:zgor]))
                print('Datoteki ' + j + ' se prilega krivulja!')
                final = ydata[spod:zgor] + result.residual
                print(result.params)
                tem = parametri(result.params)
                lm.report_fit(result.params, show_correl=False)
                file.write(j + '\n' + timestr + '\n')
                zapis(tem,file)
                values = [float(c[0]) for c in tem]
                risanje(indeks, ko)
                # risanje2(indeks)
            except Exception as e:
                print('Z ' + j + ' je neki narobe!')
                print(e)
                plt.plot(xdata, ydata, 'ro')
                plt.xscale('log')
                plt.savefig(pot + '/' + str(j) + '.png')
                plt.close()
                pass
        if a == 'AutoSaveFileName0057.ASC':
            break
    plt.show()
    file.close()
# print(temp)
#
# fig, ax = plt.subplots(1)
# plt.xscale('log')
# plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
# plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
# plt.ylim(0, 1.1)
# barve =  ['k', 'b', 'g', 'm', 'r', 'y', 'c']
# for a in seznam:
#     if a[-4:] =='.ASC':
#         xdata, ydata = beri(pot + '/' + a)
#         indeks +=1
#         if indeks%11==0:
#             plt.plot(xdata, ydata, barve[indeks//10], label='{0:4.2f} °C'.format(temp[indeks]), linewidth=2)
# plt.legend()
# plt.show()