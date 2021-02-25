import inspect
import multiprocessing
import types

TYPE_CONTEXT = 'yoga.core.context.super_context.<locals>.Y.<locals>.X'

def factorize(c):
	r = context()
	def factorize_aux(c, x=[]):
		t = str(type(c))
		if TYPE_CONTEXT in t:
			for k, v in c:
				factorize_aux(v, x+[k])
		else:
			y = tuple(x)
			if y not in r:
				r[y] = []
			r[y].append(c)
	factorize_aux(c)
	return r

def copy(c):
	c0 = context()
	c0.update(c)
	return 0

def flat_context2dict(c):
	d = dict()
	for k, v in c:
		d[k] = v
	return d

def as_context(d, clean=False):
	def aux(dd):
		dt = type(dd)
		if TYPE_CONTEXT in str(dt):
			r = context()
			for k, v in dd:
				w = as_context(v)
				if clean:
					if w is not None:
						r[k] = w
				else:
					r[k] = w
		elif dt in [dict]:
			r = context()
			for k, v in dd.items():
				w = as_context(v)
				if clean:
					if w is not None:
						r[k] = w
				else:
					r[k] = w
		elif dt in [list, tuple]:
			r = context()
			for k, v in enumerate(dd):
				w = as_context(v)
				if clean:
					if w is not None:
						r[k] = w
				else:
					r[k] = w
		else:
			r = dd
		return r
	r = aux(d)
	return r

def dict2context(d, clean=True):
	def aux(dd):
		dt = type(dd)
		if dt in [dict]:
			r = context()
			for k, v in dd.items():
				w = dict2context(v)
				if clean:
					if w is not None:
						r[k] = w
				else:
					r[k] = w
		elif dt in [list, tuple]:
			r = context()
			for k, v in enumerate(dd):
				w = dict2context(v)
				if clean:
					if w is not None:
						r[k] = w
				else:
					r[k] = w
		else:
			r = dd
		return r
	r = aux(d)
	return r

def extend(c0, c1):
	def aux(c0, k, v):
		if str(type(v)) == str(type(c0)):
			for kk, vv in v:
				aux(c0[k], kk, vv)
		else:
			c0[k] = v
	for k, v in c1:
		aux(c0, k, v)

def is_pure_lambda(f):
	if type(f) != types.LambdaType:
		return False
	args = inspect.getargspec(f).args
	return len(args) == 0

def find(d, k):
	r = []
	def aux(d0):
		for k0, v0 in d0.items():
			if k0 == k:
				r.append(v0)
			aux(v0)
	aux(d)
	return r

def super_context(lambda_as_key=False, access=False,listBehavior = True):
	def Y(dd={}, *args, **kwargs):
		d = {}
		d.update(dd)
		class X(object):
			
			def __bool__(self):
				return self.__nonzero__()
			def __call__(self, *args, **kwargs):
				if len(args) == 1:
					k = args[0]
					return self.__getitem__(k)
				else:
					dd = {k: self.__getitem__(k) for k in args}
					return context(dd)
			def __contains__(self, k):
				return k in d
			def __delattr__(self, k):
				if k not in d:
					return
				if listBehavior and type(k)==int:
					values = []
					for kk in self.keys():
						if type(kk) == int and kk>k:
							values.append(d[kk])
					for i in range(len(values)):
						d[k+i] = values[i]
					del d[k+len(values)]
				else:
					del d[k]
						
					
			def __delitem__(self, k):
				self.__delattr__(k)
					
			def __iadd__(self, other):
				extend(self, other)
				return self
			def __init__(self, *args, **kwargs):
				for k, v in enumerate(args):
					d[k] = v
				for k, v in kwargs.items():
					d[k] = v
			def __iter__(self):
				return (x for x in d.items())
			def __getattr__(self, k):
				v = self.__getitem__(k)
				if lambda_as_key:
					if is_pure_lambda(v):
						v = v()
				return v
			def __getitem__(self, k):
				if access:
					r = find(d, k)
					return r
				else:
					if isinstance(k, slice):
						i = k.start
						j = k.stop
						s = k.step
						#ks = xrange(i, j, s)
						ks = range(i, j, s)
						dd = {k:self.__getitem__(k) for k in ks}
						return context(dd)
						"""
						elif isinstance(k, tuple):
							dd = {kk:self.__getitem__(kk) for kk in k}
							return context(dd)
						"""
					else:
						if k not in d:
							self.__setitem__(k, context())
						return d[k]
			def __len__(self):
				return len(d)
			def __nonzero__(self):
				return len(d) > 0
			def __repr__(self):
				return d.__repr__()
			def __setattr__(self, k, v):
				self.__setitem__(k, v)
			def __setitem__(self, k, v):
				if listBehavior:
					if type(k)== int and k not in d.keys():
						pass
					else:
						d[k] = v
				else:
					d[k] = v
				
			def __append__(self,v):
				if listBehavior:
					k = 0
					while self.__contains__(k):
						k+=1
					d[k] = v
					pass
				
			def keys(self):
				return d.keys()
			def values(self):
				return d.values()
				
		return X(*args, **kwargs)
	def Z(*args, **kwargs):
		return Y({}, *args, **kwargs)
	return Z
	#return Y

access	= super_context(False, True, True)
context	= super_context(False, False,False)
listcontext = super_context(False, False,True)
instantContext = context("a","b","c","d")
instantContext2 = context("e","f")
#print(instantContext.__len__())
#print(instantContext)
#print(instantContext.__repr__())

def isContext(value):
	return str(type(value))==str(type(context()))

