
import os, sqlite3, shutil
from pathlib import Path
from alive_progress import alive_bar
from alive_progress import config_handler



## TODO: Error checking if datatype does not exist
## TODO: distinguish XML/ASCII

def export_media(db_path, output_dir):
    move_mime(db_path,output_dir,"pdf","PDF document")
    move_mime(db_path,output_dir,"db","SQLite 3.x database")
    move_mime(db_path,output_dir,"JPEG","JPEG image data")
    move_mime(db_path,output_dir,"png","PNG image data")
    move_mime(db_path,output_dir,"m4a","(.M4A) Audio")
    move_mime(db_path,output_dir,"MP4","ISO Media, MP4")
    move_mime(db_path,output_dir,"mov","ISO Media, Apple QuickTime movie, Apple QuickTime (.MOV/QT)")


def move_mime(db_path, output_dir, extention, keywords):
    output_dir= f"{output_dir}/{extention}s"

    if os.path.isdir(output_dir):
        pass
    else:
        os.makedirs(output_dir)

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM ios")
    res = cur.fetchall()
    con.close()

    move_list = []
    sha_list = []
    for row in res:
        if keywords in row[2]:
            # prevent from moving duplicates
            if row[3] in sha_list:
                pass
            else:
                move_list.append(row[0])
                sha_list.append(row[3])

    total_files = len(move_list)
    with alive_bar(total_files, title=f"Moving {extention}") as bar:
        for artifact in move_list:
            og_artifact_name = Path(artifact).stem
            new_af_path = f"{output_dir}/{og_artifact_name}.{extention}"
            shutil.copyfile(artifact, new_af_path)
            bar()

    print(f"Moved all {extention}s to {output_dir}")
