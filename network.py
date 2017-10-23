import ipfsapi
import configparser

class NetworkLayer(object):
	
	def upload_encrypted_chunks(hiddendirectory, encrypted_file_list):
		# ipfs add the encrypted file:: Make this configurable
		cfg_parser = configparser.RawConfigParser()
		cfg_parser.read('config.cfg')

		file_to_hash_list = []
		ip, port = cfg_parser['Network']['IP'], int(cfg_parser['Network']['Port'])
		api = ipfsapi.connect(ip, port)
		for file in encrypted_file_list:
			filename = hiddendirectory + '/' + file
			res = api.add(filename)
			file_to_hash_list.append((file , res['Hash']))
		return file_to_hash_list

	def download_encrypted_chunks(hiddendirectory, enc2hashfile_contents):
		api = ipfsapi.connect('127.0.0.1', 5001)
		for enc2hash_tuple in enc2hashfile_contents:
			downloaded_contents = api.cat(enc2hash_tuple[1])
			downloaded_file = open(enc2hash_tuple[0],'wb')
			downloaded_file.write(downloaded_contents)
