
import numpy as np
import math
import matplotlib.pyplot as plt
#plt.rcParams['font.sans-serif'] = ['STSong'] 
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文

class mul_op():
	def divide(self,answer):
	    S=[[] for i in range(len(answer))]
	    front = [[]]
	    n=[0 for i in range(len(answer))]
	    rank = [0 for i in range(len(answer))]
	    for p in range(len(answer)):
	        for q in range(len(answer)):
	            # 如果p支配q
	            if (np.array(answer[p])<=np.array(answer[q])).all() and (answer[p]!=answer[q]): 
	                if q not in S[p]:
	                    S[p].append(q)  # 同时如果q不属于sp将其添加到sp中
	            # 如果q支配p
	            elif (np.array(answer[p])>=np.array(answer[q])).all() and (answer[p]!=answer[q]):
	                n[p] = n[p] + 1  # 则将np+1
	        if n[p]==0:
	            rank[p] = 0
	            if p not in front[0]:
	                front[0].append(p)
	    i = 0
	    while(front[i] != []):
	        Q=[]
	        for p in front[i]:
	            for q in S[p]:
	                n[q] =n[q] - 1  # 则将fk中所有给对应的个体np-1
	                if( n[q]==0):   # 如果nq==0
	                    rank[q]=i+1
	                    if q not in Q:
	                        Q.append(q)
	        i = i+1
	        front.append(Q)
	    del front[len(front)-1]
	    return front
	def dis(self,answer):
	    crowder,crowd=[],[]
	    front=self.divide(answer)
	    for i in range(len(front)):
	        x=[answer[front[i][j]][0] for j in range(len(front[i]))] #取两个个目标函数的各个目标
	        y=[answer[front[i][j]][1] for j in range(len(front[i]))]
	        sig=front[i]
	        clo=[[] for j in range(len(front[i]))]
	        if(len(sig)>1):    #每层的个体大于1个做拥挤度计算
	            x_index,y_index=np.array(x).argsort(),np.array(y).argsort()
	            x.sort(),y.sort();
	            dis1,dis2=[],[]
	            dis1.append(100000);dis2.append(100000)
	            if(len(sig)>2):    #大于2个做中间个体的拥挤度计算
	                for k in range(1,len(sig)-1):
	                    distance1,distance2=(x[k+1]-x[k-1])/(x[-1]-x[0]),(y[k+1]-y[k-1])/(y[-1]-y[0])
	                    dis1.append(distance1);dis2.append(distance2)
	            dis1.append(100001);dis2.append(100001)
	            crow=[]
	            x_index=x_index.tolist()
	            y_index=y_index.tolist()
	            for m in range(len(sig)):
	                index1,index2=x_index.index(m),y_index.index(m)
	                cro=dis1[index1]+dis2[index2]
	                crow.append(cro)
	            crowd.append(crow)
	            index=np.array(crow).argsort()
	            for n in range(len(index)):     #拥挤度排列并取出
	                clo[n]=sig[index[n]]
	            for o in range(len(clo)-1,-1,-1):
	                crowder.append(clo[o])

	        else:
	            crowder.append(front[i][0])
	            crowd.append([1])
	    return front,crowd,crowder
	def draw_change(self,fit_every):
		plt.figure()
		font1={'weight':'normal','size':22}
		legend=[['最小完工时间','平均完工时间','最大完工时间'],['最小负荷','平均负荷','最大负荷']]
		title=['完工时间变化图','机器负荷变化图']
		for i in range(2):
			plt.subplot(1,2,i+1)
			x=[fit_every[i][j][0] for j in range(len(fit_every[i]))]
			y=[fit_every[i][j][1] for j in range(len(fit_every[i]))]
			z=[fit_every[i][j][2] for j in range(len(fit_every[i]))]
			plt.plot(fit_every[3],x,c='black',linestyle='-')                                                  
			plt.plot(fit_every[3],y,c='black',linestyle='--')
			plt.plot(fit_every[3],z,c='black',linestyle='-')
			plt.xlabel('迭代次数',font1)
			plt.title(title[i],font1)
			plt.legend(legend[i],fontsize=18)
			plt.tick_params(labelsize = 18)
		plt.show()
	def draw_2d(self,pareto):
		fig = plt.figure('Pareto最优解')
		x=[pareto[i][0] for i in range(len(pareto))]
		y=[pareto[i][1] for i in range(len(pareto))]
		plt.scatter(x,y,c='red',s=20)
		plt.xlabel('完工时间')
		plt.ylabel('最大机器负荷')
		plt.title("Pareto最优解")
		plt.show()

