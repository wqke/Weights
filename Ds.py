import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from numpy import *
import numpy as np
import math
from math import cos,sin,pi
import root_pandas
import pandas as pd
from root_numpy import root2array, rec2array, tree2array
from ROOT import TFile,TChain,TTree
from uncertainties import *


from sklearn.metrics import accuracy_score, log_loss, classification_report, roc_auc_score,confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import  train_test_split,KFold
from sklearn.utils.class_weight import compute_sample_weight
import joblib
import pandas.core.common as com
from pandas.core.index import Index



def returnBDT(pred):
  res=[]
  for element in pred:
    res.append(element[0])
  return res

bdt = joblib.load('/home/ke/bdt.joblib')

#D* Ds X background
#Fractions defined relative to D* Ds*(=1)
#Fit values
frac_fit={}
frac_fit['Bd2DstDs']=0.594
frac_fit['Bd2DstDsst']=1.
frac_fit['Bd2DstDs1']=0.365

frac_fit['Bu2DststDs1']=0.416*5e-4/(5e-4+0.0177+8e-3)   #fraction of the sum x relative branching fractions
frac_fit['Bu2DststDs']=0.416*0.0177/(5e-4+0.0177+8e-3)
frac_fit['Bu2DststDsst']=0.416*8e-3/(5e-4+0.0177+8e-3)


frac_fiterr={}
frac_fiterr['Bd2DstDs']=
frac_fiterr['Bd2DstDsst']=
frac_fiterr['Bd2DstDs1']=

frac_fiterr['Bu2DststDs1']=/(5e-4+0.0177+8e-3)   #fraction of the sum x relative branching fractions
frac_fiterr['Bu2DststDs']=/(5e-4+0.0177+8e-3)
frac_fiterr['Bu2DststDsst']=/(5e-4+0.0177+8e-3)



#SUB MODES
#branching fractions
BF={}
BF['Ds1']={}
BF['Dsst']={}
BF['D10']={}
BF['Dplus']={}
BF['D0']={}
BF['Dst0']={}
BF['Dstmin']={}
BF['eta']={}
BF['etap']={}
BF['rho0']={}
BF['rhoplus']={}
BF['omega']={}
BF['Dsplus']={}


###Ds1(2460) decays
#Ds1(2460)->Ds+ gamma
BF['Ds1']['dsgamma']=0.18
#Ds1(2460)->Ds*+ pi0
BF['Ds1']['dsstpi0']=0.48

###Ds*+ decays
#Ds* -> Ds gamma
BF['Dsst']['dsgamma']=0.299
#Ds* -> Ds pi0
BF['Dsst']['dspi0']=0.058

###D1(2420)0 decays
#D1(2420) -> D*- pi+
BF['D10']['dstpiplus']=1.

###D+ decays
#D+ -> Ks0 3pi
BF['Dplus']['Ks3pi']=0.0297
#D+ -> pi+pi+pi-pi0
BF['Dplus']['3pipi0']=0.0111

###D0 decays
#D0 ->K-pi+pi+pi-
BF['D0']['K3pi']=0.0811
#D0 ->K-pi+pi+pi-pi0
BF['D0']['K3pipi0']=0.042

###D*0 decays
#D*0 -> Ks0 3pi
BF['Dst0']['d0pi0']=0.647
#D*0 -> D0 gamma
BF['Dst0']['d0gamma']=0.353
  
###D*- decays
#D*- ->D0 pi-
BF['Dstmin']['D0pi']=0.677

###eta decay : eta-> pi+ pi- pi0
BF['eta']['3pi']=0.2292
###eta' decays : eta'->eta pi+ pi- 
BF['etap']['etapipi']=0.426
#eta'->rho0 gamma 
BF['etap']['rhogamma']=0.289
###rho0 decay : rho0 ->pi+pi-
BF['rho0']['2pi']=1.
###rho+ decay : rho+ ->pi+pi0
BF['rhoplus']['2pi']=1.
###omega decay : omega ->pi+pi-pi0
BF['omega']['3pi']=0.892

###Ds+ decays
#Ds+->eta pi+
BF['Dsplus']['etapi']=0.017
#Ds+->(eta->3pi) pi+
#BF['Dsplus']['etapi_3pi']=BF['Dsplus']['etapi']*BF['eta']['3pi']
BF['Dsplus']['etapi']=BF['Dsplus']['etapi']*BF['eta']['3pi']
#Ds+->omega pi+
BF['Dsplus']['omegapi']=2.4e-3
#Ds+->(omega->3pi) pi+
#BF['Dsplus']['omegapi_3pi']=BF['Dsplus']['omegapi']*BF['omega']['3pi']
BF['Dsplus']['omegapi']=BF['Dsplus']['omegapi']*BF['omega']['3pi']
#Ds+->eta rho
BF['Dsplus']['etarho']=0.089
#Ds+->(eta->3pi) (rho->2pi)
#BF['Dsplus']['etarho_5pi']=BF['Dsplus']['etarho']*BF['eta']['3pi']*BF['rho0']['2pi']
BF['Dsplus']['etarho']=BF['Dsplus']['etarho']*BF['eta']['3pi']*BF['rho0']['2pi']
#Ds+->eta' rho+
BF['Dsplus']['etaprho']=0.058
#Ds+->omega rho
BF['Dsplus']['omegarho']=0.028 
#Ds+->rho0(pi+ pi-) rho0 (pi+ pi-) pi+
BF['Dsplus']['5pi']=8e-3  


#Ds+->omega pi+pi+pi-
BF['Dsplus']['omega3pi']=0.016
#Ds+->eta' pi+
BF['Dsplus']['etappi']=0.0394
#Ds+->eta' rho+
BF['Dsplus']['etaprho']=0.058

BF['Dsplus']['etappi_etapipi']=BF['Dsplus']['etappi'] * BF['etap']['etapipi'] * BF['eta']['3pi']
BF['Dsplus']['etappi_rhogamma']=BF['Dsplus']['etappi'] * BF['etap']['rhogamma'] * BF['rho0']['2pi']
BF['Dsplus']['etaprho_etapipi']=BF['Dsplus']['etaprho'] * BF['etap']['etapipi'] * BF['eta']['3pi'] * BF['rhoplus']['2pi']
BF['Dsplus']['etaprho_rhogamma']=BF['Dsplus']['etaprho'] * BF['rhoplus']['2pi'] *BF['etap']['rhogamma'] * BF['rho0']['2pi'] 




columns=[ 'Tau_FD_z',  'Tau_M', 'Tau_E','Tau_P', '3pi_M', '3pi_PZ', 'Tau_m12', 'Tau_m13','Tau_m23',
	 'Tau_FD', 'costheta_D_reco','costheta_L_reco','q2_reco','Tau_PZ_reco','Tau_PT',
	'chi_reco', 'Tau_life_reco']






############PLOT THE TOTAL HISTOGRAMS############

#Bd2DstDs1   :   B0->D*-Ds1(2460)+
files=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsgamma_omegarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs1/dsstpi0_dsgamma_omegarho_LHCb_Total/model_vars.root']

weights0=[]
for file in files:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name, remove 'LHCb_Total'
  weight=BF['Dstmin']['D0pi'] * BF['Ds1'][components[0]]
  if components[0]=='dsgamma':
    if len(components)==2:
      weight=weight*BF['Dsplus'][components[1]]
    if len(components)==3:
      weight=weight*BF['Dsplus'][components[1]+'_'+components[2]]
  elif components[0]=='dsstpi0': 
    if len(components)==3:
      weight=weight*BF['Dsst']['dsgamma']*BF['Dsplus'][components[2]]
    if len(components)==4:
      weight=weight*BF['Dsst']['dsgamma']*BF['Dsplus'][components[2]+'_'+components[3]]
  weights0.append(weight)
  
sum0=sum(weights0)
for i in range(len(weights0)):
  weights0[i]=weights0[i]/sum0   #define the weight with regard to the sum (the proportion)

DF=root_pandas.read_root(files[0],columns=columns,key='DecayTree')
DF=DF.sample(n=int(10000000*weights0[0]*frac_fit['Bd2DstDs1']),random_state=10000)
for i in range(1,len(files)):
  df=root_pandas.read_root(files[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(10000000*weights0[i]*frac_fit['Bd2DstDs1']),random_state=10000)
  DF=pd.concat([DF, df], ignore_index=True)






#Bd2DstDs
files1=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDs/omegarho_LHCb_Total/model_vars.root']

weights1=[]
for file in files1:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  if len(components)==1:
    weight=BF['Dstmin']['D0pi']* BF['Dsplus'][components[0]]
  if len(components)==2:
    weight=BF['Dstmin']['D0pi'] * BF['Dsplus'][components[0]+'_'+components[1]]
  weights1.append(weight)
  
sum1=sum(weights1)
for i in range(len(weights1)):
  weights1[i]=weights1[i]/sum1   #define the weight with regard to the sum (the proportion)

for i in range(len(files1)):
  df=root_pandas.read_root(files1[i],columns=columns,key='DecayTree')

  df=df.sample(n=int(10000000*weights1[i]*frac_fit['Bd2DstDs']),random_state=10000)
  DF=pd.concat([DF, df], ignore_index=True)
 




#Bd2DstDsst
files2=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dsgamma_omegarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDsst/dspi0_omegarho_LHCb_Total/model_vars.root']


weights2=[]
for file in files2:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['Dstmin']['D0pi']* BF['Dsst'][components[0]]
  if len(components)==2:
    weight=weight*BF['Dsplus'][components[1]]
  if len(components)==3:
    weight=weight * BF['Dsplus'][components[1]+'_'+components[2]]
  weights2.append(weight)
  
sum2=sum(weights2)
for i in range(len(weights2)):
  weights2[i]=weights2[i]/sum2   #define the weight with regard to the sum (the proportion)

  
for i in range(len(files2)):
  df=root_pandas.read_root(files2[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(10000000*weights2[i]*frac_fit['Bd2DstDsst']),random_state=10000)
  DF=pd.concat([DF, df], ignore_index=True)
  



  
  
#Bu2DststDs
files3=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs/omegarho_LHCb_Total/model_vars.root']


weights3=[]
for file in files3:
  #df=root_pandas.read_root(file,columns=['q2_reco','costheta_L_reco','costheta_D_reco','chi_reco','Tau_life_reco'],key='DecayTree')
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['D10']['dstpiplus']   #=1.
  if len(components)==1:
    weight=weight * BF['Dsplus'][components[0]]
  if len(components)==2:
    weight=weight * BF['Dsplus'][components[0]+'_'+components[1]]
  weights3.append(weight)

sum3=sum(weights3)
for i in range(len(weights3)):
  weights3[i]=weights3[i]/sum3   #define the weight with regard to the sum (the proportion)

for i in range(len(files3)):
  df=root_pandas.read_root(files3[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(10000000*weights3[i]*frac_fit['Bu2DststDs']),random_state=10000)
  DF=pd.concat([DF, df], ignore_index=True)
 



#Bu2DststDsst
files4=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dsgamma_omegarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDsst/dspi0_omegarho_LHCb_Total/model_vars.root']

weights4=[]
for file in files4:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['D10']['dstpiplus']  * BF['Dsst'][components[0]]
  if len(components)==2:
    weight=weight * BF['Dsplus'][components[1]]
  if len(components)==3:
    weight=weight * BF['Dsplus'][components[1]+'_'+components[2]]
  weights4.append(weight)

sum4=sum(weights4)
for i in range(len(weights4)):
  weights4[i]=weights4[i]/sum4   #define the weight with regard to the sum (the proportion)

for i in range(len(files4)):
  df=root_pandas.read_root(files4[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(10000000*weights4[i]*frac_fit['Bu2DststDsst']),random_state=10000)
  DF=pd.concat([DF, df], ignore_index=True)
  



#Bu2DststDs1
files5=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsgamma_omegarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_5pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_etapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_etappi_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_etappi_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_etaprho_etapipi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_etaprho_rhogamma_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_etarho_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_omega3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_omegapi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DststDs1/dsstpi0_dsgamma_omegarho_LHCb_Total/model_vars.root']


weights5=[]
for file in files5:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['D10']['dstpiplus']  *BF['Ds1'][components[0]] 
  if components[0]=='dsgamma':
    if len(components)==2:
      weight=weight*BF['Dsplus'][components[1]]
    if len(components)==3:
      weight=weight*BF['Dsplus'][components[1]+'_'+components[2]]
  elif components[0]=='dsstpi0': 
    if len(components)==3:
      weight=weight*BF['Dsst']['dsgamma']*BF['Dsplus'][components[2]]
    if len(components)==4:
      weight=weight*BF['Dsst']['dsgamma']*BF['Dsplus'][components[2]+'_'+components[3]]
  weights5.append(weight)

sum5=sum(weights5)
for i in range(len(weights5)):
  weights5[i]=weights5[i]/sum5   #define the weight with regard to the sum (the proportion)
  
for i in range(len(files5)):
  df=root_pandas.read_root(files5[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(10000000*weights5[i]*frac_fit['Bu2DststDs1']),random_state=10000)
  DF=pd.concat([DF, df], ignore_index=True)
  





DF["hamweight_SM"]=1.
DF["hamweight_T1"]=1.
DF["hamweight_T2"]=1.


DF.to_root('Ds.root', key='DecayTree')



	

"""
ranges=[[-1.,1.],[-np.pi,np.pi],[0.,2.],[0.,13.],[-1.,1.]]
filenames=['costheta_D_reco','chi_reco','Tau_life_reco','q2_reco','costheta_L_reco']
titles=[r'cos$(\theta_D)$',r'$\chi$',r'$\tau$ life',r'$q^2$',r'cos$(\theta_L)$']

totalfile=[files,files1,files2,files3,files4,files5]

binnumber=100

labels=[r'$B^0 \rightarrow D^{*-} D_{s1}(2460)^+$',r'$B^0 \rightarrow D^{*-} D_s^+$',r'$B^0 \rightarrow D^{*-} D_s^{*+}$',r'$B^+ \rightarrow D_1(2420)^0D_s^+$',r'$B^+ \rightarrow D_1(2420)^0D_s^{*+}$',r'$B^+ \rightarrow D_1(2420)^0D_{s1}(2460)^+$']

DF.to_root('Ds.root', key='DecayTree')

for i in range(5):
  plt.hist(DF[filenames[i]][~np.isnan(DF[filenames[i]])],histtype='step',bins=100,range=ranges[i])
  plt.ylim(bottom=0)  
  plt.title(titles[i]+r'  (B $\rightarrow$ $D^*$ $D_s$ X)')
  plt.savefig(filenames[i]+'_Ds.pdf')
  plt.close()

"""