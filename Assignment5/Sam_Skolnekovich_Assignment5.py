# Sam Skolnekovich
# HW5 
# 10/07/15
'''
' Calculating this with different values for error changes the program a great deal. 
' This program is set to break for suboptimal solutions.
' Some of the nodes will act as sinks for the print function and will cause a never ending loop.
' To fix for finding suboptimal solutions you could keep track of nodes visited and unvisited.
' For World1MDP, keep e less then 16, After this it takes a step up rather then right at the startnode.
' It then gets caught in a sink between 3,7 and 2,7
'''


from sys import argv


script, filename, err = argv

txt = open(filename)
rows=0
cols=0
i=0
j=-1
#print(txt.read())



class node():
	def __init__(self,node,locationx,locationy,utility,parentnode,value,reward, adj,visited,delta,pastutil):
		self.node=node
		self.locationx=locationx
		self.locationy=locationy 			
		self.utility=utility				
		self.parentnode=parentnode #unused*
		self.reward=reward	
		self.value=value		
		self.adj=adj		#unused A*		
		self.visited=False  #unused A*
		self.delta=10000
		self.pastutil=pastutil #unused




	



with open(filename) as txt:
	for line in txt:
		line=line.strip()
		items=line.split(' ')
		for value in items:
			cols=cols+1
		rows=rows+1
rows=rows-1
cols=cols-1
cols=round(cols/rows)


allnodes=[[0 for x in range(rows)] for y in range(cols)]
currentnode=[]

with open(filename) as txt:
	for line in txt:
		line=line.strip()
		items=line.split(' ')
		i=0
		j=j+1
		for value in items:
			if(j<=rows-1 and i<=cols-1):
				allnodes[i][j]=node(None,i,j,0,None,value,None,None,None,10000,0)
			i=i+1


def calcUtility(err):
	maxdelta=100000
	pastUtil=0
	currUtil=0
	delta=0
	
	error=float(err)
	error=error/9
		
	while maxdelta>error:
		maxdelta=0
		allnodes[cols-1][0].reward=float(allnodes[cols-1][0].value)
		
		for y in range(rows):
			for x in range(cols):
				pastUtil=allnodes[x][y].utility
				if(allnodes[x][y].value!='2'): # if its a wall, set its utility very low and skip the rest
			
					if (allnodes[x][y].value=='0'):
						allnodes[x][y].reward = -1 # my function works optimally when there is a negative living reward
					
				
					if(allnodes[x][y].value=='1'):
						allnodes[x][y].reward=-2
				
					if(allnodes[x][y].value=='3'):
						allnodes[x][y].reward=-3
				
					if(allnodes[x][y].value=='4'):
						allnodes[x][y].reward=0
				
				
					if(y+1<rows and allnodes[x][y+1].value!='2'):
						if(x-1>=0 and allnodes[x-1][y].value!='2' and x+1>cols):
							if(x+1<cols and allnodes[x+1][y].value!='2'):
																	#DOWN						left						right
								u1=allnodes[x][y].reward+(.8*float(allnodes[x][y+1].utility)+.1*float(allnodes[x-1][y].utility)+.1*float(allnodes[x+1][y].utility))
						
							else:
							#u1 now has .1 chance of staying in the same spot 
							#and get rid of right chance since this is a case where you hit a wall or are out of bounds
								u1=allnodes[x][y].reward+(.8*float(allnodes[x][y+1].utility)+.1*float(allnodes[x-1][y].utility))
						else:
						
						#u1 equals .9 get rid of left chance 
							if(x+1>=cols or allnodes[x][y].value=='2'):
								u1=allnodes[x][y].reward+.8*allnodes[x][y+1].utility
							else:
								u1=allnodes[x][y].reward+.8*allnodes[x][y+1].utility+.1*allnodes[x+1][y].utility
					else:	
					
						u1=-10000000		
					#u1 is not possible
				
					if(x-1>=0 and allnodes[x-1][y].value!='2'):
						if(y+1<rows and allnodes[x][y+1].value!='2'):
							if(y-1>=0 and allnodes[x][y-1].value!='2'):
								u2=allnodes[x][y].reward+(.8*float(allnodes[x-1][y].utility)+.1*float(allnodes[x][y-1].utility)+.1*float(allnodes[x][y+1].utility))
							else:
							
								u2=allnodes[x][y].reward+(.8*float(allnodes[x-1][y].utility)+.1*float(allnodes[x][y+1].utility))
						else:
						
							if(y-1<0 or allnodes[x][y-1].value=='2'):
								u2=allnodes[x][y].reward+.8*allnodes[x-1][y].utility
							else:
								u2=allnodes[x][y].reward+(.8*float(allnodes[x-1][y].utility)+.1*float(allnodes[x][y-1].utility))
					else:	
					
						u2=-10000000		
				
					if(x+1<cols and allnodes[x+1][y].value!='2'):
						if(y+1<rows and allnodes[x][y+1].value!='2'):
							if(y-1>=0 and allnodes[x][y-1].value!='2'):
								u3=allnodes[x][y].reward+(.8*float(allnodes[x+1][y].utility)+.1*float(allnodes[x][y-1].utility)+.1*float(allnodes[x][y+1].utility))
							else:
							
								u3=allnodes[x][y].reward+(.8*float(allnodes[x+1][y].utility)+.1*float(allnodes[x][y+1].utility))
						else:
					
							if(y-1<0 or allnodes[x][y-1].value=='2'):
								u3=allnodes[x][y].reward+.8*allnodes[x+1][y].utility
							else:
								u3=allnodes[x][y].reward+(.8*float(allnodes[x+1][y].utility)+.1*float(allnodes[x][y-1].utility))
					else:	
					
						u3=-10000000							
												
					if(y-1>=0 and allnodes[x][y-1].value!='2'):
						if(x-1>=0 and allnodes[x-1][y].value!='2'):
							if(x+1<cols and allnodes[x+1][y].value!='2'):
								u4=allnodes[x][y].reward+(.8*float(allnodes[x][y-1].utility)+.1*float(allnodes[x-1][y].utility)+.1*float(allnodes[x+1][y].utility))
							else:
							
								u4=allnodes[x][y].reward+(.8*float(allnodes[x][y-1].utility)+.1*float(allnodes[x-1][y].utility))
						else:
						
							if(x+1>=cols or allnodes[x+1][y].value=='2'):
								u4=allnodes[x][y].reward+.8*allnodes[x][y-1].utility
							else:	
								u4=allnodes[x][y].reward+(.8*float(allnodes[x][y-1].utility)+.1*float(allnodes[x+1][y].utility))
					else:	
					
						u4=-10000000
		
					allnodes[x][y].utility=.9*max(u1,u2,u3,u4)
					currUtil=allnodes[x][y].utility
					delta=abs(currUtil-pastUtil)
					
					if(allnodes[x][y].value=='50'):
						allnodes[x][y].utility=50
						allnodes[x][y].delta=0
					
					if(delta<allnodes[x][y].delta):
						allnodes[x][y].delta=delta
					if(allnodes[x][y].delta>maxdelta):
						maxdelta=delta
					
					
					if(allnodes[x][y].value=='50'):
						allnodes[x][y].utility=50
						allnodes[x][y].delta=0
					
				else:
					allnodes[x][y].utility=-10000000
					
	printTest()

def printTest():
	#this lets you see a map of all the utilities
	'''for y in range(rows):
		for x in range(cols):
			print(round(allnodes[x][y].utility,2),end=' ')
			if(x==9):
				print('\n')'''
	currentnode=allnodes[0][rows-1]
	print(currentnode.locationx,currentnode.locationy,round(currentnode.utility,2))
	#i=0
	while currentnode.locationx != allnodes[cols-1][0].locationx or currentnode.locationy != allnodes[cols-1][0].locationy:
		
		x=currentnode.locationx
		y=currentnode.locationy
		if(x-1>=0):
			p1=allnodes[x-1][y].utility
		else:
			p1=-1000000
		
		if(x+1<cols):	
			p2=allnodes[x+1][y].utility			
		else:
			p2=-1000000
		
		if(y+1<rows):
			p3=allnodes[x][y+1].utility
		else:
			p3=-1000000
		
		if(y-1>=0):
			p4=allnodes[x][y-1].utility
		else:
			p4=-100000
		
		Max=max(p1,p2,p3,p4) # find value next to current node that has max utility. calc this after utilites have been calculated
		if(Max==p1):
			currentnode=allnodes[x-1][y]
		if(Max==p2):
			currentnode=allnodes[x+1][y]
		if(Max==p3):
			currentnode=allnodes[x][y+1]
		if(Max==p4):
			currentnode=allnodes[x][y-1]
		print(currentnode.locationx,currentnode.locationy,round(currentnode.utility,2))
		


calcUtility(err)
