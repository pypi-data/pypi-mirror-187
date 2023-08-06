import csv
import pandas as pd
import os




def wr_csv(name,data):
	''' this fonction for writ in csv file 
	ex: wr_csv(boudaoud.csv,['kami',99]) '''

	with open(name,'a+',newline='') as f:

		writer = csv.writer(f)
		writer.writerow(data)



def cr_csv(name,colum):
	'''this fonction for creation csv files 
	 ex : cr_csv('boudaoud.csv',['name','age','date']) '''
	data = pd.DataFrame(columns=colum)
	data.to_csv(name,index=False)



def Serch_PR(name,colon,ser,ind=0):
	''' this for serch in csv (name of fille ,name of colon, serche text ,ind=0 this is for return result'''
	bb = list(pd.read_csv(name + '.csv')[colon])
	n = 0
	nr = []
	for i in bb:
		if ser in i.split():
			nr.append(n)
			
		n += 1
		
	for i in nr:
		yield(pd.read_csv(name + '.csv').iloc[i,ind])


def norp(sect,vale,data):# this giv me resulte no repeted and sum values ex : norp(['kam','kam','do'],[5,5,3]) outp : ['kam','do'],[10,3]
	'''
	هذه الدالة تعمل مع البانداس دات تقوم بإستقبال الداتا و المحاور و القيم ثم تقوم بغربلة النتائج و إرجاعها غير متكررة مع جمع القيم الخاصة بالمحاور
	ex :
		df = pd.read_csv('kkkd.csv')
		norp('section','values',df)
		
		res : ['nono','kami'],[4,3]
	'''
	se = list(set(data[sect]))
	va = []
	for i in se:
		x = data[data[sect] == i]
		su = sum(list(x[vale]))
		va.append(su)
	return se, va
	
	
def GenL(arg):                   #  هذه الدالة تقوم بإنشاء تقوم بإستقبال عدة ليستات و إنشاء ليست جديد
	
	n = 0                           #   for exampel: x = GenL([9,0],[1,2])  rusult :  [[9,1],[0,2]]
	s = []
	x = []                                # هذه الدالة نحتاجها في برامج الدالذكاء الصناعي
	for s in range(len(arg[0])):
		
		s = []
		
		for i in arg:
			
			x.append(i[n])
			
		n += 1
		s.append(x)
		k = s[0]
		r = []
	d = list()
	t1 = 0
	t = len(arg) 
	for i in range(len(arg[0])):
		d.append(x[t1:t])
		t1 += len(arg)
		t += len(arg)
	return d




def RemRep_csv(name,ro,stat='rm',colname='non',newdata='no'):# this for remove or replace data in csv files
	''' 
		this for remove or replace data
			stat remove by default !!
		ex :
			RemRep_csv('bouda.csv',8)
			to replace :
			RemRep_csv('bouda.csv',8,rp,'age',90)
	'''
	ch = pd.read_csv(name)

	column = list(ch)
	mylist = []
	newlist = []
	for i in column:
		mylist.append(list(ch[i]))
		
	if stat == 'rm':
		for i in mylist:
			#newlist.append(i.remove(i[ro]))
			i.remove(i[ro])
			newlist.append(i)
			
	if stat == 'rp':
		n = 0
		for i in mylist:
			
			if n == column.index(colname):
				i.remove(i[ro])
				i.insert(ro,newdata)
				newlist.append(i)
				
			else:
				newlist.append(i)
			n += 1
	
	
	os.system(f'rm {name}')		
	mycsv = pd.DataFrame(columns=column,data=GenL(newlist))
	mycsv.to_csv(name,index=False)

def RemAll_csv(name):# htis for remove all csv file
	
	kk = pd.read_csv(name)
	p = kk.shape

	pr = p[0]
	for i in range(pr):
		RemRep_csv(name,0)
		

	





if __name__ == '__main__':




	print('good')
	

