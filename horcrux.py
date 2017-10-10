from encryption import EncryptLayer
from rabin import split_file_by_fingerprints
from simplecrypt import encrypt, decrypt
from configparser import SafeConfigParser
import os, shutil, pickle, ipfsapi

def main(filename):
	read_and_encrypt(filename)
	read_and_decrypt(filename)	


# Will be called by upload function
def read_and_encrypt(filename):

	# Create hidden directory for filename
	# It will hold the following:
	# -> List file which holds the file and its block listing
	# -> Actual block files held temporarily
	# -> Actual encrypted block files held temporarily

	# Ensure this gets the absolute path
	directory = create_hidden_dir(filename)

	# Read encryption password from config file
	filepassword = 'LOL'

	result = split_file_by_fingerprints(filename)

	# Loop through result list, create a list of unique block files
	filelist = set()
	for file in result:
		filelist.add(file[3])

	# Write filename :: block file list to .filename.lst
	hiddendirectory = os.path.split(filename)[0] + '/' + directory
	write_list_file(hiddendirectory, filename, result)

	# Loop through unique list of block files, encrypt each one at a time into a file
	# fetch the password from the config file
	encrypted_file_list = encrypt_all_block_files(filelist,filepassword)

	# Move block files and encrypted files to hidden folder
	move_all_block_files(filelist, filename, hiddendirectory)

	# Upload to IPFS, return dict of enc file <-> hash, save that in a new enc.lst
	enc_to_hash_list = upload_encrypted_chunks(hiddendirectory, encrypted_file_list)
	# print (enc_to_hash_list)

	# Pickle the enc_to_hash_list
	write_list_file(hiddendirectory, filename + '.enc2hash', enc_to_hash_list)

	# Unpickle and read the enc2hash list
	print(read_list_file(hiddendirectory, filename + '.enc2hash'))

	# Remove blk and enc files
	remove_files_from_dir(hiddendirectory,'.blk')
	remove_files_from_dir(hiddendirectory,'.enc')

def write_encrypted(password, filename, plaintext):
    with open(filename, 'wb') as output:
        ciphertext = EncryptLayer.encryptWrapper(password, plaintext)
        output.write(ciphertext)

def encrypt_all_block_files(filelist, filepassword):
	returnlist = []
	for file in filelist:
		newfile = file + '.enc'
		returnlist.append(newfile)
		newfilefd = open(file,"r");
		write_encrypted(filepassword, newfile, newfilefd.read())
		print (newfile + " written")
	return returnlist

def move_all_block_files(filelist, filename, hiddendirectory):
	for blockfile in filelist:
		shutil.move(os.path.split(filename)[0] + '/' + blockfile, hiddendirectory)
	for blockfile in filelist:
		shutil.move(os.path.split(filename)[0] + '/' + blockfile + '.enc', hiddendirectory)

def write_list_file(hiddendirectory, filename, result):
	with open(hiddendirectory + '/' + os.path.basename(filename) + '.lst', 'wb') as listfile:
		pickle.dump(result, listfile, protocol=pickle.HIGHEST_PROTOCOL)

def read_list_file(hiddendirectory, filename):
	with open(hiddendirectory + '/' + os.path.basename(filename) + '.lst', 'rb') as listfile:
		return pickle.load(listfile)

def create_hidden_dir(filename):
	directory = "." + os.path.basename(filename)
	if not os.path.exists(directory):
		os.makedirs(directory)
	return directory

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

def remove_files_from_dir(hiddendirectory, pattern):
	filelist = [ f for f in os.listdir(hiddendirectory) if f.endswith(pattern) ]
	for f in filelist:
		os.remove(os.path.join(hiddendirectory, f))

def read_and_decrypt(filename):
	print ("In Read and Decrypt: " + filename)
#	plaintext = EncryptLayer.decryptWrapper("One",cipher)
#	print("Decrypted: " + plaintext.decode('utf8'))

if __name__ == "__main__":
	main("/Users/aghatage/Documents/PersonalDocs/horcrux/test.txt")

