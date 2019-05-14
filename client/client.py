# -*- coding: utf-8 -*-
import sys, requests, logging
from sample_pb2 import Sample, Activity, Location
from google.protobuf.json_format import Parse

REMOTE_URL = 'http://localhost:8000'

def send_protobuf(filename, remote_url):
    """
    send_protobuf will open the filename,
    read each lines, serialize the line to protobuf bytes string,
    and send out as requests body.
    """
    with open(filename, "r") as f:
        data = f.readlines()
        for d in data:
            sample = Sample()
            Parse(d, sample)

            # Send out the protobuf message
            r = requests.post(remote_url, data=sample.SerializeToString(), headers={'Content-type': 'application/x-protobuf'})
            # If not POSTed successfully, show error message
            if r.status_code != 201:
                logging.error('{} - {}'.format(r.status_code, r.text))
            else:
                logging.info('{} - {}'.format(r.status_code, r.text))

if __name__ == '__main__':

    # Set logging level INFO
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Prompt user to filename
    # If there should be no filename, exit
    filename = input('Enter filename: ')
    if len(filename) == 0:
        logging.warning('Filename is empty')
        sys.exit(1)

    # Prompt user for server address
    # if there is none, use default REMOTE_URL
    remote_url = input('Enter remote server address: ')
    if len(remote_url) == 0:
        logging.info('Remote url is empty. Use default localhost:8000')
        remote_url = REMOTE_URL

    # Use the filename and remote address to send protobuf
    send_protobuf(filename, remote_url)
