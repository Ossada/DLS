import os
import natsort
import matplotlib.pyplot as plt
import datetime
import tkinter.filedialog as tk
from fitDLS import q2

def odpri(pot):
	time = []
	fji = []
	ferr = []
	with open(pot) as fil:
		for i, line in enumerate(fil):
			if (i+1)%10 == 2:
				time.append(line.strip())
			if (i+1)%10 == 6:
				temp = line.split('   ')
				fji.append(float(temp[0]))
				ferr.append(float(temp[1]))
	return time, fji, ferr


if __name__ == '__main__':

	root = tk.Tk()
	root.withdraw()

	pot = tk.askopenfilename(initialdir='/home/vid/MEGA/Meritve DLS/G4C2/staranje/')
	time, fji, ferr = odpri(pot)

# print(fji, ferr, time)
	time_true1 = []
	for i in time:
		time_true1.append(datetime.datetime.strptime(i, '%H:%M:%S %d.%m.%Y'))

	#print(time_true)
	time_final = [time_true1[j]-time_true1[0] for j in range(len(time_true1))]
	#print(time_final)

	time_final1 = [k.days*24*60 + k.seconds/60 for k in time_final]

	#print(time_final)

	Dji1 = [f/q2(90)/10e-14 for f in fji]

	root = tk.Tk()
	root.withdraw()

	pot = tk.askopenfilename(initialdir='/home/vid/MEGA/Meritve DLS/G4C2/staranje/')
	time, fji, ferr = odpri(pot)
	time_true2 = []
	for i in time:
		time_true2.append(datetime.datetime.strptime(i, '%H:%M:%S %d.%m.%Y'))

	#print(time_true)
	time_final = [time_true2[j]-time_true1[0] for j in range(len(time_true2))]
	#print(time_final)

	time_final2 = [k.days*24*60 + k.seconds/60 for k in time_final]

	#print(time_final)

	Dji2 = [f/q2(80)/10e-14 for f in fji]



	root = tk.Tk()
	root.withdraw()

	pot = tk.askopenfilename(initialdir='/home/vid/MEGA/Meritve DLS/G4C2/staranje/')
	time, fji, ferr = odpri(pot)
	time_true3 = []
	for i in time:
		time_true3.append(datetime.datetime.strptime(i, '%H:%M:%S %d.%m.%Y'))

	#print(time_true)
	time_final = [time_true3[j]-time_true1[0] for j in range(len(time_true3))]
	#print(time_final)

	time_final3 = [k.days*24*60 + k.seconds/60 for k in time_final]

	#print(time_final)

	Dji3 = [f/q2(80)/10e-14 for f in fji]
	print(Dji3)

	D = Dji1 + Dji2 +Dji3
	timef = time_final1 + time_final2 + time_final3

	s1 = '11:33:35 1.12.2017'
	s1time = datetime.datetime.strptime(s1, '%H:%M:%S %d.%m.%Y')
	timet = s1time - time_true1[0]
	t1 = timet.days*24*60 + timet.seconds/60 
	D1 = 0.82079

	s2 = '10:11:34 7.12.2017'
	s2time = datetime.datetime.strptime(s2, '%H:%M:%S %d.%m.%Y')
	timet = s2time - time_true1[0]
	t2 = timet.days*24*60 + timet.seconds/60 
	D2 = 0.66992

	s3 = '11:45:23 11.12.2017'
	s3time = datetime.datetime.strptime(s3, '%H:%M:%S %d.%m.%Y')
	timet = s3time - time_true1[0]
	t3 = timet.days*24*60 + timet.seconds/60 
	D3 = 0.67219

	s4 = '12:09:23 13.12.2017'
	s4time = datetime.datetime.strptime(s4, '%H:%M:%S %d.%m.%Y')
	timet = s4time - time_true1[0]
	t4 = timet.days*24*60 + timet.seconds/60 
	D4 = 0.67323

	if len(D)==len(timef):
		plt.ion()
		plt.plot(timef, D, 'bo')
		plt.scatter([t1, t2, t3, t4],  [D1, D2, D3, D4], marker='o', color='red', s=50)
		plt.ylabel('D [$\\times 10^{-10}$' + ' $m^{2}/s$]', fontsize=16)
		plt.xlabel('Time [min]', fontsize=16)
		plt.savefig('/home/vid/MEGA/Meritve DLS/G4C2/staranje/dji.png')
		plt.close() 	
	else:
		print(len(Dji), len(timef))