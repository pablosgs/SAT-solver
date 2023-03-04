import statistics
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats


DPLL = pd.read_csv('D:/OneDrive/Desktop/STATISTICS/DPLL.csv')
MOM = pd.read_csv('D:/OneDrive/Desktop/STATISTICS/MOM.csv')
JW = pd.read_csv('D:/OneDrive/Desktop/STATISTICS/Jeroslow.csv')


def check_givens(line):
    givens = 0
    for i in line:
        if i.isnumeric() == True or i.isalpha() == True:
            givens += 1
    return givens

dpll_givens = []
mom_givens = []
jw_givens = [] 

for line in range(len(DPLL['num'])):
    dpll_givens.append(check_givens(DPLL['num'][line]))

for line in range(len(MOM['num'])):
    mom_givens.append(check_givens(MOM['num'][line]))
    

for line in range(len(JW['num'])):
    jw_givens.append(check_givens(JW['num'][line]))
    
    
# dpll_givens.sort()
# mom_givens.sort()
# jw_givens.sort()

DPLL['givens'] = dpll_givens
MOM['givens'] = mom_givens
JW['givens'] = jw_givens

DPLL = DPLL.sort_values(by=['givens'])
MOM = MOM.sort_values(by=['givens'])
JW = JW.sort_values(by=['givens'])

dpll_givens_count = []
dpll_givens_small = []
dpll_success = []

for given in pd.unique(DPLL['givens']):
    given_locations = DPLL.loc[DPLL['givens'] == given]['givens'].count()
    # dpll_givens_count.append(given_locations['givens'].count())
    dpll_givens_small.append(given)
    dpll_givens_count.append(given_locations)
    success = DPLL.loc[DPLL['givens'] == given]['success']
    dpll_success.append(success.sum()/len(success))


mom_givens_count = []
mom_givens_small = []
mom_success = []

for given in pd.unique(MOM['givens']):
    given_locations = MOM.loc[MOM['givens'] == given]['givens'].count()
    # dpll_givens_count.append(given_locations['givens'].count())
    mom_givens_small.append(given)
    mom_givens_count.append(given_locations)
    success = MOM.loc[MOM['givens'] == given]['success'] 
    mom_success.append(success.sum()/len(success))



JW_givens_count = []
JW_givens_small = []
JW_success = []

for given in pd.unique(JW['givens']):
    given_locations = JW.loc[JW['givens'] == given]['givens'].count()
    # dpll_givens_count.append(given_locations['givens'].count())
    JW_givens_small.append(given)
    JW_givens_count.append(given_locations)
    success = JW.loc[JW['givens'] == given]['success']
    JW_success.append(success.sum()/len(success))



plt.plot(dpll_givens_small,dpll_success, 'g', label="DPLL")
plt.plot(mom_givens_small,mom_success, 'r', label="MOM")
plt.plot(JW_givens_small,JW_success, 'b', label="JW")
plt.legend(['DPLL', 'MOM', 'JW'], loc='lower right')
plt.ylabel('success ratio')
plt.xlabel('number of givens')
plt.suptitle('difficulty per n givens')
plt.savefig('16x16_success_ratio.png')
plt.show()


# plt.legend(['GA mean', 'GA avg max', 'MDE mean', 'MDE avg max'], loc='lower right')
#     plt.ylabel('Fitness')
#     plt.xlabel('Generations')
#     plt.suptitle('enemies 1, 3, 4')
#     plt.xticks(np.arange(0, 31, 5))
    
#     if not os.path.exists('plots'):
#         os.makedirs('plots')

#     plt.savefig(f'plots/{plot_name}.png')
#     plt.show()


givens_success = pd.DataFrame({'givens' : dpll_givens_small, 'count':dpll_givens_count, 'success': dpll_success})

print(givens_success)

# givens_success.to_csv('givens_success.csv')
