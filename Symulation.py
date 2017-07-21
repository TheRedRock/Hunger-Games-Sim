import PlayerClass
import ActionMethods
import Log
import Items
import copy
import random
import ProgressBar

class Sym:
	# logName - string
	def __init__(self,logName):
		self.listOfTeams = []	# Team - a list of players with some additional stuff.
		self.dayDuration = 12	# Amount of hours in a day
		self.hourlyCalorieCost = 50 # calorie cost per hour - no matter the action
		self.theLog = Log.LogObject(logName)	# log where stuff is going to be written. For now only for testing purposes.
	# runs symulation for one day
	def runForADay(self):
		for t in self.listOfTeams:
			t.resetPlayersTime()
			
		stringToWrite = "---Status:\n"
		for team in self.listOfTeams:
			for p in team.playerList:
				stringToWrite+=p.getStringStatus(1)+ "\tinventory\n"+ p.getStringItemList(2)
		self.theLog.writeToLog(stringToWrite)
		allFinished = False
		while not allFinished:
			random.shuffle(self.listOfTeams) # this shuffle is so that one team doesn't always go first
			result = self.findEarlyiestPlayer()
			# To implement - teams make actions as a group. Sometimes only part of the team does the action.
			if result[0] is None:
				allFinished = self.areAllFinished()
				break
			#playersPerformingAction = [result[0]]
			#action = self.makeDecisionNoCathegories(result[0])
			
			playersPerformingAction = result[1].listOfPlayersWithGivenTime(result[0].simTime)
			resultOfDecision = self.makeGroupDecisionNoCathegories(playersPerformingAction)
			action = resultOfDecision[0]
			target = [resultOfDecision[1]]
			actionResult = action.applyAction(playersPerformingAction,target)
			self.writeActionInformationToLog(action,actionResult,[x for x in playersPerformingAction if x not in target],target)
			for p in playersPerformingAction:
				p.removeCalories(self.hourlyCalorieCost*action.time)
				p.simTime+=action.time		
				# To implement - check if characters are dead.
				stringToWrite = p.getStringStatus(1) + "\tinventory\n"+ p.getStringItemList(2) + "\ttime passed so far:{}\n".format(p.simTime)
				#self.theLog.writeToLog(stringToWrite)
				isDead = p.isDead()
				if isDead[0]:
					result[1].removePlayer(p.id)
					stringToWrite=p.Name+" "+isDead[1]+'\n'
					self.theLog.writeToLog(stringToWrite)
							
			allFinished = self.areAllFinished()
	# finds a player that has the least of time passed	
	# returns None if everyone is above dayDuration time
	def findEarlyiestPlayer(self):
		playerToReturn = None
		teamToReturn = None
		playerTime = self.dayDuration
		for team in self.listOfTeams:
			for player in team.playerList:
				if player.simTime<playerTime:
					playerTime = player.simTime
					playerToReturn = player
					teamToReturn = team
		return playerToReturn,teamToReturn # player with the least time passed - and his team
	# makes decision of one player
	# player - PlayerClass.Player
	# group - list of players, where decision making takes place. Player should be inside it.
	def makeDecisionNoCathegories(self,player,group):
		group.remove(player)
		group.insert(0,player)
		actionToReturn = None
		actionTarget = None
		if player.Calories < 200:
			result = ActionMethods.EatFoodCheck([player])
			if result:
				actionToReturn = PlayerClass.getActionByName("eat food")
			elif ActionMethods.AskForFoodCheck(group,[player]):
				actionToReturn = PlayerClass.getActionByName("ask for food")
				actionTarget = player
			else:
				actionToReturn = PlayerClass.getActionByName("gather food")
		else:
			# random action
			actionToReturn = PlayerClass.getPurelyRandomAction()
			if actionToReturn.name == "ask for food":
				actionTarget = player
		return actionToReturn, actionTarget
	
	# makes decision of group of players.
	# listOfPlayers - list with Player as elements
	def makeGroupDecisionNoCathegories(self,listOfPlayers):
		actionsAndPersuasionList = []
		action = None
		actionTarget = None
		for p in listOfPlayers:
			result = self.makeDecisionNoCathegories(p,listOfPlayers) # [0] - action, [1] - player to perform action on
			action = result[0]
			actionTarget = result[1]
			persuasion = p.Charisma + 0.4 * p.Intelligence + 0.1*random.randint(0,20)
			appendIsNeeded = True
			for AaP in actionsAndPersuasionList:
				if AaP[0].name == action.name:
					appendIsNeeded = False
					AaP[1]+=persuasion
					break
			if appendIsNeeded:
				actionsAndPersuasionList.append([action,persuasion,actionTarget])
		# find action with the biggest persuasion
		action = None
		actionTarget = None
		persuasion = -1
		for AaP in actionsAndPersuasionList:
			if AaP[1]> persuasion:
				persuasion = AaP[1]
				action = AaP[0]
				actionTarget = AaP[2]
		return action,actionTarget

	#detects if all players in all teams have finished actions for today	
	def areAllFinished(self):
		for team in self.listOfTeams:
			if not team.checkAllPlayersFinished(self.dayDuration):
				return False
		return True
			
	# Writes information about performed action into the log
	def writeActionInformationToLog(self,action,actionResult,playerList,targetList = None):
		if actionResult:
			textToPrint = "success"
		else:
			textToPrint = "failure"
		playerNames = ""
		for p in playerList:
			playerNames+=p.Name+', '
		playerNames = playerNames[:-2]
		targetNames =""
		if (not targetList is None) and (not targetList[0] is None):
			for t in targetList:
				targetNames+=t.Name+', '
			targetNames = targetNames[:-2]
		stringToWriteToLog = "\n==== Action Performed: {0}, result:{1}\n== Action performed by:{2}".format(action.name,textToPrint,playerNames)
		if not targetNames == "":
			stringToWriteToLog+=" targets: {}\n".format(targetNames)
		else:
			stringToWriteToLog+='\n'
		self.theLog.writeToLog(stringToWriteToLog)
	
class Team:
	# listOfPlayers - list with players as elements
	def __init__(self,listOfPlayers):
		self.playerList = listOfPlayers
		self.allPlayersFinished = False
	# returns a player from list. None, if player is not in team.
	# name - either string or int
	def getPlayer(self,name):
		if type(name) is int:
			for p in self.playerList:
				if p.id == name:
					return p
		elif type(name) is str:
			for p in self.playerList:
				if p.Name == name:
					return p
		else:
			raise Exception("Wrong parameter type")
		return None
	# checks if all players have finished the day.
	# dayTimeLimit - int
	def checkAllPlayersFinished(self,dayTimeLimit):
		for p in self.playerList:
			if p.simTime<dayTimeLimit:
				self.allPlayersFinished = False
		self.allPlayersFinished = True
	# sets all players time in the team to zero
	def resetPlayersTime(self):
		for p in self.playerList:
			p.simTime = 0
	# checks, if all players have the same time.
	# players with different times can't perform an action together.
	# becasue they are in different points in time
	def areAllPlayersTheSameTime(self):
		time = self.playerList[0].simTime
		for p in self.playerList:
			if not p.simTime == time:
				return False
		return True
	# Returns list of players with the same time	
	def listOfPlayersWithGivenTime(self,time):
		listToReturn = []
		for p in self.playerList:
			if p.simTime == time:
				listToReturn.append(p)
		return listToReturn
				
	# removes player from team. Returns true if player was removed.
	# name - str or int
	def removePlayer(self,name):
		for p in self.playerList:
			if p.Name == name or p.id == name:
				self.playerList.remove(p)
				return True
		return False

# --- test ---

pl = PlayerClass.Player(0)
pl.BaseWisdom = 5
pl.Name = "Jan Kowalski"
pl.calculateStartStatistics()
pl2 = PlayerClass.Player(0)
pl2.BaseWisdom = 0
pl2.Name = "Adam Nowak"
pl2.calculateStartStatistics()
team = Team([pl,pl2])
theLog = Log.LogObject('log1')
s = Sym('log1')
s.listOfTeams.append(team)
maxdays = 100
pbar = ProgressBar.ProgressBar(maxdays)
for x in range(1,101):
	theLog.writeToLog("\n~~ DAY {}~~\n\n".format(x))
	s.runForADay()
	pbar.changeToDay(x)
pbar.finish()