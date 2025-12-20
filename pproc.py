#code="""
#for(var x=0,x<10,x+=1){
#print(x*x) #prints out the squares
#}
#"""
from another_lexer import Token
from debracer import OpNode
def post_tokenisation(code):
  #Locate ++ and -- and += and -= tokens
  idx=0
  temp=code.copy()
  while(idx<len(temp)):
    #print("Checking index",idx,"out of",len(temp))
    if(temp[idx].tvalue=="++"):
      temp=temp[:idx-1]+[temp[idx-1],Token("symbol","="),temp[idx-1],Token("symbol","+"),Token("number","1")]+temp[idx+1:]
    elif(temp[idx].tvalue=="--"):
      temp=temp[:idx-1]+[temp[idx-1],Token("symbol","="),temp[idx-1],Token("symbol","-"),Token("number","1")]+temp[idx+1:]
    else:
      for op in list("+-*/")+["//"]:
        if(temp[idx].tvalue==(op+"=")):
          temp=temp[:idx-1]+[temp[idx-1],Token("symbol","="),temp[idx-1],Token("symbol",op),temp[idx+1]]+temp[idx+2:]
          break
    idx+=1
  return temp
#def get_vars(code):
#  variables=set()
#  for idx in range(len(code)):
#    if(code[idx].ttype!="word"):continue
#    if(code[idx].tvalue!="var"):continue
#    variables|={code[idx+1].tvalue}
#  return list(variables)
#class Bracket(Token):
#  dest=None
#  where=None
#  def __repr__(s):
#    if s.dest==None:
#      return f"(unpaired '{s.tvalue}')"
#    else:
#      return f"('{s.tvalue}' @ {s.where} -> {s.dest})"
    
  
  
      
