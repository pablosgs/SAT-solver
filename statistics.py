#import statistics
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import csv
from scipy import stats


def plot_boxplots_runtime(DPLL, MOM, JW, size, metric):

    # Here, I'm going to do a lot of extra work to specifically calculate the means of the mean of all runs. his is because
    # It's specifically stated in the assignment, and perhaps this leads to different boxplots compared to cal. it directly

    
    runtime_dpll = []
    runtime_MOM = []
    runtime_JW = []

    count_dpll = 0
    count_mom = 0
    count_jw = 0

    for i in range(len(DPLL['success'])):
        if DPLL['success'][i] == '0':
            
            continue
        else: runtime_dpll.append(DPLL[f'{metric}'][i])
    
    for i in range(len(MOM[f'success'])):
        if MOM['success'][i] == '0' :
            
            continue
        else: runtime_MOM.append(MOM[f'{metric}'][i])
        
    for i in range(len(JW[f'success'])):
        if JW['runtime'][i] :
            
            continue

        else: runtime_JW.append(JW[f'{metric}'][i])
        

    # for counting:

    # for i in range(len(DPLL['runtime'])):
    #     if DPLL['runtime'][i] > 250.0:
    #         count_dpll += 1
            
    
    # for i in range(len(MOM[f'runtime'])):
    #     if MOM['runtime'][i] > 250.0:
    #         count_mom += 1
            
        
        
    # for i in range(len(JW[f'runtime'])):
    #     if JW['runtime'][i] > 250.0:
    #         count_jw += 1
            

    runtime_dpll = DPLL[f'{metric}']
    runtime_MOM = MOM[f'{metric}']
    runtime_JW = JW[f'{metric}']

    
    print(f'dpll: {count_dpll}, mom: {count_mom}, jw: {count_jw}')

    fig1, ax1 = plt.subplots()
    ax1.boxplot([runtime_dpll, runtime_MOM, runtime_JW], labels =('DPLL', 'MOM', 'JW'))
    #ax1.set_aspect(0.01, 0.01)
    if metric == 'runtime':
        plt.ylabel('runtime (s)')
        plt.ylim(0,650)
    elif metric == 'number of backtracks':
        plt.ylabel('backtracks (n)')
        # plt.ylim(-4, 4)
    plt.suptitle(f'{size} sudoku')
    plt.savefig(f'{size}_{metric}_boxplot.png')
    # plt.show()


#Choose for which size you want to create plots and statistics


DPLL = pd.read_csv("results/16x16/DPLL.csv")
MOM = pd.read_csv('results/16x16/MOM.csv')
JW = pd.read_csv('results/16x16/Jeroslow.csv')
size = '16x16'

#DPLL = pd.read_csv("results/9x9/DPLL.csv")
#MOM = pd.read_csv('results/9x9/MOM.csv')
#JW = pd.read_csv('results/9x9/Jeroslow.csv')
#size = '9x9'
#
#DPLL = pd.read_csv("results/4x4/DPLL.csv")
#MOM = pd.read_csv('results/4x4/MOM.csv')
#JW = pd.read_csv('results/4x4/Jeroslow.csv')
#size = '4x4'




plot_boxplots_runtime(DPLL, MOM, JW, size , metric = 'runtime')
plot_boxplots_runtime(DPLL, MOM, JW, size, metric = 'number of backtracks')

print(f'\n\nSudocu size: {size}\n')


dpll_runtime = []
dpll_success = list(DPLL['success'])
dpll_backtracks = []


MOM_runtime = []
MOM_success = list(MOM['success'])
MOM_backtracks = []


JW_runtime = []
JW_success = list(JW['success'])
JW_backtracks = []



for i in range(len(DPLL['success'])):
    if DPLL['success'][i] == '0':
        continue
    else: 
        dpll_runtime.append(DPLL['runtime'][i])
        dpll_backtracks.append(DPLL['number of backtracks'][i])

for i in range(len(MOM[f'success'])):
    if MOM['success'][i] == '0':
        continue
    else: 
        MOM_runtime.append(MOM['runtime'][i])
        MOM_backtracks.append(MOM['number of backtracks'][i])
    
for i in range(len(JW['success'])):
    if JW['success'][i] == '0':
        continue
    else: 
        
        JW_runtime.append(JW['runtime'][i])
        JW_backtracks.append(JW['number of backtracks'][i])

A = pd.DataFrame({'dpll_runtime' : dpll_runtime, 'dpll_backtracks' : dpll_backtracks, 'MOM_runtime' : MOM_runtime, 'MOM_backtracks':MOM_backtracks, 'JW_runtime' : JW_runtime, 'JW_backtracks' : JW_backtracks})

dpll_runtime = A['dpll_runtime']
dpll_backtracks = A['dpll_backtracks']
MOM_runtime = A['MOM_runtime']
MOM_backtracks = A['MOM_backtracks']
JW_runtime = A['JW_runtime']
JW_backtracks = A['JW_backtracks']


groupdpll = [0,0,0,0,0,0]
groupMOM = [0,0,0,0,0,0]
groupJW = [0,0,0,0,0,0]

for i in range(len(dpll_runtime)):
    if dpll_runtime[i] < 50:
        groupdpll[0] +=1
    elif dpll_runtime[i] < 70:
        groupdpll[1] += 1
    elif dpll_runtime[i] < 90:
        groupdpll[2] += 1
    elif dpll_runtime[i] < 110:
        groupdpll[3] += 1
    elif dpll_runtime[i] < 300:
        groupdpll[4] +=1
    else:
        groupdpll[5] +=1

for i in range(len(MOM_runtime)):
    if MOM_runtime[i] < 50:
        groupMOM[0] +=1
    elif MOM_runtime[i] < 70:
        groupMOM[1] += 1
    elif MOM_runtime[i] < 90:
        groupMOM[2] += 1
    elif MOM_runtime[i] < 110:
        groupMOM[3] += 1
    elif MOM_runtime[i] < 300:
        groupMOM[4] +=1
    else:
        groupMOM[5] += 1

for i in range(len(JW_runtime)):
    if JW_runtime[i] < 50:
        groupJW[0] +=1
    elif JW_runtime[i] < 70:
        groupJW[1] += 1
    elif JW_runtime[i] < 90:
        groupJW[2] += 1
    elif JW_runtime[i] < 110:
        groupJW[3] += 1
    elif JW_runtime[i] < 300:
        groupJW[4] +=1
    else:
        groupJW[5] +=1

labels = ['0-100', '100-200', "200-300", "300-400", "400-600", "big"]


x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, groupdpll, width, label='DPLL')
rects2 = ax.bar(x , groupMOM, width, label='MOM')
rects3 = ax.bar(x + width, groupJW, width, label='JW')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('n')
ax.set_title('Distribution of runtimes per Heuristic')

ax.legend()




fig.tight_layout()

plt.show()



print(f'DPLL runtime mean: {dpll_runtime.mean()} median: {dpll_runtime.median()}, max: {dpll_runtime.max()}, min: {dpll_runtime.min()}')
print(f'DPLL backtracks mean: {dpll_backtracks.mean()} median: {dpll_backtracks.median()}, max: {dpll_backtracks.max()}, min: {dpll_backtracks.min()}')
print(f'Succes/Total ratio: {dpll_success.count(1)}/{len(dpll_success)}')


print(f'MOM runtime mean: {MOM_runtime.mean()} median: {MOM_runtime.median()}, max: {MOM_runtime.max()}, min: {MOM_runtime.min()}')
print(f'MOM backtracks mean: {MOM_backtracks.mean()} median: {MOM_backtracks.median()}, max: {MOM_backtracks.max()}, min: {MOM_backtracks.min()}')
print(f'Succes/Total ratio: {MOM_success.count(1)}/{len(MOM_success)}')



print(f'JW runtime mean: {JW_runtime.mean()} median: {JW_runtime.median()}, max: {JW_runtime.max()}, min: {JW_runtime.min()}')
print(f'JW backtracks mean: {JW_backtracks.mean()} median: {JW_backtracks.median()}, max: {JW_backtracks.max()}, min: {JW_backtracks.min()}')
print(f'Succes/Total ratio: {JW_success.count(1)}/{len(JW_success)}')

print(f'\nStatistics:\n')

print('Runtime:')
print(f'DPLL vs MOM: {stats.mannwhitneyu(dpll_runtime, MOM_runtime, alternative="greater")}')
print(f'DPLL vs JW: {stats.mannwhitneyu(dpll_runtime, JW_runtime,alternative="greater")}')
print(f'MOM vs JW: {stats.mannwhitneyu(MOM_runtime, JW_runtime, alternative="less")}')



list_mean_dpll = [0.00268**(1/3), .68189**(1/3), 673.07**(1/3)]
list_mean_mom = [0.002696**(1/3), .6421**(1/3), 632.60**(1/3)]
list_mean_jw = [0.0068991152**(1/3), .6463**(1/3), 816.54**(1/3)]
list_gens = [4, 9, 16]
plt.plot(list_gens,list_mean_dpll, 'g', label="DPLL", marker ='o')
plt.plot(list_gens,list_mean_mom,'b' , label="MOM",marker ='o')
plt.plot(list_gens,list_mean_jw,'r' , label="Jeroslow-Wang",marker ='o')
plt.legend(['DPLL', 'MOM', 'Jeroslow-Wang'], loc='lower right')
plt.ylabel('Runtime^(1/3) (s)')
plt.xlabel('Sudoku size')
plt.suptitle('Sudoku Size Runtime')

plt.savefig('runtime_size.png')
plt.show()
