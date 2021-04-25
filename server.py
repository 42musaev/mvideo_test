import csv
import time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs
import json




def read_file_to_dict(filename):
    x_dixt = defaultdict(list)
    with open(filename, 'r') as f:
        data = csv.DictReader(f, fieldnames=['sku', 'r_sku', 'rank'])
        iter = 0
        for row in data:
            iter += 1
            if iter == 1000000:
                break
            x_dixt[row['sku']].append({row['r_sku']: row['rank']})
    return dict(x_dixt)


def sort_dict_by_list_value(data):
    for k, v in data.items():
        data[k].sort(key=lambda d: sorted(list(d.values()), reverse=True))
    return data


def get_sku(data, value, rank=0):
    try:    
        result = data[value]
    except KeyError:
        result = {}
    if rank == 0:
        return result
    else:
        return [d for d in result for k, v in d.items() if float(v) >= rank]



print('Load structure to RAM')
f = read_file_to_dict('recommends.csv')
SORTED_DICT = sort_dict_by_list_value(f)
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
    print('Start server')
    http_server = HTTPServer(('0.0.0.0', 5000), Handler)
    http_server.serve_forever()


if __name__ == '__main__':
    main()