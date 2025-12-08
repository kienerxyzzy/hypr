import another_lexer
import debracer
import pproc
public=True#False is for developers only
def handle(C,V):
  T=another_lexer.tokenise(C)
  T=pproc.post_tokenisation(T)
  T=debracer.parse(T,V)
  return T[1]
while public:
  try:
    with open(input("Input File:")) as f:
      code=f.read()
    break
  except OSError as e:
    print("Failed to open file, please try again")
    print("Reason:")
    print(e)
  except KeyboardInterrupt:
    exit()
if not public:
  with open("sample_programs\\sqrt.phf") as f:
      code=f.read()
V=[]
#VL=[]
slots=dict()#alloted slots
slot_max=0
code=code.replace(";","\n").split("\n")
labels=dict()
for i in range(len(code)):
  temp=code[i]
  if((_:=temp.find("#"))!=-1):
    temp=temp[:_]
  code[i]=temp
  ts=temp.split()
  if(len(ts)>0 and ts[0]=="var"):
    V.append(" ".join(ts[1:]))
    code[i]=""
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
def establish(S):
  global slots,slot_max
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
def cpl(line):
  temp=line.split()
  if line[0]=="@":
    addline(line)
    return
  arg=" ".join(temp[1:])
  if len(temp)==0:
    return
  elif temp[0]=="push":
    argp=handle(arg,V).comp()
    addline(argp+" >s")
  elif temp[0]=="pop":
    addline(establish(arg)+" <s =")
  elif temp[0]=="jmp":
    argp="%"+arg[1:]+"%"
    addline(argp+" jmp")
    #print("Jump to",argp)
  elif temp[0]=="jsr":
    argp="%"+arg[1:]+"%"
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
#label squishing
compiled=compiled.split("\n")
squished=""
si=0
i=0
while i<len(compiled):
  if(len(compiled[i])==0):
    i+=1
    continue
  if(compiled[i][0]=="@"):
    labels[compiled[i][1:]]=si
    i+=1
  squished+=compiled[i]
  squished+="\n"
  i+=1
  si+=1
for label in labels:
  squished=squished.replace("%"+label+"%",str(labels[label]))
squished=[i.strip() for i in squished.split("\n") if i.strip()!=""]
squished="\n".join(squished)
#print(squished)
#c=input("Newline character? (must be one that doesn't exist in your program):")
print("Min Allot Size:",slot_max)
while public:
  try:
    with open(input("Output file?"),"w") as f:
      f.write(squished)
    break
  except OSError as e:
    print("Failed to open file, please try again")
    print("Reason:")
    print(e)
  except KeyboardInterrupt:
    exit()
