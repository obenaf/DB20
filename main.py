import mysql.connector
import tkinter
import os

# DEBUG FLAG
debug = False
#

# host1="localhost"
# user1="root"
# passwd1="Tr332AndStuff"
# database1="sakila"

#UI and init
root = tkinter.Tk()
root.title("RA Interpreter")

canvas = tkinter.Canvas(root, width = 300, height = 10)
canvas.pack()

hostEntry = tkinter.Entry(root)
canvas.create_window(200, 140, window = hostEntry)
hostEntry.insert(0, 'localhost')
hostEntry.pack()

userEntry = tkinter.Entry(root)
canvas.create_window(200, 140, window = userEntry)
userEntry.insert(0, 'root')
userEntry.pack()

passwdEntry = tkinter.Entry(root)
canvas.create_window(200, 140, window = passwdEntry)
passwdEntry.insert(0, 'Tr332AndStuff')
passwdEntry.pack()

databaseEntry = tkinter.Entry(root)
canvas.create_window(200, 140, window = databaseEntry)
databaseEntry.insert(0, 'sakila')
databaseEntry.pack()

label = tkinter.Label(root, text = 'Enter RA statement: ')
canvas.create_window(300, 100, window = label)
label.pack()

entry = tkinter.Entry(root)
canvas.create_window(200, 140, window = entry)
entry.pack()



def popupmsg(msg):
    popup = tkinter.Tk()
    popup.wm_title("Output")
    label = tkinter.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def runScript(myScript):
    db = mysql.connector.connect(
            host = hostEntry.get(),
            user = userEntry.get(),
            passwd = passwdEntry.get(),
            database = databaseEntry.get()
        )
    mycursor = db.cursor()
    mycursor.execute(myScript)
    for x in mycursor:
        print(x)


def interpretRA():
    relationalStatement = entry.get()

    table1 = ""
    table2 = ""
    setDiff = False
    findPredicate = True

    sqlStatement = "("
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
                    elif n == "X":
                        fromStatement = fromStatement + ", "
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
    runScript(sqlStatement)
    if debug:
        print(sqlStatement) 
    else:
        popupmsg(sqlStatement)

    

button = tkinter.Button(text='Interpret RA Statement', bg = 'blue', fg = 'white', command=interpretRA)
canvas.create_window(300, 180, window = button)
button.pack()

#Awaits button press to run interpretRA with input
root.mainloop()
#END interpretRA   

