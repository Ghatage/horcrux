from encryption import EncryptLayer
from rabin import split_file_by_fingerprints
from simplecrypt import encrypt, decrypt
import os, shutil

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

	# ipfs add the encrypted file


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
	listfile = open(hiddendirectory + '/' + os.path.basename(filename) + '.lst', "w")
	listfile.write(str(result))
	listfile.close()

def create_hidden_dir(filename):
	directory = "." + os.path.basename(filename)
	if not os.path.exists(directory):
		os.makedirs(directory)
	return directory


def read_and_decrypt(filename):
	print ("In Read and Decrypt: " + filename)
#	plaintext = EncryptLayer.decryptWrapper("One",cipher)
#	print("Decrypted: " + plaintext.decode('utf8'))

if __name__ == "__main__":
	main("/Users/aghatage/Documents/PersonalDocs/horcrux/test.txt")

