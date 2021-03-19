import numpy as np
import matplotlib.pyplot as plt
import os.path
import statistics as stats
import sys

'''Arrays para automatizarlo'''
zsims = ['0', '0.142']  # ,'3.61', '4.038','5.017']
simnom = ['SAGE']
cm = plt.get_cmap('tab10')  # Colour map to draw colours from

'''True o False si estoy haciendo un test o el programa entero'''
test = True
n = 1000

'''Hago los bines de masa'''

# Cortes de las masas, la masa mínima y la masa máxima que voy a usar:
gmin = 8.5
gmax = 12.3

# intervalo:
dex = 0.2
# límites de los intervalos y punto del medio:
gedges = np.array(np.arange(gmin, gmax + dex, dex))  # Desde gmin hasta gmax+dex sumando dex cada vez.

ghist = gedges[1:] - 0.5 * dex  # centros de los intervalos, que es lo que nos interesa

for iiz in range(len(zsims)):

    '''Leemos el archivo'''
    ffsim = 'C:/Users/Olivia/TFG-TUT/Datos_simulaciones/Mass_SFR_SAGE_z_' + zsims[iiz] + '.csv'

    if not os.path.isfile(ffsim):
        continue

    # print(ffsim)
    # dataSim = np.loadtxt(ffsim, dtype=str, unpack=True)  # dtype str para poder leer palabras también.
    # f = open(ffsim, 'r') #'r': python read file.

    '''Definimos lista de colores'''
    cols = []
    col = cm(1. * iiz / len(zsims))
    cols.append(col)

    '''inicializamos contadores'''
    sumasfr = np.zeros(shape=len(ghist))  # SFR acumulativa
    ngal = np.zeros(shape=len(ghist))  # numero de galaxias
    medias = np.zeros(shape=len(ghist))  # media(sumasfr/ngal)
    errormedias = np.zeros(shape=len(ghist))  # error de la media (sig/sqrt(ngal))
    sig = np.zeros(shape=len(ghist))  # Desviación estándar sqrt((sum(sfr-medias)^2/ngal-1))

    '''Empezamos a leer linea a linea'''
    ff = open(ffsim, 'r')
    iline = -1  # Para que en el bucle empiece en el 0


    for line in ff:
        iline += 1  # Cuenta las lineas que ya hay en el fichero. Quizá no haría falta ya que el fichero ya las tiene
        # contadas, preguntar a Violeta qué es más eficiente.
        char1 = line[0]  # Primer caracter de la linea 1.

        if not char1.isdigit(): continue  # (para saltar header)

        if test and iline > n:
            continue


        data = np.array(line.split(','),
                        dtype=float)  # Así ya va a ser float, data[0] = columna que cuenta, data[1] = masas, data[2] = SFR

        SFR = data[2]
        Mass = data[1]


        # loop por los bines las masas hasta el penultimo edge
        for ie, edge in enumerate(gedges[:-1]):
            # print(ie,gedges[ie],gedges[ie+1])
            # print (Mass, edge, ie,gedges[ie],gedges[ie+1] )
            if Mass >= gedges[ie] and Mass < gedges[ie + 1]:
                sumasfr[ie] = sumasfr[ie] + SFR
                ngal[ie] = ngal[ie] + 1
                break

                # print(gedges[ie],gedges[ie+1], Mass)
            # print(ie, len(gedges) -2, iline)

        # Aquí llegan todas las SFR

    # OJO
    #Una vez
    # Una vez leído el fichero calculamos las MEDIAS con los números totales en cada bin. Hay que leer
    # el fichero y por eso salir del loop del fichero.
    for ie, edge in enumerate(gedges[:-1]):
        if ngal[ie] > 1:
            medias[ie] = sumasfr[ie] / ngal[ie]
    #print(medias, len(medias))

    # OJO
    # Segunda lectura del fichero para calcular los errores


    for line in ff:
        print(ffsim)
        iline += 1
        char1 = line[0]  # Primer caracter de la linea 1.

        if not char1.isdigit():
            continue  # (para saltar header)


        if test and iline > n:
            break    #He puesto un continue, porque con el break se paraba el código aquí, sin embargo arriba
                        # funciona con el break, no entiendo por qué. Sigo, dejando uno de cada a ver qué pasa.



        data = np.array(line.split(','),
                        dtype=float)  # Así ya va a ser float, data[0] = columna que cuenta, data[1] = masas, data[2] = SFR
        SFR = data[2]

'''



        for ie, edge in enumerate(gedges[:-1]):
            # Addition for the numerator
            sig[ie] = sig[ie] + (SFR - medias[ie]) ** 2
            print(sig[ie])

        print(SFR)

    # Una vez leído todo el fichero calculamos los ERRORES con los números totales en cada bin. Hay que leer todo
    # el fichero y por eso salir del loop del fichero.
    for ie, edge in enumerate(gedges[:-1]):
        if ngal[ie] > 1:
            sig[ie] = (sig[ie] / ((ngal[ie]-1)*ngal[ie]))**.5

    print(medias,sig)

    #plt.plot(ghist, medias, marker='.', color=col, linewidth=0, label='SAGE z = ' + zsims[iiz] + '')
    #plt.errorbar(ghist, medias, yerr=errormedias, xerr=None, fmt='.', ecolor=None)
    #plt.ylabel('$Log_{10} \; $(SFR $[M_{\odot} \; h^{-1}\; yr^{-1}$])')
    #plt.xlabel('$Log_{10} \; (Masa \; [M_{\odot} \; h^{-1} $])')
    #plt.title('Media de la función SFR SAGE frente bines de masa de las galaxias')
    #plt.xlim(8.5, 12.5)
    #plt.legend()
    # plotnom = 'C:/Users/Olivia/TFG-TUT/Figuras/avSFR_vs_Mass_Sage_z_' + zsims[iiz] + '.png'
    # print(plotnom)
    # plt.savefig(plotnom)

    #plt.show()
'''