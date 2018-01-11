from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import *
import os
from tkinter import filedialog
import lmfit as lm


class SelectFromCollection(object):
    """Select indices from a matplotlib collection using `LassoSelector`.

    Selected indices are saved in the `ind` attribute. This tool highlights
    selected points by fading them out (i.e., reducing their alpha values).
    If your collection has alpha < 1, this tool will permanently alter them.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    collection : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, self.Npts).reshape(self.Npts, -1)

        self.lasso = LassoSelector(ax, onselect=self.onselect)  # Sprememba glede na originalno kodo
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero([path.contains_point(xy) for xy in self.xys])[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

def premica(parametri, x, y):
    k = parametri['k'].value
    n = parametri['n'].value

    model = k*x + n

    return model - y

def poimenovanje(lista):
    vzorec = []
    if 'vzorec.dat' in lista:
        a = open(pot + '/vzorec.dat', 'r')
        for b in a:
            print(b)
            vzorec.append(b.strip())
        print(vzorec)

    if 'vzorec.dat' not in lista:
        a = open(pot + '/vzorec.dat', 'w')
        vzorec.append(input('Vnesi ime vzorca: '))
        a.write(str(vzorec[0]) + '\n')
        vzorec.append(input('Vnesi koncentracijo oligonukleotida v mM: '))
        a.write(str(vzorec[1]) + '\n')
        vzorec.append(input('Vnesi koncentracijo soli v mM: '))
        a.write(str(vzorec[2]) + '\n')
        vzorec.append(input('Vnesi koncentracijo pufra v mM: '))
        a.write(str(vzorec[3]) + '\n')
        vzorec.append(input('Vnesi datum denaturacije: '))
        a.write(str(vzorec[4]) + '\n')
        vzorec.append((input('Vnesi datum meritve: ')))
        a.write(str(vzorec[5]) + '\n')
    a.close()
    return vzorec

def zvitje(ydata, xdata, k1, n1, k2, n2):
    stevec = ydata - (k2*xdata + n2)
    imenovalec = (k1*xdata + n1) - (k2*xdata + n2)
    return stevec/imenovalec



if __name__ == '__main__':

    root = filedialog.Tk()
    root.withdraw()
    pot = filedialog.askdirectory(initialdir='/home/vid/IJS/Meritve')

    seznam = os.listdir(pot)
    seznam = os.listdir(pot)
    di = {}
    temperatura = []
    absor = []
    vzor = poimenovanje(seznam)
    for a in seznam:
        if a[-4:] == '.txt':
            key = a.split('.')[0]
            # print('nutr')
            # try:
            with open(pot + '//' + a, encoding='windows-1250') as file:
                next(file)
                for line in file:
                    temp = line.split(',')
                    temperatura.append(float(temp[0]))
                    absor.append(float(temp[1]))
                di[key] = ([temperatura, absor])
            # except:
            #     print(a)
            temperatura = []
            absor = []
    repeat = 1

    while(repeat):
        text = str(list(di.keys())).rstrip(']').lstrip('[')
        mode = input('Vnesi ' + text + ': ')

        if mode == 'SEG1':
            title = 'Prvo segrevanje'
            color = 'r'
            fit = 'b'
        if mode == 'SEG2':
            title = 'Drugo segrevanje'
            color = '#ff6400'
            fit = 'b'
        if mode == 'OHL':
            title = 'Ohlajanje'
            color = 'b'
            fit = 'r'

        plt.ion()
        plt.draw()
        subplot_kw = dict(autoscale_on=True)
        fig, ax = plt.subplots(subplot_kw=subplot_kw)

        pts = ax.scatter(di[mode][0], di[mode][1], s=10, color=color, edgecolors='none')
        plt.xlabel('Temperatura [°C]')
        plt.ylabel('Absorpcija')
        selector = SelectFromCollection(ax, pts)


        input('Press any key to accept selected points')
        data = selector.xys[selector.ind]
        # print("Selected points:")
        # print(selector.xys[selector.ind])
        # print(type(selector.xys[selector.ind]))
        selector.disconnect()
        # x0 = input('Enter approximate x0 value! ')
        # try:
        #     x0 = float(x0) - 10
        # except Exception as e:
        #     print('Invalid characters!')
        #     x0 = input('Enter approximate x0 value! ')
        #     x0 = float(x0) - 10
        selector = SelectFromCollection(ax, pts)


        input('Press any key to accept selected points')
        data2 = selector.xys[selector.ind]
        # print("Selected points:")
        # print(selector.xys[selector.ind])
        # print(type(selector.xys[selector.ind]))
        selector.disconnect()

        par = lm.Parameters()
        par.add('k', value=1)
        par.add('n', value=1)

        result1 = lm.minimize(premica, par, args=(data[:, 0], data[:, 1]))
        lm.report_fit(result1.params)
        tem = []
        for i in result1.params:
            tem.append(((str(result1.params[i]).split(',')[1]).split('=')[1]).split('+/-'))
        print(tem)
        # print(tem[2][0])
        final = data[:, 1] + result1.residual

        result2 = lm.minimize(premica, par, args=(data2[:, 0], data2[:, 1]))
        lm.report_fit(result2.params)
        tem2 = []
        for i in result2.params:
            tem2.append(((str(result2.params[i]).split(',')[1]).split('=')[1]).split('+/-'))
        print(tem2)
        # print(tem[2][0])
        final2 = data2[:, 1] + result2.residual

        plt.plot(data[:, 0], final, color=fit, linewidth=2)
        plt.plot(data2[:, 0], final2, color=fit, linewidth=2)
        v = '${0}$\n${1}mM$ $oligo$\n${2} mM$ $NaCl$\n${3} mM$ $NaPi$\n$Denaturirano:$ ${4}$\n$Merjeno:$ ${5}$'.format(vzor[0], vzor[1], vzor[2], vzor[3], vzor[4], vzor[5])
        plt.text(0.05, 0.4, v, transform=ax.transAxes, fontsize=14, verticalalignment='top')
        plt.title(title)
        plt.draw()
        s = input('Vnesi s za shranjevanje, karkoli drugega za nadaljevanje: ')
        if s == 's' or s == 'S':
            plt.savefig(pot + '/' + mode + '_premica.jpg')
            print('Shranjeno!')
        plt.close()

        k1 = float(tem[0][0])
        n1 = float(tem[1][0])

        k2 = float(tem2[0][0])
        n2 = float(tem2[1][0])

        normalizirano = []
        for i in range(len(di[mode][0])):
            normalizirano.append(zvitje(di[mode][1][i], di[mode][0][i], k1, n1, k2, n2))

        bl = []
        raz = 1
        for i in range(len(normalizirano)):
            n = abs(normalizirano[i]-0.5)
            if n < 0.01:
                if n < raz:
                    raz = n
                    bl = [i, normalizirano[i]]



        print(bl)
        tex = '$T_m = {0:.2f}^o C$'.format(di[mode][0][bl[0]])
        print(tex)
        fig = plt.figure()
        plt.plot(di[mode][0], normalizirano)
        plt.axhline(0.5, color='r')
        plt.title(title)
        plt.text(0.7, 0.6, tex, transform=ax.transAxes, fontsize=14, verticalalignment='top')
        plt.xlabel('$Temperatura [^o C]$')
        v = '${0}$\n${1}mM$ $oligo$\n${2} mM$ $NaCl$\n${3} mM$ $NaPi$\n$Denaturirano:$ ${4}$\n$Merjeno:$ ${5}$'.format(vzor[0], vzor[1], vzor[2], vzor[3], vzor[4], vzor[5])
        plt.text(0.05, 0.4, v, transform=ax.transAxes, fontsize=14, verticalalignment='top')        
        plt.ylim(0, 1.05)
        plt.xlim(5, 95)

        plt.draw()
        plt.show()
        s1 = input('Vnesi s za shranjevanje, karkoli drugega za nadaljevanje! ')
        if s1 == 's' or s1 == 'S':
            fig.savefig(pot + '/' + mode + '_norm.jpg', dpi=fig.dpi)
        plt.close()
        repeat = int(input('Vnesi 1 za ponovno fitanje ali 0 za končanje: '))






    