#!/usr/bin/env python
# coding: utf-8

# In[7]:


#calculo de productos para tanques cisterna simetricos
import numpy as np
import pandas as pd
import math
import datetime
from datetime import timedelta

def model_calc(m1,m2,m3,m4,n1,n2,n3,n4,C,c_min,h):
    if n1==0 and n2==0 and n3==0 and n4==0:
        print("no todos los tanques pueden estar vacios, no se puede resolver")
    n1=1
    n2=1
    n3=1
    n4=1
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
    #n0=1
    #n1=1
    #n2=1
    #n3=1
        
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
                row['min_after']=row['min_after']-180
                #product_list=random.sample(product_list, len(product_list))  #ordeno aleatoriamente para ver si puedo salir de la condicion de romper stock
                #results_filtered.loc[i]=[m0, m1, m2, m3, row['min_after'], row['product_1'], row['product_2'], row['product_3'], row['product_4']]
                #i=i+1
            else:
                results_filtered.loc[i]=[m0, m1, m2, m3, row['min_after'], row['product_1'], row['product_2'], row['product_3'], row['product_4']]
                break;
            i=i+1
    results_filtered=results_filtered[results_filtered['min_after']==results_filtered['min_after'].min()]
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
    H=(results['min_after'].min())/60 #horas que tarda en llenarse un camion de C litros
    print(H)
    window_lower, window_upper, H_window, H_shifted=shift_windows(revision_date,H,0)
    return results, H, round(window_lower,0), round(window_upper,0), H_window, H_shifted


# In[8]:


##Seleccion de tanques estacion de servicio

##calculo de stocks por productos

def stocks_pd(data, q1_,q9_,q7_,q3_,q5_,q8_,q11_,q4_,q6_):
    stocks_pd = pd.DataFrame(data, columns=['fueltank.code','product.name','stock','fueltank.capacity'])
    return stocks_pd



def stocks_by_products(data):
    grouped_data=data.groupby(['product.name']).sum().reset_index()
    q0_=grouped_data[grouped_data['product.name']=='Shell V-Power Diesel']
    q1_=grouped_data[grouped_data['product.name']=='Shell Evolux Diesel B 500']
    q2_=grouped_data[grouped_data['product.name']=='Shell V-Power Nafta']
    q3_=grouped_data[grouped_data['product.name']=='Nafta Super Bio']
    return int(q0_['stock']), int(q1_['stock']), int(q2_['stock']), int(q3_['stock'])

#calculo de capacidades maxima por producto


def capacities_pd(data):
    stocks_pd = pd.DataFrame(data, columns=['fueltank.code','product.name','stock','fueltank.capacity'])
    return stocks_pd



def capacities_by_products(data):
    grouped_data=data.groupby(['product.name']).sum().reset_index()
    c0_=grouped_data[grouped_data['product.name']=='Shell V-Power Diesel']
    c1_=grouped_data[grouped_data['product.name']=='Shell Evolux Diesel B 500']
    c2_=grouped_data[grouped_data['product.name']=='Shell V-Power Nafta']
    c3_=grouped_data[grouped_data['product.name']=='Nafta Super Bio']
    return int(c0_['fueltank.capacity']), int(c1_['fueltank.capacity']), int(c2_['fueltank.capacity']), int(c3_['fueltank.capacity'])

def tank_selector(stocks,m1__,m3__,m4__,m5__,m6__,m7__,m8__,m9__,m11__,h,c_min):
    shell_v_power_D=stocks[stocks['product.name']=='Shell V-Power Diesel']
    evolux_D=stocks[stocks['product.name']=='Shell Evolux Diesel B 500']
    shell_v_power_n=stocks[stocks['product.name']=='Shell V-Power Nafta']
    Nafta_super_bio=stocks[stocks['product.name']=='Nafta Super Bio']
  
    #prevision de stock
   
    #shell_v_power_D['capacity_prevision']=shell_v_power_D['fueltank.capacity']-shell_v_power_D['stock']+(m0/2)*h*60
    #shell_v_power_n['capacity_prevision']=shell_v_power_n['fueltank.capacity']-shell_v_power_n['stock']+(m2/3)*h*60
    #Nafta_super_bio['capacity_prevision']=Nafta_super_bio['fueltank.capacity']-Nafta_super_bio['stock']+(m3/3)*h*60
    
    #Tanque evolux calculo de consumo
    evolux_D['capacity_prevision']=evolux_D['fueltank.capacity']-evolux_D['stock']+(m7__)*h*60
    
    #Tanques Shell V power Diesel calculo consumo
    shell_v_power_D_1=shell_v_power_D[shell_v_power_D['fueltank.code']==1]
    shell_v_power_D_1['capacity_prevision']=shell_v_power_D_1['fueltank.capacity']-shell_v_power_D_1['stock']+m1__*h*60
    shell_v_power_D_9=shell_v_power_D[shell_v_power_D['fueltank.code']==9]
    shell_v_power_D_9['capacity_prevision']=shell_v_power_D_9['fueltank.capacity']-shell_v_power_D_9['stock']+m9__*h*60
    shell_v_power_D=pd.concat([shell_v_power_D_1, shell_v_power_D_9], axis=0,ignore_index=True)
    
    
    shell_v_power_n_3=shell_v_power_n[shell_v_power_n['fueltank.code']==3]
    shell_v_power_n_3['capacity_prevision']=shell_v_power_n_3['fueltank.capacity']-shell_v_power_n_3['stock']+m3__*h*60
    shell_v_power_n_5=shell_v_power_n[shell_v_power_n['fueltank.code']==5]
    shell_v_power_n_5['capacity_prevision']=shell_v_power_n_5['fueltank.capacity']-shell_v_power_n_5['stock']+m5__*h*60
    shell_v_power_n_8=shell_v_power_n[shell_v_power_n['fueltank.code']==8]
    shell_v_power_n_8['capacity_prevision']=shell_v_power_n_8['fueltank.capacity']-shell_v_power_n_8['stock']+m8__*h*60
    shell_v_power_n=pd.concat([shell_v_power_n_3, shell_v_power_n_5,shell_v_power_n_8], axis=0,ignore_index=True)
    

    Nafta_super_bio_4=Nafta_super_bio[Nafta_super_bio['fueltank.code']==4]
    Nafta_super_bio_4['capacity_prevision']=Nafta_super_bio_4['fueltank.capacity']-Nafta_super_bio_4['stock']+m4__*h*60
    Nafta_super_bio_6=Nafta_super_bio[Nafta_super_bio['fueltank.code']==6]
    Nafta_super_bio_6['capacity_prevision']=Nafta_super_bio_6['fueltank.capacity']-Nafta_super_bio_6['stock']+m6__*h*60
    Nafta_super_bio_11=Nafta_super_bio[Nafta_super_bio['fueltank.code']==11]
    Nafta_super_bio_11['capacity_prevision']=Nafta_super_bio_11['fueltank.capacity']-Nafta_super_bio_11['stock']+m11__*h*60
    Nafta_super_bio=pd.concat([Nafta_super_bio_4, Nafta_super_bio_6, Nafta_super_bio_11], axis=0, ignore_index=True) 
    
    
    
    #x<5000
    shell_v_power_D.loc[ (shell_v_power_D.capacity_prevision<c_min), 'available'] = 0  
    evolux_D.loc[ (evolux_D.capacity_prevision<c_min), 'available'] = 0
    shell_v_power_n.loc[ (shell_v_power_n.capacity_prevision<c_min), 'available'] = 0
    Nafta_super_bio.loc[ (Nafta_super_bio.capacity_prevision<c_min), 'available'] = 0
    
    ####   5000<x<10000
    shell_v_power_D.loc[ ((shell_v_power_D.capacity_prevision<2*c_min) & (shell_v_power_D.capacity_prevision>c_min)), 'available'] = 5000  
    evolux_D.loc[ ((evolux_D.capacity_prevision<2*c_min) & (evolux_D.capacity_prevision>c_min)), 'available'] = 5000
    shell_v_power_n.loc[ ((shell_v_power_n.capacity_prevision<2*c_min) & (shell_v_power_n.capacity_prevision>c_min)), 'available'] = 5000
    Nafta_super_bio.loc[ ((Nafta_super_bio.capacity_prevision<2*c_min) & (Nafta_super_bio.capacity_prevision>c_min)), 'available'] = 5000
    
    ####    10000<x<15000date_store_validation
    
    shell_v_power_D.loc[ ((shell_v_power_D.capacity_prevision<3*c_min) & (shell_v_power_D.capacity_prevision>2*c_min)), 'available'] = 10000  
    evolux_D.loc[ ((evolux_D.capacity_prevision<3*c_min) & (evolux_D.capacity_prevision>2*c_min)), 'available'] = 10000
    shell_v_power_n.loc[ ((shell_v_power_n.capacity_prevision<3*c_min) & (shell_v_power_n.capacity_prevision>2*c_min)), 'available'] = 10000
    Nafta_super_bio.loc[ ((Nafta_super_bio.capacity_prevision<3*c_min) & (Nafta_super_bio.capacity_prevision>2*c_min)), 'available'] = 10000
    
    ####    15000<x<20000
    
    shell_v_power_D.loc[ ((shell_v_power_D.capacity_prevision<4*c_min) & (shell_v_power_D.capacity_prevision>3*c_min)), 'available'] = 15000  
    evolux_D.loc[ ((evolux_D.capacity_prevision<4*c_min) & (evolux_D.capacity_prevision>3*c_min)), 'available'] = 15000
    shell_v_power_n.loc[ ((shell_v_power_n.capacity_prevision<4*c_min) & (shell_v_power_n.capacity_prevision>3*c_min)), 'available'] = 15000
    Nafta_super_bio.loc[ ((Nafta_super_bio.capacity_prevision<4*c_min) & (Nafta_super_bio.capacity_prevision>3*c_min)), 'available'] = 15000
    
    ####    20000<x<25000
    
    shell_v_power_D.loc[ ((shell_v_power_D.capacity_prevision<5*c_min) & (shell_v_power_D.capacity_prevision>4*c_min)), 'available'] = 20000  
    evolux_D.loc[ ((evolux_D.capacity_prevision<5*c_min) & (evolux_D.capacity_prevision>3*c_min)), 'available'] = 20000
    shell_v_power_n.loc[ ((shell_v_power_n.capacity_prevision<5*c_min) & (shell_v_power_n.capacity_prevision>4*c_min)), 'available'] = 20000
    Nafta_super_bio.loc[ ((Nafta_super_bio.capacity_prevision<5*c_min) & (Nafta_super_bio.capacity_prevision>4*c_min)), 'available'] = 20000
    
    #### x>25000
    
    shell_v_power_D.loc[ (shell_v_power_D.capacity_prevision>5*c_min), 'available'] = 25000  
    evolux_D.loc[ (evolux_D.capacity_prevision>5*c_min), 'available'] = 25000
    shell_v_power_n.loc[ (shell_v_power_n.capacity_prevision>5*c_min), 'available'] = 25000
    Nafta_super_bio.loc[ (Nafta_super_bio.capacity_prevision>5*c_min), 'available'] = 25000
    
    shell_v_power_D['available_stock']=shell_v_power_D['fueltank.capacity']-shell_v_power_D['capacity_prevision']
    evolux_D['available_stock']=evolux_D['fueltank.capacity']-evolux_D['capacity_prevision']
    shell_v_power_n['available_stock']=shell_v_power_n['fueltank.capacity']-shell_v_power_n['capacity_prevision']
    Nafta_super_bio['available_stock']=Nafta_super_bio['fueltank.capacity']-Nafta_super_bio['capacity_prevision']
    
    return shell_v_power_D, evolux_D, shell_v_power_n, Nafta_super_bio, shell_v_power_D['available'].sum(),evolux_D['available'].sum(), shell_v_power_n['available'].sum(), Nafta_super_bio['available'].sum() 


def filter_orders_by_tank(orders,max_shell_v_power_D,max_evolux_D, max_shell_v_power_n, max_Nafta_super_bio):
    orders=orders[orders['Shell V-Power Diesel']<=max_shell_v_power_D]
    orders=orders[orders['Shell Evolux Diesel B 500']<=max_evolux_D]
    orders=orders[orders['Shell V-Power Nafta']<=max_shell_v_power_n]
    orders=orders[orders['Nafta Super Bio']<=max_Nafta_super_bio]
    return orders


# In[9]:


##estimaciones de flujos de ventas por producto y por tanque (fuente excel)
def read_xlsx_file(month, path):
    if month==1:
        month_="enero"
    if month==2:
        month_="febrero"
    if month==3:
        month_="marzo"
    if month==4:
        month_="abril"
    if month==5:
        month_="mayo"
    if month==6:
        month_="junio"
    if month==7:
        month_="julio"
    if month==8:
        month_="agosto"
    if month==9:
        month_="septiembre"
    if month==10:
        month_="octubre"
    if month==11:
        month_="noviembre"
    if month==12:
        month_="diciembre"    
    #prevision=pd.read_excel('est1132.xlsx')  #archivo excel con toda la informacion de consumo
    prevision=pd.read_excel(path)  #archivo excel con toda la informacion de consumo
    prevision=prevision[prevision['Mes']==month_]
    return prevision


def day_translate(day):
    if  day=='Monday':
        day_week='lunes'
    if  day=='Tuesday':
        day_week='martes'
    if  day=='Wednesday':
        day_week='miércoles'
    if  day=='Thursday':
        day_week='jueves'
    if  day=='Friday':
        day_week='viernes'
    if  day =='Saturday':
        day_week='sábado'
    if  day =='Sunday':
        day_week='domingo'
    return day_week
#estimacion de flujos de ventas por producto

def flow_estimation(prevision,product, DayOfWeek, hour):
    columns_names= [product]
    results=pd.DataFrame(columns = columns_names)
    prevision=prevision[prevision['Producto']==product]
    products_grouped=prevision.groupby(['Hora','DayOfWeek']).sum().reset_index()
    day_array=np.array(['lunes', 'martes', 'miércoles', 'jueves', 'viernes','sábado','domingo','lunes','martes','miercoles','jueves','viernes','sábado','domingo'])
    for i in range(0,len(day_array)):
        if day_array[i]==DayOfWeek:
            cum_hours=0
            liters=0
            for j in range(i,len(day_array)):
                prevision_= products_grouped[ products_grouped['DayOfWeek']==day_array[j]]
                for w, row in prevision_.iterrows():
                    if (row['Hora']+100*cum_hours>=hour):  #primer dia
                        liters=liters+int(row['CANT FACT'])
                        #print(row['Hora'])
                        results.loc[cum_hours]=[liters]
                        cum_hours=cum_hours+1
                    
            break
    return results

#estimacion de flujos de venta por tanque

def flow_estimation_by_tank(prevision,tank, DayOfWeek, hour,tot_hours):
    columns_names= [tank]
    results=pd.DataFrame(columns = columns_names)
    prevision=prevision[prevision['TANQUE']==tank]
    day_array=np.array(['lunes', 'martes', 'miércoles', 'jueves', 'viernes','sábado','domingo','lunes','martes','miercoles','jueves','viernes','sábado','domingo'])
    for i in range(0,len(day_array)):
        if day_array[i]==DayOfWeek:
            cum_hours=0
            liters=0
            for j in range(i,len(day_array)):
                prevision_= prevision[prevision['DayOfWeek']==day_array[j]]
                for w, row in prevision_.iterrows():
                    if (row['Hora']+100*cum_hours>=hour):  #primer dia
                        liters=liters+int(row['CANT FACT'])
                        #print(row['Hora'])
                        results.loc[cum_hours]=[liters]
                        cum_hours=cum_hours+1
            break
    liters=results.iloc[int(tot_hours)]
    m=int(liters)/tot_hours/60
    return m

def model_flow_eval_by_tank(prevision,day,hour,H__):
    m1__= flow_estimation_by_tank(prevision,'Tanque 01',day,hour,H__)
    m3__= flow_estimation_by_tank(prevision,'Tanque 03',day,hour,H__)
    m4__= flow_estimation_by_tank(prevision,'Tanque 04',day,hour,H__)
    m5__= flow_estimation_by_tank(prevision,'Tanque 05',day,hour,H__)
    m6__= flow_estimation_by_tank(prevision,'Tanque 06',day,hour,H__)
    m7__= flow_estimation_by_tank(prevision,'Tanque 07',day,hour,H__)
    m8__= flow_estimation_by_tank(prevision,'Tanque 08',day,hour,H__)
    m9__= flow_estimation_by_tank(prevision,'Tanque 09',day,hour,H__)
    m11__= flow_estimation_by_tank(prevision,'Tanque 11',day,hour,H__)
    return m1__,m3__,m4__,m5__,m6__,m7__,m8__,m9__, m11__

def model_flow_eval(prevision,day,hour,C):
    results_1=flow_estimation(prevision,'V-Power Diesel',day,hour)
    results_2=flow_estimation(prevision,'Nafta Super',day,hour)
    results_3=flow_estimation(prevision,'Evolux',day,hour)
    results_4=flow_estimation(prevision,'V-Power Nafta',day,hour)
    fuel_consumption=pd.concat([results_1, results_2, results_3, results_4], axis=1)
    fuel_consumption['sum']=fuel_consumption['V-Power Diesel']+fuel_consumption['Nafta Super']+fuel_consumption['Evolux']+fuel_consumption['V-Power Nafta']
    H=(fuel_consumption[(fuel_consumption['sum']>C)].reset_index()).iloc[0]
    h=H['index']
    m0=H['V-Power Diesel']/H['index']/60
    m3=H['Nafta Super']/H['index']/60
    m1=H['Evolux']/H['index']/60
    m2=H['V-Power Nafta']/H['index']/60
    return h, m0, m1, m2, m3


# In[12]:


###################################inputs del modelo para productos############################################

#capacidad maxima del camion, capacidad del compartimiento (input)
C=25000
c_min=5000


######################################
#capacidades de tanques por producto, es la suma de los tanques de la estacion
#c0_max=25000   #v power diesel
#c1_max=10000   #evolux
#c2_max=30000   #vpower nafta
#c3_max=35000   #nafta super bio
######################################

######################################
#fecha de revision

revision_date="23-02-06 03:13:00"
revision_date = datetime.datetime.strptime(revision_date, '%y-%m-%d %H:%M:%S')



##################################input seleccion de tanques estacion#######################################
#stocks por tanque unica variable que cambia necesito consumir esto de la api
#vpower diesel
q1_=11544
q9_=8616

#evolux
q7_=7762

#vpower nafta

q3_=7854
q5_=5678
q8_=4567

#nafta super bio

q11_=4248
q4_=2206
q6_=4585



#estacion de servicio, seleccion de tanques llegada de camiones##################################

data = {'fueltank.code': [1,9,7,3,5,8,11,4,6],
            'product.name': ['Shell V-Power Diesel', 'Shell V-Power Diesel','Shell Evolux Diesel B 500','Shell V-Power Nafta','Shell V-Power Nafta','Shell V-Power Nafta','Nafta Super Bio','Nafta Super Bio','Nafta Super Bio'],
            'stock':[q1_,q9_,q7_,q3_,q5_,q8_,q11_,q4_,q6_],
            'fueltank.capacity':[15000,10000,10000,10000,10000,10000,15000,10000,10000]}


#################################################################################################

#generacion de estructura de stock y de stock por productos 

stocks=stocks_pd(data, q1_,q9_,q7_,q3_,q5_,q8_,q11_,q4_,q6_) #generacion de stocks
q0, q1, q2, q3=stocks_by_products(stocks) 

#generacion de capacidades maximas por tanque
capacities_pd_=capacities_pd(data)
c0_max, c1_max, c2_max, c3_max=capacities_by_products(capacities_pd_)

#generacion de flujos de ventas de combustible por producto y por tanque###################

hour_=revision_date.hour
month_=revision_date.month
day_week=day_translate(revision_date.strftime('%A'))

prevision=read_xlsx_file(month_,'est_mensual_2022.xlsx')   ####ESTO DEBO SACARLO DE LA API###

print("flujo de consumos por producto:")

H_, m0_,m1_,m2_,m3_=model_flow_eval(prevision,day_week,hour_,C)
print('Shell v power diesel')
print(m0_)
print('Evolux')
print(m1_)
print('Shell v power_nafta')
print(m2_)
print('Nafta super bio')
print(m3_)

print("flujos de consumo por tanuqe")

m1__,m3__,m4__,m5__,m6__,m7__,m8__,m9__,m11__=model_flow_eval_by_tank(prevision,day_week,hour_,H_)

print('Tanque 1')
print(m1__)
print('Tanque 3')
print(m3__)
print('Tanque 4')
print(m4__)
print('Tanque 5')
print(m5__)
print('Tanque 6')
print(m6__)
print('Tanque 7')
print(m7__)
print('Tanque 8')
print(m8__)
print('Tanque 9')
print(m9__)
print('Tanque 11')
print(m11__)



#eval
orders, H, window_lower, window_upper, windows_exact, shifted_hours=model_run(revision_date, m0_,m1_,m2_,m3_,C,c_min,c0_max,c1_max,c2_max,c3_max,q0,q1,q2,q3)

shell_v_power_D, evolux_D, shell_v_power_n, Nafta_super_bio, max_shell_v_power_D, max_evolux_D, max_shell_v_power_n, max_Nafta_super_bio=tank_selector(stocks,m1__,m3__,m4__,m5__,m6__,m7__,m8__,m9__,m11__,window_lower,c_min)

orders_filtered=filter_orders_by_tank(orders,max_shell_v_power_D,max_evolux_D, max_shell_v_power_n, max_Nafta_super_bio)

if orders_filtered.empty:
    pass
    shell_v_power_D, evolux_D, shell_v_power_n, Nafta_super_bio, max_shell_v_power_D, max_evolux_D, max_shell_v_power_n, max_Nafta_super_bio=tank_selector(stocks,m1__,m3__,m4__,m5__,m6__,m7__,m8__,m9__,m11__,window_lower+6,c_min)

    orders_filtered=filter_orders_by_tank(orders,max_shell_v_power_D,max_evolux_D, max_shell_v_power_n, max_Nafta_super_bio)

orders_filtered['valid']='True'
orders=pd.concat([orders_filtered,orders])
orders=orders.drop_duplicates(subset=orders.columns.difference(['valid']))

#salida del motor de calculo

#orders si la orden es valida tiene un True, sino NaN
#window_lower     (ventana inferior en horas)
#window_upper     (ventana superior en horas)
#shell_v_power_D  (disponibilidad de tanques v power diesel)
#evolux_D         (disponibilidad de tanques evolux)
#shell_v_power_n  (disponibilidad de tanques shell_v_power_n)
#Nafta_super_bio  (disponibilidad de tanques nafta super)

    
    


# In[13]:


orders.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




