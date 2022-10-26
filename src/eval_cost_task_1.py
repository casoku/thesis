import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.1
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
small_subtasks = [18.43]
std_small_subtasks = [4.4]
big_subtasks = [19.3]
std_bigsubtasks = [4.8]
DiRL = [17.3]
std_DiRL = [4.7]
SPECTRL = [23.3]
std_SPECTRL = [5.3]
# Set position of bar on X axis
br1 = np.arange(len(small_subtasks))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
 
# Make the plot
bar1 = plt.bar(br1, small_subtasks, yerr = std_small_subtasks, color ='firebrick', width = barWidth-0.02, capsize = 15,
         label ='OM + small subtasks')
plt.bar_label(bar1, fontsize = 18)
bar2 = plt.bar(br2, big_subtasks, yerr = std_bigsubtasks, color ='darkgreen', width = barWidth-0.02, capsize = 15,
        label ='OM + big subtasks')
plt.bar_label(bar2, fontsize = 18)
bar3 = plt.bar(br3, DiRL, yerr = std_DiRL, color ='midnightblue', width = barWidth-0.02, capsize = 15,
        label ='DiRL')
plt.bar_label(bar3, fontsize = 18)
bar4 = plt.bar(br4, SPECTRL, yerr = std_SPECTRL, color ='darkorange', width = barWidth-0.02, capsize = 15,
        label ='SPECTRL')
plt.bar_label(bar4, fontsize = 18)
 
# Adding Xticks
plt.ylabel('Cost(# of steps)', fontsize = 20)
plt.xticks([r + barWidth + 0.05 for r in range(len(small_subtasks))],
        ['Task 1'])
plt.tick_params(labelsize = 18)
#plt.legend(loc = 'center left' , bbox_to_anchor=(1, 0.5), fontsize = 20)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5, fontsize = 18)
plt.tight_layout()
plt.show()