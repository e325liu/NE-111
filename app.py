# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:16:23 2025

@author: Emily
"""

import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
#will be using norm, uniform, logistic, gamma, beta, gumbel_r, lognorm, chi2, t, weibull, rayleigh

#do ctrl-t to see streamlit options
st.title("Fit Histograms to Statistical Data")
st.header('NE111 Final Project')

tab1,tab2=st.tabs(['Input Data', 'View/Adjust Fit'])

#input data
tab1.subheader('To start, please input data by either typing or uploading')
tab1.text('*Please clear/delete the currently inputted data before switching to another input method.')

textinput,uploadinput=tab1.columns(2)
value1=textinput.text_area(
    'Type to input data. (Include commas between values).', 
    value="", 
    height=135, 
    max_chars=None, 
    placeholder='Click to type. Hit Ctrl-Enter finish input.', 
    disabled=False, 
    label_visibility="visible", 
    )

value2=uploadinput.file_uploader(
    'Click to upload data (CSV file)', 
    type=None, 
    accept_multiple_files=False,  
    disabled=False, 
    label_visibility="visible", 
    )

#%%
#processing stuff

tab1.subheader('Preview of graphed data without fit')

data = None
check=uploadinput.checkbox('Is there a non-numeric header in the CSV file?')

if value2 is not None: 
    if check is False:
        dframe = pd.read_csv(value2,header=None)
        data = dframe.iloc[:, 0].values  
    else:
        dframe = pd.read_csv(value2)
        data = dframe.iloc[:, 0].values  
    
elif value1.strip():
    try:
        value1 = value1.replace(',', ' ').split()
        listinput=[]
        for i in value1:
            listinput.append(float(i))
        data= np.array(listinput)
    except ValueError:
        tab1.error("Please check your input for non-numeric data.")
        data=None

if data is None:
    tab1.info("Please enter valid data via text or upload a CSV file.")
if data is not None:
    tab1.info('Please click on "View/Adjust Fit" tab to continue.')         
    

#preview of graphs
datamin, datamax = min(data), max(data)
pad = (datamax - datamin) * 0.1 

fig, ax = plt.subplots(figsize=[5, 5])
fig1, ax1 = plt.subplots(figsize=[5, 5])
ax1.plot(data, 'c.')
ax1.set_xlabel('Measurement Number')
ax1.set_ylabel('Value')
ax1.set_ylim([0, max(data)+pad])
ax1.set_title('Scatterplot')

 
fig2, ax2 = plt.subplots(figsize=[5, 5])
ax2.hist(data, bins=25, density=True, color='skyblue', edgecolor='dodgerblue')
ax2.set_xlabel('Value')
ax2.set_ylabel('Density')
if min(data)>0:
    ax2.set_xlim([0, datamax+pad])
else:
    ax2.set_xlim([datamin-pad, datamax+pad])
ax2.set_title('Histogram')

graphscatter, graphhisto = tab1.columns(2)
graphscatter.pyplot(fig1)
graphhisto.pyplot(fig2)
#%%
#choose type of distribution
options = ['Beta', 'Chi-squared', 'Gamma', 'Gumbel', 'Lognormal', 'Logistic', 'Normal', 'Rayleigh', 'Student’s t', 'Uniform', 'Weibull']

parameters,fittedgraph=tab2.columns([3,5])
option=parameters.selectbox(
    "Select type of fit", 
    options,
    index=0, 
    disabled=False, 
    label_visibility="visible", 
    accept_new_options=False
    )

optdict={
    'Normal': stats.norm,
    'Uniform': stats.uniform,
    'Logistic': stats.logistic,
    'Gamma': stats.gamma,
    'Beta': stats.beta,
    'Gumbel': stats.gumbel_r,
    'Lognormal': stats.lognorm,
    'Chi-squared': stats.chi2,
    'Student’s t': stats.t,
    'Weibull': stats.weibull_min,
    'Rayleigh': stats.rayleigh 
}

#manual fit (parameters)

parameters.text('')
parameters.markdown('**Manual Fit Adjustments**')

shift= parameters.slider('Adjust Fit Shift',
          min_value=float(-np.median(data)/4),
          max_value=float(np.median(data)/4),
          value=0.0,
          step=0.1,
          disabled=False,
          label_visibility="visible",
          )

spread= parameters.slider('Adjust Fit Spread',
          min_value=-float((max(data)-min(data))/2),
          max_value=float((max(data)-min(data))/2),
          value=1.0,
          step=0.1,
          disabled=False,
          label_visibility="visible",
          )
#%%
#start of tab2 (fit line of graphs)

choice=optdict[option]
params = choice.fit(data)
myfit = choice(*params)
x = np.linspace(0, 25, 100)
fit = myfit.pdf(x)


fig, ax = plt.subplots(figsize=[5, 5])
ax.plot(x+shift, fit, color='black')
ax.hist(data, 
        bins=25, 
        density=True, 
        color='skyblue', 
        edgecolor='dodgerblue');
# The semi colon stops matplotlib from writing to the console
ax.set_xlabel('Value')
ax.set_ylabel('Density')
if min(data)>0:
    ax.set_xlim([0, datamax+pad])
else:
    ax.set_xlim([datamin-pad, datamax+pad])
ax.set_title('Fitted Histogram')

fittedgraph.pyplot(fig)



#%%
#errors

histobar, binbounds= np.histogram(data, bins=25, density=True)
binavg= (binbounds[:-1] + binbounds[1:]) / 2
fitvalues = myfit.pdf(binavg)

avgerr = np.mean(np.abs(histobar- (fitvalues+ shift)))
maxerr = np.max(np.abs(histobar- (fitvalues+ spread)))

parameters.text('')
parameters.markdown(f'**The average error is:** {avgerr}')
parameters.markdown(f'**The maximum error is:** {maxerr}')

fittedgraph.caption('*Generally, lower average and maximum error values indicate a better fit.')



