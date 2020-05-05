import mysql.connector

relationalStatement = "ΠID(σName='Kabul'(city))"

sqlStatement = ""


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Tr332AndStuff",
    database="world"
)

mycursor = db.cursor()

def runScript(myScript):
    mycursor.execute(myScript)
    for x in mycursor:
        print(x)

def interpretRA(relationalStatement, sqlStatement):
    selectStatement = ""
    fromStatement = ""
    whereStatement = ""
    for x in range( len(relationalStatement) ):
        if relationalStatement[x] == "Π":
            selectStatement = selectStatement + "SELECT "
            i = 1
            n = relationalStatement[x + i]
            while n != "(":
                selectStatement = selectStatement + n
                i = i + 1 
                n = relationalStatement[x + i]  
            selectStatement = selectStatement + " "
        if relationalStatement[x] == "(":
            if relationalStatement[x+1] == "σ":
                whereStatement = whereStatement + "WHERE "
                i = 2
                n = relationalStatement[x + 2]
                while n != "(":
                    whereStatement = whereStatement + n
                    i = i + 1
                    n = relationalStatement[x+i]
                whereStatement = whereStatement + " "
            else:
                fromStatement = fromStatement + "FROM "
                i = 1
                n = relationalStatement[x + i]
                while n != ")":
                    fromStatement = fromStatement + n
                    i = i +1
                    n = relationalStatement[x+i]
                fromStatement = fromStatement + " "
    sqlStatement = selectStatement + fromStatement + whereStatement
    print(sqlStatement)
    runScript(sqlStatement)
    
    
interpretRA(relationalStatement, sqlStatement)
#print(sqlStatement)
#runScript("SELECT Name FROM city WHERE Name = 'Kabul'")
