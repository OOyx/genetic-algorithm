
import random
import numpy as np
class nsga_II():
	def __init__(self,generation,popsize,to,oh,work,job_num):
		self.generation=generation                  #迭代次数
		self.popsize = popsize                      # 种群规模
		self.to=to
		self.oh=oh
		self.work=work
		self.job_num=job_num
	def to_MT(self,W1,M1,T1,W2,M2,T2): #把加工机器编码和加工时间编码转化为对应列表，目的是记录工件的加工时间和加工机器
		Ma_W1,Tm_W1,Ma_W2,Tm_W2,WCross=[],[],[],[],[]
		
		for i in range(self.job_num):
			Ma_W1.append([]),Tm_W1.append([]),Ma_W2.append([]),Tm_W2.append([]),WCross.append([]);
		for i in range(W1.shape[1]):
			signal1=int(W1[0,i])
			Ma_W1[signal1].append(M1[0,i]),Tm_W1[signal1].append(T1[0,i]);
			signal2=int(W2[0,i])
			Ma_W2[signal2].append(M2[0,i]),Tm_W2[signal2].append(T2[0,i]);
			index=np.random.randint(0,2,1)[0]
			WCross[signal2].append(index)       #随机生成一个为0或者1的列表，用于后续的机器的均匀交叉
		return Ma_W1,Tm_W1,Ma_W2,Tm_W2,WCross
	def back_MT(self,W1,W2,Ma_W1,Tm_W1,Ma_W2,Tm_W2):  #列表返回机器及加工时间编码
		memory1,memory2=np.zeros((1,self.job_num),dtype=np.int),np.zeros((1,self.job_num),dtype=np.int)
		m1,m2,t1,t2=np.zeros((1,W1.shape[1])),np.zeros((1,W1.shape[1])),np.zeros((1,W1.shape[1])),np.zeros((1,W1.shape[1]))
		for i in range(W1.shape[1]):
			signal1=int(W1[0,i])
			signal2=int(W2[0,i])
			# print(signal1)
			# print(signal2)
			# print(Ma_W1[signal1])
			# print(memory1[0,signal1])
			m1[0,i]=Ma_W1[signal1][memory1[0,signal1]]
			m2[0,i]=Ma_W2[signal2][memory2[0,signal2]]
			t1[0,i]=Tm_W1[signal1][memory1[0,signal1]]
			t2[0,i]=Tm_W2[signal2][memory2[0,signal2]]
			memory1[0,signal1]+=1
			memory2[0,signal2]+=1
		return m1,m2,t1,t2
	def mac_cross(self,Ma_W1,Tm_W1,Ma_W2,Tm_W2,WCross):  #机器均匀交叉
		MC1,MC2,TC1,TC2=[],[],[],[]
		for i in range(self.job_num):     
			MC1.append([]),MC2.append([]),TC1.append([]),TC2.append([]);
			for j in range(len(WCross[i])):
				if(WCross[i][j]==0):  #为0时继承另一个父代的加工机器选择
					MC1[i].append(Ma_W1[i][j]),MC2[i].append(Ma_W2[i][j]),TC1[i].append(Tm_W1[i][j]),TC2[i].append(Tm_W2[i][j]);
				else:                #为1时继承父代的机器选择
					MC2[i].append(Ma_W1[i][j]),MC1[i].append(Ma_W2[i][j]),TC2[i].append(Tm_W1[i][j]),TC1[i].append(Tm_W2[i][j]);
		return MC1,TC1,MC2,TC2
	def job_cross(self,chrom_L1,chrom_L2):       #工序的pox交叉
		num=list(set(chrom_L1[0]))
		np.random.shuffle(num)
		index=np.random.randint(0,len(num),1)[0]
		jpb_set1=num[:index+1]                  #固定不变的工件
		jpb_set2=num[index+1:]                  #按顺序读取的工件
		C1,C2=np.zeros((1,chrom_L1.shape[1]))-1,np.zeros((1,chrom_L1.shape[1]))-1
		sig,svg=[],[]
		for i in range(chrom_L1.shape[1]):#固定位置的工序不变
			ii,iii=0,0
			for j in range(len(jpb_set1)):
				if(chrom_L1[0,i]==jpb_set1[j]):
					C1[0,i]=chrom_L1[0,i]
				else:
					ii+=1
				if(chrom_L2[0,i]==jpb_set1[j]):
					C2[0,i]=chrom_L2[0,i]
				else:
					iii+=1
			if(ii==len(jpb_set1)):
				sig.append(chrom_L1[0,i])
			if(iii==len(jpb_set1)):
				svg.append(chrom_L2[0,i])
		signal1,signal2=0,0             #为-1的地方按顺序添加工序编码
		for i in range(chrom_L1.shape[1]):
			if(C1[0,i]==-1):
				C1[0,i]=svg[signal1]
				signal1+=1
			if(C2[0,i]==-1):
				C2[0,i]=sig[signal2]
				signal2+=1
		return C1,C2
	def nsga_total(self):
		answer=[]
		fit_every=[[],[],[],[]]
		job_init=np.zeros((self.popsize,len(self.work)))
		work_job1,work_M1,work_T1=np.zeros((self.popsize,len(self.work))),np.zeros((self.popsize,len(self.work))),np.zeros((self.popsize,len(self.work)))
		work_job,work_M,work_T=np.zeros((self.popsize,len(self.work))),np.zeros((self.popsize,len(self.work))),np.zeros((self.popsize,len(self.work)))
		for gen in range(self.generation):
			if(gen<1):                      #第一次生成多个可行的工序编码，机器编码，时间编码
				for i in range(self.popsize):
					job,machine,machine_time=self.to.creat_job()
					C_finish,Twork,_,_,_,_=self.to.caculate(job,machine,machine_time)
					answer.append([C_finish,Twork])
					work_job[i],work_M[i],work_T[i]=job[0],machine[0],machine_time[0]

				front,crowd,crowder=self.oh.dis(answer)    #计算分层，拥挤度，种群排序结果
				signal=front[0]
				pareto=np.array(answer)[signal].tolist()
				pareto_job,pareto_machine,pareto_time=work_job[signal],work_M[signal],work_T[signal]
				x=[pareto[i][0] for i in range(len(pareto))]
				y=[pareto[i][1] for i in range(len(pareto))]
				#z=[pareto[i][2] for i in range(len(pareto))]
				fit_every[3].append(gen)
				fit_every[0].append([min(x),sum(x)/len(x),max(x)])
				fit_every[1].append([min(y),sum(y)/len(y),max(y)])
				#fit_every[2].append([min(z),sum(z)/len(z),max(z)])

			index_sort=crowder
			work_job,work_M,work_T=work_job[index_sort][0:self.popsize],work_M[index_sort][0:self.popsize],work_T[index_sort][0:self.popsize]
			answer=np.array(answer)[index_sort][0:self.popsize].tolist()
			
			answer1=[]
			for i in range(0,self.popsize,2):    #用最优位置进行工序编码的更新
				W1,M1,T1=work_job[i:i+1],work_M[i:i+1],work_T[i:i+1]
				W2,M2,T2=work_job[i+1:i+2],work_M[i+1:i+2],work_T[i+1:i+2]
				Ma_W1,Tm_W1,Ma_W2,Tm_W2,WCross=self.to_MT(W1,M1,T1,W2,M2,T2)
				# print(W1)
				# print(W2)
				W1,W2=self.job_cross(W1,W2)
				# print(W1)
				# print(W2)
				m1,m2,t1,t2=self.back_MT(W1,W2,Ma_W1,Tm_W1,Ma_W2,Tm_W2)       #机器编码矩阵转回

				C_finish,Twork,_,_,_,_=self.to.caculate(W1,m1,t1)
				work_job1[i]=W1[0]  #更新工序编码
				work_M1[i],work_T1[i]=m1[0],t1[0]
				answer1.append([C_finish,Twork])

				C_finish,Twork,_,_,_,_=self.to.caculate(W2,m2,t2)
				work_job1[i+1]=W2[0]  #更新工序编码
				work_M1[i+1],work_T1[i+1]=m2[0],t2[0]
				answer1.append([C_finish,Twork])

			work_job,work_M,work_T=np.vstack((work_job,work_job1)),np.vstack((work_M,work_M1)),np.vstack((work_T,work_T1))
			front,crowd,crowder=self.oh.dis(answer)
			index_sort=crowder
			work_job,work_M,work_T=work_job[index_sort][0:self.popsize],work_M[index_sort][0:self.popsize],work_T[index_sort][0:self.popsize]
			answer=np.array(answer)[index_sort][0:self.popsize].tolist()
			answer1=[]
			for i in range(0,self.popsize,2):
				W1,M1,T1=work_job[i:i+1],work_M[i:i+1],work_T[i:i+1]
				W2,M2,T2=work_job[i+1:i+2],work_M[i+1:i+2],work_T[i+1:i+2]
				Ma_W1,Tm_W1,Ma_W2,Tm_W2,WCross=self.to_MT(W1,M1,T1,W2,M2,T2)

				MC1,TC1,MC2,TC2=self.mac_cross(Ma_W1,Tm_W1,Ma_W2,Tm_W2,WCross)
				m1,m2,t1,t2=self.back_MT(W1,W2,MC1,TC1,MC2,TC2)       #机器编码矩阵转回
				
				C_finish,Twork,_,_,_,_=self.to.caculate(W1,m1,t1)
				work_job1[i]=W1[0]  #更新工序编码
				work_M1[i],work_T1[i]=m1[0],t1[0]
				answer1.append([C_finish,Twork])

				C_finish,Twork,_,_,_,_=self.to.caculate(W2,m2,t2)
				work_job1[i+1]=W2[0]  #更新工序编码
				work_M1[i+1],work_T1[i+1]=m2[0],t2[0]
				answer1.append([C_finish,Twork])

			work_job,work_M,work_T=np.vstack((work_job,work_job1)),np.vstack((work_M,work_M1)),np.vstack((work_T,work_T1))
			answer=answer+answer1
			
			front,crowd,crowder=self.oh.dis(answer) 
			signal=front[0]
			pareto=np.array(answer)[signal].tolist()
			pareto_job,pareto_machine,pareto_time=work_job[signal],work_M[signal],work_T[signal]
			x=[pareto[i][0] for i in range(len(pareto))]
			y=[pareto[i][1] for i in range(len(pareto))]
			fit_every[3].append(gen+1)
			fit_every[0].append([min(x),sum(x)/len(x),max(x)])
			fit_every[1].append([min(y),sum(y)/len(y),max(y)])
			print('算法迭代到了第%.0f次'%(gen+1))
			print(pareto)
		return pareto,pareto_job,pareto_machine,pareto_time,fit_every  #返回pareto解及其编码
