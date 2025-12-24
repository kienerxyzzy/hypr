import another_lexer
import debracer
import pproc
import coda_onset
import jsr
from time import time
STYLE_ERROR="\033[31m"
STYLE_INPUT="\033[33m\033[1m"
STYLE_SUCCESS="\033[32m"
CLEAR="\033[0m"
def handle(C,V):
  T=another_lexer.tokenise(C)
  T=pproc.post_tokenisation(T)
  T=debracer.parse(T,V)
  return T[1]
DEV_MODE_NAME=""
DEV_MODE_ENABLE=True
if not DEV_MODE_ENABLE:
  while True:
    try:
      with open(input(STYLE_INPUT+"Input File:"+CLEAR)) as f:
        code=f.read()
      break
    except OSError as e:
      print(STYLE_ERROR,"Failed to open file, please try again",CLEAR)
      print(STYLE_ERROR,"Reason:",e,CLEAR)
else:
  DEV_MODE_NAME=input(STYLE_INPUT+">>"+CLEAR)
  with open("sample_programs\\"+DEV_MODE_NAME+".phf") as f:
    code=f.read()
COMPILE_TIMER=time()
V=[]
#VL=[]
slots=dict()#alloted slots
slot_max=0


#Optional features
if(code[0]=="#"):
  FLAGS=code.split("\n")[0][1:].split(",")
else:
  FLAGS=[]
  
if "legacy10" not in FLAGS:
  code=jsr.fhandle(coda_onset.coda_onset(code))

  
code=code.replace(";","\n").split("\n")
labels=dict()
for i in range(len(code)):
  temp=code[i]
  if((_:=temp.find("#"))!=-1):
    temp=temp[:_]
  code[i]=temp
  ts=temp.split()
  #if(len(ts)>0 and ts[0]=="var"):
  #  V.append(" ".join(ts[1:]))
  #  code[i]=""
code=[line.strip() for line in code if line != '']
def encode(S):
  if type(S) is str:
    S2='"'
    for b in S:
      S2+=hex(256+ord(b)%256)[3:]
    return S2
  elif type(S) is int:
    return str(S)#asis
  elif type(S) is float:
    return "f"+str(S)
  return str(S)
CURRENT_CONTEXT="_"
def addvc(Sr):
  global CURRENT_CONTEXT
  if(Sr[0]!="_"):
    S=CURRENT_CONTEXT+"."+Sr
  else:
    S=Sr
  return S
def establish(Sr):
  global slots,slot_max
  #if S2 ==r
  S=addvc(Sr)
  if S not in slots:
    slots[S]=slot_max
    slot_max+=1
  return str(slots[S])
def compbn(S,show=False):
  
  
  if(S.isvar and not show):
      return establish(S.val)+" ?"
  elif S.isvar:
      return establish(S.val)
  else:
    return encode(S.val)
def compop(S,show=False):
  op=S.op
  args=S.arg
  if op in ["+","-"] and len(args)==1:
    op=op+"u"
  for i in range(len(args)):
    args[i]=args[i].comp(i==0 and op=="=")
  return " ".join([e for e in args])+" "+op
debracer.BaseNode.comp=compbn
debracer.OpNode.comp=compop
compiled=""
def addline(l):
  global compiled
  if len(l)==0:
    return
  compiled+=l
  compiled+="\n"
  #if w:
  #  print(l,"was added from",w)
LABEL_DENOTER="%"
def cpl(line):
  global CURRENT_CONTEXT
  temp=line.split()
  if line[0]=="@":
    addline(line)
    return
  arg=" ".join(temp[1:])
  if len(temp)==0:
    return
  elif temp[0]=="push":
    argp=handle(arg,V).comp()
    addline(argp+"")
  elif temp[0]=="pop":
    addline(establish(arg)+" swap =")
  elif temp[0]=="jmp":
    argp=LABEL_DENOTER+arg[1:]+LABEL_DENOTER
    addline(argp+" jmp")
  elif temp[0]=="context":
    CURRENT_CONTEXT=arg
  elif temp[0]=="var":
    V.append(arg)
    #print("Jump to",argp)
  elif temp[0]=="jsr":
    argp=LABEL_DENOTER+arg[1:]+LABEL_DENOTER
    addline(argp+" jsr")
    #print("JSRing to",argp)
    #cp=argp
  elif temp[0]=="rtn":
    addline("rtn")
    #print("Returning from Subroutine")
    #cp=rstack.pop()
  elif temp[0]=="invoke":
    op=arg;#The Preprocessor Method!
    addline(encode(op)+" invoke")
  elif temp[0]=="if":
    then=temp.index("then")
    cond=handle(" ".join(temp[1:then]),V).comp()
    run=" ".join(temp[then+1:])
    addline(cond+" isf")
    cpl(run)
  else:
    argp=handle(line,V).comp()
    addline(argp)
    #print("Excluding",argp)
    #addline("WORK IN PROGRESS")
for i in range(len(code)):
  line=code[i]
  cpl(line)

#statement squishing
compiled=compiled.split("\n")
squished=[]
temp=""
skip=False
for line in compiled:
  if len(line)==0:
    continue
  arg=line.split()[-1]
  #print("Processing line",line)
  #print("Very Last Token:",arg)
  if line[0]=="@":
    squished.append(temp)#labels cause the immediate termination of a line
    squished.append(line)
    temp=""
  elif arg=="isf":
    squished.append(temp+line)#ISF is the odd one out here
    skip=True
    temp=""
  elif arg in ["jmp","jsr","rtn"] or skip:
    skip=False
    squished.append(temp+line)#ending statements cause the immediate termination of a line
    temp=""
  else:
   temp+=line+" "
squished.append(temp)#clear out any lines we might have had before
#squished=[i.strip() for i in squished]
squished=[i for i in squished if len(i)>0]
#label squishing
compiled=squished
squished=""
si=0
i=0
while i<len(compiled):
  if(len(compiled[i])==0):
    i+=1
    continue
  if(compiled[i][0]=="@"):
    labels[compiled[i][1:]]=si
    #i+=1
  else:
    si+=1
    squished+=compiled[i]
    squished+="\n"
  i+=1
  
for label in labels:
  squished=squished.replace(LABEL_DENOTER+label+LABEL_DENOTER,str(labels[label]))
squished=[i.strip() for i in squished.split("\n") if i.strip()!=""]
squished="\n".join(squished)
#print(squished)
#c=input("Newline character? (must be one that doesn't exist in your program):")
COMPILE_TIMER=(time()-COMPILE_TIMER)*1000
print(STYLE_SUCCESS,"Compilation successful in",f"{COMPILE_TIMER:.3f}","ms",CLEAR)
print(STYLE_SUCCESS,"Min Allot Size:",slot_max,CLEAR)
#open("sample_programs\\"+DEV_MODE_NAME+".phf")
if not DEV_MODE_ENABLE:
  while True:
    try:
      with open(input(STYLE_INPUT+"Output file:"+CLEAR),"w") as f:
        f.write(squished)
      break
    except OSError as e:
      print(STYLE_ERROR,"Failed to open file, please try again",CLEAR)
      print(STYLE_ERROR,"Reason:",e,CLEAR)
    except KeyboardInterrupt:
      exit()
else:
  with open("compiled\\"+DEV_MODE_NAME+".chf","w") as f:
    f.write(squished)
