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

data = json.loads(switch_stats)
# for flow in data["72520098379858177"]:
#     print flow
# print data


req = requests.get('http://localhost:8080/stats/flow/72520098379858177')
# print(req.jsorn())
stats = json.loads(req.text)
print(type(stats))
print(type(stats["72520098379858177"]))
for flows in stats["72520098379858177"]:
    if flows["priority"] == 10:
        if 'nw_src' in flows["match"].keys():
            print("DNS query up stats: {} bytes uploaded ".format(flows["byte_count"]) )
        else:
            print("DNS query down stats: {} bytes downloaded ".format(flows["byte_count"]))