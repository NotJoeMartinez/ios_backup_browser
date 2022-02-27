import argparse, os, sqlite3 
from scripts import *
from scripts import find_db_contacts 

def main(args):
    make_db("ios_data.db")
    if args.find_mimes:
        parse_data(args.find_mimes)
    if args.data_report:
        report_dir = make_report_dir()
        find_contacts("ios_data.db", report_dir)
        make_report("ios_data.db", report_dir)
    if args.find_contacts:
        report_dir = make_report_dir()
        find_contacts("ios_data.db", report_dir)
    if args.export_media:
        output_dir = args.export_media
        export_media("ios_data.db", output_dir)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='iOS forensic tool')
    parser.add_argument('-fm','--find-mimes', action="store", help='pass it a directory of ios extraction')
    parser.add_argument('-dr','--data-report', action="store_true", help='generate html showing stuff')
    parser.add_argument('-fc','--find-contacts', action="store_true", help='Print data of current DB')
    parser.add_argument('-em','--export-media', action="store", help='Save media from backup to specified directory')

    args = parser.parse_args()
    main(args)