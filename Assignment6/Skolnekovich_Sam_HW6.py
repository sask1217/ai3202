# Sam Skolnekovich
# 10/28/15
# HW6


import getopt, sys

class node():
	def __init__(self,name):
		self.setval=0
		self.conditions={}
		self.name="None"
		self.children=[]
		self.parents=[]

cnode=node("Cancer Node")
snode=node("Smoking Node")
pnode=node("Pollution Node")
xnode=node("X-Ray Node")
dnode=node("Dyspnoe Node")
	
	# pol low=.9 smoking=true=.3
	
pnode.setval=.9
snode.setval=.3
	
cnode.parents.append(pnode)
cnode.parents.append(snode)
xnode.parents.append(cnode)
dnode.parents.append(cnode)
	
pnode.children.append(cnode)
snode.children.append(cnode)
cnode.children.append(xnode)
cnode.children.append(dnode)
	
dnode.conditions["c"] = 0.65
dnode.conditions["~c"] = 0.3
	
xnode.conditions["c"] = 0.9
xnode.conditions["~c"] = 0.2
	
cnode.conditions["ps"] = 0.03
cnode.conditions["sp"] = 0.03
cnode.conditions["~ps"] = 0.05
cnode.conditions["s~p"] = 0.05
cnode.conditions["~p~s"] = 0.02
cnode.conditions["~s~p"] = 0.02
cnode.conditions["p~s"] = 0.001
cnode.conditions["~sp"] = 0.001
	
def setprior(a,value):
	if a == 'P':
		pnode.setval = value
		#pollution is low equals value
	elif a == 'S':
		snode.setval=value
		#smoking true=value
		
def calcMarginal(arg):
		a=arg
		if(arg[0] == '~'):
			a=arg[1]
		if a=='P' or a=='p':
			marginal=pnode.setval
		if a=='S' or a=='s':
			marginal=snode.setval
		if a=='C' or a=='c':
			#print(cnode.conditions["ps"],cnode.conditions["~ps"],cnode.conditions["p~s"],cnode.conditions["~p~s"])
			#marginal= (cnode.conditions["ps"]*pnode.setval*snode.setval)+(cnode.conditions["~ps"]*(1-pnode.setval)*(snode.setval))+(cnode.conditions["s~p"]*(snode.setval)*(1-pnode.setval))+(cnode.conditions["~p~s"]*(1-pnode.setval)*(1-snode.setval))
			marginal=(cnode.conditions["ps"]*pnode.setval*snode.setval) + (cnode.conditions["~ps"]*(1-pnode.setval)*(snode.setval)) + (cnode.conditions["p~s"]*pnode.setval*(1-snode.setval))+ (cnode.conditions["~p~s"]*(1-pnode.setval)*(1-snode.setval))
		if a=='X' or a=='x':
			cnode.setval=(cnode.conditions["ps"]*pnode.setval*snode.setval) + (cnode.conditions["~ps"]*(1-pnode.setval)*(snode.setval)) + (cnode.conditions["p~s"]*pnode.setval*(1-snode.setval))+ (cnode.conditions["~p~s"]*(1-pnode.setval)*(1-snode.setval))
			marginal= xnode.conditions["c"]*cnode.setval+xnode.conditions["~c"]*(1-cnode.setval)
		elif a=='D' or a=='d':
			cnode.setval=(cnode.conditions["ps"]*pnode.setval*snode.setval) + (cnode.conditions["~ps"]*(1-pnode.setval)*(snode.setval)) + (cnode.conditions["p~s"]*pnode.setval*(1-snode.setval))+ (cnode.conditions["~p~s"]*(1-pnode.setval)*(1-snode.setval))
			marginal= dnode.conditions["c"]*cnode.setval+dnode.conditions["~c"]*(1-cnode.setval)
		if(arg[0]=='~'):
			return 1-marginal	
		else:
			return marginal

	
def jointParser(arg):
	
	jointVarList = []
	newArg = ""
	argLength = len(arg)
	i = 0
	#print("1st")
	while (i < argLength):
		if arg[i] == "~":
			i = i + 1
		newArg = newArg + arg[i].lower()
		i = i + 1
	length = len(newArg)
	for i in range(0, length):
		newVar = []
	#	print("2nd")
		if len(jointVarList) == 0:
			newVar.append(newArg[i])
			newVar.append("~" + newArg[i])
	#		print("3rd")
		else: 
		    for var in jointVarList:
			    newVar.append(var + newArg[i])
	#		    print("4th")
			    newVar.append(var + "~" + newArg[i])
		jointVarList = newVar
	return jointVarList
		

def calcJointDistribution(arg):
	p=1
	length=len(arg)
	i=0
	arglist = jointParser(arg)
	probs = {}
	if arg in arglist:
		while (i < length):
			
			if arg[i] == "~":
				i = i + 1
				newArg = "~" + arg[i]
				p = p * calcConditional(newArg, arg[i+1:])
			else:
				p = p * calcConditional(arg[i], arg[i+1:])
			i = i + 1
		return p
	else:
		for elements in arglist:
			i=0
			while (i < length):
				if arg[i] == "~":
					
					i = i + 1
					newArg = "~" + arg[i]
					p = p * calcConditional(newArg, arg[i+1:])
				else:
					p = p * calcConditional(arg[i], arg[i+1:])
				i = i + 1	
				probs[elements]=p		
		return probs

def calcConditional(arg, cons):
	c=0
	if arg[0] == '~':
		newArg = arg[1]
	else:
		newArg = arg
	conlist = jointParser(cons)
	
	if newArg == "p":
		node =pnode
	elif newArg == "s":
		node = snode
	elif newArg == "c":
		node = cnode
	elif newArg == "x":
		node = xnode
	elif newArg == "d":
		node = dnode
	else:
		print("Argument not found")
	
	if (len(conlist) == 0):
		return calcMarginal(arg)
	if cons in cnode.conditions:
		c = cnode.conditions[con]
		print("hi")
	elif cons in dnode.conditions:
		c=dnode.conditions[con]
		print("2", dnode.conditions[con])
	elif cons in xnode.conditions:
		c=xnode.conditions[con]
		print("3")
	else:
		c = calcCondition(node, conList[0])
	'''elif (len(conList) == 3):
		c = calcCondThree(arg, conList)
		print("6")'''
	
	if arg[0]=='~':
		return 1 - c
	else:
		print("c",c)
		return c
# could not implement conditional calculations for the joint distributions. Exceeding recursion limit.
# con1 and con2 are not returning, need to set it up for more cases and lengths of cons
'''def calcCondition(node, cons):
	if cons[0] == "~":
		con = cons[1]
	else:
		con = cons
	arg = node.name
	if arg == "p" or arg == "s":
		if con == "p" or con == "s":
			return calcMarginal(network, arg)
		elif con == "c":
			return (calcConditional(cons, arg)*calcMarginal(arg))/calcMarginal(cons)
		elif con == "d" or con == "x":
			con1 = calcConditional(arg, "c")*calcConditional("c", con)
			con2 = calcConditonal(arg, "~c")*calcConditional("~c", con)
			return 
	elif arg == "c":
		if con == "p":
			
			return calcConditional(arg, cons+"s")*calcMarginal("s") + calcConditional(arg, cons + "~s")*calcMarginal("~s")
	#return con1+con2 and con1 and con1,2,3 [argument cases]
	'''


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print (str(err)) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print ("flag", o)
			print ("args", a)
			print (a[0])
			print (float(a[1:]))
			setprior(a[0], float(a[1:]))
		
		elif o in ("-m"):
			print ("flag", o)
			print ("args", a)
			print (type(a))
			print(calcMarginal(a))
		
		elif o in ("-g"):
			print ("flag", o)
			print ("args", a)
			print (type(a))
			p = a.find("|")
			print (a[:p])
			print (a[p+1:])
			calcConditional(a[:p], a[p+1:])
		
		elif o in ("-j"):
			print ("flag", o)
			print ("args", a)
			print(calcJointDistribution(a))
			
		else:
			assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()




'''
'Resources:
'Had trouble with the jointParser so I used this:
'https://github.com/jepetty/ai3202/blob/master/Assignment6/Bayes.py
'
'''
