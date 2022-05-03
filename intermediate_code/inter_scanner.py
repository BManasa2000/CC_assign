# list of delimiters
delimiters = ['(',')','{','}',';',' ']
operators = ['+','*','/','-','<','>','=','&','|']
stoppers = ['(',')','{','}',';',' ','\t','+','*','/','-','<','>','=','&','|','\n']
valid2CharOps = ['<=','>=','==','<>']
# list of keywords
keywords = ['if','else','while','float','int','char','return','void','start']

#state lexemes
letters =["a" , "A" , "b" , "B" , "c" , "C" , "d" , "D" , "e" , "E" , "f" , "F" , "g" , "G" , "h" , "H" , "i" , "I" , "j" , "J" , "k" , "K" , "l" , "L" , "m" , "M" , "n" , "N" , "o" , "O" , "p" , "P" , "q" , "Q" , "r" , "R" , "s" , "S" , "t" , "T" , "u" , "U" , "v" , "V" ,"w" , "W" , "x" , "X" , "y" , "Y" , "z" , "Z"]
digits = ["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
dot = "."
tokenNumbers = {'(':1 ,')':2 ,'{':3 ,'}':4 ,';':5 ,'+':6, '*':7 ,'/':8 ,'-':9 ,'<':10 ,'>':11 ,'=':12 ,'&':13 ,'|':14 ,'<=':15 ,'>=':16 ,'==':17 ,'<>':18 , 'if':19 ,'else':20 ,'while':21 ,'float':22 ,'int':23 ,'char':24 ,'return':25 ,'void':26 ,'start':27 , 'character':28 , 'integerLiteral':29 ,'floatingPointLiteral':30 , 'identifier':31, 'string':32 }
# tokenValues = ['(',')','{','}',';','+','*','/','-','<','>','=','&','|','<=','>=','==','<>','if','else','while','float','int','char','return','void','start','return']
#look up table
lookupTable = []
lexemes = []
lexemes_modified = []

# returns code in the form of a string
def readFile(input):
	file1 = open(input, 'r')
	code = file1.read()
	return code

# return the token of the lexeme
def checkToken(lexeme):
	if lexeme in keywords:
		return "keyword"
	elif lexeme in lookupTable:
		return "identifier"
	else:
		ans = dfa(lexeme)
		return ans

#rechceking error
def errorRecheck(lexeme,lineCount):
	left=0
	right=0
	tokenPrev="error"
	while(right<len(lexeme)):
		tokenNew=checkToken(lexeme[left:right+1])
		#abc	
		if(tokenNew=="error" and left!=right):
			tokenVal=tokenNumbers[tokenPrev]
			# print(f'Lexeme:{lexeme[left:right]}, Token:{tokenPrev}, TokenVal:{tokenVal}, LineNumber:{lineCount}')
			lexemes.append(f'Lexeme:{lexeme[left:right]}, Token:{tokenPrev}, TokenVal:{tokenVal}, LineNumber:{lineCount}')
			temp=[]
			temp.append(lexeme[left:right])
			temp.append(tokenPrev)
			temp.append(tokenVal)
			temp.append(lineCount)
			lexemes_modified.append(temp)
			left=right
			tokenPrev="error"
		elif(tokenNew!="error"):
			tokenPrev=tokenNew
			right+=1
		else:
			# print(f"Lexeme:{lexeme[left:right+1]} lexical error")
			lexemes.append(f"Lexeme:{lexeme[left:right+1]} lexical error")
			left+=1
			right+=1

		if(right==len(lexeme) and left!=right):
			tokenVal=tokenNumbers[tokenPrev]
			# print(f'Lexeme:{lexeme[left:right]}, Token:{tokenPrev}, TokenVal:{tokenVal}, LineNumber:{lineCount}')
			lexemes.append(f'Lexeme:{lexeme[left:right]}, Token:{tokenPrev}, TokenVal:{tokenVal}, LineNumber:{lineCount}')
			temp=[]
			temp.append(lexeme[left:right])
			temp.append(tokenPrev)
			temp.append(tokenVal)
			temp.append(lineCount)
			lexemes_modified.append(temp)




#for checking dfa
def dfa(lexeme):
	size = len(lexeme)
	if lexeme[0]=='\'' and lexeme[-1]=='\'' and size==3:
		return "character"
	# if lexeme[0]=='"' and lexeme[-1]=='"' and size>=2:
	# 	return ""
	if lexeme in lookupTable:
		return "identifier"
	currState = 0
	counter = 0
	# loops through the lexeme and checks with DFA
	while(counter<size):
		# updates state according to the read input
		if(currState==0):
			if lexeme[counter] in digits:
				currState=1
			elif lexeme[counter] in letters:
				currState=4
			else:
				currState=5
		elif(currState==1):
			if(lexeme[counter] in digits):
				currState=1
			elif(lexeme[counter] == dot):
				currState=2
			else:
				currState=5
		elif(currState==2):
			if(lexeme[counter] in digits):
				currState=3
			else:
				currState=5
		elif(currState==3):
			if(lexeme[counter] in digits):
				currState=3
			else:
				currState=5
		elif(currState==4):
			if((lexeme[counter] in digits) or (lexeme[counter] in letters)):
				currState=4
			else:
				currState=5
		else:
			return "error"

		counter+=1 # read next input

	if counter==size:
		if currState==1:
			return "integerLiteral"
		elif currState==3:
			return "floatingPointLiteral"
		elif currState==4:
			lookupTable.append(lexeme)
			# print(lookupTable)
			return "identifier"
		else:
			return "error"


# parses the code and displays info of tokens
def parser(code):
	left=0
	right=0
	lineCount = 1 # inc if you find '\n'
	codeLength = len(code)
	# for right in range(0,codeLength):
	while right < codeLength:
		if code[right] == '#':
			while(code[right] != '\n'):
				right += 1
			right = right + 1
			left = right
			lineCount += 1
			continue

		if ((code[right] in stoppers) and (left != right)):
			lexeme = code[left:right]
			token = checkToken(lexeme)
				
			if(token=="keyword"):
				tokenVal = tokenNumbers[lexeme]
			elif token!="error":
				tokenVal = tokenNumbers[token]
			# print or store
			# handle error
			if token!="error":
				# print(f'Lexeme:{lexeme}, Token:{token}, TokenVal:{tokenVal}, LineNumber:{lineCount}')
				lexemes.append(f'Lexeme:{lexeme}, Token:{token}, TokenVal:{tokenVal}, LineNumber:{lineCount}')
				temp=[]
				temp.append(lexeme)
				temp.append(token)
				temp.append(tokenVal)
				temp.append(lineCount)
				lexemes_modified.append(temp)
			else:
				errorRecheck(lexeme,lineCount)
				#print("lexical error")
			left = right

		# For delimietrs
		if code[right] in stoppers and left == right:
			if (right<codeLength-1 and code[left:right+2] in valid2CharOps):
				# print(f'Lexeme:{code[left:right+2]}, Token:{"Operator"}, TokenVal:{tokenNumbers[code[left:right+2]]}, LineNumber:{lineCount}')
				lexemes.append(f'Lexeme:{code[left:right+2]}, Token:{"Operator"}, TokenVal:{tokenNumbers[code[left:right+2]]}, LineNumber:{lineCount}')
				temp=[]
				temp.append(code[left:right+2])
				temp.append("Operator")
				temp.append(tokenNumbers[code[left:right+2]])
				temp.append(lineCount)
				lexemes_modified.append(temp)
				left = right + 2
				right = right + 1
				# print(f'Debug: {code[left]} {code[right]}')
				# continue
			else:
				# handle space
				if code[right] != ' ' and code[right] != '\n':
					# print(f'Lexeme:{code[right]}, Token:{"Operator"}, TokenVal:{tokenNumbers[code[right]]}, LineNumber:{lineCount}')
					lexemes.append(f'Lexeme:{code[right]}, Token:{"Operator"}, TokenVal:{tokenNumbers[code[right]]}, LineNumber:{lineCount}')
					temp=[]
					temp.append(code[right])
					temp.append("Operator")
					temp.append(tokenNumbers[code[right]])
					temp.append(lineCount)
					lexemes_modified.append(temp)
				# else:
					# print('space')
				left = right + 1

		if code[right] == '\n':
			lineCount += 1
			left = right + 1
			# right = right + 1

		right = right + 1


# driver
def driver(i):
	fileIp = f'inter_sample{i}.txt'
	code = readFile(fileIp)
	print(code)
	parser(code)
	fileOp = open(f'output{i}.txt', 'w')
	for j in lexemes:
		fileOp.write(j+'\n')
	fileOp.close()
	#lexemes.clear()
	print(lexemes_modified)
	return lexemes_modified

def main():
	driver()
if __name__ == "__main__":
    main()
