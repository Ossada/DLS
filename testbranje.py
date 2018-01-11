import tkinter.filedialog as tk

pot = tk.askopenfilename(initialdir='/media/vid/SILICON 16G')
with open(pot, encoding='windows-1250') as file:
	for line in file:
		if '"StandardDeviation"' in line:
			for i in range(6):
				next(file)
			for line in file:
				print(line)