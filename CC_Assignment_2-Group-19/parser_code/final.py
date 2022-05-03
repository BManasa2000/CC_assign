#tree.py is not being used currently
#The parser_output files are not being generated by this code.

from parsing import *
from generator import *
import csv
import scanner

file_no = 5
def readFile(input):
	file1 = open(input, 'r')
	code = file1.read()
	return code

def stateIndex(stack):
	return stack[2 * ((len(stack) - 1) >> 1)]

def panic_recovery(stack,tokens,index_input,finallex):
    while(1): #synch
        # print("Stack[-2] = ", stack[-2])
        if(stack[-2]=='stmnt'):
            break
        elif(stack[-2]=='{'):
            break
        else:
            stack.pop()
            stack.pop()
    while(index_input<len(tokens)): #skip
        if(tokens[index_input]==';'):
            tokens.pop(index_input)
            finallex.pop(index_input)
            break
        elif(tokens[index_input]=='}'):
            break
        else:
            tokens.pop(index_input)
            finallex.pop(index_input)
    return stack,tokens,finallex

def main():
    stack=[]
    error_output=[]
    stack.append(0)
    finallex=scanner.driver(file_no)
    # print(finallex)
    tokens_input=[]
    for i in finallex:
        if(i[1]=="keyword"):
            tokens_input.append(i[0])
        if(i[1]=="identifier"):
            tokens_input.append('id')
        if(i[1]=="Operator"):
            tokens_input.append(i[0])
        if(i[1]=="integerLiteral"):
            tokens_input.append('intType')
        if(i[1]=="character"):
            tokens_input.append('charType')
        if(i[1]=="floatingPointLiteral"):
            tokens_input.append('floatType')
    tokens_input.append('$end')
    tokens=tokens_input
    token_no = 0
    i = 0
    for t in tokens:
        print(i, t)
        i+=1
    tokenindex=0
    token=tokens[tokenindex]
    s_index=stateIndex(stack)
    gr=get_grammar()
    stateid=0
    with open('LALR3.csv','r') as csvDataFile:
        csvReader = csv.DictReader(csvDataFile)
        flag=1
        step=0
        index_input=0
        cnt=0
        ind=0
        parsetree=[]
        while(flag==1):
            cnt=0
            temp=""
            csvDataFile.seek(0)
            csvReader = csv.DictReader(csvDataFile)
            # print("INPUT: ", finallex[index_input][0], tokens[index_input])
            # print(tokens[index_input])
            for row in csvReader:
                if(cnt==stateid):
                    if(tokens[index_input]=="$end"):
                        temp=row[tokens[index_input]]
                    else:
                        temp=row["'"+tokens[index_input]+"'"]
                    # print(temp)
                    if(temp==''):
                        # print("Error", index_input)
                        st = "The Error is encountered on input :"+str(finallex[index_input][0])+" i.e after token no. = "+str(token_no)
                        error_output.append(st)
                        stack,tokens,finallex=panic_recovery(stack,tokens,index_input,finallex)
                        # print("\n\nSTACK AFTER PANIC RECOVERY: ", stack, "\n\n")
                        stateid=int(stack[-1])
                    elif(temp[0]=='s'):
                        token_no += 1
                        stack.append(tokens[index_input])
                        y=2
                        intermed=temp[1]
                        while(y<len(temp)):
                            intermed=intermed+temp[y]
                            y=y+1
                        stack.append(int(intermed))
                        # print(stack)
                        stateid=int(intermed)
                        index_input=index_input+1
                    elif(temp[0]=='r'):
                        y=2
                        intermed=temp[1]
                        while(y<len(temp)):
                            intermed=intermed+temp[y]
                            y=y+1
                        # print(intermed)
                        replacement=gr.productions[int(intermed)+1][0]
                        times_pop=len(gr.productions[int(intermed)+1][1])
                        # print(times_pop)
                        # print(replacement)
                        if(len(stack)>1):
                            while(times_pop!=0):
                                stack.pop()
                                stack.pop()
                                times_pop=times_pop-1
                        ind=ind+1
                        gotorow=int(stack[-1])
                        #print(gotorow)
                        stack.append(replacement)
                        # print(stack)
                        x=0
                        csvDataFile.seek(0)
                        csvReader1 = csv.DictReader(csvDataFile)
                        for row in csvReader1:
                            #print(row)
                            if(x==gotorow):
                                temp=row[replacement]
                                #print(temp)
                                stack.append(int(temp))
                                stateid=int(temp)
                                # print(stack)
                                break
                            x=x+1
                    else:
                        flag=0
                    break
                cnt=cnt+1
        with open(f"error{file_no}.txt", 'w') as f:
            for k in error_output:
                f.write(k)
        for k in error_output:
            print(k)
            

if __name__ == "__main__":
    main()
