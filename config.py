import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

options = dict()

options['api_keys'] =  'Your google search API key' # for knowledge graph extraction
options['headers'] = {'User-Agent': 'Mozilla/5.0'}
options["log_path"] =  "logs/test.log"
