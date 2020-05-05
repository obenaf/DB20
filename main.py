import mysql.connector
# there appears to be an error with the way python handles the ⟕ character. 
relationalStatement = "Π*(actor⟕film_actor)"

sqlStatement = ""


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Tr332AndStuff",
    database="sakila"
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
        if relationalStatement[x] == "Π":#Project symbol found, start writing select statement
            selectStatement = selectStatement + "SELECT "
            i = 1
            n = relationalStatement[x + i]
            while n != "(":
                selectStatement = selectStatement + n
                i = i + 1 
                n = relationalStatement[x + i]  
            selectStatement = selectStatement + " "
        if relationalStatement[x] == "(":# First paranthese found. 
            if relationalStatement[x+1] == "σ":#Select symbol found, start writing where statement
                whereStatement = whereStatement + "WHERE "
                i = 2
                n = relationalStatement[x + 2]
                while n != "(":
                    if n == "∧":
                        whereStatement = whereStatement + " and "
                    if n == "∨":
                        whereStatement = whereStatement + " or "
                    else:
                        whereStatement = whereStatement + n
                    i = i + 1
                    n = relationalStatement[x+i]
                whereStatement = whereStatement + " "
            else:#There was no select sybmol after a forward facing paranthese, or there was another open paranthese so start the from statement
                fromStatement = fromStatement + "FROM "
                i = 1
                n = relationalStatement[x + i]
                while n != ")":
                    if n == "⋈":
                        fromStatement = fromStatement + " natural join "
                    elif n == "⟖":
                        fromStatement = fromStatement + " natural right outer join "
                    elif n == "⟕":
                        fromStatement = fromStatement + " natural left outer join "
                    else:
                        fromStatement = fromStatement + n
                    i = i +1
                    n = relationalStatement[x+i]
                fromStatement = fromStatement + " "
    sqlStatement = selectStatement + fromStatement + whereStatement
    print(sqlStatement)
    #runScript(sqlStatement)
    
    
interpretRA(relationalStatement, sqlStatement)
#print(sqlStatement)
#runScript("SELECT Name FROM city WHERE Name = 'Kabul'")
