import mysql.connector
# there appears to be an error with the way python handles the ⟕ character. 
relationalStatement = "Π*(σactor_id<100∧first_name='Penelope'(actor, film))"

sqlStatement = "("
table1 = ""
table2 = ""
setDiff = False
findPredicate = True

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

def interpretRA(relationalStatement, sqlStatement, findPredicate, setDiff):
    selectStatement = ""
    fromStatement = ""
    whereStatement = ""
    predicate = ""
    
    for x in range( len(relationalStatement) ):
        if relationalStatement[x] == "∪":
            sqlStatement = "(" + selectStatement + fromStatement + whereStatement + ") UNION ("
            selectStatement = ""
            fromStatement = ""
            whereStatement = ""
        if relationalStatement[x] == "-":
            table1 = "(" + selectStatement + fromStatement + whereStatement + ")"
            selectStatement = ""
            fromStatement = ""
            whereStatement = ""
            setDiff = True
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
                if findPredicate == True:
                    while n != "<":
                        predicate = predicate + n
                        i = i + 1
                        n = relationalStatement[x+i] 
                    findPredicate = False
                i = 2
                n = relationalStatement[x + 2]
                while n != "(":
                    
                    if n == "∧":
                        whereStatement = whereStatement + " and "
                    elif n == "∨":
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
    if setDiff == True:
        table2 = "(" + selectStatement + fromStatement + whereStatement + ")"
        sqlStatement = selectStatement + "from " + table1 + "as t1 " + "natural left join " + table2 + "as t2 " + "where t2." + predicate + " IS NULL;" 
    else:
        sqlStatement = sqlStatement + selectStatement + fromStatement + whereStatement + ")"
    print(sqlStatement)
    
    runScript(sqlStatement)
    
    
interpretRA(relationalStatement, sqlStatement, findPredicate, setDiff)
#print(sqlStatement)
#runScript("(SELECT * FROM film WHERE film_id<20 ) MINUS (SELECT * FROM film WHERE film_id>500 )")
