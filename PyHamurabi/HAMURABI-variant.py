#PYTHON VARIANT VERSION OF CLASSIC TEXT GAME 'HAMURABI'
#HAS EXTRA CONDITIONS TO MAKE IT DIFFERENT AND EXCITING



#import statement here
import random

#global variables here
POPULATION_FOOD_DEMAND = 20
POPULATION_TILL_CAPACITY = 10


def main():

    growth = []         #population growth record
    casualty = []       #starvation casualty
    landOwnership = []  #these values are used to judge your performance

    #traditional default game value
    currentBushels = 2800
    currentLandOwned = 1000
    currentPopulation = 100

    harvestRate = 3
    landTradeRate = 17
    cropDamage = 200
    starvation = 0
    migration = 5           

    arePeopleAngry = False
    plague = False
    famine = False



    #THE GAME START HERE!
    introduction()


    #until 11th year...
    for currentYear in range(1, 12):


        #save current progress
        growth.append(currentPopulation)
        casualty.append(starvation)
        landOwnership.append(currentLandOwned)

        
        #status report
        print("\nHAMURABI: I BEG TO REPORT TO YOU,")
        print("IN YEAR " + str(currentYear) + ",", starvation, "PEOPLE STARVED.")
        print(migration, "PEOPLE CAME TO THE CITY.")
        
        #IF PLAUGE OCCURS, HALF OF POPULATION DIES
        if plague == True:
            print("A HORRIBLE PLAGUE HAS STRUCK!! HALF OF POPULATION DIED!!")
        
        print("THE CITY POPULATION IS NOW", currentPopulation)
        print("THE CITY NOW OWNS", currentLandOwned, "ACRES")
        
        #IF FAMIN HAPPENS, NO BUSHELS GET PRODUCED
        if famine == True:
            print("A TERRIBLE FAMINE IS UPON US. NO BUSHELS OF GRAIN ARE GAINED FROM OUR LANDS!!")
        
        print("YOU HARVESTED", harvestRate, "BUSHELS PER ACRE")
        print("RATS ATE", cropDamage, "BUSHELS")
        print("YOU NOW HAVE", currentBushels, "IN STORE")
        
        #this is here so we can always start game with random rates
        landTradeRate = 17 + random.randint(0,9)
        
        print("\nLAND IS TRADING AT", landTradeRate, "BUSHELS PER ACRE\n")

        
        
        #you will be evaluated if this is the end of your term
        if currentYear == 11:
            endGame(growth, casualty, landOwnership)
            break
        
        #otherwise, you may proceed with your administration
        else:
            tradeBuyPolicy = False
            tradeSellPolicy = False
            
            domesticPolicy = False
            food = 0
            
            farmingPolicy = False
            seed = 0
            
            userInput = 0


        try:
        
            #TRADE
            while tradeBuyPolicy == False:
            
                userInput = int(input("HOW MANY ACRES DO YOU WITH TO BUY?:"))
                
                
                #if user enters negative number, throw exception                    
                if userInput < 0:
                    raise

                #if user enters more than they can pay, then say you can't afford them.
                elif (userInput * landTradeRate) > currentBushels:
                    admonish4Grains(currentBushels)

                #if you are not buying, perhaps your would sell instead?
                elif userInput == 0:

                    while tradeSellPolicy == False:
                        
                        userInput = int(input("HOW MANY ACRES DO YOU WITH TO SELL?:"))
                
                        if userInput < 0:
                            raise
                    
                        #if user tries to sell all or more lands, then say you can't sell off
                        elif userInput >= currentLandOwned:
                            admonish4Lands(currentLandOwned)
                    
                        else:
                            currentLandOwned = currentLandOwned - userInput
                            currentBushels = currentBushels + (userInput * landTradeRate)
                            tradeSellPolicy = True
                            print()

                    tradeBuyPolicy = True

                else:
                    currentBushels = currentBushels - ( userInput * landTradeRate)
                    currentLandOwned += userInput
                    tradeBuyPolicy = True
                    print()
                    
                    

            #FEED
            while domesticPolicy == False:
            
                userInput = int(input("HOW MANY BUSHELS DO YOU WISH TO FEED YOUR PEOPLE?:"))
                
                
                if userInput < 0:
                    raise
                    
                #If more bushesl than you have are listed, tell user they can't be done (NOTE: 0 is an acceptable answer)
                elif userInput > currentBushels:
                    admonish4Grains(currentBushels)
                    
                else:
                    food = userInput
                    currentBushels = currentBushels - userInput
                    domesticPolicy = True
                    print()
                    
                    
            #FARM
            while farmingPolicy == False:
            
                userInput = int(input("HOW MANY ACRES DO YOU WISH TO PLANT WITH SEED?:"))
                
                
                if userInput < 0:
                    raise
                    
                #If more bushels or acre than you own is entered, then tell user they can't do that.
                elif userInput > currentBushels:
                    admonish4Grains(currentBushels)

                elif userInput > currentLandOwned:
                    admonish4Lands(currentLandOwned)
                    
                #also, amount of population dictates how much can it tilled.
                elif userInput > (currentPopulation * POPULATION_TILL_CAPACITY):
                    admonish4Workers(currentPopulation)
                    
                else:
                    seed = userInput
                    currentBushels = currentBushels - userInput
                    farmingPolicy = True


        except:
            #IF YOU ENTER NEGATIVE NUMBER AT ANY GIVEN TIME, THIS GAME WILL END WITH 'GET SOMEBODY ELSE TO DO IT'...
            rageQuit()
            break
        

        #Calculate your move        
        starvation = int(((currentPopulation * POPULATION_FOOD_DEMAND) - food) / POPULATION_FOOD_DEMAND)

        if starvation < 0:
            starvation = 0

        #IF PEOPLE ARE NOT SATISFIED WITH YOUR GOVERNANCE, A PEASANT REBELLION WILL OCCUR AND YOUR RULE WILL END IMMEDIATELY
        elif starvation >= (currentPopulation / 2):
            arePeopleAngry == True
            print("\nYOU STARVED", starvation, "IN ONE YEAR!!!")
            
            youFailAtWork()
            break

        else:
            currentPopulation -= starvation
        

        migration = random.randint(0, 10)

        #if current population is too small, you get extra modifier to increase the population quickly (for sake of game mechanics)
        if currentPopulation < 100:
            migration = migration * 2
            currentPopulation += migration

        else:
            currentPopulation += migration


        #EVENTS
        plague = True if random.randint(0,3) == 1 else False    #ternary conditional operator
        if plague == True:
            currentPopulation = int(currentPopulation / 2)
        
        famine = True if random.randint(0,3) == 1 and plague == False else False 
        harvestRate = 1 if famine == True else random.randint(2, 5)
        cropDamage = 0 if random.randint(0,2) == 1 else int(currentBushels * 0.2)
        
        currentBushels = currentBushels + (seed * harvestRate) - cropDamage

        if currentBushels < 0:
            currentBushels = 0


    
    print("\nSO LONG FOR NOW.")
    #THE GAME ENDS!





def introduction():

    print ("""\t\t\t\tHAMURABI
    \t\t\tORIGINAL GAME BY David Ahl\n
    The classic game of strategy and resource allocation\n
    Try your hand at governing ancient Sumeria successfully for a 10 year term of office.\n

    \t\t\t\tGAME RULES
    * Each turn is a year, and total duration of game is 10 years
    * For each turn, you may make decisions for allocating bushels of grain to trade farming lands, feed people, and plant crops. ALL DECISION IS FINAL!
    * At 11th year of your governance, your performance will be evaluated. However, people will not suffer your terrible rule for too long.\n\n\n""")



def admonish4Grains(bushels):
    print("HAMURABI: THINK AGAIN. YOU HAVE ONLY", bushels, "BUSHELS OF GRAIN. NOW THEN,")


def admonish4Lands(acre):
    print("HAMURABI: THINK AGAIN. YOU OWN ONLY", acre, "ACRE. NOW THEN,")


def admonish4Workers(people):
    print("BUT YOU HAVE ONLY", people, "PEOPLE TO TEND THE FIELDS! NOW THEN,")


def rageQuit():
    print("""\nHAMURABI: I CANNOT DO WHAT YOU WISH!
    GET YOURSELF ANOTHER STEWARD!!!!!\n""")


def youFailAtWork():
   
    print("""DUE TO THIS EXTREME MISMANAGEMENT YOU ARE NOT ONLY BEEN IMPEACHED AND THROWN OUT OF OFFICE
BUT YOU HAVE ALSO BEEN DECLARED NATIONAL FINK!!!""")


def endGame(growthPattern, casualtyCounts, landsRecord):

    starvationTotal = 0
    starvationRate = 0.00

    for i in range(10):
        starvationTotal += casualtyCounts[i]
        starvationRate += (casualtyCounts[i] / growthPattern[i]) * 100


    yearlyStarvation = starvationRate / 10
    landAcquisition = landsRecord[9] / growthPattern[9]

    
    print("IN YOUR 10-YEAR TERM OF OFFICE,", format(yearlyStarvation,",.2f"), "PERCENT OF THE POPULATION STARVED PER YEAR ON AVERAGE,")
    print("I.E. A TOTAL OF", starvationTotal,"PEOPLE DIED!!\n")
    print("YOU STARTED WITH 10 ACRES PER PERSON AND ENDED WITH", format(landAcquisition,",.2f"),"ACRES PER PERSON.\n")


    #FINAL JUDEGEMENT
    if yearlyStarvation < 10.00 and landAcquisition > 10.00:
        #GOOD ENDING: you managed starvation and increased the wealth
        print("A FANTASTIC PERFORMANCE'!! CHARLEMAGNE,\n DISRAELI, AND JEFFERSON COMBINED COULD NOT HAVE DONE BETTER!")
        
    elif yearlyStarvation > 30.00 or landAcquisition < 5.00:
        #BAD ENDING: too many people died or great loss of land occurs
        youFailAtWork()
                
    else:
        #SUMERIAN ENDING: everything else, which is a typical state of populace...
        print("YOUR HEAVY-HANDED PERFORMANCE SMACKS OF NERO AND IVAN IV.\nTHE PEOPLE (REMAINING) FINDS YOU AN UNPLEASANT RULER, AND, \nFRANKLY, HATE YOUR GUTS!!")
        


    

main()
