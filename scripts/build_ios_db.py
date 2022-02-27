import sys, os, sqlite3
import magic
from alive_progress import alive_bar

def parse_data(filepath):
    total_files= 0
    for root, dir, files in os.walk(filepath):
        for file in files:
            total_files += 1

    current_count = 0
    with alive_bar(total_files) as bar:
        for root, dir, files in os.walk(filepath):
            for file in files:       
                full_path = os.path.join(root, file)
                file_size = os.path.getsize(full_path)
                file_type = magic.from_file(full_path)
                current_count += 1
                # progress(current_count, total_files)
                insert_db("ios_data.db", full_path, file_size, file_type)
                bar()    




def progress(count, total, status=''):
  bar_len = 60
  filled_len = int(round(bar_len * count / float(total)))

  percents = round(100.0 * count / float(total), 1)
  bar = '=' * filled_len + '-' * (bar_len - filled_len)


  sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
  sys.stdout.flush()




def insert_db(db_path, fpath, file_size, file_type):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO ios VALUES (?, ?, ?)", (fpath, file_size, file_type))
    con.commit()
    con.close()


def make_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS ios 
            (fpath TEXT, size TEXT, mimetype TEXT) 
                ''')
    con.commit()
    con.close()            
