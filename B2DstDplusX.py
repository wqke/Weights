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

#D* D+ X background
#Fractions defined with regard to the biggest one. B+ and B0 are assumed to have the same amount (so we directly use the branching fractions)
#Fit values
frac_fit={}
frac_fit['Bd2DstDK0']=2.47e-3/2.47e-3
frac_fit['Bu2DstDK']=6.3e-4/2.47e-3


  
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
BF['Dplus']['ks3pi']=0.0297
#D+ -> pi+pi+pi-pi0
BF['Dplus']['3pipi0']=0.0111

###D0 decays
#D0 ->K-pi+pi+pi-
BF['D0']['k3pi']=0.0811
#D0 ->K-pi+pi+pi-pi0
BF['D0']['kpipi0']=0.042

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


############PLOT THE TOTAL HISTOGRAMS############

#Bd2DstDK0
files=['/data/lhcb/users/hill/bd2dsttaunu_angular/RapidSim_tuples/Bd2DstDK0/3pipi0_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/bd2dsttaunu_angular/RapidSim_tuples/Bd2DstDK0/ks3pi_LHCb_Total/model_vars.root']


weights0=[]
for file in files:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name, remove 'LHCb_Total'
  weight=BF['Dplus'][components[0]]
  weights0.append(weight)

sum0=sum(weights0)
for i in range(len(weights0)):
  weights0[i]=weights0[i]/sum0   #define the weight with regard to the sum (the proportion)

DF=root_pandas.read_root(files[0],columns=['q2_reco','costheta_L_reco','costheta_D_reco','chi_reco','Tau_life_reco'],key='DecayTree')
DF=DF.sample(n=int(2000000*weights0[0]*frac_fit['Bd2DstDK0']))
for i in range(1,len(files)):
  df=root_pandas.read_root(files[i],columns=['q2_reco','costheta_L_reco','costheta_D_reco','chi_reco','Tau_life_reco'],key='DecayTree')
  df=df.sample(n=int(2000000*weights0[i]*frac_fit['Bd2DstDK0']))
  DF=pd.concat([DF, df], ignore_index=True)



#Bu2DstDK
files1=['/data/lhcb/users/hill/bd2dsttaunu_angular/RapidSim_tuples/Bu2DstDK/3pipi0_LHCb_Total/model_vars.root',
'/data/lhcb/users/hill/bd2dsttaunu_angular/RapidSim_tuples/Bu2DstDK/ks3pi_LHCb_Total/model_vars.root']

weights1=[]
for file in files1:
  components=(file.split('/')[-2]).split('_')
  components=components[:-2]   #extract the sub mode from the file name
  weight=BF['Dplus'][components[0]]
  weights1.append(weight)

sum1=sum(weights1)
for i in range(len(weights1)):
  weights1[i]=weights1[i]/sum1   #define the weight with regard to the sum (the proportion)

for i in range(len(files1)):
  df=root_pandas.read_root(files1[i],columns=['q2_reco','costheta_L_reco','costheta_D_reco','chi_reco','Tau_life_reco'],key='DecayTree')
  df=df.sample(n=int(2000000*weights1[i]*frac_fit['Bu2DstDK']))
  DF=pd.concat([DF, df], ignore_index=True)


                                       
                                              ### HISTOGRAMS ###
ranges=[[-1.,1.],[-np.pi,np.pi],[0.,6.],[0.,13.],[-1.,1.]]
filenames=['costheta_D_reco','chi_reco','Tau_life_reco','q2_reco','costheta_L_reco']
titles=[r'cos$(\theta_D)$',r'$\chi$',r'$\tau$ life',r'$q^2$',r'cos$(\theta_L)$']
binnumber=100
                                              
DF.to_root('B2DstDplusX.root', key='DecayTree')

for i in range(5):
  plt.hist(DF[filenames[i]][~np.isnan(DF[filenames[i]])],histtype='step',bins=binnumber,range=ranges[i])
  plt.ylim(bottom=0)  
  plt.title(titles[i]+r'  (B $\rightarrow$ $D^*$ $D^+$ X)')
  plt.savefig(filenames[i]+'_DstDplusX.pdf')
  plt.close()
