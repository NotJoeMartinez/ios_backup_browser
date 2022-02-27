import sqlite3, os, csv, shutil, subprocess
from pathlib import Path
import datetime as dt

def find_contacts(db_path, report_dir):
    ## search for Manifest.db
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM ios")
    res = cur.fetchall()
    con.close()

    # copy  Manifest.db to tmp dir
    manifest = ""
    for row in res:
        fpath = row[0]
        size = int(row[1])
        mime_data = row[2]
        if "Manifest.db" in fpath:
            manifest = fpath
            break 

    tmp_manifest = f"/tmp/Manifest.db"
    shutil.copyfile(manifest,tmp_manifest)

    # search manifest.db for the file id of our address book
    con = sqlite3.connect(tmp_manifest)
    cur = con.cursor()
    cur.execute("SELECT fileID FROM Files WHERE relativePath = 'Library/AddressBook/AddressBook.sqlitedb' ")
    res = cur.fetchall()
    con.close()
    file_id = res[0][0]


    # search our database for this the address book given the file id
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(f"SELECT fpath FROM ios WHERE fpath LIKE '%{file_id}%'")
    res = cur.fetchall()
    con.close()
    address_book_path = res[0][0]

    # copy address book to tmp
    tmp_address_book_path = f"/tmp/{file_id}.db"
    shutil.copyfile(address_book_path, tmp_address_book_path)

    # Search this database for our contacts

    con = sqlite3.connect(tmp_address_book_path)
    cur = con.cursor()

    #  Stole this from  
    # https://github.com/abrignoni/iLEAPP/blob/2657d4a2840ec819e1e8ed4dd2ed44cc8ccbd050/scripts/artifacts/addressBook.py

    cur.execute(""" 
    SELECT 
    ABPerson.ROWID,
    c16Phone,
    FIRST,
    MIDDLE,
    LAST,
    c17Email,
    DATETIME(CREATIONDATE+978307200,'UNIXEPOCH'),
    DATETIME(MODIFICATIONDATE+978307200,'UNIXEPOCH'),
    NAME
    FROM ABPerson
    LEFT OUTER JOIN ABStore ON ABPerson.STOREID = ABStore.ROWID
    LEFT OUTER JOIN ABPersonFullTextSearch_content on ABPerson.ROWID = ABPersonFullTextSearch_content.ROWID
    """)

    res = cur.fetchall()
    con.close()

    csv_list = []

    for row in res:
        if row[1] is not None:
            numbers = row[1].split(" +")
            number = numbers[1].split(" ")
            phone_number = "+{}".format(number[0])
        else:
            phone_number = ''

        contact_id = row[0]
        first_name = row[2]
        last_name = row[4]

        csv_list.append([contact_id, phone_number, first_name, last_name])

    with open(f"{report_dir}/contacts.csv", "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(['contact_id','phone_number', 'first_name', 'last_name'])
        for row in csv_list:
            writer.writerow(row)
    print(f"Wrote contacts to {report_dir}/contacts.csv") 
    
  
 
    
  

    subprocess.run("rm /tmp/*.db ", shell=True)
    






