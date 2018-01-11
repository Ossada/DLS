import math


def n(T, lamb, ro):
    Tref = 273.15

    lambdaref = 589  # v nanometrih
    roref = 1000
    a0 = 0.244257733
    a1 = 9.74634476*10**(-3)
    a2 = -3.73234996*10**(-3)
    a3 = 2.68678472*10**(-4)
    a4 = 1.58920570*10**(-3)
    a5 = 2.45934259*10**(-3)
    a6 = 0.900704920
    a7 = -1.66626219*10**(-2)
    lambUV = 0.2292020
    lambIR = 5.432937

    B = a0 + a1*(ro/roref) + a2*(T/Tref) + a3*(T/Tref)*(lamb/lambdaref)**2 + \
        a4/(lamb/lambdaref)**2 + a5/((lamb/lambdaref)**2 - lambUV**2) + \
        a6/((lamb/lambdaref)**2 - lambIR**2) + a7*(ro/roref)**2

    return pow(((2*B + 1)/(1 - B)), 0.5)


# print(n(298, 700, 1000))

def visk(T):  # V stopinjah celzija
    vis20 = 1006.2  # v Pa s x10^-6
    b = ((20-T)/(T+96))*(1.2378 - 1.37*(20-T)*10**(-3) + \
        5.7*((20-T)**2)*10**(-6))
    return vis20 * 10**(b)

# print(visk(25.7))


def q2(fi):
    return ((4*math.pi*1.33*math.sin(fi*math.pi/360))/(532*10**(-9)))**2


def roH20(T):
    a0 = 0.9998396
    a1 = 18.224944e-3
    a2 = -7.922210e-6
    a3 = -55.44846e-9
    a4 = 149.7562e-12
    a5 = -393.2952e-15
    b = 18.159725e-3
    return ((a0 + a1*T + a2*T*T + a3*(T**3) + a4*(T**4) + a5*(T**5))/(1 + b*T))*1e3

def viskCrt(T, ro):  # V stopinjah celzija, kg/m3
    Tcrt = (T + 273.15)/647.27
    rocrt = ro/317.763
    prvi = (1/Tcrt) - 1
    drugi = rocrt - 1
    etazvezdica = 55.071

    Hk = [1, 0.978197, 0.579829, -0.202354]
    Hij = [[0.5132047, 0.2151778, -0.2818107, 0.1778064, -0.0417661, 0, 0],
           [0.3205656, 0.7317883, -1.070786, 0.460504, 0, -0.01578386, 0], 
           [0, 1.2141044, -1.263184, 0.2340379, 0, 0, 0],
           [0, 1.476783, 0, -0.4924179, 0.1600435, 0, -0.003629481],
           [-0.7782567, 0, 0, 0, 0, 0, 0],
           [0.1885447, 0, 0, 0, 0, 0, 0]]
    imen = 0
    for k in Hk:
        # print('k = ' + str(k) + '\n' + str(Tcrt) + ' na ' + str(Hk.index(k)))
        imen += (k/(pow(Tcrt, Hk.index(k))))
        # print('Seštevek je: ' + str(imen))
    # print(imen)
    eksp = 0

    # print(prvi, drugi)
    for i in Hij:
        t = 0
        for j in i:
            # print('i = ' + str(Hij.index(i)) + ', j = ' + str(t) + ', Hij = ' + str(j))
            vmes = j*(pow(prvi, Hij.index(i)))*pow(drugi, t)
            # print('Zmnožek = ' + str(vmes))
            eksp += vmes
            t += 1
            # print(eksp)
    konc = (math.sqrt(Tcrt)/imen)*math.exp(rocrt*eksp)

    return  konc * etazvezdica, konc

def viskozaD2O(T):
    a = 1301
    b = 930.349
    c = 7.8061
    d = 0.000833
    e = 3.30103
    log = a/(b + c*(T-20) + d*(T-20)*(T-20)) - e

    return math.pow(10, log)

def viskD20(T, ro):  # V stopinjah celzija, kg/m3
    T = T + 273.15
    f0 = 1.0914
    f1 = 0.3276
    f2 = 0.3721
    g0 = 1.0964
    Tcrt = T/647.27
    rocrt = ro/317.763

    f = f0 + f1 * (T - 1) + f2 * (Tcrt - 1)*(Tcrt - 1)

def normalizacijaD2O(D, T, ch2o, cd2o):
    nov_vis = ch2o * visk(T)/1000 + cd2o * viskozaD2O(T)
    visk25 = visk(25)/1000
    Dnorm = D * (298/(T+273))*(nov_vis/visk25)
    return Dnorm

def normalizacija(D, T):
    return D*(298/(T+273))*(visk(T)/visk(25))
  