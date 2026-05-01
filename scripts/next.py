from sc50 import SQL

db = SQL("sqlite:///dat.csv")

dat = input("Dat:")

rows = db.execute("SELECT COUNT(*) As n FROM dat WHERE problem = ?", dat)

if rows:
    print(rows[0]["n"])
else:
    print("No matching rows found.")
    
                    