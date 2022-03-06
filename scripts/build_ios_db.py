import sys, os, sqlite3, hashlib
import magic
from alive_progress import alive_bar

def parse_data(filepath):
    total_files= 0
    for root, dir, files in os.walk(filepath):
        for file in files:
            total_files += 1

    current_count = 0
    with alive_bar(total_files, title="Building database. This might take some time") as bar:
        for root, dir, files in os.walk(filepath):
            for file in files:       
                full_path = os.path.join(root, file)

                if check_if_exists(full_path) == True:
                    pass
                else:
                    file_size = os.path.getsize(full_path)
                    file_type = magic.from_file(full_path)
                    file_hash = get_file_hash(full_path)
                    insert_db("ios_data.db", full_path, file_size, file_type, file_hash)

                current_count += 1
                bar()    




def progress(count, total, status=''):
  bar_len = 60
  filled_len = int(round(bar_len * count / float(total)))

  percents = round(100.0 * count / float(total), 1)
  bar = '=' * filled_len + '-' * (bar_len - filled_len)


  sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
  sys.stdout.flush()




def insert_db(db_path, fpath, file_size, file_type, file_hash):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO ios VALUES (?, ?, ?, ?)", (fpath, file_size, file_type, file_hash))
    con.commit()
    con.close()


def make_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS ios 
            (fpath TEXT, size TEXT, mimetype TEXT, shasum TEXT) 
                ''')
    con.commit()
    con.close()            


def get_file_hash(fpath):
    with open(fpath, "rb") as f:
        bytes = f.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()
        return readable_hash

def check_if_exists(fpath):
    con = sqlite3.connect("ios_data.db")
    c = con.cursor()
    c.execute('''SELECT fpath FROM ios WHERE fpath=?''', (fpath,))
    exists = c.fetchall()
    con.close()  
    if not exists:
        return False
    else:
        return True


