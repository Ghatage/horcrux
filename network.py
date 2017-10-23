import ipfsapi
import configparser

class NetworkLayer(object):

	def __init__(self):
		self.cfg_parser = configparser.RawConfigParser()
		self.cfg_parser.read('config.cfg')

	def upload_encrypted_chunks(self, hiddendirectory, encrypted_file_list):
		file_to_hash_list = []
		ip, port = self.cfg_parser['Network']['IP'], int(self.cfg_parser['Network']['Port'])
		api = ipfsapi.connect(ip, port)
		for file in encrypted_file_list:
			filename = hiddendirectory + '/' + file
			res = api.add(filename)
			file_to_hash_list.append((file , res['Hash']))
		return file_to_hash_list

	def download_encrypted_chunks(self, hiddendirectory, enc2hashfile_contents):
		ip, port = self.cfg_parser['Network']['IP'], int(self.cfg_parser['Network']['Port'])
		api = ipfsapi.connect(ip, port)
		for enc2hash_tuple in enc2hashfile_contents:
			downloaded_contents = api.cat(enc2hash_tuple[1])
			downloaded_file = open(enc2hash_tuple[0],'wb')
			downloaded_file.write(downloaded_contents)
