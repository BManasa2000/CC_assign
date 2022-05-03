# Was trying to implement for relational and conditional expressions, wasn't able to complete it
# Will have to add attributes. Can't use just temp and code.
# Need to fix the grammar for arithmetic expressions. Currently the expressions of the form (E) are not working as expected.


from parsing import *
from inter_generator import *
import csv
import inter_scanner

temp_cnt = 0
cur_st = 0
ids = []

def new_temp():
    global temp_cnt
    temp_cnt += 1
    return "t" + str(temp_cnt)

def semantic_action(semantic_stack, intermed, i=""):
    global ids
    ind = int(intermed) + 1
    temp = ""
    code = ""
    if (ind == 1): #S'->S
        (t,c) = semantic_stack.pop()
        code = c

    # ARITHMETIC
    elif (ind == 2): #S->id = E
        list = []
        (t,c) = semantic_stack.pop()
        list.append(c);
        list.append("\n");
        i = ids.pop()
        st = i + " = " + str(t)
        list.append(st)
        for c in list:
            code = code + c
    elif (ind == 3 or ind == 4): #E->E+T || E->E-T
        temp = new_temp()
        list = []
        (t2,c2) = semantic_stack.pop() #popping attribute of T
        (t1,c1) = semantic_stack.pop() #popping attribute of E
        list.append(c1)
        list.append("\n")
        list.append(c2)
        list.append("\n")
        if (ind == 3):
            st = temp + " = " + t1 + " + " + t2
        else:
            st = temp + " = " + t1 + " - " + t2
        list.append(st)
        for c in list:
            code = code + c
    elif (ind == 5): #E->T
        (t,c) = semantic_stack.pop()
        temp = t   
        code = (c)
    elif (ind == 6 or ind == 7): #T->T*F
        temp = new_temp()
        list = []
        (t2,c2) = semantic_stack.pop() #popping attribute of F
        (t1,c1) = semantic_stack.pop() #popping attribute of T
        list.append(c1)
        list.append("\n")
        list.append(c2)
        list.append("\n")
        if (ind == 6):
            st = temp + " = " + t1 + " * " + t2
        else:
            st = temp + " = " + t1 + " / " + t2
        list.append(st)
        for c in list:
            code = code + c
    elif (ind == 8): #T->F
        # temp = new_temp()
        (t,c) = semantic_stack.pop() #popping attributes of T
        temp = t
        code = c
    elif (ind == 9): #F->( E )
        (t,c) = semantic_stack.pop() #popping attributes of E
        temp = t
        code = "( " + c + " )"
    elif (ind == 10): #F->id
        temp = ids.pop()

    # RELATIONAL
    elif (ind in [11,12,13,14,15,16]):
        oper = {11: "<", 12: "<=", 13: ">", 14: ">=", 15: "==", 16: "<>"}
        temp = new_temp()
        id1 = ids.pop()
        id2 = ids.pop()
        str1 = f"if {id1} {oper[ind]} {id2} goto cur + 3\n"
        str2 = f"{temp} = 0\n"
        str3 = f"goto cur + 2\n"
        str4 = f"{temp} = 1\n"
        code = str1 + str2 + str3 + str4

    # CONDITIONAL
    elif (ind == 17):
        

    semantic_stack.append((temp,code))

    print("\n\nSEMANTIC STACK!!!\n")
    for i in semantic_stack:
        print(i)
    print("\n")

    return semantic_stack

def readFile(input):
	file1 = open(input, 'r')
	code = file1.read()
	return code

def stateIndex(stack):
	return stack[2 * ((len(stack) - 1) >> 1)]

def main():
    global ids
    stack=[]
    semantic_stack = []
    # error_output=[]
    stack.append(0)
    finallex=inter_scanner.driver(1)
    print(finallex)
    tokens_input=[]
    for i in finallex:
        if(i[1]=="keyword"):
            tokens_input.append(i[0])
        if(i[1]=="identifier"):
            # ids.append(i[0])
            tokens_input.append('id')
        if(i[1]=="Operator"):
            tokens_input.append(i[0])
    tokens_input.append('$end')
    tokens=tokens_input
    i = 0
    for t in tokens:
        print(i, t)
        i+=1
    tokenindex=0
    token=tokens[tokenindex]
    s_index=stateIndex(stack)
    gr=get_grammar()
    stateid=0
    with open('LALR_inter.csv','r') as csvDataFile:
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
            print(tokens[index_input])
            for row in csvReader:
                if(cnt==stateid):
                    if(tokens[index_input]=='id'):
                        ids.append(finallex[index_input][0])
                    if(tokens[index_input]=="$end"):
                        temp=row[tokens[index_input]]
                    else:
                        temp=row["'"+tokens[index_input]+"'"]
                    # print(temp)
                    if(temp==''):
                        # print("Error", index_input)
                        # error_output.append("The Error is encountered on input :"+str(finallex[index_input][0]))
                        # stack,tokens,finallex=panic_recovery(stack,tokens,index_input,finallex)
                        # print("\n\nSTACK AFTER PANIC RECOVERY: ", stack, "\n\n")
                        stateid=int(stack[-1])
                    elif(temp[0]=='s'):
                        stack.append(tokens[index_input])
                        y=2
                        intermed=temp[1]
                        while(y<len(temp)):
                            intermed=intermed+temp[y]
                            y=y+1
                        stack.append(int(intermed))
                        print(stack)
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

                        # ######################################
                        #SEMANTIC PART
                        m = int(intermed) + 1
                        id_ = ""
                        semantic_stack = semantic_action(semantic_stack, intermed)
                        # ######################################
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
                        print(stack)
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
                                print(stack)
                                break
                            x=x+1
                    else:
                        flag=0
                    break
                cnt=cnt+1
        # for k in error_output:
        #     print(k)
    t, c = semantic_stack.pop()
    print(c)
            

if __name__ == "__main__":
    # gr=get_grammar()
    # for i in gr.productions:
    #     print(i)
    # print(len(gr.productions))
    # print(gr.productions[0])
    main()
