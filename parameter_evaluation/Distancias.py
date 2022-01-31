#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 18:22:16 2021

@author: lucas
"""



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


from random import randint
from scipy.stats import ks_2samp
from scipy.stats import wasserstein_distance


from numpy import linspace



r_mins = ["3","5","7","9","11"]
r_maxs = ["12","15","18","21","24"]
#r_cut_names = ["30"]
experimentos = ["WT"]
nombres = ["WT_new_data.csv",]
#frep_names = ["20","25","30","40","50"]
#fadh_names = ["0.2","0.4","0.6"]
#fadh = "0.75"

#
for rmin in r_mins:
    for rmax in r_maxs:
        #experimentos.append(r"$R_{cut}$: "+r_cut+" $\mu$m")
        #experimentos.append(r"$F_{adh}$: "+fadh+" $\mu$m/m")
        experimentos.append(r"$R_{min}$: "+rmin+" $\mu$m " + "$R_{max}$: " + rmax + " $\mu$m ")
        nombres.append("Simulacion_data_rmin_"+rmin+"rmax"+rmax+".csv")


#nombres = ["Dock8_procesado.csv"]    
all_data = {}
n_tren = []
n_solas = []

#distancia_inver_total=[]
#
distancias_por_exp = {}
distancias_por_exp_solas = {}



distancias_totales = []
distancias_menores_50 = []

velocidades_totales = []
velocidades_tren = []
velocidades_solas = []



for k in range(len(experimentos)):    
    experimento = experimentos[k]
    all_data[experimento] = pd.read_csv(nombres[k])
    all_data[experimento] = all_data[experimento][all_data[experimento]["Time"]<61]
    df = all_data[experimento]
    
    
        
    #calculo de veces que ina particula invierte su direccion

    df = df.sort_values("Time")
    
    
    print("")
    print("")
    
    print(experimento)

    distancias_totales.append(list(df[df["Dist_Closest"]<float("inf")]["Dist_Closest"]))
    distancias_menores_50.append(list(df[df["Dist_Closest"] < 50]["Dist_Closest"]))
#    acompañadas = df[df["Agrupada"]]
#    solas = df[df["Agrupada"] == False]
    
 #   n_tren.append(acompañadas.shape[0])
#    n_solas.append(solas.shape[0])
    
    velocidades_totales.append(list(abs(df["Velocidad X suavizada"])))
#    velocidades_tren.append(list(abs(acompañadas["Velocidad X suavizada"])))
#    velocidades_solas.append(list(abs(solas["Velocidad X suavizada"])))
    
    
    
#    print(acompañadas.shape[0])
#    print(solas.shape[0])
    
    
    df_no_inf = df[df['Dist_Closest']<float('inf')]
    
    df_distancias_cortas = df[df['Dist_Closest'] < 50]
    
    df_no_inf_adelante = df[df['Distancia_adelante']<float('inf')]
    
#    distancia_inversiones = list(df_no_inf_adelante[df_no_inf_adelante["Inversion_velocidad"]]["Distancia_adelante"])
    
#    distancia_inver_total.append(distancia_inversiones)
    
#    
#    distancias_por_exp[experimento] = list(abs(acompañadas["Dist_Closest"]))
 #   distancias_por_exp_solas[experimento] = list(abs(solas["Dist_Closest"]))
#    
#    
    
    ###print_particles diferenciando colores segun este en grupo o sola:

    
    
    
    
    

    all_data[experimento]=df
#






###Distncias
#
#ajuste_dist = {}
#fig = plt.figure()
#fig.clear()
#
#wt = (distancias_totales[0])
#
#maxima_distancia = max(wt)
#bins = 25
#wt_pdf, bin_loc = np.histogram(wt, bins, range = (0,maxima_distancia), density = True)
#plt.plot( bin_loc[:-1], wt_pdf, ".-", label = "WT",lw = 2 )
#sims = []
##bins = 10
#similitud = []
#for k in range(1,len(experimentos),1):   
#    sim = distancias_totales[k]
#    #similitud.append(ks_2samp(wt,sim)[1])
#    sim_pdf, bin_loc = np.histogram(sim, bins, range = (0,maxima_distancia), density = True)
#    #sims.append(sim_pdf)
#    ajuste_dist[experimentos[k]] = wasserstein_distance(wt,sim)
#    if(wasserstein_distance(wt,sim) < 0.9):
#        plt.plot( bin_loc[:-1], sim_pdf, ".-" , label = experimentos[k],lw = 1  )    
#
#plt.semilogy()
#plt.legend()
#plt.xlabel(r"Distance ($\mu$m)",fontsize = 16)
#plt.ylabel(r"PDF ",fontsize = 16)
#plt.grid()
#
#fig.savefig("PDF_distances_all_sims.png",dpi=300,bbox_inches="tight")
##
##
##
    
    




ajuste_short_dist = {}


rn = []
rx = []
emd = []


fig = plt.figure()
fig.clear()

wt = (distancias_menores_50[0])
maxima_distancia = max(wt)
bins = 25
wt_pdf, bin_loc = np.histogram(wt, bins, range = (0,maxima_distancia), density = True)
plt.plot( bin_loc[:-1], wt_pdf, ".-", label = "WT",lw = 2 )
sims = []
#bins = 10

for k in range(1,len(experimentos),1):   
    sim = distancias_menores_50[k]
    sim_pdf, bin_loc = np.histogram(sim, bins, range = (0,maxima_distancia), density = True)
    ajuste_short_dist[experimentos[k]]=wasserstein_distance(wt,sim)
    exp = experimentos[k]
    rn.append(int(exp.split(" ")[1]))
    rx.append(int(exp.split(" ")[4]))
    emd.append(wasserstein_distance(wt,sim))
    #sims.append(sim_pdf)
    #if (wasserstein_distance(wt,sim) < 5):
    if ( ((exp.split(" ")[1] == "5") and (exp.split(" ")[4]=="12"))  or     ((exp.split(" ")[1] == "7") and (exp.split(" ")[4]=="12")) ):
        plt.plot( bin_loc[:-1], sim_pdf, ".-" , label = experimentos[k],lw = 1 )    

#plt.semilogy()
plt.legend()
plt.xlabel(r"Distance ($\mu$m)",fontsize = 16)
plt.ylabel(r"PDF ",fontsize = 16)
plt.grid()

fig.savefig("PDF_ShortDistances_all.png",dpi=300,bbox_inches="tight")
fig.clear()

df = pd.DataFrame.from_dict(np.array([rn,rx,emd]).T)
df.columns = ['rmin','rmax','Dist']
df['Dist'] = pd.to_numeric(df['Dist'])
pivotted = df.pivot('rmax','rmin','Dist')

#sns.heatmap(pivotted,cmap='RdYlGn_r')
sns.heatmap(pivotted,cmap='RdYlGn_r',square = True, annot=True, cbar_kws={'orientation': 'horizontal', 'location': 'top',"shrink": .52})
#plt.title("Short Distances")
plt.ylabel("$R_{max}$  ($\mu$m)",fontsize=14)
plt.xlabel("$R_{min}$ ($\mu$m)",fontsize=14)

fig.savefig("Short_distances_Heatmap.png", dpi = 300, bbox_inches = "tight")
   # plot the results



ajuste_by_sim = {}

####Velocidades
fig = plt.figure()
fig.clear()



rn = []
rx = []
emd = []


wt = (velocidades_totales[0])
maxima_distancia = max(wt)
bins = 25
wt_pdf, bin_loc = np.histogram(wt, bins, range = (0,maxima_distancia), density = True)
plt.plot( bin_loc[:-1], wt_pdf, ".-", label = "WT",lw = 2 )
sims = []
#bins = 10
diferencia_con_wt = []
for k in range(1,len(experimentos),1):   
    sim = velocidades_totales[k]
    #similitud_v.append(ks_2samp(wt,sim)[1])
    diferencia_con_wt.append(wasserstein_distance(wt,sim))
    ajuste_by_sim[experimentos[k]]=wasserstein_distance(wt,sim)
    sim_pdf, bin_loc = np.histogram(sim, bins, range = (0,maxima_distancia), density = True)
    #sims.append(sim_pdf)
    exp = experimentos[k]
    rn.append(int(exp.split(" ")[1]))
    rx.append(int(exp.split(" ")[4]))
    emd.append(wasserstein_distance(wt,sim))
    
    #if (wasserstein_distance(wt,sim) < 0.9):   
    if ( ((exp.split(" ")[1] == "11") and (exp.split(" ")[4]=="15")) or     ((exp.split(" ")[1] == "7") and (exp.split(" ")[4]=="12")) ):    
        plt.plot( bin_loc[:-1], sim_pdf, ".-" , label = experimentos[k],lw = 1  )    

#plt.semilogy()
plt.legend()
plt.xlabel(r"Speed ($\mu$m)",fontsize = 16)
plt.ylabel(r"PDF ",fontsize = 16)
plt.grid()

fig.savefig("PDF_V_all_sims.png",dpi=200,bbox_inches="tight")
#    
    
fig.clear()    
df = pd.DataFrame.from_dict(np.array([rn,rx,emd]).T)
df.columns = ['$R_{min}$','$R_{max}$','Dist']
df['Dist'] = pd.to_numeric(df['Dist'])
pivotted = df.pivot('$R_{max}$','$R_{min}$','Dist')
sns.heatmap(pivotted,cmap='RdYlGn_r',square = True, annot=True, cbar_kws={'orientation': 'horizontal', 'location': 'top',"shrink": .52})
plt.ylabel("$R_{max}$: ($\mu$m)",fontsize=14)
plt.xlabel("$R_{min}$: ($\mu$m)",fontsize=14)

fig.savefig("Speed_heatmap.png", dpi = 300, bbox_inches = "tight")



##
    
#    
#for df_name in all_data.keys():
#    if not df_name=="WT":
#        print(df)
#        df = all_data[df_name]
#        
#        fig2, axs = plt.subplots(2)
#        for j, part in df.groupby(["TrackID","Canal"]):
#            if part["Time"].shape[0] > 4 :
#            ##crear_subgrupos
#            
#                #part["sub_grupo"]=part["Transicion"].cumsum()
#                axs[0].clear()
#                axs[1].clear()
#                #for l, g in part.groupby('sub_grupo'):
#                    # = "g" if (g["Dist_Closest"].values[0]<30) else "b"
#                part.plot(ax=axs[0],x="Time", y='Position X',marker=".",color="b", label=None)
#                part.plot(ax=axs[1],x="Time", y='Velocidad X suavizada',marker=".",color="b", label=None)
#                #axs[1].plot(part[part["Inversion_velocidad"]]["Time"],part[part["Inversion_velocidad"]]["Velocidad X suavizada"],"r*")
#                #axs[0].plot(part[part["Inversion_velocidad"]]["Time"],part[part["Inversion_velocidad"]]["Position X"],"r*")
#                axs[0].legend_.remove()
#                axs[1].legend_.remove()
#                axs[0].set_ylabel(r"Position X ($\mu$m)")
#                axs[1].set_ylabel(r"Velocity X  ($\mu$m/frame)")
#                
#                
#                
#                #for legends only
#    #            custom_lines = [plt.Line2D([0], [0], color="b", lw=1),
#    #                            plt.Line2D([0], [0], color="g", lw=1)]
#    #
#    #            
#    #           
#    #            axs[0].legend(custom_lines, ["Aisladas","Agrupadas"])
#    #            axs[1].legend(custom_lines, ["Aisladas","Agrupadas"])
#    #            
#                
#                fig2.savefig("./simuladas/" +experimento +"_"+  str(list(part["Canal"])[0])+ "_" + str(j[0]) +".png",dpi=200, bbox_inches="tight" )
#        
#    
#aisladas_y_planas = [ ]
#
#df = all_data["WT"]
#df = df[df["Dist_Closest"]>40]
##df = df[df["Inversion_velocidad"]==False]
#for descarte, part in df.groupby("TrackID"):
#    if  (all(part["Inversion_velocidad"] == False)):
#        aisladas_y_planas.append(list(part["Velocidad X suavizada"]))
#
#
#desvios = [] 
#dif_max = []
#
#for partid in range(len(aisladas_y_planas)):                
#        desvios.append( np.std(aisladas_y_planas[partid]) )
#        dif_max.append( max(aisladas_y_planas[partid]) - min(aisladas_y_planas[partid]) )
#
#
#
#fig = plt.figure()
#plt.plot(desvios)
#plt.plot(dif_max)
#mean_dif = np.mean(dif_max)
#










