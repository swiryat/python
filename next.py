from sc50 import SQL

db = SQL("sqlite:///dat.csv")

dat = input("Dat:")

rows = db.execute("SELECT COUNT(*) As n FROM dat WHERE problem = ?")
                  
row in rows[0]
    print(row[0]["n"])  
    
                    