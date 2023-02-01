#!/usr/bin/env python
# coding: utf-8

# In[21]:


#calculo de productos para tanques cisterna simetricos
import numpy as np
import pandas as pd
import math
import datetime
from datetime import timedelta

def model_calc(m1,m2,m3,m4,n1,n2,n3,n4,C,c_min,h):
    if n1==0 and n2==0 and n3==0 and n4==0:
        print("no todos los tanques pueden estar vacios, no se puede resolver")
        
    ####sacar luego
    n1=1
    n2=1
    n3=1
    n4=1
    ####
    h=C/(n1*m1+n2*m2+n3*m3+n4*m4)
    product_1=n1*m1*h
    product_2=n2*m2*h
    product_3=n3*m3*h
    product_4=n4*m4*h
    products=np.array([product_1,product_2,product_3,product_4])
    tank_fill=products/c_min
    return h, tank_fill
    
def model_calc_by_stock(m0,m1,m2,m3,n0,n1,n2,n3,q0,q1,q2,q3,c0_max,c1_max,c2_max,c3_max, C,c_min,h):
    if n0==0 and n1==0 and n2==0 and n3==0:
        print("no todos los tanques pueden estar vacios, no se puede resolver")
    ####sacar luego
    n0=1
    n1=1
    n2=1
    n3=1
    ####  
    #h=(C-c0_max-c1_max-c2_max-c3_max+q0+q1+q2+q3)/(n0*m0+n1*m1+n2*m2+n3*m3)
    h=C/(n0*m0+n1*m1+n2*m2+n3*m3)
    #if h<=0:
      #  h=6    
    product_1=(c0_max-q0+n0*m0*h)
    product_2=(c1_max-q1+n1*m1*h)
    product_3=(c2_max-q2+n2*m2*h)
    product_4=(c3_max-q3+n3*m3*h)
    
    p_sum=product_1+product_2+product_3+product_4
    products=np.array([product_1,product_2,product_3,product_4])
    tank_fill=products/c_min
    return h, tank_fill


def round_loading(tank_fill__,posibilities):
    tank_fill_= tank_fill__
    #print(posibilities)
    if posibilities[0]==1.0:
        tank_fill_[0]=math.ceil(tank_fill_[0])
    if posibilities[0]==0.0:
        tank_fill_[0]=math.floor(tank_fill_[0])
    if posibilities[1]==1.0:
        tank_fill_[1]=math.ceil(tank_fill_[1])
    if posibilities[1]==0.0:
        tank_fill_[1]=math.floor(tank_fill_[1])
    if posibilities[2]==1.0:
        tank_fill_[2]=math.ceil(tank_fill_[2])
    if posibilities[2]==0.0:
        tank_fill_[2]=math.floor(tank_fill_[2])
    if posibilities[3]==1.0:
        tank_fill_[3]=math.ceil(tank_fill_[3])
    if posibilities[3]==0.0:
        tank_fill_[3]=math.floor(tank_fill_[3])
    return tank_fill_,tank_fill__
    #chequear cuentas de esta funcion (valores y pendientes)
    #1-Que entre en los tanques individuales
    #2-si hay mas de una que ingresen a los tanques, priorizo la ventana temporal
    #3-productos
#------------------------------------
def truck_loading_posibilities(m0,m1,m2,m3,C,c_min,h):
    i=0 #contador
    columns_names= ['flow_1','flow_2','flow_3','flow_4','min_after','product_1','product_2','product_3','product_4','product_1_f','product_2_f','product_3_f','product_4_f']
    results=pd.DataFrame(columns = columns_names)
    posibilities=np.array([[0,0,0,0],[1,0,0,0],[0,1,0,0],[1,1,0,0],[0,0,1,0],[1,0,1,0],[0,1,1,0],[1,1,1,0],[0,0,0,1],[1,0,0,1],[0,1,0,1],[0,0,1,1],[1,0,1,1],[0,1,1,1],[1,1,1,1]])
    for iteration in range(1,len(posibilities)):
        for pos in range(0,len(posibilities)):
            h,tank_fill__=model_calc(m0,m1,m2,m3,posibilities[iteration,0],posibilities[iteration,1],posibilities[iteration,2],posibilities[iteration,3],C,c_min,h)
            values_=np.copy(tank_fill__)
            tank_fill_fixed,p=round_loading(tank_fill__,posibilities[pos,:])
            if sum(tank_fill_fixed)==5.0:
                results.loc[i]=[m0, m1, m2, m3, round((h),2), int(tank_fill_fixed[0]), int(tank_fill_fixed[1]), int(tank_fill_fixed[2]), int(tank_fill_fixed[3]),values_[0], values_[1], values_[2], values_[3]]
                #print(model_calc(m0,m1,m2,m3,posibilities[iteration,0],posibilities[iteration,1],posibilities[iteration,2],posibilities[iteration,3],C,c_min,h))
                i=i+1
    return results.drop_duplicates()
    
def truck_loading_posibilities_by_stock(m0,m1,m2,m3,q0,q1,q2,q3,c0_max,c1_max,c2_max,c3_max, C,c_min,h):
    i=0 #contador
    columns_names= ['flow_1','flow_2','flow_3','flow_4','min_after','product_1','product_2','product_3','product_4','product_1_f','product_2_f','product_3_f','product_4_f']
    results=pd.DataFrame(columns = columns_names)
    posibilities=np.array([[0,0,0,0],[1,0,0,0],[0,1,0,0],[1,1,0,0],[0,0,1,0],[1,0,1,0],[0,1,1,0],[1,1,1,0],[0,0,0,1],[1,0,0,1],[0,1,0,1],[0,0,1,1],[1,0,1,1],[0,1,1,1],[1,1,1,1]])
    for iteration in range(1,len(posibilities)):
        for pos in range(0,len(posibilities)):
            h,tank_fill__=model_calc_by_stock(m0,m1,m2,m3,posibilities[iteration,0],posibilities[iteration,1],posibilities[iteration,2],posibilities[iteration,3],q0,q1,q2,q3,c0_max,c1_max,c2_max,c3_max,C,c_min,h)           
            values_=np.copy(tank_fill__)
            if sum(tank_fill__)>(C/c_min) and sum(tank_fill__)<2*(C/c_min):
                tank_fill__=tank_fill__/2
            if sum(tank_fill__)>2*(C/c_min):
                tank_fill__=tank_fill__/4
            tank_fill_fixed,p=round_loading(tank_fill__,posibilities[pos,:])
            if sum(tank_fill_fixed)==5.0:
                results.loc[i]=[m0, m1, m2, m3, round((h),2), int(tank_fill_fixed[0]), int(tank_fill_fixed[1]), int(tank_fill_fixed[2]), int(tank_fill_fixed[3]),values_[0], values_[1], values_[2], values_[3]]
                #print(model_calc(m0,m1,m2,m3,posibilities[iteration,0],posibilities[iteration,1],posibilities[iteration,2],posibilities[iteration,3],C,c_min,h))
                i=i+1
    return results.drop_duplicates()

def stock_overfill_check(c0_max, c1_max, c2_max, c3_max, q0,q1,q2,q3,m0,m1,m2,m3,c_min,results):
    i=0
    columns_names= ['flow_1','flow_2','flow_3','flow_4','min_after','product_1','product_2','product_3','product_4']
    results_filtered=pd.DataFrame(columns = columns_names)
    for index, row in results.iterrows():
        cap0=c0_max-q0+m0*row['min_after']
        cap1=c1_max-q1+m1*row['min_after']
        cap2=c2_max-q2+m2*row['min_after']
        cap3=c3_max-q3+m3*row['min_after']
        diff_0=cap0-row['product_1']*c_min   #cheque si los valores entre lo que puedo llenar y lo que lleno son positivos, si son negativos no va la solucion
        diff_1=cap1-row['product_2']*c_min
        diff_2=cap2-row['product_3']*c_min
        diff_3=cap3-row['product_4']*c_min
        if (diff_0 < 0 or diff_1 < 0 or diff_2 < 0 or diff_3 < 0):
            pass
        #print("solucion no valida, se supera la capacidad maxima del tanque")
        else:
            results_filtered.loc[i]=[m0, m1, m2, m3, row['min_after'], row['product_1'], row['product_2'], row['product_3'], row['product_4']]
            i=i+1
    return results_filtered


def stock_underfill_check(c0_max, c1_max, c2_max, c3_max, q0,q1,q2,q3,m0,m1,m2,m3,c_min,results):
    i=0
    columns_names= ['flow_1','flow_2','flow_3','flow_4','min_after','product_1','product_2','product_3','product_4']
    results_filtered=pd.DataFrame(columns = columns_names)
    for index, row in results.iterrows():
        for j in range(1,30):
            cap0=q0-m0*row['min_after']
            cap1=q1-m1*row['min_after']
            cap2=q2-m2*row['min_after']
            cap3=q3-m3*row['min_after']
            if (cap0 < 0 or cap1 < 0 or cap2 < 0 or cap3 < 0):
                pass
                #row['min_after']=row['min_after']-60
                #product_list=random.sample(product_list, len(product_list))  #ordeno aleatoriamente para ver si puedo salir de la condicion de romper stock
                #results_filtered.loc[i]=[m0, m1, m2, m3, row['min_after'], row['product_1'], row['product_2'], row['product_3'], row['product_4']]
            else:
                results_filtered.loc[i]=[m0, m1, m2, m3, row['min_after'], row['product_1'], row['product_2'], row['product_3'], row['product_4']]
                i=i+1
    return results_filtered

def eval_model(m0, m1, m2, m3, C, c_min, c0_max, c1_max, c2_max, c3_max, window, q0, q1, q2, q3):
    h_max=100
    #evaluar modelo
    results_all=pd.DataFrame()
    results_=pd.DataFrame()
    results__=pd.DataFrame()
    matrix_1=pd.DataFrame()
    for w in range(1,3):
        results=truck_loading_posibilities(m0,m1,m2,m3, C,c_min,h_max) #calculo de estimacion de ventas y modelo de carga
        results1=stock_underfill_check(c0_max, c1_max, c2_max, c3_max, q0,q1,q2,q3,m0,m1,m2,m3,c_min,results) #no quebrarstock
        results2=stock_overfill_check(c0_max, c1_max, c2_max, c3_max, q0,q1,q2,q3,m0,m1,m2,m3,c_min,results1) #no pasar del maximo
        results2['product_1_liters']=results2['product_1']*c_min
        results2['product_2_liters']=results2['product_2']*c_min
        results2['product_3_liters']=results2['product_3']*c_min
        results2['product_4_liters']=results2['product_4']*c_min
        results_all=results_all.append(results2, ignore_index=True)
        results_=results_.append(results)
        results__=results__.append(results1)
    return results_all.drop_duplicates(), results_.drop_duplicates(), results__.drop_duplicates()
    
def eval_model_by_stock(m0, m1, m2, m3, C, c_min, c0_max, c1_max, c2_max, c3_max, window, q0, q1, q2, q3):
    h_max=100
    #evaluar modelo
    results_all=pd.DataFrame()
    results_=pd.DataFrame()
    results__=pd.DataFrame()
    matrix_1=pd.DataFrame()
    for w in range(1,3):
        results=truck_loading_posibilities_by_stock(m0,m1,m2,m3, q0,q1,q2,q3,c0_max,c1_max,c2_max,c3_max,C,c_min,h_max) #calculo de estimacion de ventas y modelo de carga
        results1=stock_underfill_check(c0_max, c1_max, c2_max, c3_max, q0,q1,q2,q3,m0,m1,m2,m3,c_min,results) #no quebrarstock
        results2=stock_overfill_check(c0_max, c1_max, c2_max, c3_max, q0,q1,q2,q3,m0,m1,m2,m3,c_min,results1) #no pasar del maximo
        results2['product_1_liters']=results2['product_1']*c_min
        results2['product_2_liters']=results2['product_2']*c_min
        results2['product_3_liters']=results2['product_3']*c_min
        results2['product_4_liters']=results2['product_4']*c_min
        results_all=results_all.append(results2, ignore_index=True)
        results_=results_.append(results)
        results__=results__.append(results1)
    return results_all.drop_duplicates(), results_.drop_duplicates(), results__.drop_duplicates()

def shift_windows(revision_date,H,shift):
        #aca va el codigo de corrimiento de H para que coincida con el inicio o fin de las ventanas
        H_shifted=(revision_date)+datetime.timedelta(hours=float(H))
        H_ventana=H_shifted.hour  #obtengo el valor en horas del dia, para luego calcular cuantas horas debo sumar o restar para coincidir con la ventana
        if (H_ventana>=0.0 and H_ventana<6.0):
            window_lower=H-H_ventana
            window_upper=H+(6.0-H_ventana)
        if (H_ventana>=6.0 and H_ventana<12.0):
            window_lower=H-(H_ventana-6.0)
            window_upper=H+(12.0-H_ventana)
        if (H_ventana>=12.0 and H_ventana<=18.0):
            window_lower=H-(H_ventana-12.0)
            window_upper=H+(18.0-H_ventana)
        if (H_ventana>=18.0 and H_ventana<24.0):
            window_lower=H-(H_ventana-18.0)
            window_upper=H+(24.0-H_ventana)
        return window_lower, window_upper, H_ventana,H_shifted
    
#eval
def model_run(revision_date, m0, m1, m2, m3, C, c_min, c0_max, c1_max, c2_max, c3_max, q0, q1, q2, q3):
    window=0
    r1,r2,r3=eval_model(m0, m1, m2, m3, C, c_min, c0_max, c1_max, c2_max, c3_max, window, q0, q1, q2, q3)
    r1=r1.drop_duplicates()
    r1_,r2_,r3_=eval_model_by_stock(m0, m1, m2, m3, C, c_min, c0_max, c1_max, c2_max, c3_max, window, q0, q1, q2, q3)
    r1_=r1_.drop_duplicates()
    results=pd.concat([r1,r1_]).drop_duplicates()
    #asignacion de nombre de productos, se podria dejar en general pero es mas facil.
    results=results.rename(columns = {'product_1_liters':'Shell V-Power Diesel','product_2_liters':'Shell Evolux Diesel B 500','product_3_liters':'Shell V-Power Nafta', 'product_4_liters':'Nafta Super Bio'})
    results=results.groupby(['Shell V-Power Diesel', 'Shell Evolux Diesel B 500','Shell V-Power Nafta','Nafta Super Bio'], as_index=False).mean()
    H=results['min_after'].min() #horas que tarda en llenarse un camion de C litros
    window_lower, window_upper, H_window, H_shifted=shift_windows(revision_date,H/60,0)
    return results, round(window_lower,0), round(window_upper,0), H_window, H_shifted


# In[22]:




###################################inputs del modelo para productos############################################
#######################################
m0=1.721
m1=0.685
m2=3.828
m3=5.047
#######################################
#capacidad maxima del camion, capacidad del compartimiento
C=25000
c_min=5000
######################################
#capacidades de tanques por producto, es la suma de los tanques de la estacion
c0_max=25000   #v power diesel
c1_max=10000   #evolux
c2_max=30000   #vpower nafta
c3_max=35000   #nafta super bio
######################################
#Stocks sumados de los productos
q0=17745
q1=4632
q2=19231
q3=32100
######################################
#fecha de revision
revision_date="23-01-17 03:00:00"
revision_date = datetime.datetime.strptime(revision_date, '%y-%m-%d %H:%M:%S')
##############################################################################################################

model_run(revision_date, m0,m1,m2,m3,C,c_min,c0_max,c1_max,c2_max,c3_max,q0,q1,q2,q3)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




