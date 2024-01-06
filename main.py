
from data_solve import data_deal
from fjsp import FJSP
from multi_opt import mul_op
from nsga_2 import nsga_II
import numpy as np

oj=data_deal(6,6)               #工件数，机器数
Tmachine,Tmachinetime,tdx,work,tom=oj.cacu()
parm_data=[Tmachine,Tmachinetime,tdx,work,tom]
to=FJSP(6,6,0.5,parm_data)      #工件数，机器数，选择最短机器的概率和mk01的数据
oh=mul_op()
ho=nsga_II(5,100,to,oh,work,6)     #数50,100,10分别代表迭代的次数、种群的规模、工件数
#to是柔性车间模块，oh是多目标模块

pareto,pareto_job,pareto_machine,pareto_time,fit_every=ho.nsga_total()  #最后一次迭代的最优解
#print(pareto)
oh.draw_change(fit_every)        #每次迭代过程中pareto解中2个目标的变化
oh.draw_2d(pareto) 				 #Pareto图

sig=0
job,machine=np.array([pareto_job[sig]]),np.array([pareto_machine[sig]])
machine_time=np.array([pareto_time[sig]])
# C_finish,Twork,list_M,list_S,list_W,tmax=to.caculate(job,machine,machine_time)
to.draw(job,machine,machine_time)#画pareto解的第一个解的甘特图

