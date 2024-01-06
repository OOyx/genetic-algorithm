
import numpy as np
from data_solve import data_deal
import random 
import matplotlib.pyplot as plt 
#plt.rcParams['font.sans-serif'] = ['STSong'] 
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文


class FJSP():
	def __init__(self,job_num,machine_num,pi,parm_data):
		self.job_num=job_num     			#工件数
		self.machine_num=machine_num		#机器数
		self.pi=pi  				#随机挑选机器的概率
		self.Tmachine,self.Tmachinetime,self.tdx,self.work,self.tom=parm_data[0],parm_data[1],parm_data[2],parm_data[3],parm_data[4]
	def axis(self):
		index=['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12',
		'M13','M14','M15','M16','M17','M18','M19','M20']
		scale_ls,index_ls=[],[]   
		for i in range(self.machine_num):
			scale_ls.append(i+1)
			index_ls.append(index[i])
		return index_ls,scale_ls  #返回坐标轴信息，按照工件数返回，最多画20个机器，需要在后面添加
	def creat_job(self):
		job=np.copy(self.work)
		np.random.shuffle(job)
		job=np.array(job).reshape(1,len(self.work))
		ccount=np.zeros((1,self.job_num),dtype=np.int)
		machine=np.ones((1,job.shape[1]))
		machine_time=np.ones((1,job.shape[1]))    #初始化矩阵
		for i in range(job.shape[1]):
			oper=int(job[0,i])
			highs=self.tom[oper][ccount[0,oper]]
			lows=self.tom[oper][ccount[0,oper]]-self.tdx[oper][ccount[0,oper]]
			n_machine=self.Tmachine[oper,lows:highs]
			n_time=self.Tmachinetime[oper,lows:highs]
			ccount[0,oper]+=1
			if np.random.rand()>self.pi:     			#选取最小加工时间机器     
				machine_time[0,i]=min(n_time)
				index=np.argwhere(n_time==machine_time[0,i])
				machine[0,i]=n_machine[index[0,0]]
			else:										#否则随机挑选机器								 
				index=np.random.randint(0,len(n_time),1)
				machine[0,i]=n_machine[index[0]]
				machine_time[0,i]=n_time[index[0]]
		return job,machine,machine_time
	def caculate(self,job,machine,machine_time):
		jobtime=np.zeros((1,self.job_num))        
		tmm=np.zeros((1,self.machine_num))   			
		tmmw=np.zeros((1,self.machine_num))			
		startime=0
		list_M,list_S,list_W=[],[],[]
		for i in range(job.shape[1]):
			svg,sig=int(job[0,i]),int(machine[0,i])-1  
			if(jobtime[0,svg]>0):								
				startime=max(jobtime[0,svg],tmm[0,sig])   	
				tmm[0,sig]=startime+machine_time[0,i]
				jobtime[0,svg]=startime+machine_time[0,i]
			if(jobtime[0,svg]==0):							
				startime=tmm[0,sig]
				tmm[0,sig]=startime+machine_time[0,i]
				jobtime[0,svg]=startime+machine_time[0,i]

			tmmw[0,sig]+=machine_time[0,i]
			list_M.append(machine[0,i])
			list_S.append(startime)
			list_W.append(machine_time[0,i])
				       
		tmax=np.argmax(tmm[0])+1		#结束最晚的机器
		C_finish=max(tmm[0])			#最晚完工时间
		trest=tmm-tmmw					#空闲时间
		Twork=max(tmmw[0])                   #机器负荷
		return C_finish,Twork,list_M,list_S,list_W,tmax
	def draw(self,job,machine,machine_time):#画图
		C_finish,Twork,list_M,list_S,list_W,tmax=self.caculate(job,machine,machine_time)    
		figure,ax=plt.subplots()
		count=np.zeros((1,self.job_num))
		for i in range(job.shape[1]):  #每一道工序画一个小框
			count[0,int(job[0,i])-1]+=1
			plt.bar(x=list_S[i], bottom=list_M[i], height=0.5, width=list_W[i], orientation="horizontal",color='white',edgecolor='black')
			plt.text(list_S[i]+list_W[i]/32,list_M[i], '%.0f' % (job[0,i]+1),color='black',fontsize=10,weight='bold')#12是矩形框里字体的大小，可修改
		plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='完工时间=%.1f'% (C_finish))#用虚线画出最晚完工时间
		plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='最大机器负荷=%.1f'% (Twork))
		#plt.plot([C_finish,C_finish],[0,tmax],c='black',linestyle='-.',label='能耗=%.1f'% (E_all))#可以选择显示几个目标，其他的用#号屏蔽

		font1={'weight':'bold','size':22}#汉字字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.title("甘特图",font1)
		plt.ylabel("机器",font1)

		scale_ls,index_ls=self.axis()
		plt.yticks(index_ls,scale_ls)
		plt.axis([0,C_finish*1.1,0,self.machine_num+1])
		plt.tick_params(labelsize = 22)#坐标轴刻度字体大小，可以修改
		labels=ax.get_xticklabels()
		[label.set_fontname('Times New Roman')for label in labels]
		plt.legend(prop={'family' : ['SimHei'], 'size'   : 16})#标签字体大小，可以修改
		plt.xlabel("加工时间",font1)
		plt.show()

