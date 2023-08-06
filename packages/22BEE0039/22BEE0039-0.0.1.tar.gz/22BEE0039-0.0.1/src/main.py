import functions
while True:
	print('MENU:')
	print('S.no.\tTask')
	print('1\tAddition of two numbers')
	print('2\tExponentiate')
	print('3\tExit')
	i=input('\nEnter the S.no. of the task you want to perform: ')
	if i=='1':
		a=int(input('\nEnter the first number: '))
		b=int(input('Enter the second number: '))
		sum1=functions.summ(a,b)
		print('\nthe sum of the two numbers is',sum1,'\n')
	elif i=='2':
		a=int(input('\nEnter the base: '))
		b=int(input('Enter the power: '))
		power1=functions.power(a,b)
		print('the exponentiation is ',power1)
	elif i=='3':
		break
	else:
		print('INVALID INPUT!')
		print('Please enter a valid input from the menu.\n')