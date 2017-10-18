import ipfsapi

class NetworkLayer(object):
	
	def upload_encrypted_chunks(hiddendirectory, encrypted_file_list):
		# ipfs add the encrypted file:: Make this configurable
		hash_list = []
		api = ipfsapi.connect('127.0.0.1', 5001)
		for file in encrypted_file_list:
			filename = hiddendirectory + '/' + file
			res = api.add(filename)
			print ("File: " + filename + "Hash: " + res['Hash'])
			hash_list.append((file , res['Hash']))
		return hash_list

	def download_encrypted_chunks(enc2hashfile_contents):
		api = ipfsapi.connect('127.0.0.1', 5001)
		for enc2hash_tuple in enc2hashfile_contents:
			blockfile = api.cat(enc2hash_tuple[1])
			blkfile = open(enc2hash_tuple[0],'wb')
#			blkfile.write(str(EncryptLayer.decryptWrapper('LOL',blockfile)))
			blkfile.write(blockfile)
