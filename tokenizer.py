import fileinput

def tokenize (text):
    seplist =['<<=','>>=',
              '++','--','->','<<','>>','<=','>=','==','!=','&&','||','+=','-=','*=','/=','%=','&=','^=','|=',
              '(',')','[',']','.' ,'+','-','!','~','*','&','/','%','<','>','^','|','?',':','=',',',
              '{','}','=',';','#',' ']
    for sep in seplist:
        index = text.find(sep)
        if index == -1:
            continue
        left = tokenize(text[0:(index)])
        right = tokenize(text[index+len(sep):])
        return left + [sep] + right
    return [text]

for line in fileinput.input():
    line = line.rstrip('\n')
    list = []
    for text in line.split("\t"):
        if len(text) == 0:
            continue
        if text[0] == '\"' or text[0] == '\'':
            list.append(text) 
        else:
            list = list + tokenize(text) 
    for item in list:
        item = item.strip()
        if len(item) > 0:
            print(item,end='\t')
    print()
