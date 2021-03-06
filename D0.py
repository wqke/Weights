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
import random

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


import sys
num = sys.argv[1]



def returnBDT(pred):
  res=[]
  for element in pred:
    res.append(element[0])
  return res

bdt = joblib.load('/home/ke/bdt.joblib')

#D* D0 X background
#Fractions defined with regard to the biggest one. B+ and B0 are assumed to have the same amount (so we directly use the branching fractions)
#Fit values
frac_fit={}
frac_fiterr={}
frac_fit['Bu2DstD0K0']=3.8e-3/1.06e-2
frac_fiterr['Bu2DstD0K0']=0.4e-3/1.06e-2
frac_fit['Bu2DstDst0K0']=9.2e-3/1.06e-2
frac_fiterr['Bu2DstDst0K0']=1.2e-3/1.06e-2
frac_fit['Bd2DstD0K']=2.47e-3/1.06e-2
frac_fiterr['Bd2DstD0K']=0.21e-3/1.06e-2
frac_fit['Bd2DstDst0K']= 1.06e-2/1.06e-2
frac_fiterr['Bd2DstDst0K']= 0.09e-2/1.06e-2
frac_fit['Bd2DstDstK0']=8.1e-3/1.06e-2
frac_fiterr['Bd2DstDstK0']=0.7e-3/1.06e-2

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

BFerr={}
BFerr['Ds1']={}
BFerr['Dsst']={}
BFerr['D10']={}
BFerr['Dplus']={}
BFerr['D0']={}
BFerr['Dst0']={}
BFerr['Dstmin']={}
BFerr['eta']={}
BFerr['etap']={}
BFerr['rho0']={}
BFerr['rhoplus']={}
BFerr['omega']={}
BFerr['Dsplus']={}



###Ds1(2460) decays
#Ds1(2460)->Ds+ gamma
BF['Ds1']['dsgamma']=0.18
BFerr['Ds1']['dsgamma']=0.04

#Ds1(2460)->Ds*+ pi0
BF['Ds1']['dsstpi0']=0.48
BFerr['Ds1']['dsstpi0']=0.11

###Ds*+ decays
#Ds* -> Ds gamma
BF['Dsst']['dsgamma']=0.299
BFerr['Dsst']['dsgamma']=0.007

#Ds* -> Ds pi0
BF['Dsst']['dspi0']=0.058
BFerr['Dsst']['dspi0']=0.007

###D1(2420)0 decays
#D1(2420) -> D*- pi+
BF['D10']['dstpiplus']=1.
BFerr['D10']['dstpiplus']=0.

###D+ decays
#D+ -> Ks0 3pi
BF['Dplus']['Ks3pi']=0.0297
BFerr['Dplus']['Ks3pi']=0.0011

#D+ -> pi+pi+pi-pi0
BF['Dplus']['3pipi0']=0.0111
BFerr['Dplus']['3pipi0']=8e-4


###D0 decays
#D0 ->K-pi+pi+pi-
BF['D0']['k3pi']=0.0811
BFerr['D0']['k3pi']=1.5e-3

#D0 ->K-pi+pi+pi-pi0
BF['D0']['k3pipi0']=0.042
BFerr['D0']['k3pipi0']=4e-3


###D*0 decays

BF['Dst0']['d0pi0']=0.647
BFerr['Dst0']['d0pi0']=9e-3

#D*0 -> D0 gamma
BF['Dst0']['d0gamma']=0.353
BFerr['Dst0']['d0gamma']=9e-3


###D*- decays
#D*- ->D0 pi-
BF['Dstmin']['D0pi']=0.677
BFerr['Dstmin']['D0pi']=5e-3


###eta decay : eta-> pi+ pi- pi0
BF['eta']['3pi']=0.2292
BFerr['eta']['3pi']=2.8e-3
###eta' decays : eta'->eta pi+ pi- 
BF['etap']['etapipi']=0.426
BFerr['etap']['etapipi']=7e-3
#eta'->rho0 gamma 
BF['etap']['rhogamma']=0.289
BFerr['etap']['rhogamma']=5e-3
###rho0 decay : rho0 ->pi+pi-
BF['rho0']['2pi']=1.
BFerr['rho0']['2pi']=0.
###rho+ decay : rho+ ->pi+pi0
BF['rhoplus']['2pi']=1.
BFerr['rhoplus']['2pi']=0.
###omega decay : omega ->pi+pi-pi0
BF['omega']['3pi']=0.892
BFerr['omega']['3pi']=7e-3

###Ds+ decays
#Ds+->eta pi+
BF['Dsplus']['etapi']=0.017
BFerr['Dsplus']['etapi']=9e-4

#Ds+->omega pi+
BF['Dsplus']['omegapi']=2.4e-3
BFerr['Dsplus']['omegapi']=6e-4

#Ds+->eta rho
BF['Dsplus']['etarho']=0.089
BFerr['Dsplus']['etarho']=8e-3

#Ds+->eta' rho+
BF['Dsplus']['etaprho']=0.058
BFerr['Dsplus']['etaprho']=0.015
#Ds+->omega rho
BF['Dsplus']['omegarho']=0.028 
BFerr['Dsplus']['omegarho']=0.
#Ds+->rho0(pi+ pi-) rho0 (pi+ pi-) pi+
BF['Dsplus']['5pi']=8e-3  
BFerr['Dsplus']['5pi']=8e-4

#Ds+->omega pi+pi+pi-
BF['Dsplus']['omega3pi']=0.016
BFerr['Dsplus']['omega3pi']=0.005
#Ds+->eta' pi+
BF['Dsplus']['etappi']=0.0394
BFerr['Dsplus']['etappi']=0.25e-2
#Ds+->eta' rho+
BF['Dsplus']['etaprho']=0.058
BFerr['Dsplus']['etaprho']=0.015



frac_names=list(frac_fit)
for name in frac_names:
  frac_fit[name]=random.uniform(-frac_fiterr[name]+frac_fit[name],frac_fiterr[name]+frac_fit[name])


mode_names=list(BFerr)
for mode in mode_names:
  submode_names=list(BFerr[mode])
  for sub in submode_names:
    BF[mode][sub]=random.uniform(-BFerr[mode][sub]+BF[mode][sub],BFerr[mode][sub]+BF[mode][sub])

print frac

#Ds+->(eta->3pi) pi+
#BF['Dsplus']['etapi_3pi']=BF['Dsplus']['etapi']*BF['eta']['3pi']
BF['Dsplus']['etapi']=BF['Dsplus']['etapi']*BF['eta']['3pi']

#Ds+->(omega->3pi) pi+
#BF['Dsplus']['omegapi_3pi']=BF['Dsplus']['omegapi']*BF['omega']['3pi']
BF['Dsplus']['omegapi']=BF['Dsplus']['omegapi']*BF['omega']['3pi']

#Ds+->(eta->3pi) (rho->2pi)
#BF['Dsplus']['etarho_5pi']=BF['Dsplus']['etarho']*BF['eta']['3pi']*BF['rho0']['2pi']
BF['Dsplus']['etarho']=BF['Dsplus']['etarho']*BF['eta']['3pi']*BF['rho0']['2pi']

BF['Dsplus']['etappi_etapipi']=BF['Dsplus']['etappi'] * BF['etap']['etapipi'] * BF['eta']['3pi']
BF['Dsplus']['etappi_rhogamma']=BF['Dsplus']['etappi'] * BF['etap']['rhogamma'] * BF['rho0']['2pi']
BF['Dsplus']['etaprho_etapipi']=BF['Dsplus']['etaprho'] * BF['etap']['etapipi'] * BF['eta']['3pi'] * BF['rhoplus']['2pi']
BF['Dsplus']['etaprho_rhogamma']=BF['Dsplus']['etaprho'] * BF['rhoplus']['2pi'] *BF['etap']['rhogamma'] * BF['rho0']['2pi'] 

############PLOT THE TOTAL HISTOGRAMS############

columns=[ 'Tau_FD_z',  'Tau_M', '3pi_M', 'Tau_m12', 'Tau_m13','Tau_m23',
         'Tau_FD', 'costheta_D_reco','costheta_L_reco','q2_reco',
        'chi_reco', 'Tau_life_reco']


#Bu2DstD0K0
files=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DstD0K0/k3pi_LHCb_Total/model_vars.root',
       '/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DstD0K0/k3pipi0_LHCb_Total/model_vars.root']

weights0=[]
for file in files:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name, remove 'LHCb_Total'
  weight=BF['D0'][components[0]]
  weights0.append(weight)

sum0=sum(weights0)
for i in range(len(weights0)):
  weights0[i]=weights0[i]/sum0   #define the weight with regard to the sum (the proportion)

DF=root_pandas.read_root(files[0],columns=columns,key='DecayTree')
DF=DF.sample(n=int(4000000*weights0[0]*frac_fit['Bu2DstD0K0']))

print 'OK'

for i in range(1,len(files)):
  df=root_pandas.read_root(files[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(4000000*weights0[i]*frac_fit['Bu2DstD0K0']))
  DF=pd.concat([DF, df], ignore_index=True)
  print 'OK'



#Bu2DstDst0K0
files1=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DstDst0K0/d0gamma_k3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DstDst0K0/d0gamma_k3pipi0_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DstDst0K0/d0pi0_k3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bu2DstDst0K0/d0pi0_k3pipi0_LHCb_Total/model_vars.root']

weights1=[]
for file in files1:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['Dst0'][components[0]] * BF['D0'][components[1]]
  weights1.append(weight)

sum1=sum(weights1)
for i in range(len(weights1)):
  weights1[i]=weights1[i]/sum1   #define the weight with regard to the sum (the proportion)

for i in range(len(files1)):
  df=root_pandas.read_root(files1[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(4000000*weights1[i]*frac_fit['Bu2DstDst0K0']),random_state=6000)
  DF=pd.concat([DF, df], ignore_index=True)
  print 'OK'


#Bd2DstD0K
files2=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstD0K/k3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstD0K/k3pipi0_LHCb_Total/model_vars.root']

weights2=[]
for file in files2:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['D0'][components[0]]
  weights2.append(weight)
sum2=sum(weights2)
for i in range(len(weights2)):
  weights2[i]=weights2[i]/sum2   #define the weight with regard to the sum (the proportion)

for i in range(len(files2)):
  df=root_pandas.read_root(files2[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(4000000*weights2[i]*frac_fit['Bd2DstD0K']),random_state=6000)
  DF=pd.concat([DF, df], ignore_index=True)
  print 'OK'




#Bd2DstDst0K
files3=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDst0K/d0gamma_k3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDst0K/d0gamma_k3pipi0_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDst0K/d0pi0_k3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDst0K/d0pi0_k3pipi0_LHCb_Total/model_vars.root']


weights3=[]
for file in files3:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['Dst0'][components[0]] * BF['D0'][components[1]]
  weights3.append(weight)

sum3=sum(weights3)
for i in range(len(weights3)):
  weights3[i]=weights3[i]/sum3   #define the weight with regard to the sum (the proportion)

for i in range(len(files3)):
  df=root_pandas.read_root(files3[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(4000000*weights3[i]*frac_fit['Bd2DstDst0K']),random_state=6000)
  DF=pd.concat([DF, df], ignore_index=True)
  print 'OK'





#Bd2DstDstK0
files4=['/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDstK0/k3pi_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Bd2DstDstK0/k3pipi0_LHCb_Total/model_vars.root']

weights4=[]
for file in files4:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['D0'][components[0]]
  weights4.append(weight)
sum4=sum(weights4)
for i in range(len(weights4)):
  weights4[i]=weights4[i]/sum4   #define the weight with regard to the sum (the proportion)

for i in range(len(files4)):
  df=root_pandas.read_root(files4[i],columns=columns,key='DecayTree')
  df=df.sample(n=int(4000000*weights4[i]*frac_fit['Bd2DstDstK0']),random_state=6000)
  DF=pd.concat([DF, df], ignore_index=True)
  print 'OK'


branch_names=['3pi_M',  'Tau_m12', 'Tau_m13','Tau_m23','Tau_FD','Tau_life_reco']

DF=DF.query("Tau_FD>4000.")

DF["hamweight_SM"]=1.
DF["hamweight_T1"]=1.
DF["hamweight_T2"]=1.

DF.to_root("/home/ke/tmps/D0.root","DecayTree",columns=branch_names)

print "THE LENGTH OF THIS FILE : ", len(DF)

#toy_rand = random.randint(1,1e10)
#toy_suf = "_%s" % toy_rand



D0 = root2array("/home/ke/tmps/D0.root","DecayTree",branch_names)
D0 = rec2array(D0)
y_predicted_D0 = bdt.decision_function(D0)
y_predicted_D0.dtype = [('BDT', np.float64)]

DF["BDT"]=returnBDT(y_predicted_D0)
DF.to_root('/data/lhcb/users/hill/Bd2DstTauNu_Angular/RapidSim_tuples/Merged_Bkg/D0/D0_%s.root' %num, key='DecayTree')


print "FILENAME : ", num



