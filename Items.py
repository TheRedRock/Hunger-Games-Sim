import random

class typeException(Exception):
	def __init__(self,desc):
		self.desc = desc

class ItemFunction:
	def __init__(self,Id,Name,NameValueList):
		self.id = Id
		self.name = Name
		self.nameValueList = NameValueList
	def getString(self):
		str = ""
		str+= self.name
		for nv in self.nameValueList:
			str+="\n\t"+nv[0]
		return str
	def getRandomItem(self):
		randomNumber = random.randint(0,len(self.nameValueList)-1)
		return Item(self,randomNumber)

class Item:
	def __init__(self,Function,NVNumber):
		self.function = Function
		self.nameValue = Function.nameValueList[NVNumber]
		self.value = self.nameValue[1]
	def __str__(self):
		return self.nameValue[0]+" "+str(self.nameValue[1])
		
ItemFunctionList = []
ItemFunctionList.append(ItemFunction(0,"processed food",[["canned meat",400],["dry rations",600],["energy bar",300]]))
ItemFunctionList.append(ItemFunction(1,"medicine",[["bandage",5],["painkillers",2],["antivenom",4]]))
ItemFunctionList.append(ItemFunction(2,"meele weapon",[["stone hatchet",8],["wooden spear",6],["big stick",3]]))
ItemFunctionList.append(ItemFunction(3,"advanced meele weapon",[["steel sword",16],["steel trident",15],["steel knife",12]]))
ItemFunctionList.append(ItemFunction(4,"ranged weapon",[["improvised bow",7],["slingshot",3]]))
ItemFunctionList.append(ItemFunction(5,"ammunition",[["improvised arrow",2],["small stone",1]]))
ItemFunctionList.append(ItemFunction(6,"useless plant",[["oak leaves",0],["grass",0],["harmless moss",0]]))
ItemFunctionList.append(ItemFunction(7,"harmfull plant",[["posion berries",3],["weird mushrooms",2],["posion ivy",1]]))
ItemFunctionList.append(ItemFunction(8,"edible plant",[["wild onions",300],["blackberries",200],["edible roots",150]]))

def getItemFunction(name):
	global ItemFunctionList
	if type(name) is int:
		for f in ItemFunctionList:
			if f.id == name:
				return f
	elif type(name) is str:
		for f in ItemFunctionList:
			if f.name == name:
				return f
	else:
		raise Exception("Wrong parameter type")
	return None
	
	


#I was thinking how relationship mechanics is going to affect the symulation. It surprisingly offers a lot of depth. As for mechanics of forming teams:

#First of all - there is a need for neutral characters to meet and form teams. So, during an action there is a small chance that action performer will bump into another random character. That chance will be higher during first few days. Both characters perform an action from "bump" cathegory, that can be nice (chat, gift), neutral (leave), or agressive (attack). If relationship value is high enough, a character with higher one will ask to join/form a team. Action ends up in failure if agressive bump action succeeds. 

#Maybe there should be "track down another tribute" action, that will result in bump if succeeds. I am not sure yet in which cathegory this one should be. 

#Since groups will often do actions together, bump will affect all of them.

#Okay, "bump" cathegory sounds stupid. I'll try to make another name for that.
