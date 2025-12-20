#Overhaul the function system, adding support for variable scoping
#via our favourite friend, THE STACK ! THE STACK ! NANPASTACKEN !
import split
code="""
function test
takes arg1 arg2 arg3
var m n
return result result2

function test2
var m n
call test2 m n m+n
retrieve p q
return

call test2
"""
#Comments must be pre-stripped by the preprocessor engine,
#if not, then we're screwed.
def fhandle(code):
  result="context _\n"
  context=""
  for line in code.split("\n"):
    temp=split.sasplit(line)
    if len(temp)==0:
      continue
    elif temp[0]=="function":
      arg=temp[1]
      context=arg
      result+="context "+arg+"\n"
      result+="@hfun."+arg+"\n"
    elif temp[0]=="takes":
      #Convention:
      #Arguments pushed in  left  -to- right 
      #Arguments popped out right -to- left
      for c in temp[-1:0:-1]:
        result+="var "+c+"\n"
        result+="pop "+c+"\n"
    elif temp[0]=="return":
      for c in temp[1:]:
        result+="push "+c+"\n"
      result+="rtn\ncontext _\n"
    elif temp[0]=="retrieve":
      for c in temp[-1:0:-1]:
        result+="pop "+c+"\n"
    elif temp[0]=="call":
      for c in temp[2:]:
        result+="push "+c+"\n"
      result+="jsr @hfun."+temp[1]+"\n"
    else:
      result+=line+"\n"
  return result
  
