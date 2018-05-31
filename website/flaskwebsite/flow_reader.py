# import csv
#
# with open('stats.csv') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#
#     print(csv_reader)
#
#     with open('new_stats.csv') as new_file:
#         field_names = ['first_name', 'last_name', 'email']
#         csv_writer = csv.writer(new_file, delimiter='-')
#
#         csv_writer = csv.DictWriter(new, fieldnames=field_names, delimiter='\t')
#          # skips first line: next(csv_reader)
#         for line in csv_reader:
#             csv_writer.writerow(line)
#
#
#     #dictionary reader/writer
#
# def clear_file(filename):
#     f = open(filename, 'r+')
#     f.truncate()

import time
import json
import requests
switch_stats = '''{
    "72520098379858177": [
        {
            "actions": [
                "OUTPUT:NORMAL"
            ],
            "idle_timeout": 0,
            "cookie": 0,
            "packet_count": 2,
            "hard_timeout": 0,
            "byte_count": 146,
            "duration_sec": 61,
            "duration_nsec": 434000000,
            "priority": 10,
            "length": 104,
            "flags": 0,
            "table_id": 0,
            "match": {
                "dl_type": 2048,
                "nw_proto": 17,
                "nw_src": "1.0.0.1",
                "tp_dst": 53
            }
        },
        {
            "actions": [
                "OUTPUT:NORMAL"
            ],
            "idle_timeout": 0,
            "cookie": 0,
            "packet_count": 2,
            "hard_timeout": 0,
            "byte_count": 178,
            "duration_sec": 61,
            "duration_nsec": 433000000,
            "priority": 10,
            "length": 104,
            "flags": 0,
            "table_id": 0,
            "match": {
                "dl_type": 2048,
                "tp_src": 53,
                "nw_proto": 17,
                "nw_dst": "1.0.0.1"
            }
        },
        {
            "actions": [
                "OUTPUT:3",
                "OUTPUT:NORMAL"
            ],
            "idle_timeout": 0,
            "cookie": 0,
            "packet_count": 52,
            "hard_timeout": 0,
            "byte_count": 7154,
            "duration_sec": 61,
            "duration_nsec": 407000000,
            "priority": 5,
            "length": 96,
            "flags": 0,
            "table_id": 0,
            "match": {}
        }
    ]
}'''

# data = json.loads(switch_stats)
# for flow in data["72520098379858177"]:
#     print flow
# print data
while True:
    dlfile = open("dl_usage.txt", "w")
    upfile = open("up_usage.txt", "w")
    totfile = open("tot_usage.txt", "w")
    print("------------------------------------")

    http_total = 0
    https_total = 0
    dns_total = 0
    ssh_total = 0
    other_total = 0

    req = requests.get('http://localhost:8080/stats/flow/72520098379858177')
    # print(req.jsorn())
    stats = json.loads(req.text)
    print(type(stats))
    print(type(stats["72520098379858177"]))
    for flows in stats["72520098379858177"]:
        # Handle HTTPS
        if flows["priority"] == 15:
            if 'nw_src' in flows["match"].keys():
                print("HTTPS query up stats: {} bytes uploaded ".format(flows["byte_count"]))
                string = "https " + str(flows["byte_count"]) + "\n"
                upfile.write(string)
            else:
                print("HTTPS query down stats: {} bytes downloaded ".format(flows["byte_count"]))
                string = "https " + str(flows["byte_count"])+ "\n" 
                dlfile.write(string)
            # Handle total
            https_total += flows["byte_count"]
            

        # Handle HTTP
        elif flows["priority"] == 16:
            if 'nw_src' in flows["match"].keys():
                print("HTTP query up stats: {} bytes uploaded ".format(flows["byte_count"]) )
                string = "http " + str(flows["byte_count"])+ "\n"
                upfile.write(string)
            else:
                print("HTTP query down stats: {} bytes downloaded ".format(flows["byte_count"]))
                string = "http " + str(flows["byte_count"]) + "\n"
                dlfile.write(string)
            http_total += flows["byte_count"]

        # Handle DNS
        elif flows["priority"] == 10:
            if 'nw_src' in flows["match"].keys():
                print("DNS query up stats: {} bytes uploaded ".format(flows["byte_count"]))
                string = "dns " + str(flows["byte_count"]) + "\n"
                upfile.write(string)
            else:
                print("DNS query down stats: {} bytes downloaded ".format(flows["byte_count"]))
                string = "dns " + str(flows["byte_count"]) + "\n"
                dlfile.write(string)
            dns_total += flows["byte_count"]

        # Handle SSH
        elif flows["priority"] == 14:
            if 'nw_src' in flows["match"].keys():
                print("SSH query up stats: {} bytes uploaded ".format(flows["byte_count"]))
                string = "ssh " + str(flows["byte_count"]) + "\n"
                upfile.write(string)
            else:
                print("SSH query down stats: {} bytes downloaded ".format(flows["byte_count"]))
                string = "ssh " + str(flows["byte_count"]) + "\n"
                dlfile.write(string)
            ssh_total += flows["byte_count"]

        # Handle other
        elif flows["priority"] == 2:
            if 'nw_src' in flows["match"].keys():
                print("Other query up stats: {} bytes uploaded ".format(flows["byte_count"]))
                string = "other " + str(flows["byte_count"]) + "\n"
                upfile.write(string)
            else:
                print("Other query down stats: {} bytes downloaded ".format(flows["byte_count"]))
                string = "other " + str(flows["byte_count"]) + "\n"
                dlfile.write(string)
            other_total += flows["byte_count"]

    totfile.write("http " + str(http_total) + "\n")
    totfile.write("https " + str(https_total) + "\n")
    totfile.write("dns " + str(dns_total) + "\n")
    totfile.write("ssh " + str(ssh_total) + "\n")
    totfile.write("other " + str(other_total) + "\n")
    totfile.close()
    upfile.close()
    dlfile.close()
    print("------------------------------------")
    time.sleep(5)

