__author__ = 'vid'
import tkinter.filedialog as tk
import matplotlib.pyplot as plt
from matplotlib.patches import *
import os

# root = tk.Tk()
# root.withdraw()
pot = tk.askdirectory(initialdir='/home/vid/IJS/Meritve/')
ime = pot[22:]
ime1 = ime.split('/')
print(ime1)
seznam = os.listdir(pot)
di = {}
temperatura = []
absor = []
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

# print (di)
# print(di)
seznam = list(di.keys())

try:
    fig, ax = plt.subplots(1)
    plt.plot(di['SEG1'][0], di['SEG1'][1], 'r', label='Prvo segrevanje')
    plt.plot(di['OHL'][0], di['OHL'][1], 'b', label='Ohlajanje')
    plt.plot(di['SEG2'][0], di['SEG2'][1], color='#ff6400', label='Drugo segrevanje')
    tex = '$c=0.5mM$ $Seq4Amod35$ $+$' + '\n' '$10mM$ $NaPi$ $+$ $100mM$ $NaCl$' +\
        '\n' + '$\\lambda = 295 nm$'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.35, 0.95, tex, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.xlabel('$Temperatura$ $[^{\\circ}]$')
    plt.ylabel('$Absorbcija$')
    plt.xlim(10,90)
    # plt.title(ime1[1])
    # fully use the given bounding box.
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
    # plt.ylim(-0.01, 0.01)
    try:
        plt.savefig(pot + '/' + str(ime1[0]) + '.jpeg')
        print('Shranjeno?')
    except:
       plt.savefig(pot + '/' + str(ime1[1]) + '.jpeg')
    plt.show()
    print(pot + '/'  + str(ime1[2])+ '.jpeg')

except Exception as e:
    print(e)

#
# for ne in di:
#     for i in range(len(di[ne][1])-1):
#         vmes = abs(di[ne][1][i+1] - di[ne][1][i])
#
#         if vmes > 0.017:
#             try:
#                 ods = (di[ne][1][i+1] + di[ne][1][i+2])/2 -(di[ne][1][i] + di[ne][1][i-1])/2
#                 tocka = i
#             except:
#                 pass
#         try:
#             di[ne][1][i+1] -= ods
#         except:
#             pass
#     try:
#         di[ne][1][tocka] += ods
#     except:
#         pass
#     tocka = 0
#     ods = 0
#
# try:
#     plt.plot(di['SEG1'][0], di['SEG1'][1], 'y')
#     plt.plot(di['OHL'][0], di['OHL'][1], 'b')
#     plt.plot(di['SEG2'][0], di['SEG2'][1], 'r')
#     plt.xlim(5, 100)
#     plt.xlabel('$Temperature$ $[^{\\circ}C]$')
#     plt.ylabel('$Absorbtion$')
#     plt.show()
#     # plt.close()
# except:
#     pass
# try:
#     fig, ax = plt.subplots(1)
#     plt.plot(di['SPEKC'][0], di['SPEKC'][1], 'b')
#     print(di['SPEKT'])
#     plt.plot(di['SPEK2'][0], di['SPEK2'][1], 'r')
#     plt.plot(di['SPEK3'][0], di['SPEK3'][1], 'g')
#     plt.xlabel('$\\lambda$ $[nm]$')
#     plt.xlim(182, 320)
#     plt.ylim(0, 4.2)
#     plt.ylabel('$Absorbtion$')
#     tex = '$c=1mM$ $Seq4Amod3$ $+$ $10mM$ $NaPi$ $+$ $100mM$ $NaCl$'
#     props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#     ax.text(0.08, 0.10, tex, transform=ax.transAxes, fontsize=14,
#             verticalalignment='top', bbox=props)
#     plt.show()
# except:
#     pass