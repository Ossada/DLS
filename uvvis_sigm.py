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

def sigmoida(parametri, xdata, ydata):
    A1 = parametri['A1'].value
    A2 = parametri['A2'].value
    x0 = parametri['x0'].value
    d0 = parametri['d0'].value

    model = A2 + ((A1 - A2)/(1 + np.exp((xdata - x0)/d0)))

    return model - ydata

    
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


if __name__ == '__main__':
    # import matplotlib.pyplot as plt
    # import os
    # from tkinter import filedialog



    root = filedialog.Tk()
    root.withdraw()
    pot = filedialog.askdirectory(initialdir='/home/vid/IJS/Meritve')

    seznam = os.listdir(pot)
    di = {}
    temperatura = []
    absor = []
    vzor = poimenovanje(seznam)
    # print(seznam)

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
        mode = input('Vnesi SEG1, SEG2, ali OHL: ')
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
        par = lm.Parameters()
        par.add('A1', value=1)
        par.add('A2', value=0)
        par.add('x0', value=50, min=10, max=90)
        par.add('d0', value=1)

        result = lm.minimize(sigmoida, par, args=(data[:, 0], data[:, 1]))
        lm.report_fit(result.params, show_correl=False)
        tem = []
        for i in result.params:
            tem.append(((str(result.params[i]).split(',')[1]).split('=')[1]).split('+/-'))
        print(tem)
        print(tem[2][0])
        final = data[:, 1] + result.residual

        print('mimo printa')

        plt.plot(data[:, 0], final, color=fit, linewidth=2)
        plt.title(title)
        text = '$T_m=%.2f$ $\pm$ $%.2f ^o C$' % (float(tem[2][0]), float(tem[2][1]))
        # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.65, 0.05, text, transform=ax.transAxes, fontsize=14,
                verticalalignment='top')
        v = '${0}$\n${1}mM$ $oligo$\n${2} mM$ $NaCl$\n${3} mM$ $NaPi$\n$Denaturirano:$ ${4}$\n$Merjeno:$ ${5}$'.format(vzor[0], vzor[1], vzor[2], vzor[3], vzor[4], vzor[5])
        ax.text(0.05, 0.4, v, transform=ax.transAxes, fontsize=14, verticalalignment='top')
        plt.draw()
        save = input('Press s to save, anything else to continue: ')
        if save == 's' or save == 'S':
            plt.savefig(pot+ '/' + mode + '.jpg')
            print('Saved!')
        plt.close()
        repeat = int(input('Vnesi 1 za ponovno fitanje ali 0 za končanje: '))
    # Block end of script so you can check that the lasso is disconnected.

