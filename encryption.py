from simplecrypt import encrypt, decrypt
import os, pickle

class EncryptLayer(object):

	def encryptWrapper(password, message):
		return encrypt(password, message)

	def decryptWrapper(password, cipher):
		return decrypt(password, cipher)

	def encrypt_all_block_files(filelist, encryption_password):
		list_of_encrypted_files = []
		for file in filelist:
			encrypted_filename = file + '.enc'

			block_file_handle = open(file,'rb')
			encrypted_file_handle = open(encrypted_filename, 'wb')

			plaintext = block_file_handle.read().decode('utf8')
			ciphertext = encrypt(encryption_password, plaintext.encode('utf8'))

			pickle.dump(ciphertext, encrypted_file_handle, protocol=pickle.HIGHEST_PROTOCOL)
			print ('Encrypting file ' + encrypted_filename)

			list_of_encrypted_files.append(encrypted_filename)

			block_file_handle.close()
			encrypted_file_handle.close()
		return list_of_encrypted_files

	def decrypt_chunks(list_of_encrypted_files, encryption_password):
		for encrypted_file_name in list_of_encrypted_files:
			read_from_enc_file = open(encrypted_file_name[0],'rb')
			filename = os.path.splitext(encrypted_file_name[0])[0]

			read_contents = pickle.load(read_from_enc_file)
			print('Decrypting file ' + str(encrypted_file_name[0]))
			data_to_write = decrypt(encryption_password, read_contents)

			block_file_handle = open(filename,'wb')
			block_file_handle.write(data_to_write)
			block_file_handle.close()
			read_from_enc_file.close()
