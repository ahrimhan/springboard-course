#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'exploratory-data-analysis/EDA_hospital_readmit'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Hospital Readmissions Data Analysis and Recommendations for Reduction
# 
# ### Background
# In October 2012, the US government's Center for Medicare and Medicaid Services (CMS) began reducing Medicare payments for Inpatient Prospective Payment System hospitals with excess readmissions. Excess readmissions are measured by a ratio, by dividing a hospital’s number of “predicted” 30-day readmissions for heart attack, heart failure, and pneumonia by the number that would be “expected,” based on an average hospital with similar patients. A ratio greater than 1 indicates excess readmissions.
# 
# ### Exercise Directions
# 
# In this exercise, you will:
# + critique a preliminary analysis of readmissions data and recommendations (provided below) for reducing the readmissions rate
# + construct a statistically sound analysis and make recommendations of your own 
# 
# More instructions provided below. Include your work **in this notebook and submit to your Github account**. 
# 
# ### Resources
# + Data source: https://data.medicare.gov/Hospital-Compare/Hospital-Readmission-Reduction/9n3s-kdb3
# + More information: http://www.cms.gov/Medicare/medicare-fee-for-service-payment/acuteinpatientPPS/readmissions-reduction-program.html
# + Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# ****

#%%
get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bokeh.plotting as bkp
from mpl_toolkits.axes_grid1 import make_axes_locatable


#%%
# read in readmissions data provided
hospital_read_df = pd.read_csv('data/cms_hospital_readmissions.csv')
hospital_read_df.head()

#%%
hospital_read_df.info()

#%% [markdown]
# ****
# ## Preliminary Analysis

#%%
# deal with missing and inconvenient portions of data 
clean_hospital_read_df = hospital_read_df.loc[hospital_read_df['Number of Discharges'] != 'Not Available']
clean_hospital_read_df.loc[:, 'Number of Discharges'] = clean_hospital_read_df['Number of Discharges'].astype(int)
clean_hospital_read_df = clean_hospital_read_df.sort_values('Number of Discharges')


#%%
# generate a scatterplot for number of discharges vs. excess rate of readmissions
# lists work better with matplotlib scatterplot function
# arhan: 'Number of Discharges' = 0 (index 0 - index 80)
# arhan: exclude the last 3 rows (outlier?)
x = [a for a in clean_hospital_read_df['Number of Discharges'][81:-3]]
y = list(clean_hospital_read_df['Excess Readmission Ratio'][81:-3])

fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(x, y, alpha=0.2)

ax.fill_between([0,350], 1.15, 2, facecolor='red', alpha = .15, interpolate=True)
ax.fill_between([800,2500], .5, .95, facecolor='green', alpha = .15, interpolate=True)

ax.set_xlim([0, max(x)])
ax.set_xlabel('Number of discharges', fontsize=12)
ax.set_ylabel('Excess rate of readmissions', fontsize=12)
ax.set_title('Scatterplot of number of discharges vs. excess rate of readmissions', fontsize=14)

ax.grid(True)
fig.tight_layout()

#%% [markdown]
# ****
# 
# ## Preliminary Report
# 
# Read the following results/report. While you are reading it, think about if the conclusions are correct, incorrect, misleading or unfounded. Think about what you would change or what additional analyses you would perform.
# 
# **A. Initial observations based on the plot above**
# + Overall, rate of readmissions is trending down with increasing number of discharges
# + With lower number of discharges, there is a greater incidence of excess rate of readmissions (area shaded red)
# + With higher number of discharges, there is a greater incidence of lower rates of readmissions (area shaded green) 
# 
# **B. Statistics**
# + In hospitals/facilities with number of discharges < 100, mean excess readmission rate is 1.023 and 63% have excess readmission rate greater than 1 
# + In hospitals/facilities with number of discharges > 1000, mean excess readmission rate is 0.978 and 44% have excess readmission rate greater than 1 
# 
# **C. Conclusions**
# + There is a significant correlation between hospital capacity (number of discharges) and readmission rates. 
# + Smaller hospitals/facilities may be lacking necessary resources to ensure quality care and prevent complications that lead to readmissions.
# 
# **D. Regulatory policy recommendations**
# + Hospitals/facilties with small capacity (< 300) should be required to demonstrate upgraded resource allocation for quality care to continue operation.
# + Directives and incentives should be provided for consolidation of hospitals and facilities to have a smaller number of them with higher capacity and number of discharges.

#%% [markdown]
# ****
# ### Exercise
# 
# Include your work on the following **in this notebook and submit to your Github account**. 
# 
# A. Do you agree with the above analysis and recommendations? Why or why not? <br>
#
# I do not agree with the above analysis with the following reasons.
# 
# 1. There is not trend for the incident of excess rate of readmissions and the number of discharges. <br>
# : With the visualization, the red and green shaded in the figure are biased. <br>
# : The number of hospitals regarding the discharges are not evenly distributed. 
# There is larger number of hospitals with low dischage (HLD) than the number of hospitals with high discharge (HHD). <br>
# : The HHD have two potential outliers with extremely high excess readmission


#%%
# Your turn


#%% [markdown]
# B. Provide support for your arguments and your own recommendations with a statistically sound analysis:
# 
#    1. Setup an appropriate hypothesis test.
#    2. Compute and report the observed significance value (or p-value).
#    3. Report statistical significance for $\alpha$ = .01. 
#    4. Discuss statistical significance and practical significance. Do they differ here? How does this change your recommendation to the client?
#    5. Look at the scatterplot above. 
#       - What are the advantages and disadvantages of using this plot to convey information?
#       - Construct another plot that conveys the same information in a more direct manner.
# 
# You can compose in notebook cells using Markdown: 
# + In the control panel at the top, choose Cell > Cell Type > Markdown
# + Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# ****


