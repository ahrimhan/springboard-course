#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'exploratory-data-analysis/EDA_racial_discrimination'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Examining Racial Discrimination in the US Job Market Using EDA: Submitted by Ahrim Han (2019/2/23)
# 
# ### Background
# Racial discrimination continues to be pervasive in cultures throughout the world. Researchers examined the level of racial discrimination in the United States labor market by randomly assigning identical résumés to black-sounding or white-sounding names and observing the impact on requests for interviews from employers.
# 
# ### Data
# In the dataset provided, each row represents a resume. The 'race' column has two values, 'b' and 'w', indicating black-sounding and white-sounding. The column 'call' has two values, 1 and 0, indicating whether the resume received a call from employers or not.
# 
# Note that the 'b' and 'w' values in race are assigned randomly to the resumes when presented to the employer.
#%% [markdown]
# ### Exercises
# You will perform a statistical analysis to establish whether race has a significant impact on the rate of callbacks for resumes.
# 
# Answer the following questions **in this notebook below and submit to your Github account**. 
# 
#    1. What test is appropriate for this problem? Does CLT apply?
#    2. What are the null and alternate hypotheses?
#    3. Compute margin of error, confidence interval, and p-value. Try using both the bootstrapping and the frequentist statistical approaches.
#    4. Write a story describing the statistical significance in the context or the original problem.
#    5. Does your analysis mean that race/name is the most important factor in callback success? Why or why not? If not, how would you amend your analysis?
# 
# You can include written notes in notebook cells using Markdown: 
#    - In the control panel at the top, choose Cell > Cell Type > Markdown
#    - Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# 
# #### Resources
# + Experiment information and data source: http://www.povertyactionlab.org/evaluation/discrimination-job-market-united-states
# + Scipy statistical methods: http://docs.scipy.org/doc/scipy/reference/stats.html 
# + Markdown syntax: http://nestacms.com/docs/creating-content/markdown-cheat-sheet
# + Formulas for the Bernoulli distribution: https://en.wikipedia.org/wiki/Bernoulli_distribution

#%%
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms


#import sys
#sys.path.insert(0, '../../EDA_human_temperature/src/')
#import EDA_human_temperature

#%%
data = pd.io.stata.read_stata('data/us_job_market_discrimination.dta')

#%%
data.head()

#%% [markdown]
# <div class="span5 alert alert-success">
# <p>Your answers to Q1 and Q2 here</p>
# </div>

#%% [markdown]
# ### 1. What test is appropriate for this problem? Does CLT apply?
#
# The problem is to compare the probability of the success in two populations.  <br>
# A two sample z-test would be appropriate.  
# Given the number of samples ar large (2435 + 2435 = 4870 resumes), the Central Limit Theorem (CLT) can be applied.  

# ### 2. What are the null and alternate hypotheses?
# We compare the rate of callbacks for resumes of different groups of white-sounding names and black-sounding names. <br>
# The null hypothesis can be set as that the probability of interview request in black population is the same as that in the white population. <br>
# The alternative hypothesis can be set as that the probability of interview request in black population is **NOT** the same as that in the white population. <br>
# Let's say that the callback rate for the resumes with white-sounding names is $p_w$ and the callback rate for resumes with black-sounding names is $p_b$. <br>
#
# - $H_0$: $p_w$ = $p_b$  
# - $H_1$: $p_w$ $\neq$ $p_b$  (or $p_w$ > $p_b$)
# - We chose the significance level at 5% ($\alpha$ = 0.05).  
#
# Helpful material: ["comparing two proportions"](http://biostat.mc.vanderbilt.edu/wiki/pub/Main/AnesShortCourse/HypothesisTestingPart2.pdf)

#%% 
#g = sns.FacetGrid(data, col="id", hue="call")
#g = g.map(plt.hist, "call")

#%% [markdown]
# <div class="span5 alert alert-success">
# <p> Your solution to Q3 here </p>
# </div>

#%%
w = data[data.race=='w']
b = data[data.race=='b']

# number of callbacks for black-sounding names
white_calls = np.sum(data[data.race=='w'].call)
black_calls = np.sum(data[data.race=='b'].call)
total_calls = white_calls + black_calls
print("white calls: {}, black calls: {}, total calls: {}".format(white_calls, black_calls, total_calls))
# total resumes of black-sounding and white-sounding
total_white_sounding = len(w)
total_black_sounding = len(b)
total_resumes = total_white_sounding + total_black_sounding
print("white-sounding total: {}, black-sounding total: {}, total resumes: {}".format(total_white_sounding, total_black_sounding, total_resumes))
#probability of interview requests in black population and white population
p_w = white_calls / total_white_sounding
p_b = black_calls / total_black_sounding

print("probability of interview requests in white ($p_w$): {:.3f}".format(p_w))
print("probability of interview requests in black ($p_b$): {:.3f}".format(p_b))

std_error = np.sqrt((p_w*(1-p_w)/total_white_sounding) + (p_b*(1-p_b)/total_black_sounding))
empirical_diff = p_w - p_b
print("$p_w$ - $p_b$ : {}".format(empirical_diff))
print("standard error (SE): {}".format(std_error))

#%% [markdown]
# ### 3. Compute margin of error, confidence interval, and p-value.  
# Try using both the bootstrapping and the frequentist statistical approaches. <br>

# **3.1. Bootstrap hypothesis test**  

#%%
def diff_rate(data1, data2):
	# Function to calculate the difference of the rates between two data samples
	p1 = np.sum(data1)/len(data1)
	p2 = np.sum(data2)/len(data2)
	return p1 - p2

# Draw bootstrap replicates.
# Permutation of two samples.	
def draw_perm_reps(data1, data2, func, size):
	
	# Initialize array of replicates: bs_replicates
	perm_replicates = np.empty(size)
	data = np.concatenate((data1, data2))
	
	# Generate replicates
	for i in range(size):
		sample_perm = np.random.permutation(data)
		perm_data1 = sample_perm[:len(data1)]
		perm_data2 = sample_perm[len(data1):]
		perm_replicates[i] = diff_rate(perm_data1, perm_data2)
	return perm_replicates

#We compute the test statistic for each simulated data set.
bootstrap_replicates = draw_perm_reps(w.call, b.call, func=diff_rate, size=10000)
print(bootstrap_replicates)

#%%
# bootstrap approach: 95% confidence interval, margin of error, p-value
print('Bootstrap approach:')
bs_ci = np.percentile(bootstrap_replicates, [2.5, 97.5])
print('95% confidence interval range: [{:.3f}, {:.3f}]'.format(bs_ci[0], bs_ci[1]))
print('Margin of error is {:.4f} degrees.'.format((bs_ci[1]-bs_ci[0])/2))
# empirical_diff = p_w - p_b
p_val = np.sum(bootstrap_replicates >= empirical_diff) / len(bootstrap_replicates)
print('p-value = {:.10f}'.format(p_val))

#%% [markdown]
# ==> Since the $p-$value is much smaller than $\alpha$ = 0.05, we reject the null hypothesis that the probability of interview request in black population is the same as that in the white population.

#%% [markdown]
# **3.2. Frequentist statistical testing**

#%%
# Frequentist statistical testing 
# confidence interval: t-test, z-test
def CI_printout(sample, interval = 0.95, method = 't'):
	mean_val = sample.mean()
	n = sample.count()
	stdev = sample.std()
	if method == 't':
		test_stat = stats.t.ppf((interval + 1)/2, n)
	elif method == 'z':
		test_stat = stats.norm.ppf((interval + 1)/2)
	lower_bound = mean_val - test_stat * stdev / np.sqrt(n)
	upper_bound = mean_val + test_stat * stdev / np.sqrt(n)
	return lower_bound, upper_bound


# confidence interval: z-test, t-test (ratio comparison)
def CI_printout_ratio(data1, data2, interval = 0.95, method = 't'):
	p1 = np.sum(data1)/len(data1)
	p2 = np.sum(data2)/len(data2)
	#ratio-based sample stdev
	# variance: p*(1-p)/n
	# variance of a difference is equal to the sum of the variance (if they are uncorrelated)
	std_error = np.sqrt((p1*(1-p1)/len(data1)) + (p2*(1-p2)/len(data2)))
	#print("standard error (SE): {}".format(std_error))
	if method == 't':
		n = len(data1) + len(data2)
		test_stat = stats.t.ppf((interval + 1)/2, n)
		print("t: {}".format(test_stat))
	elif method == 'z':
		#ppf: Percent point function (inverse of cdf — percentiles).
		test_stat = stats.norm.ppf((interval + 1)/2)
		print("Z: {:.2f}".format(test_stat))

	# margin of error (error_margin) = test_stat * stdev / sqrt(n)
	# margin of error (error_margin) = test_stat * std_error
	# std_error = stdev / sqrt(n)
	# test_stat = Z = 1.96
	# empirical_diff = p1-p2
	error_margin = test_stat * std_error
	lower_bound = (p1-p2) - (test_stat * std_error)
	upper_bound = (p1-p2) + (test_stat * std_error)
	return error_margin, lower_bound, upper_bound


#%%
# Frequentist approach using two-sample z-test: 95% confidence interval, margin of error, p-value
print('Frequentist approach:')
#Run z test
error_margin, lower_bound, upper_bound = CI_printout_ratio(w.call, b.call, 0.95, 'z')
print('95% confidence interval range: [{:.3f}, {:.3f}]'.format(lower_bound, upper_bound))
print('Margin of error is {:.4f} degrees.'.format(error_margin))
z_score = empirical_diff / std_error
print("z_score: {}".format(z_score))
p_val = stats.norm.sf(abs(z_score)) #one-sided
print('p-value = {:.10f}'.format(p_val))

#%% [markdown]
# ==> Since the $p-$value is much smaller than $\alpha$ = 0.05, we reject the null hypothesis that the probability of interview request in black population is the same as that in the white population.

#%% 
#todo: Chi-squared test statistic

#%% [markdown]
# <div class="span5 alert alert-success">
# <p> Your answers to Q4 and Q5 here </p>
# </div>

#%% [markdown]
# ### 4. Write a story describing the statistical significance in the context or the original problem.
#In this study, we find that the racial discrimnation plays a significant role in the US labor market in terms of getting interview calls. <br>
#To achieve this result, 4870 resumes containing both black-sounding names and white-sounding names were collected. <br>
#We observed that 392 candidates out of 4870 received interview calls. There were 157 black-sounding names and 235 white-sounding names in the list of callback candidates. <br>
#This observation shows that the interview calls are related to races.  <br>
#To confirm this observation, we carried out two hypothesis tests assuming the null hypothesis that the probability of interview request in black population is the same as that in the white population. <br>
#We found the $p-$value to be significantly smaller than $\alpha$=0.05. <br>
#This means that we can reject the null hypothesis in favor of the alternate hypothesis that the number of interview callbacks do depend on whther the candidate's name is black-sounding or white-sounding. <br>
#In fact, the difference between the white-sounding resume callback proportion and black-sounding resume callback proportion is statistically significant. <br>
#The 95% confidence interval for this proportion difference is 0.017 ~ 0.047 using the frequentist statistical testing. <br>
#The 95% confidence interval for this proportion difference is -0.016 ~ 0.016 using the bootstrap approach.

#%% [markdown]
# ### 5. Does your analysis mean that race/name is the most important factor in callback success? Why or why not? If not, how would you amend your analysis?
#The analysis does not mean race/name is the most important factor in callback success because we have not yet studied other features. 
#In this work, only the effect of race on the nuber of callbacks was studied. 
#There could be other important factors, such as age, years of experience, sex, and education, that can affect the callback numbers.
#Therefore, we cannot conclude that the race is the most (and/or only) important factor. 
#In order to find the most important factor, each factor needs to be studied separately and see its effect on the number of callbacks. 
