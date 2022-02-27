
import os, sqlite3, shutil
from pathlib import Path

def export_media(db_path, output_dir):
    get_jpegs(db_path,output_dir)

def get_jpegs(db_path, output_dir):
    new_jpeg_dir = f"{output_dir}/jpegs"
    os.makedirs(new_jpeg_dir)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM ios")
    res = cur.fetchall()
    con.close()

    move_list = []
    for row in res:
        if "JPEG image data" in row[2]:
            move_list.append(row[0])
    
    for jpeg in move_list:
        og_jpeg_name = Path(jpeg).stem
        new_jpeg_fpath = f"{new_jpeg_dir}/{og_jpeg_name}.JPEG"
        shutil.copyfile(jpeg, new_jpeg_fpath)
    print(f"Moved all jpegs to {new_jpeg_dir}")
            





