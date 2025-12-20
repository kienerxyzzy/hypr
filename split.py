#Stringaware(TM) Splitter
def sasplit(S):
  l=[]
  a=""
  slash=False
  instr=False
  for c in S.strip():
    if(c==" "):
      #Are we inside a string?
      if not instr:
        l.append(a)
        a=""
        continue
    if(c=='\"'):
      if not slash:
        instr=not instr
    slash=(c=="\\")#Update the slash for the next symbol
    a+=c
  l.append(a)
  return l
  
        
  
