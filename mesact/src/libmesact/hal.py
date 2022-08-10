
def buildHal(parent):
	parent.halPTE.clear()
	for i in range(6):
		net = []
		if getattr(parent, f'halFunctionCB_{i}').currentData():
			net.append(getattr(parent, f'halSignalLE_{i}').text())
			net.append(getattr(parent, f'halFunctionCB_{i}').currentData())
			net.append(getattr(parent, f'halPin_{i}').text())
			net.append(getattr(parent, f'inputPinPB_{i}').text())
			net.append(getattr(parent, f'outputPinPB_{i}').text())

			fo = filter(lambda x: x != 'Select', net)
			fl = list(fo)
			netString = ' '.join(x for x in list(fl))

			if netString:
				parent.halPTE.appendPlainText(f'net {netString}')

def functionChanged(parent):
	pass
	#parent.halPTE.clear()

	#print(parent.sender().currentData())
	#print(parent.sender().objectName())
	'''
	functionList = []
	for i in range(6):
		if getattr(parent, f'halFunctionCB_{i}').currentData():
			functionName = getattr(parent, f'halFunctionCB_{i}').currentData()
			functionList.append(functionName)
			n = functionList.count(functionName)

	if functionList:
		functions = set(functionList)
		parent.halPTE.clear()
		for item in functions:
			n = functionList.count(item)
			parent.halPTE.appendPlainText(f'loadrt {item} count={n}')
			for i in range(n):
				parent.halPTE.appendPlainText(f'addf {item}.{i} servo-thread')
			n = 0
			for i in range(6):
				if getattr(parent, f'halFunctionCB_{i}').currentData() == item:
					# print(f'{getattr(parent, f"halFunctionCB_{i}").currentData()} {item}')
					getattr(parent, f'halNameLB_{i}').setText(f'{item}.{n}')
					n += 1


	else:
		parent.halPTE.clear()

	#print(functionList)
	# halPTE
	# halNameLB_
	# halPin_
	# inPin_
	# outPin_
	# getattr(parent, f'halFunctionCB_{i}').addItem(item[0], item[1])
	'''

def countChanged(parent):
	parent.halAddPTE.clear()
	halFunctions = 	[['Select', False],]
	functions1 = ['not']
	functions2 = ['and2', 'or2', 'xor2']
	for i in range(4):
		if getattr(parent, f'functionCountSB_{i}').value() > 0:
			count = getattr(parent, f'functionCountSB_{i}').value()
			function = getattr(parent, f'functionCountSB_{i}').property('function')
			parent.halAddPTE.appendPlainText(f'loadrt {function} count={count}')
			for i in range(count):
				parent.halAddPTE.appendPlainText(f'addf {function}.{i} servo-thread')
				if function in functions1:
					halFunctions.append([f'{function}.{i}.in',f'{function}.{i}.in'])
					halFunctions.append([f'{function}.{i}.out',f'{function}.{i}.out'])
				if function in functions2:
					halFunctions.append([f'{function}.{i}.in0',f'{function}.{i}.in0'])
					halFunctions.append([f'{function}.{i}.in1',f'{function}.{i}.in1'])
					halFunctions.append([f'{function}.{i}.out',f'{function}.{i}.out'])


	for i in range(6):
		getattr(parent, f'halFunctionCB_{i}').clear()
		for item in halFunctions:
			getattr(parent, f'halFunctionCB_{i}').addItem(item[0], item[1])




