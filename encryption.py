from simplecrypt import encrypt, decrypt
import os

class EncryptLayer(object):

	def encryptWrapper(password, message ):
		return encrypt(password, message)

	def decryptWrapper(password, cipher):
		return decrypt(password, cipher)

	def encrypt_all_block_files(filelist, filepassword):
		returnlist = []
		for file in filelist:
			newfile = file + '.enc'
			returnlist.append(newfile)
			newfilefd = open(file,"r");
			write_encrypted(filepassword, newfile, newfilefd.read())
			print (newfile + " written")
		return returnlist

	def write_encrypted(password, filename, plaintext):
	    with open(filename, 'wb') as output:
	        ciphertext = encryptWrapper(password, plaintext)
	        output.write(ciphertext)

	def decrypt_chunks(encfile_list,password):
		for blkfile in encfile_list:
			read_from = open(blkfile[0],'rb')
			read_contents = read_from.read()
			print (read_contents)
			filename = os.path.splitext(blkfile[0])[0]
			print('Decrypting file ' + str(filename))
			blockfile = open(filename,'wb')
		#	blockfile.write(decrypt(password, read_contents))
			blockfile.close()
			read_from.close()
