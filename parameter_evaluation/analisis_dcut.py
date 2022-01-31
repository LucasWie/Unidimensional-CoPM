#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 20:31:19 2021

@author: lucas
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import randint

#from numpy import linspace

def ubicar_puntos(largo, N):
    pos=np.zeros(N)
    for i in range(N):
        pos[i] = np.random.uniform(0,largo)
    return pos




def get_dist_frontal(row):
    d_frontal = row["Dist_derecha"] if row["Velocidad X suavizada"] >= 0 else row["Dist_izquierda"] 
    return (d_frontal)
    

def get_dist_atras(row):
    d_atras = row["Dist_derecha"] if row["Velocidad X suavizada"] < 0 else row["Dist_izquierda"] 
    return (d_atras)
    


def agrupada_o_tren(df,distancia_tren):
    ##Si pasa 5 frames a menos distancia
    df["Agrupada"] = [False]*df.shape[0]
    for part_id,part in df.groupby(["TrackID","Canal"]):
        tiempos = list(part["Time"])
        last_time = max(tiempos)
        first_time = min(tiempos)
        part=part.sort_values("Time")
       
        for t, row in part.groupby("Time"):
            
            if (row.shape[0]>1):
                break
                #("Error")
               

            if list(row["Dist_Closest"])[0] < distancia_tren : 
                ##Contar 5 adelante o atras
                instantes_agrupados = 0
                i = t-4 if (t-4 >= first_time) else first_time
               
                while( list(part[part["Time"]==i]["Dist_Closest"])[0] < distancia_tren and i<t):
                    instantes_agrupados += 1
                    i += 1
                    if (instantes_agrupados == 4):
                        cond = (df["TrackID"] == part_id[0]) &  (df["Canal"] == part_id[1])  &   (df["Time"] == t) 
                        
                        df.loc[cond,"Agrupada"] = True
                        
                        break
                    
                i=t+1
                if i<last_time:
                    while( list(part[part["Time"]==i]["Dist_Closest"])[0] < distancia_tren ):
                       
                        instantes_agrupados += 1
                        i += 1
                        
                        if (instantes_agrupados == 5):
                            cond = (df["TrackID"] == part_id[0]) &  (df["Canal"] == part_id[1]) & (df["Time"] == t) 
                        
                            df.loc[cond,"Agrupada"] = True
                    
                            break
                      
                        if i>=last_time:
                            break
                  
       # df[df["TrackID"] == part_id] = part
                        
    return(df)

#fadh_name = ["0.2","0.4","0.6"]

#r_cut = 35
#d_cuts_name = [20,25,30,35,40]
#d_cuts_name = [30]


r_mins = ["3","5","7","9","11"]
r_maxs = ["12","15","18","21","24"]

for r_min in r_mins: 
    for r_max in r_maxs:
        r_cut = 30
        df = pd.read_csv("t_cells_rmin_"+r_min +"rmin_"+r_max+""+".txt")
        df.columns = ["TrackID","Position X","Velocidad X suavizada","Time_exact","Canal","Radio"]
        df["Time"] = np.round(df["Time_exact"])
        
        df = df[df["Time"]>0]
        df = df[df["Time"]<61]
        
        
        df['Position X'] = df['Position X'].astype(float)
        #df['Position Y'] = df['Position Y'].astype(float)
        df['Time'] = df['Time'].astype(float)
        df['Time'] = df['Time']
        df['TrackID'] = df['TrackID'].astype('Int64')
        
        
        indices=pd.Series(df.index)
        df["TrackID"] = df["TrackID"].fillna(value=indices)##Esto le pone como id el indice a las que no tengaan id definido
        df['TrackID'] = df['TrackID'].astype('str')
        df["Tren_ID"] = df["TrackID"] ##al iniciar, toads las celulas son su propio tren
        df["Dist_Closest"] = [float('inf')]*df.shape[0]
        df["Dist_derecha"] = [float('inf')]*df.shape[0]
        df["Dist_izquierda"] = [float('inf')]*df.shape[0]
        df["Distancia_adelante"] = [float('inf')]*df.shape[0]
        df["Distancia_atras"] = [float('inf')]*df.shape[0]
        df["Vecino_der"] = [""]*df.shape[0]
        df["Vecino_izq"] = [""]*df.shape[0]
        
        #print("Analisis de " + archivo_entrada)
        df = df.sort_values("Position X")
        
        for i, grp in df.groupby(["Time","Canal"]):
            
            if grp.shape[0] > 1:
                distancias = []
                closest = [float('inf')]*grp.shape[0]
                
                grp = grp.sort_values("Position X")
                x = list(grp["Position X"])
                #print(i,x)
                indice = list(grp.index)
                for pos_ind in range(len(indice)-1):
                    dist = (x[pos_ind + 1] - x[pos_ind]  )
                    distancias.append(dist)
                    
                    if dist < r_cut:
                        grp.loc[indice[pos_ind+1],"Tren_ID"] = grp.loc[indice[pos_ind],"Tren_ID"] 
            
            
                vec_i = [""]*grp.shape[0]
                vec_d = [""]*grp.shape[0]
                di_i = [float('inf')]*grp.shape[0]
                di_d = [float('inf')]*grp.shape[0]
                for pos in range(grp.shape[0]):
                    if (pos == 0):
                        closest[pos] = distancias[0]
                        di_d[pos] = distancias[pos]
                        vec_d[pos] = list(grp[grp["Position X"]==x[pos+1]]["TrackID"].values)[0]
                        
                    else:
                        if (pos > 0 and pos < grp.shape[0]-1):
                            closest[pos]=(min(distancias[pos-1],distancias[pos]))
                            di_i[pos] = distancias[pos-1]
                            di_d[pos] = distancias[pos]
                            vec_i[pos] = list(grp[grp["Position X"]==x[pos-1]]["TrackID"].values)[0]
                            vec_d[pos] = list(grp[grp["Position X"]==x[pos+1]]["TrackID"].values)[0]
                            
                        else:
                            closest[pos]=(distancias[-1])
                            di_i[pos] = distancias[pos-1]
                            vec_i[pos] = list(grp[grp["Position X"]==x[pos-1]]["TrackID"].values)[0]
            
                df.loc[( indice), "Tren_ID"] = grp["Tren_ID"]
                df.loc[indice ,"Dist_Closest"] = closest
                df.loc[indice, "Dist_derecha"] = di_d
                df.loc[indice, "Dist_izquierda"] = di_i
                df.loc[indice, "Vecino_der"] = vec_d
                df.loc[indice, "Vecino_izq"] = vec_i
        #
        df["Distancia_adelante"] = df.apply(lambda x: get_dist_frontal(x), axis=1)
        df["Distancia_atras"] = df.apply(lambda x: get_dist_atras(x), axis=1)
    
    
    #df = agrupada_o_tren(df,30)
        df.to_csv("Simulacion_data_rmin_"+r_min+"rmax"+r_max+".csv",index=False)
    
    #Animacion
    #df=df.sort_values("Time")
    #for t, momento in df.groupby("Time"):
    #    #fig.clear()
    #    momento["Canal"] = momento["Canal"].astype("category")
    #    #fig = plt.figure()
    #
    #    if (momento.shape[0] > 0):
    #         p = momento.plot.scatter(x="Position X", y="Canal")
    #         for i in range(max(df["Canal"])+1):
    #             plt.plot([min(df["Position X"]), max(df["Position X"])] , [i-0.5, i-0.5] , "k:")
    #         plt.xlim([min(df["Position X"])-50,max(df["Position X"])+50])
    #         plt.ylim([-2 , max(df["Canal"])+2 ])
    #         #plt.ylim([min(data["Position Y"])-50,max(data["Position Y"])+50])
    #         fig = p.get_figure()
    #         fig.savefig("./video/"+"frame_"+str('%04d' % t)+".png", dpi = 500, bbox_inches="tight" )
    #         plt.close(fig)
    
    #
    #  
    #fig = plt.figure() # note we must use plt.subplots, not plt.subplot
    #ax = plt.axes()
    #  
    #
    #ylabel = [str(x) for x in range(20)]
    #y_tick_pos = [x for x in range(0,609,32)]
    #for t, subdf in df.groupby("Time"):    
    #    print(t)
    #    ax.patches = []
    #    #fig.clear()
    #    x = list(subdf["Position X"])
    #    canal = list(subdf["Canal"])
    #    radios = list(subdf["Radio"])
    #    y = [x*32 for x in canal]             
    #    #print(len(x))
    #    
    #    for j in range(0,len(x)):
    #        #print(str(x[j])+" "+str(y[j]))
    #        circle = plt.Circle( (x[j], y[j]), radios[j],lw = 1,fill=False)
    #        ax.add_patch(circle)
    #   
    #    
    #    plt.xlabel(r"x ($\mu$m)",fontsize = 16)
    #    plt.ylabel(r"Microchannel ID",fontsize = 16)
    #    plt.axis("square")
    #    #plt.xlim(-15,715)
    #    plt.ylim(-15,20*32)
    #    plt.xlim([min(df["Position X"])-50,max(df["Position X"])+50])
    #    plt.yticks(y_tick_pos,ylabel)
    #    #plt.ylim([-2 , max(df["Canal"])+2 ])
    #    for i in range(max(df["Canal"])+1):
    #        plt.plot([min(df["Position X"]), max(df["Position X"])] , [i*32-16, i*32-16] , "k:")
    #    
    #    fig.savefig("./video/"+"frame_"+str('%04d' % t)+".png", dpi = 500, bbox_inches="tight")
    #    
    
    
    #

