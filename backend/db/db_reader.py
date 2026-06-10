#import sqlite3
#import csv
#import pandas as pd
#import os

#def export_to_csv():
    #conn = sqlite3.connect("Database/db.sqlite3")
    #cursor = conn.cursor()

    #query = "SELECT * FROM notes_notes"
    #cursor.execute(query)
    #rows = cursor.fetchall()

    #with open("teacher_notes.csv", "w", newline="", encoding="utf-8") as file:
        #writer = csv.writer(file)

       # writer.writerow([i[0] for i in cursor.description])
        #writer.writerows(rows)

    #conn.close()
    #print("✅ CSV exported successfully!")

#export_to_csv()

####step2###
print("File is running...")
import sqlite3
import pandas as pd
import os
import re
from datetime import datetime


def clean_text(value):
    if isinstance(value, str):
        value = value.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        value = value.encode("ascii", "ignore").decode()
        value = re.sub(r'[\x00-\x1F\x7F]', '', value)
        return value.strip()
    return value


def export_reports():
    print("Generating reports...")

    import sqlite3, os
    import pandas as pd
    from datetime import datetime

    conn = sqlite3.connect("Database/db.sqlite3")

    query = """
    SELECT 
        Created_date,
        Username,
        User_id,
        Grade,
        School,
        What_I_prepared,
        What_I_did_well,
        What_went_well,
        Where_to_improve
    FROM Notes_notes
    WHERE School IN ('Udavi', 'Isaiambalam', 'Government School', 'Aikiyam', 'NES')
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print("Total rows:", len(df))

    # Clean data
    df = df.applymap(clean_text)

    # Fix column names (IMPORTANT)
    df.columns = df.columns.str.strip()

    # Convert date
    #df['Created_date'] = pd.to_datetime(df['Created_date'], errors='coerce')
    df['Created_date'] = pd.to_datetime(df['Created_date'], errors='coerce').dt.date

    # Sort full data
    df = df.sort_values(by=['School', 'Grade', 'Created_date'])

    # Create Output folder
    os.makedirs("Output", exist_ok=True)

    filename = f"Output/final_report_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    # =========================
    # MULTIPLE SHEETS (School + Grade)
    # =========================
    with pd.ExcelWriter(filename) as writer:

        for school in df['School'].unique():
            school_df = df[df['School'] == school]

            for grade in school_df['Grade'].unique():
                grade_df = school_df[school_df['Grade'] == grade]

                sheet_name = f"{school}_{grade}"

                # Excel sheet name limit = 31 chars
                sheet_name = sheet_name[:31]

                grade_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ Final report created: {filename}")
    
export_reports()