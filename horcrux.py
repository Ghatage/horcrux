from encryption import EncryptLayer
from filehandler import FileHandlingLayer
from network import NetworkLayer
from rabin import split_file_by_fingerprints
import os, ipfsapi, configparser

def main(filename):
	horcrux = Horcrux()
	horcrux.read_and_encrypt(filename)
	horcrux.read_and_decrypt(filename)

class Horcrux(object):

	def __init__(self):
		self.fl = FileHandlingLayer()
		self.el = EncryptLayer()
		self.nl = NetworkLayer()
		self.cfg_parser = configparser.RawConfigParser()
		self.cfg_parser.read('config.cfg')

	# Will be called by upload function
	def read_and_encrypt(self, filename):

		# Create hidden directory for filename
		# It will hold the following:
		# -> List file which holds the file and its block listing
		# -> Actual block files held temporarily
		# -> Actual encrypted block files held temporarily
		# Ensure this gets the absolute path
		directory = self.fl.create_hidden_dir(filename)
		hiddendirectory = os.path.split(filename)[0] + '/' + directory

		# Read encryption password from config file
		filepassword = self.cfg_parser['Encryption']['Password']

		result = split_file_by_fingerprints(filename)

		# Loop through result list, create a list of unique block files
		filelist = set()
		for file in result:
			filelist.add(file[3])

		# Write filename :: block file list to .filename.lst
		self.fl.write_list_file(hiddendirectory, filename, result)

		# Loop through unique list of block files, encrypt each one at a time into a file
		encrypted_file_list = self.el.encrypt_all_block_files(filelist,filepassword)

		# Move block files and encrypted files to hidden folder
		self.fl.move_all_block_files(filelist, filename, hiddendirectory)

		# Upload to IPFS, return dict of enc file <-> hash, save that in a new enc.lst
		enc_to_hash_list = self.nl.upload_encrypted_chunks(hiddendirectory, encrypted_file_list)

		# Pickle the enc_to_hash_list FIX HACK OF APPENDING EXTN
		self.fl.write_list_file(hiddendirectory, filename + '.enc2hash', enc_to_hash_list)

		# Remove blk and enc files
		self.fl.remove_files_from_dir(hiddendirectory,'.blk')
		self.fl.remove_files_from_dir(hiddendirectory,'.enc')

	def read_and_decrypt(self, filename):
		# Open the enc file and unpickle the contents, loop thru and print enc and hashes
		# -> Add download from IPFS functionality to the hashes and write those as .blk.enc files
		# -> Loop thru the encrypted files and decrypt them and add them to a string
		# -> re-write the new string to a file and call it target

		# Look for hidden directory with the file name and check if lst and enc.lst files exist.
		hiddendirectory = os.path.split(filename)[0] + '/' + '.' + os.path.split(filename)[1] + '/'
		listfile = hiddendirectory + os.path.split(filename)[1] + '.lst'
		enc2hashfile = hiddendirectory + os.path.split(filename)[1] + '.enc2hash.lst'

		if self.fl.check_if_lst_enc_files_exist(hiddendirectory, listfile, enc2hashfile) == True:
			listfile_contents = self.fl.read_list_file(hiddendirectory, os.path.split(filename)[1])
			enc2hashfile_contents = self.fl.read_list_file(hiddendirectory, os.path.split(filename)[1] + '.enc2hash')
			self.nl.download_encrypted_chunks(hiddendirectory, enc2hashfile_contents)
			self.el.decrypt_chunks(enc2hashfile_contents, 'LOL')
			self.fl.reconstruct_file(listfile_contents,'test1.txt')
			self.fl.remove_files_from_dir('./','.blk')
			self.fl.remove_files_from_dir('./','.enc')
		else:
			return


if __name__ == "__main__":
	main("/Users/aghatage/Documents/PersonalDocs/horcrux/test.txt")

