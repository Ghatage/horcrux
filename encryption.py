from simplecrypt import encrypt, decrypt
import os, pickle

class EncryptLayer(object):

	def encryptWrapper(password, message):
		return encrypt(password, message)

	def decryptWrapper(password, cipher):
		return decrypt(password, cipher)

	def encrypt_all_block_files(filelist, filepassword):
		returnlist = []
		for file in filelist:
			blkfilefd = open(file,"r")
			plaintext = blkfilefd.read()
			enc_blk_file_name = file + '.enc'
			enc_fd = open(enc_blk_file_name, 'wb')
			ciphertext = encrypt(filepassword, plaintext.encode('utf8'))
			pickle.dump(ciphertext,enc_fd,protocol=pickle.HIGHEST_PROTOCOL)
			print ('Encrypting file ' + enc_blk_file_name)

			returnlist.append(enc_blk_file_name)
		return returnlist

	def decrypt_chunks(encfile_list,password):
		for blkfile in encfile_list:
			read_from_enc_file = open(blkfile[0],'rb')
			filename = os.path.splitext(blkfile[0])[0]

			read_contents = pickle.load(read_from_enc_file)
			print('Decrypting file ' + str(blkfile[0]))
			data_to_write = decrypt(password, read_contents)

			blockfile = open(filename,'wb')
			blockfile.write(data_to_write)
			blockfile.close()
			read_from_enc_file.close()
