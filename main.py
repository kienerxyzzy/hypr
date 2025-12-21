#WARNING! This interpreter has been deprecated,
#and will only run Hypr 1.0 files.
#Use the compiler and executor for a (way) better experience.
import another_lexer
import debracer
import pproc

def handle(C,V):
  T=another_lexer.tokenise(C)
  T=pproc.post_tokenisation(T)
  T=debracer.parse(T,V)
  return T[1]


"""
PLANNED FEATURES
print ... (strings were unified into code)
jmp ... (haha)
jsr ...
rtn
push ... / pop ... /invoke
(function stuff)
goal: make cursed programming language
that treates assignments as if they were operators
yes, "=" is an operator, and so is "=="
planned:
if/then/else
temporary if: if <COND> then <CODE> yes
"""

with open("hworld.txt") as f:
  code=f.read()
#load file above
#V=pproc.get_vars(another_lexer.tokenise(code))
V=[]
#VL=[]
code=code.replace(";","\n").split("\n")
labels=dict()
for i in range(len(code)):
  temp=code[i]
  if((_:=temp.find("#"))!=-1):
    temp=temp[:_]
  code[i]=temp
code=[line for line in code if line != '']
for i in range(len(code)):
  temp=code[i]
  if len(temp)>0 and temp[0]=="@":
    labels[temp[1:]]=i
    code[i]=""
stack=[]#shared stack for coprocs and args
rstack=[]#independent stack for control flow
cp=0
variables=dict()
from random import random
#for var in V:
#  variables[var]=None
def interpret(line,where):
  
  global cp,stack
  temp=line.split()
  if len(temp)==0:
    return
  arg=" ".join(temp[1:])
  if temp[0]=="var":
    variables[arg]=None
    V.append(arg)
  #print("INTERPRETING",line)
  
  #print("At line",where,end=": ")
  #if temp[0]=="print":
  #  argp=handle(arg,V).calc()
  #  #print("Print",argp)
  #  print(argp)
  elif temp[0]=="push":
    argp=handle(arg,V).calc()
    #print("Print",argp)
    stack.append(argp)
  elif temp[0]=="pop":
    if len(stack)>0:
      variables[arg]=stack.pop()
    else:
      raise Exception("attempting to pop from null stack")
  elif temp[0]=="invoke":
    op=arg;#The Preprocessor Method!
    if(op=="print"):
      print(stack.pop())
    elif(op=="input"):
      stack.append(input(stack.pop()))
    elif(op=="rand"):
      stack.append(round(random()*stack.pop()))
    elif(op=="int"):
      stack.append(int(stack.pop()))
    elif(op=="float"):
      stack.append(float(stack.pop()))
      
  elif temp[0]=="jmp":
    argp=labels[arg[1:]]
    #print("Jump to",argp)
    cp=argp
  elif temp[0]=="jsr":
    argp=labels[arg[1:]]
    #print("JSRing to",argp)
    rstack.append(cp)
    cp=argp
  elif temp[0]=="rtn":
    #print("Returning from Subroutine")
    cp=rstack.pop()
  elif temp[0]=="if":
    then=temp.index("then")
    cond=handle(" ".join(temp[1:then]),V).calc()
    run=" ".join(temp[then+1:])
    #print("If",cond,"Then: ")
    if cond:
      interpret(run,cp)
  else:
    argp=handle(line,V).calc()
    #print("Running",argp)
def calcbn(S,show=False):
  global variables
  if(S.isvar and not show):
    return variables[S.val]
  else:
    return S.val
def isnum(a):
  return type(a) in [int,float]
def calcop(S,show=False):
  global variables
  op=S.op
  args=S.arg
  for i in range(len(args)):
    args[i]=args[i].calc(i==0 and S.op=="=")
  if(op=="+"):
    if len(args)==2:
      if(isnum(args[0]) and isnum(args[1])):
        return args[0]+args[1]
      else:
        return str(args[0])+str(args[1])
  if(op=="-"):
    if len(args)==2:
      if(isnum(args[0]) and isnum(args[1])):
        return args[0]-args[1]
    elif len(args)==1:
      if(isnum(args[0])):
        return -args[0]
  if(op=="*"):
    if(isnum(args[1])):
      return args[0]*args[1] #string * number
  if(op=="/"):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]/args[1]
  if(op=="//"):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]//args[1]
  if(op=="%"):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]%args[1]
  if(op==">"):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]>args[1]
  if(op=="<"):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]<args[1]
  if(op==">="):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]>=args[1]
  if(op=="<="):
    if(isnum(args[0]) and isnum(args[1])):
      return args[0]<=args[1]
  if(op=="=="):
    return args[0]==args[1]
  if(op=="!="):
    return args[0]!=args[1]
  if(op=="="):
    #print("Set",args[0],"To",args[1])
    variables[args[0]]=args[1]
    return
  raise TypeError('Operator "'+op+'" doesn\'t exist for types ['+", ".join([str(type(i)) for i in args])+']')
debracer.BaseNode.calc=calcbn
debracer.OpNode.calc=calcop
while cp<len(code):
  interpret(code[cp],cp)
  cp+=1
  


