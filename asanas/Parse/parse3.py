import re
import contexttest as context
import random
import copy
#import Y

def parse(f, x, l='{', r='}'):
	ll = l*2
	rr = r*2
	slots		= '({0}{0}|{1}{1}|{0}\d*{1})'.format(l, r)
	specials	= '([\&\%?\\\\.[\]()*+\^$!\|])'
	def replace(m):
		return '\\' + m.group(0)
	def expression():
		e = []
		for p in re.split(slots, f):
			print(p)
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == '}}':
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				n = '(.+)'
			else:
				n = re.sub(specials, replace, p)
				print("this is n:", n)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e #adds ^ to the beggining the string e in the middle and $ to the end
		print("this is e:",e)
		return e
	c = context.context()
	if '{}' in f:
		e = expression()
		print("expression", e)
		
		m = re.match(e, x)
		print("this is m:",m)
		if m is not None:
			g = m.groups()
			print("this is g:",g)
			for k, v in enumerate(g):
				c[k] = v
		return c
	else:
		if f == x:
			c[0] = f
	return c

TEST = True

#print(parse("a{}b{}jkls","acb7bjkls"))
#print(parse("a{name}b","acb"))
#print(parse("hello","hello")) #matching just return "dictionary" context with the same thing at key 0



def parse2(f, x, l='{', r='}', forbiddens=''):
	if TEST:
		if False:
			pass
	if TEST:
		if False:
			pass
	def replace(m):
		return '\\' + m.group(0)
	ll = l*2
	rr = r*2
	slots		= '({0}{0}|{1}{1}|{0}\d*{1})'.format(l, r)
	specials	= '([\&\%?\\\\.[\]()*+\^$!\|])'
	specials2	= re.sub(slots, '', f)
	specials3	= re.sub(slots, '', f)+forbiddens
	specials2	= re.sub(specials, replace, specials2)
	specials3	= re.sub(specials, replace, specials3)
	#ctx = Y.C(seen=False)
	def expressions():
		if False:
			n = f.count('{}')#len(list(re.finditer(f, '{}')))
			if TEST: pass
			for i in range(n):
				yield expression(i)
		e0 = expression0()
		e1 = expression(0)
		e2 = expression(1)
		if TEST:
			if False:
				pass
		if TEST:
			if False:
				pass
		yield e0
		yield e1
		yield e2
	def expression0():
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == '}}':
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				n = '((?:.|\n)+)'
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	def expression1(j):
		i = 0
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == '}}':
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				if i == j:
					n = '([^'+specials3+']+)'
				else:
					n = '((?:.|\n)+)'
				i += 1
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	def expression(j):
		i = 0
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == '}}':
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				if i == j:
					n = '([^'+specials3+']+)'
				else:
					n = '((?:.|\n)+)'
				i += 1
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	c = context.context()
	if '{}' in f:
		es = list(expressions())
		
		for e in es:
			ms = re.finditer(e, x)
			for m in ms:
				d = context.context()
				if m is not None:
					g = m.groups()
					for k, v in enumerate(g):
						d[k] = v
					if False:
						pass
					if TEST: pass
					c0 = all(v.count('(')==v.count(')') for k, v in d)
					c1 = all(v.count('[')==v.count(']') for k, v in d)
					if c0 and c1:
						c = d
			if TEST:
				if False:
					pass
					pass
	else:
		if f == x:
			c[0] = f
	return c

def parse3(f, x, l='{', r='}', forbiddens=''):
	if TEST:
		if False:
			pass
	if TEST:
		if False:
			pass
	
	def removeName(f):
		names = []
		output = list(f)
		start = False
		startIndex =0
		for i in range(len(f)):
			if f[i]==r:
				start = False
				names.append("".join(f[startIndex:i]))
			if start==True:
				output[i] = ""
			if f[i]==l:
				start = True
				startIndex = i+1
		f = "".join(output)
		return [f,names]
	
	def replace(m):
		return '\\' + m.group(0)
	ll = l*2
	rr = r*2
	
	slots		= '({0}{0}|{1}{1}|{0}\d*{1})'.format(l, r)
	specials	= '([\&\%?\\\\.[\]()*+\^$!\|])'
	specials2	= re.sub(slots, '', f)
	specials3	= re.sub(slots, '', f)+forbiddens
	specials2	= re.sub(specials, replace, specials2)
	specials3	= re.sub(specials, replace, specials3)
	removeName=removeName(f)
	f= removeName[0]
	names = removeName[1]
	#ctx = Y.C(seen=False)
	def expressions():
		if False:
			lr = l+r
			n = f.count(lr)#len(list(re.finditer(f, '{}')))
			if TEST: pass
			for i in range(n):
				yield expression(i)
		e0 = expression0()
		e1 = expression(0)
		e2 = expression(1)
		if TEST:
			if False:
				pass
		if TEST:
			if False:
				pass
		yield e0
		yield e1
		yield e2
	def expression0():
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == rr:
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				n = '((?:.|\n)+)'
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	def expression1(j):
		i = 0
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == rr:
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				if i == j:
					n = '([^'+specials3+']+)'
				else:
					n = '((?:.|\n)+)'
				i += 1
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	def expression(j):
		i = 0
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == rr:
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				if i == j:
					n = '([^'+specials3+']+)'
				else:
					n = '((?:.|\n)+)'
				i += 1
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	c = context.context()
	lr = l+r
	if lr in f:
		es = list(expressions())
		
		for e in es:
			ms = re.finditer(e, x)
			for m in ms:
				d = context.context()
				if m is not None:
					g = m.groups()
					for k, v in enumerate(g):
						d[k] = v
					if False:
						pass
					if TEST: pass
					#c0 = all(v.count('(')==v.count(')') for k, v in d)
					#c1 = all(v.count('[')==v.count(']') for k, v in d)
					#if c0 and c1:
					#	c = d
					c=d
			if TEST:
				if False:
					pass
					pass
					
		originalLen = c.__len__()
		unamed = 0
		for d in range(originalLen):
			if names[d]!="":
				c.__setattr__(names[d],c.__getitem__(d))
				c.__delattr__(d)
			else:
				item = c.__getitem__(d)
				c.__delattr__(d)
				c.__setattr__(unamed,item)
				unamed +=1
				
	else:
		c =c
		#if f == x:
		#	c[0] = f
	return c

#parser that only does max parsing when there is no contenxt key given 
def parseSpecial(f, x, l='{', r='}', forbiddens=''):
	if TEST:
		if False:
			pass
	if TEST:
		if False:
			pass
	
	def removeName(f):
		names = []
		output = list(f)
		start = False
		startIndex =0
		for i in range(len(f)):
			if f[i]==r:
				start = False
				names.append("".join(f[startIndex:i]))
			if start==True:
				output[i] = ""
			if f[i]==l:
				start = True
				startIndex = i+1
		f = "".join(output)
		return [f,names]
	
	def replace(m):
		return '\\' + m.group(0)
	ll = l*2
	rr = r*2
	
	slots		= '({0}{0}|{1}{1}|{0}\d*{1})'.format(l, r)
	specials	= '([\&\%?\\\\.[\]()*+\^$!\|])'
	specials2	= re.sub(slots, '', f)
	specials3	= re.sub(slots, '', f)+forbiddens
	specials2	= re.sub(specials, replace, specials2)
	specials3	= re.sub(specials, replace, specials3)
	removeName=removeName(f)
	f= removeName[0]
	names = removeName[1]
	#ctx = Y.C(seen=False)
	def expressions():
		if False:
			lr = l+r
			n = f.count(lr)#len(list(re.finditer(f, '{}')))
			if TEST: pass
			for i in range(n):
				yield expression(i)
		e0 = expression0()
		e1 = expression(0)
		e2 = expression(1)
		if TEST:
			if False:
				pass
		if TEST:
			if False:
				pass
		yield e0
		yield e1
		yield e2
	def expression0():
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == rr:
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				n = '((?:.|\n)+)'
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	def expression1(j):
		i = 0
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == rr:
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				if i == j:
					n = '([^'+specials3+']+)'
				else:
					n = '((?:.|\n)+)'
				i += 1
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	def expression(j):
		i = 0
		e = []
		for p in re.split(slots, f):
			n = None
			if not p:
				pass
			elif p == ll:
				n = '\\'+l
			elif p == rr:
				n = '\\'+r
			elif p[0] == l and p[-1] == r:
				if i == j:
					n = '([^'+specials3+']+)'
				else:
					n = '((?:.|\n)+)'
				i += 1
			else:
				n = re.sub(specials, replace, p)
			if n:
				e.append(n)
		e = ''.join(e)
		e = '^%s$' % e
		return e
	c = context.context()
	lr = l+r
	if lr in f:
		es = list(expressions())
		
		for e in es:
			ms = re.finditer(e, x)
			for m in ms:
				d = context.context()
				if m is not None:
					g = m.groups()
					for k, v in enumerate(g):
						d[k] = v
					if False:
						pass
					if TEST: pass
					#c0 = all(v.count('(')==v.count(')') for k, v in d)
					#c1 = all(v.count('[')==v.count(']') for k, v in d)
					#if c0 and c1:
					#	c = d
					c=d
			if TEST:
				if False:
					pass
										
		originalLen = c.__len__()
		unamed = 0
		for d in range(originalLen):
			if names[d]!="":
				dnext = d+1
				itemToAdd = c[d]
				if dnext in c.keys():
					c[dnext] = itemToAdd[1:]+c[dnext]
				itembeingadded = itemToAdd[0]
				c.__setattr__(names[d],itembeingadded)
				c.__delattr__(d)
			else:
				item = c.__getitem__(d)
				c.__delattr__(d)
				c.__setattr__(unamed,item)
				unamed +=1
				
	else:
		c =c
		#if f == x:
		#	c[0] = f
	return c
	
def expectedResult(f,x):
	if f==x:
		return context.context()
	else:
		flist = list(f)
		xlist = list(x)
		i = 0
		names = []
		holes = 0
		locations = []
		while i<len(flist):
			if flist[i]=="{":
				holes +=1
				locations.append("")
				s = i+1
				while (flist[i]!="}" and i<len(flist)):
					i+=1
				e = i
				names.append("".join(flist[s:e]))
				for j in range(s-1,e+1):
					flist[j] =""
			else:
				locations.append(flist[i])
			i+=1
		c = context.context()
		curName = 0
		noNameCount = 0
		for l in range(len(locations)):
			if locations[l] == "":
				if names[curName] == "":
					c.__setattr__(noNameCount, x[l])
					noNameCount+=1
				else: c.__setattr__(names[curName], x[l])
				curName +=1
		return c

def genfx():
	while True:
		l = random.randint(1,10)
		if l//2>1:
			h = random.randint(1,l//2)
		else:
			h=0
		x1 = []
		for a in range(l):
			c =random.randint(32,127)
			while (chr(c)=="{" or chr(c)=="}" or chr(c)=="-" or chr(c)=="\""):
				c = random.randint(32,127)
			x1.append(chr(c))
		f1 = copy.copy(x1)
		names = []
		for b in range(h):
			addname = random.choice([True,False])
			aname = ""
			if addname:
				aname = chr(random.randint(65,91))
				while aname in names:
					aname = chr(random.randint(65,91))
				names.append(aname)
			f1[b*2]="{"+aname+"}"			
		f = "".join(f1)
		x = "".join(x1)
		yield f,x
	
def checker(numofchecks):
	for i in range(numofchecks):
		gen = genfx()
		f,x = next(gen)
		expect = expectedResult(f,x)
		parser = parse3(f,x)
		if expect.keys()==parser.keys():
			for k in expect.keys():
				if expect.__getattr__(k)!=parser.__getattr__(k):
					yield (f,x,expect,parser)
		else:
			yield (f,x,expect,parser)

g = checker(100)
for x in g:
	print(x)
	print("\n")
	
C = context.context
def Debug(*args0,cast=None,active = True):
    i = C(0)
    def h(f):
        
        def g(*args,**kwargs):
            j = i[0]
            i[0]+=1
            depth = 0     
            if "depth" in kwargs:
                depth = kwargs["depth"]
            args1=[(kwargs[arg] if arg in kwargs else None) if(type(arg)!=int) else args[arg] for arg in args0]
            if active:
                print("\t"*depth,j,f.__name__,*args1)
            y = f(*args,**kwargs)
            z = y 
            if cast:
                z = cast(z)
                y = z
            if active:
                print("\t"*depth,j,f.__name__,*args1,z)
            return y 
        return g
    return h


def matchContext(x,y):
	@Debug(0,1,active = False)
	def aux(x,y):
		ok = True
		r = False, C()
		test1 = True
		if type(x)==str:
			c = parse3("[hole{num}]",x)
			if c:
				cc = C()
				cc.hole[int(c.num)] = y
				r = len(c)>0, cc
				test1 = False	
		if test1:
			tx = str(type(x))
			ty = str(type(y))
			if tx==ty:
				if tx==str(type(C())):
					kx = list(x.keys())
					ky = list(y.keys())
					if kx == ky:
						c = C()
						for k in kx:
							#print("start")
							fl,cc = aux(x[k],y[k])
							#print("end")
							if fl:
								c+=cc
							else:
								ok = False
								r =  False, C()
						if ok: r = True,c
					else:
						r = False, C()
				elif type(x)==list:
					
					#if len(x)==len(y):
					if True:
						c = C()
						z = zip(x,y)
						for u,v in z:
							fl,cc = aux(u,v)
							if fl:
								c+=cc
							else:
								ok = False
								r =  False, C()
						if ok: r = True, c
					#else:
				#		er = False, C()
					'''
					else:
						c0 = []
						c = C()
						for u in x:
							for v in y:
								fl,cc = aux(u,v)
								print("cc",cc,fl)
								if fl:
									print("cc c before",c,cc)
									c =cc
									print("cc c",c)
								else:
									ok = False
									r = False,C()
							print("c",c)
						
						if ok: r = True, c
					'''
				
				elif type(x)==str:
					if "{" not in x and "}" not in x:
						r = x==y, C()
					else:
						c = parse3(x,y,"{","}")
						r = len(c)>0,c
			else:
				r = False, C()
		
		return r
	fl, c = aux(x,y)
	return c

def convertToContext(d):
    if type(d)==dict:
        c = context.context()
        for k,v in d.items():
            c[k] = convertToContext(v)
    elif type(d)==list:
        c = []
        for i in d:
            c.append(convertToContext(i))
    else:
        c = d
    return c

'''
x1 = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['(', {'node': 'A', 'subtrees': '[hole0]'}, ')']}, '[hole1]']}, {'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['(', {'node': 'A', 'subtrees': '[hole2]'}, ')']}, '[hole3]']}]}]}]
y1 = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['(', {'node': 'A', 'subtrees': ["[",',',"]"]}, ')']}, '?']}, {'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['(', {'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ["[",'**',"]"]}, {'node': 'A', 'subtrees': ['@']}]}, ')']}, '?']}]}]}]

x1 = convertToContext(x1)
y1 = convertToContext(y1)
print(matchContext(x1,y1))
'''
