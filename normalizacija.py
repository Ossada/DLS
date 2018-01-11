import tkinter.filedialog as tk
import matplotlib.pyplot as plt

def normal(a0sp, ksp, a0zg, kzg, T, A):

	 nov = A - ((a0sp + ksp * T)/((a0zg + kzg * T) - (a0sp + ksp * T)))

	 return nov

root = tk.Tk()
root.withdraw()
datoteka = tk.askopenfilename(initialdir='../Meritve/')
temper = []
absorb = []

with open(datoteka, 'r') as file:
	for line in file:
            temp = line.strip().split(',')
            temper.append(float(temp[0]))
            absorb.append(float(temp[1]))

norm = []
azg = 0.65744
asp = 0.81689
kZG = 0.00314
kSP = 0.00188
for i in range(len(temper)):
	b = normal(asp, kSP, azg, kZG, temper[i], absorb[i])
	norm.append(b)

plt.plot(temper, norm)
plt.show()
