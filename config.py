import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

options = dict()

options['api_keys'] =  'AIzaSyDrNsO47enZNTf_1GWo8KuTfqiqNo0k7Fg' # for knowledge graph extraction
options['headers'] = {'User-Agent': 'Mozilla/5.0'}
options["log_path"] =  "logs/test.log"