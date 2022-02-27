import os, re, sqlite3, json
from jinja2 import Environment, FileSystemLoader
import math
import subprocess

def make_report(db_path, report_dir):
    print("report_dir:", report_dir)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM ios")
    res = cur.fetchall()
    con.close()

    type_dict = get_mime_type_dict()

    all_data = {
            "size": 0,
            "count": 0
        }

    for entry in res:

        fpath = entry[0]
        size = int(entry[1])
        mime_data = entry[2]

        all_data["count"] += 1
        all_data["size"] += size

        # Search for strings and assign values to dict
        if "JPEG image data" in mime_data:
            type_dict["jpegs"]["count"] += 1
            type_dict["jpegs"]["size"] += size
            type_dict["jpegs"]["filepaths"].append(fpath)
        elif "PNG image data" in mime_data:
            type_dict["pngs"]["count"] += 1
            type_dict["pngs"]["size"] += size
            type_dict["pngs"]["filepaths"].append(fpath)
        elif "Audio" in mime_data:
            type_dict["audio"]["count"] += 1
            type_dict["audio"]["size"] += size
            type_dict["audio"]["filepaths"].append(fpath)
        elif "PDF document" in mime_data:
            type_dict["pdfs"]["count"] += 1
            type_dict["pdfs"]["size"] += size
            type_dict["pdfs"]["filepaths"].append(fpath)
        elif "SQLite 3.x database" in mime_data:
            type_dict["databases"]["count"] += 1
            type_dict["databases"]["size"] += size
            type_dict["databases"]["filepaths"].append(fpath)
        elif "ISO Media, Apple QuickTime movie" in mime_data:
           type_dict["videos"]["count"] += 1
           type_dict["videos"]["size"] += size
           type_dict["videos"]["filepaths"].append(fpath)
        elif "ASCII text" in mime_data:
            type_dict["ascii_text"]["count"] += 1
            type_dict["ascii_text"]["size"] += size
            type_dict["ascii_text"]["filepaths"].append(fpath)
        elif "JSON data" in mime_data:
            type_dict["json_data"]["count"] += 1
            type_dict["json_data"]["size"] += size
            type_dict["json_data"]["filepaths"].append(fpath)
        elif "XML" in mime_data:
            type_dict["xml_data"]["count"] += 1
            type_dict["xml_data"]["size"] += size
            type_dict["xml_data"]["filepaths"].append(fpath)
        elif mime_data == "data":
            type_dict["data"]["count"] += 1
            type_dict["data"]["size"] += size
            type_dict["data"]["filepaths"].append(fpath)

            
    # Write json file for pie chart
    json_data = write_json(type_dict,all_data, report_dir)

    # Convert all data to human
    all_data["size"] = convert_size(all_data["size"]) 

    # Convert everything in dataset from bytes to human
    dataset = bytes_to_human(type_dict)
    # Load the templates and make output
    file_loader = FileSystemLoader('scripts/templates')
    env = Environment(loader=file_loader)
    print(json.dumps(json_data))

    # make data overview
    template = env.get_template('report.html')
    data_overview = template.render(dataset=dataset, all_data=all_data, json_data=json.dumps(json_data))
    write_html(data_overview, report_dir, "report.html")

    # Make contacts page
    template = env.get_template('contacts.html')
    contacts = parse_contacts_csv(report_dir) 
    contacts_page = template.render(contacts=contacts)
    write_html(contacts_page,report_dir,"contacts.html")

    print(report_dir)
    subprocess.run(f"open {report_dir}/report.html", shell=True)

def write_json(type_dict, all_data,report_dir):
    real_sum = all_data["size"]

    known_sum = 0
    for type_size in type_dict:
        known_sum += type_dict[type_size]["size"]
    other_data = real_sum - known_sum

    # calculates percentage
    json_list = []
    for type in type_dict:
        current = type_dict[type]["size"]
        percent_total = (current/real_sum ) * 100
        json_list.append({'y': round(percent_total, 2), 'label': f"{type}"})
    
    # json_list = str(json_list).replace("\'","")
    return json_list 
    # json_pie_dict["other"] = other_data
    # with open(f"{report_dir}/chart.json", 'w') as f:
        # json.dump(json_pie_dict, f)

    print(f"save json file to {report_dir}/chart.json")




def write_html(html_string, report_dir, html_name):
    with open(f"{report_dir}/{html_name}", "w") as f:
        f.writelines(html_string)


def parse_contacts_csv(report_dir):

    contact_list = []
    with open(f"{report_dir}/contacts.csv", "r") as f:
        lines = f.readlines()
        tmp_list = [line.strip().split(",") for line in lines]
        for contact in tmp_list:
            id = contact[0]
            number = contact[1]
            fname = contact[2]
            lname = contact[3]
            contact_list.append({"id":id, "number": number, "fname":fname, "lname": lname})
    return contact_list



def bytes_to_human(dataset):
    new_dict_list = []

    for dtype in dataset:
        size_bytes = dataset[dtype]["size"] 
        new_size = convert_size(size_bytes)
        temp_dict = {
            "type": dtype, 
            "size": new_size, 
            "count": dataset[dtype]["count"],
            "filepaths": dataset[dtype]["filepaths"]
        }
        new_dict_list.append(temp_dict)
        # dataset[dtype]["size"] = new_size
    
    return new_dict_list 

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def get_mime_type_dict():
    mime_type_dict = {
       

        "jpegs" : {
            "type": "jpeg",
            "size" : 0,
            "count": 0,
            "filepaths": []
        },

        "pngs" : {
            "type" : "png",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },

        "audio" : {
            "type": "audio",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },

        "pdfs" : {
            "type": "pdf",
            "size": 0,
            "count" : 0,
            "filepaths": []
        }, 

        "databases" : {
            "type": "sql",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },

        "videos" : {
            "type": "video",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },

        "ascii_text" : {
            "type": "ascii",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },

        "json_data" : {
            "type": "json",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },

        "xml_data" : {
            "type": "xml",
            "size": 0,
            "count" : 0,
            "filepaths": []
        },
        "data":{
            "type": "data",
            "size": 0,
            "count": 0,
            "filepaths": []
        }
    }
    return mime_type_dict
