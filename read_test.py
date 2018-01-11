import tkinter.filedialog as tk
import os

pot = tk.askdirectory()
seznam = os.listdir(pot)

vzorec = []

if 'vzorec.txt' in seznam:
	a = open('vzorec.txt', 'r')
	for b in a:
		print(b)
		vzorec.append(b.strip())
	print(vzorec)