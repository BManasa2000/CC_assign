'''
Group Members:
Virag Lakhani - 2018B3A70973H
Yashika Chopra - 2018B3A70894H
Manasa Reddy Bollavaram - 2018B4A70774H
A.S.N.Rishika - 2018B2A70730H
'''

# list of keywords
keywords = ['return','void','if','else','while','float','int','char','main','string']
# list of delimiters
delimiters = ['(',')','{','}',';',' ',',']
separators = ['(',')','{','}',';',' ','\t','%','+','*','/','-','<','>','=','&','|','\n',',']
#list of operators
operators = ['<','>','=','&','|','%','+','*','/','-']
twoCharOperators = ['<=','>=','&&','||','==','<>']

#state lexemes
smallLetters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
letters =["a" , "A" , "b" , "B" , "c" , "C" , "d" , "D" , "e" , "E" , "f" , "F" , "g" , "G" , "h" , "H" , "i" , "I" , "j" , "J" , "k" , "K" , "l" , "L" , "m" , "M" , "n" , "N" , "o" , "O" , "p" , "P" , "q" , "Q" , "r" , "R" , "s" , "S" , "t" , "T" , "u" , "U" , "v" , "V" ,"w" , "W" , "x" , "X" , "y" , "Y" , "z" , "Z", "_"]
digits = ["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
dot = "."
#string literal identifier
quote = ["\""]
tokenNumbers = {'(':1 ,')':2 ,'{':3 ,'}':4 ,';':5 ,'+':6, '*':7 ,'/':8 ,'-':9 ,'<':10 ,'>':11 ,'=':12 ,'&':13 ,'|':14 ,'<=':15 ,'%':16,',':17,'&&':18,'||':19,'>=':20 ,'==':21 ,'<>':22 , 'if':23 ,'else':24 ,'while':25 ,'float':26 ,'int':27 ,'char':28 ,'return':29 ,'void':30 ,'main':31 , 'character':32 , 'integerLiteral':33 ,'floatingPointLiteral':34 , 'identifier':35, 'string':36, 'stringLiteral':37}
#look up table
lookupTable = []
counterrorlines=0
counterrors=0
# returns code in the form of a string
def readFile(input):
	file1 = open(input, 'r')
	code = file1.read()
	return code

# Writes output in text file
def writeFile(input):		
	file2 = open(input, 'w')
	for i in lexemes:
		file2.write(i+'\n')
	file2.close()


# return the token of the lexeme
def isToken(lexeme):
	if lexeme in keywords:
		return "keyword"
		flag=0
	elif lexeme in lookupTable:
		flag = 1
		return "identifier"
	else:
		flag = 2
		ans = dfa(lexeme)
	return ans

#rechecking error
def errorRecheck(lexeme,lineCount):
	left=0
	right=left
	tokenPrevious="error"
	while(right<len(lexeme)):
		newToken=isToken(lexeme[left:right+1])
		if(newToken=="error" and left!=right):
			tokenValue=tokenNumbers[tokenPrevious]
			lexemes.append(f'Lexeme:{lexeme[left:right]}, Token:{tokenPrevious}, tokenValue:{tokenValue}, LineNumber:{lineCount}')
			left=right
			tokenPrevious="error"
		elif(newToken!="error"):
			tokenPrevious=newToken
			right+=1
		else:
			lexemes.append(f"Lexeme:{lexeme[left:right+1]} lexical error")
			left+=1
			right+=1

		if(right==len(lexeme) and left!=right):
			tokenValue=tokenNumbers[tokenPrevious]
			lexemes.append(f'Lexeme:{lexeme[left:right]}, Token:{tokenPrevious}, tokenValue:{tokenValue}, LineNumber:{lineCount}')


#for checking dfa
def dfa(lexeme):
	size = len(lexeme)
	if lexeme[0]=='\'' and lexeme[-1]=='\'' and size==3:
		return "character"
	if lexeme in lookupTable:
		return "identifier"
	currentState = 0
	position = 0
	# loop through the lexeme and checks with DFA
	while(position<size):
	# update state according to the read input
		if(currentState==0):
			if lexeme[position] in digits:
				currentState=1
			elif lexeme[position] in smallLetters:
				currentState=4
			else:
				currentState=5
		elif(currentState==4):
			if((lexeme[position] in digits) or (lexeme[position] in letters)):
				currentState=4
			else:
				currentState=5
		elif(currentState==3):
			if(lexeme[position] in digits):
				currentState=3
			else:
				currentState=5
		elif(currentState==2):
			if(lexeme[position] in digits):
				currentState=3
			else:
				currentState=5
		elif(currentState==1):
			if(lexeme[position] in digits):
				currentState=1
			elif(lexeme[position] == dot):
				currentState=2
			else:
				currentState=5		
		else:
			return "error"

		position+=1

	if position==size:
		if currentState==1:
			flag = 1
			return "integerLiteral"
		elif currentState==4:
			lookupTable.append(lexeme)
			return "identifier"
		elif currentState==3:
			flag = 1
			return "floatingPointLiteral"
		else:
			return "error"


# parse code, display info of tokens
def parser(code):
	left=0
	right=left
	lineCount = 1
	codeLength = len(code)
	while right < codeLength:
	#For Multi line comments
		if ((code[right]=="$") and (left == right)):
			right=right+1
			while(code[right]!="$"):
				if(code[right]=="\n"):
					lineCount += 1
				right=right+1
			left=right+1
		#For single line comments
		if code[right] == '#':
			while(code[right] != '\n'):
				right += 1
			right = right + 1
			left = right
			lineCount += 1
			continue

		# For Strings
		if ((code[right] in quote) and (left == right)):
			right=right+1
			while(code[right] not in quote):
				right=right+1
			lookupTable.append(code[left:right+1])
			lexemes.append(f'Lexeme:{code[left:right+1]}, Token:{"String"}, tokenValue:{tokenNumbers["stringLiteral"]}, LineNumber:{lineCount}')
			left=right+1

		#For keywords,identifiers/none
		if ((code[right] in separators) and (left != right)):
			lexeme = code[left:right]
			token = isToken(lexeme)
			if(token=="keyword"):
				tokenValue = tokenNumbers[lexeme]
				flag=1
			elif token!="error":
				tokenValue = tokenNumbers[token]
			# handle error
			if token!="error":
				lexemes.append(f'Lexeme:{lexeme}, Token:{token}, tokenValue:{tokenValue}, LineNumber:{lineCount}')
			else:
				errorRecheck(lexeme,lineCount)
			left = right


		# For delimietrs and operators
		if code[right] in separators and left == right:
			if (right<codeLength-1 and code[left:right+2] in twoCharOperators):
				lexemes.append(f'Lexeme:{code[left:right+2]}, Token:{"Operator"}, tokenValue:{tokenNumbers[code[left:right+2]]}, LineNumber:{lineCount}')
				right = right + 1
				left = right + 1

			else:
			# handle space
				if code[right] != ' ' and code[right] != '\n':
					if code[right] not in delimiters:
						lexemes.append(f'Lexeme:{code[right]}, Token:{"Operator"}, tokenValue:{tokenNumbers[code[right]]}, LineNumber:{lineCount}')
					else:
						lexemes.append(f'Lexeme:{code[right]}, Token:{"Delimiter"}, tokenValue:{tokenNumbers[code[right]]}, LineNumber:{lineCount}')
				
				left = right + 1

		if code[right] == '\n':
			lineCount += 1
			left = right + 1

		right = right + 1


# driver
for i in range(1,5):
	Ipfile = f'input{i}.txt'
	code = readFile(Ipfile)
	lexemes = []
	parser(code)
	fileOp = writeFile(f'output{i}.txt')
	lexemes.clear()