#c=input("Newline character? (should be known while compiling)")
STYLE_ERROR="\033[31m"
STYLE_INPUT="\033[33m\033[1m"
STYLE_SUCCESS="\033[32m"
CLEAR="\033[0m"
from time import time
while True:
  try:
    a=int(input(STYLE_INPUT+"Allot size? "+CLEAR))
    if a<0:
      print(STYLE_ERROR,"Cannot allocate a negative number of variables.",CLEAR)
    else:
      break
  except:
    print(STYLE_ERROR,"What you entered wasn't a number.",CLEAR)
    
while True:
  try:
    with open(input(STYLE_INPUT+"Compiler output file? "+CLEAR)) as f:
      code=f.read()
    break
  except OSError as e:
    print(STYLE_ERROR,"Failed to open file, please try again",CLEAR)
    print(STYLE_ERROR,"Reason:",e,CLEAR)

code=code.split("\n")
pointer=0#Instruction Pointer
memory=[None]*a#Allot passing will be done in the future :)
rstack=[]#Return stack, for jsr and rtn
vstack=[]#Value stack, now merged with the return stacks
#Next up: Unify the rest of the stacks into one unified stack
keys={'0':0,'1':1,'2':2,'3':3,
      '4':4,'5':5,'6':6,'7':7,
      '8':8,'9':9,'a':10,'b':11,
      'c':12,'d':13,'e':14,'f':15}
import math
EXEC_TIMER=time()
def strlit(s):
  S=""
  for i in range(0,len(s)-1,2):
    c=keys[s[i]]*16+keys[s[i+1]]
    S+=chr(c)
  return S
#encountered=set()
def run(token):
  #encountered.add(token)
  #return
  global pointer,memory,rstack,vstack,vstack
  if token=="-u":
    vstack.append(-vstack.pop())
  if token=="jmp":
    pointer=vstack.pop()-1
  if token=="jsr":
    rstack.append(pointer)
    pointer=vstack.pop()-1
  if token=="rtn":
    pointer=rstack.pop()
  if token=="<=":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0<=arg1)
  if token==">=":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0>=arg1)
  if token=="<":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0<arg1)
  if token==">":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0>arg1)
  if token=="==":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0==arg1)
  if token=="!=":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0!=arg1)
  if token=="+":
    arg1=vstack.pop()
    arg0=vstack.pop()
    try:
      vstack.append(arg0+arg1)
    except:
      vstack.append(str(arg0)+str(arg1))
  if token=="-":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0-arg1)
  if token=="*":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0*arg1)
  if token=="/":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0/arg1)
  if token=="//":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0//arg1)
  if token=="%":
    arg1=vstack.pop()
    arg0=vstack.pop()
    vstack.append(arg0%arg1)
  if token=="swap":
    arg0=vstack.pop()
    arg1=vstack.pop()
    vstack.append(arg0)
    vstack.append(arg1)
  if token=="?":
    vstack.append(memory[vstack.pop()])
  if token=="=":
    arg1=vstack.pop()
    arg0=vstack.pop()
    memory[arg0]=arg1
  if token=="isf":
    if(not vstack.pop()):
      pointer+=1
  if token=="invoke":
    op=vstack.pop()
    if op=="print":
      print(vstack.pop())
    if op=="input":
      vstack.append(input(vstack.pop()))
    if op=="int":
      vstack.append(int(vstack.pop()))
    if op=="float":
      vstack.append(float(vstack.pop()))
    if op=="str":
      vstack.append(str(vstack.pop()))
    if op=="round":
      vstack.append(round(vstack.pop()))
    if op=="log":
      vstack.append(math.log(vstack.pop(),10))
def handle(token):
  global vstack
  if len(token)==0:
      return
  if token[0]=='"':
    #String literal
    vstack.append(strlit(token[1:]))
  elif token[0]=='f':
    #Floating-point literal
    vstack.append(float(token[1:]))
  elif token[0] in "0123456789":
    #Integer literal
    vstack.append(int(token))
  else:
    #Command token
    run(token)
while pointer<len(code):
  line=code[pointer]
  #(line)
  line=line.split(" ")
  #print("Line:",line)
  for token in line:
    handle(token)
    #print("T:",token,"S:",vstack)
  pointer+=1
EXEC_TIMER=(time()-EXEC_TIMER)*1000
print(STYLE_SUCCESS,"Execution successful in",f"{EXEC_TIMER:.3f}","ms",CLEAR)
try:
  input("Press any key to continue... (or press Ctrl+C)")#pause a little bit
except:
  exit()
