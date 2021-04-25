import csv
import time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs
import json




def gen_read_file(filename):
    with open(filename) as f:
        for row in f:
            yield row.splitlines()[0].split(',')

def list_line_to_dict(gen):
    dict_x = defaultdict(list)
    for row in gen:
        dict_x[row[0]].append(
            [
                row[1],
                row[2]
            ]
        )
    return dict_x


def sort_dict_by_list_value(data):
    for k, v in data.items():
        data[k].sort(key=lambda row: row[1])
    return data


def get_sku(data, value, rank=0):
    try:    
        result = data[value]
    except KeyError:
        result = {}
    if rank == 0:
        return result
    else:
        return [[k, v] for k, v in result if float(v) >= float(rank)]



print('Load structure to RAM')
gen = gen_read_file('recommends.csv')
data = list_line_to_dict(gen)
SORTED_DICT = sort_dict_by_list_value(data)
print('Finish load')


class Handler(BaseHTTPRequestHandler):

    def get_params(self):
        url = self.path
        params = urlparse.urlparse(url)
        return parse_qs(params.query)

    def do_GET(self):
        params = self.get_params()
        if params.get('value'):           
            if params.get('rank'):
                print()
                print(params.get('rank')[0])
                data = get_sku(SORTED_DICT, params.get('value')[0], float(params.get('rank')[0]))
            else:
                data = get_sku(SORTED_DICT, params.get('value')[0])
            
            response_data = json.dumps(data, indent=2).encode('utf-8')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response_data)
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Enter value')



def main():
    address_port = ('0.0.0.0', 5000)
    print(f'Start server http://{address_port[0]}:{address_port[1]}')
    http_server = HTTPServer(address_port, Handler)
    http_server.serve_forever()


if __name__ == '__main__':
    main()