import random
import Items
import Log
import copy
theLog = Log.LogObject('testLog')

def FoodSearchCheck(*variables):
	PlayerList = variables[0]
	sum =0
	for p in PlayerList:
		sum += 2+p.Wisdom
	rn = random.randint(0,7*len(PlayerList))
	theLog.writeToLog('sum = {0}, rn = {1}'.format(sum,rn))
	return sum>rn
	
def FoodSearchSuccess(*variables):
	PlayerList = variables[0]
	theLog.writeToLog('FoodSearchSuccess\n')
	itemF = Items.getItemFunction('edible plant')
	for p in PlayerList:
		p.addItem(itemF.getRandomItem())
		wisdom = p.Wisdom-random.randint(2,5)
		while wisdom>0:
			p.addItem(itemF.getRandomItem())
			wisdom-=random.randint(3,6)
		p.Stress+=20
		p.removeCalories(20)

def FoodSearchFailure(*variables):
	PlayerList = variables[0]
	theLog.writeToLog('FoodSearchFailure\n')
	for p in PlayerList:
		if (p.Wisdom+random.randint(0,2))> 7:
			p.addItem(Items.item(itemF,2))
		p.Stress+=100
		p.removeCalories(20)
		
def AlwaysTrueCheck(*variables):
	return True
	
def Nothing(*variables):
	pass
	
	#To be honest, this is only for one character.
def EatFoodCheck(*variables):
	PlayerList = variables[0]
	for p in PlayerList:
		functionList = [Items.getItemFunction("edible plant"), Items.getItemFunction("processed food")]
		result = p.findItemWithOneOfItemFunctions(functionList)
	return result[0]

def EatFoodSuccess(*variables):
	PlayerList = variables[0]
	for p in PlayerList:
		itemToEat = None
		for i in p.itemList:
			functionList = [Items.getItemFunction("edible plant"), Items.getItemFunction("processed food")]
			result = p.findItemWithOneOfItemFunctions(functionList)
			if result[0] is True:
				theLog.writeToLog('{0} eats {1} for {2} Calories\n'.format(p.Name,result[1].nameValue[0],result[1].nameValue[1]))
				p.addCalories(result[1].nameValue[1])
				p.removeItem(result[1])
			else:
				theLog.writeToLog('Error, motherfucker! No food to eat, even though check found some!\n')
				
	
	#First person in the list is one who asks
def AskForFoodCheck(*variables):
	PlayerList = variables[0]
	TargetList = variables[1]
	DonorsList = [x for x in PlayerList if x not in TargetList]
	if len(DonorsList)<1 or len(TargetList)<1:
		return False
	functionList = [Items.getItemFunction("edible plant"), Items.getItemFunction("processed food")]
	foodExists = False
	foodNeeded = len(TargetList)
	charismaSum = 0
	beggarCharismaSum = 0
	for p in DonorsList:
		charismaSum+=p.Charisma
		#result = p.findItemWithOneOfItemFunctions(functionList)
		result = p.findListOfItemsWithOneOfItemFunctions(functionList)
		if len(result)>0:
			foodNeeded-=len(result)
			if foodNeeded<=0:
				foodExists = True
	for b in TargetList:
		beggarCharismaSum+=b.Charisma
	randomNumber = random.randint(0,5)
	if foodExists and (beggarCharismaSum/len(TargetList)+randomNumber)>(charismaSum/(len(DonorsList))):
		return True
	return False
	
	# here should be a change in relationship
def AskForFoodSuccess(*variables):
	PlayerList = variables[0]
	TargetList = variables[1]
	DonorsList = [x for x in PlayerList if x not in TargetList]
	if len(DonorsList)<1 or len(TargetList)<1 :
		return False
		
	listOfPlayersAndCalories = []
	functionList = [Items.getItemFunction("edible plant"), Items.getItemFunction("processed food")]
	maxCalorie = 0
	maxCaloriePlayer = None
	for b in TargetList:
		for p in DonorsList:
			itemCalories = 0
			listOfFoodItems = p.findListOfItemsWithOneOfItemFunctions(functionList)
			for foodItem in listOfFoodItems:
				itemCalories+=foodItem.value
			if itemCalories>maxCalorie:
				maxCalorie = itemCalories
				maxCaloriePlayer = p
		itemToGive = maxCaloriePlayer.findItemWithOneOfItemFunctions(functionList)
		if maxCalorie == 0 or not itemToGive[0]:
			theLog.writeToLog('Error, motherfucker! No food to give, even though check found some!\n')
			raise Exception("Error: food can't be given")
		b.addItem(itemToGive[1])
		maxCaloriePlayer.removeItem(itemToGive[1])
	
	# here should be a change in relationship
def AskForFoodFailure(*variables):
	pass
		
	
	
