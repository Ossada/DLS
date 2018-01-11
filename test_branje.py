import tkinter.filedialog as tk
import time

pot = tk.askdirectory(initialdir='/home/vid/IJS/Meritve')

temper = []

indeks = 0
with open(pot + '/parametri.txt', 'r') as file:
	for i in range(4):
		next(file)
	for line in file:
		temp = line.strip().split(' ')
		temper.append(temp)


y0 = []
jd = []
A = []
f1 = []
f2 = []
s1 = []
s2 = []

for i in temper:
	# print(i)
	if 'mod' in i:
		continue
	if 'y0' in i:
		y0.append([i[1], i[2]])
		continue
	if 'jd' in i:
		jd.append([i[1], i[2]])
		continue
	if 'A' in i:
		A.append([i[1], i[2]])
		continue
	if 'f1' in i:
		f1.append([i[1], i[2]])
		continue
	if 'f2' in i:
		f2.append([i[1], i[2]])
		continue
	if 's1' in i:
		s1.append([i[1], i[2]])
		continue
	if 's2' in i:
		s2.append([i[1], i[2]])
		continue


