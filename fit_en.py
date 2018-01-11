import lmfit as lm
import tkinter.filedialog as tk
import numpy as np
import fitDLS as fit
import matplotlib.pyplot as plt

values = []
root = tk.Tk()
# root.withdraw()
pot = tk.askopenfilename(initialdir='/home/vid/IJS/Meritve/seq4Amod3 daša/gretje 175 NaCl/')
values = [-0.0715, 0.7, 0.33, 52, 0.37, 0.8, 0.9]

print(values)

params = lm.Parameters()
params.add('A', value=values[0])
params.add('y0', value=values[1])
params.add('jd', value=values[2], min=0, max=10)
params.add('f1', value=values[3], min=0)
params.add('f2', value=values[4])
params.add('s1', value=values[5], min=0, max=1)
params.add('s2', value=values[6], min=0, max=1)

spod = 20
zgor = 180

xdata, ydata = fit.beri(pot)
erro = fit.berierr(pot)
print('ydata: ' + str(len(ydata)))
print('err: ' + str(len(erro)))

eps = 0
naj = 180
for i in range(100, 180):
	if ydata[i-1] < (ydata[i] - 0.001):
		if i < naj:
			naj = i
		eps += 0.1
if eps > 0.2:
	print('Zaznana stopnica pri mestu: ' + str(naj) + ', moč: ' + str(eps))
	zgor = naj

result = lm.minimize(fit.slowfastmode, params, args=(xdata[spod:zgor], ydata[spod:zgor]))
final = ydata[spod:zgor] + result.residual

# a = lm.report_fit(result.params, show_correl=False)
rezul = {'A' : 0, 'y0' : 0, 'jd' : 0, 'f1' : 0, 'f2' : 0, 's1' : 0, 's2' : 0}
tem = []
for a in result.params:
    tem.append(((str(result.params[a]).split(',')[1]).split('=')[1]).split('+/-'))

pot1 = tk.askdirectory(initialdir='/home/vid/IJS/Meritve/seq4Amod3 daša/gretje 175 NaCl/')
# print(tem)
tem = [[float(j) for j in i] for i in tem]
file = open(pot1 + '/parametri' + pot[-10:] + '.txt', 'w')
for a in tem:
    file.write('%s\n' % a[0])
file.close()
print(tem)

fig, ax = plt.subplots(1)

plt.plot(xdata, ydata, 'bo', alpha=0.8)
plt.plot(xdata[spod:zgor], final, 'r', linewidth=2)
plt.xscale('log')
plt.xlabel('$\\tau$ $[ms]$', fontsize=22)
plt.ylabel('$g^{(2)}(\\tau)-1$', fontsize=22)
# plt.ylim(0, 1.1)
text = '$y_{0}=%.4f$ \n$j_{d}=%.4f$\n$A=%.4f$\n$f_{1}=%.4f$\n$f_{2}=%.4f$\n$s_{1}=%.4f$\n$s_{2}=%.4f$' \
          % (float(tem[1][0]), float(tem[2][0]), float(tem[0][0]), float(tem[3][0]),
             float(tem[4][0]), float(tem[5][0]), float(tem[6][0]))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.70, 0.95, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

plt.savefig(pot + '1.jpg')
plt.show()

plt.close()
