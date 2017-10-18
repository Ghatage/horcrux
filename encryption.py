from simplecrypt import encrypt, decrypt
import os, pickle

class EncryptLayer(object):

	def encryptWrapper(password, message):
		return encrypt(password, message)

	def decryptWrapper(password, cipher):
		return decrypt(password, cipher)

	def encrypt_all_block_files(filelist, filepassword):
		print(filelist)
		returnlist = []
		for file in filelist:
			blkfilefd = open(file,"r")
			plaintext = blkfilefd.read()
			print(type(plaintext.encode('utf8')))
			print(plaintext)
			enc_blk_file_name = file + '.enc'
			enc_fd = open(enc_blk_file_name, 'wb')
			ciphertext = encrypt(filepassword, plaintext.encode('utf8'))
			pickle.dump(ciphertext,enc_fd,protocol=pickle.HIGHEST_PROTOCOL)
			print (enc_blk_file_name + " written")

			returnlist.append(enc_blk_file_name)
		return returnlist

	def decrypt_chunks(encfile_list,password):
		print(str(encfile_list))
		for blkfile in encfile_list:
			read_from_enc_file = open(blkfile[0],'rb')
			print("Opened " + blkfile[0] + " for reading in binary")
			filename = os.path.splitext(blkfile[0])[0]

			read_contents = pickle.load(read_from_enc_file)
			print('Decrypting file ' + str(blkfile[0]))
			data_to_write = decrypt(password, read_contents)

			blockfile = open(filename,'wb')
			blockfile.write(data_to_write)
			blockfile.close()
			read_from_enc_file.close()
