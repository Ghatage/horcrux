from simplecrypt import encrypt, decrypt

class EncryptLayer(object):

	def encryptWrapper(password, message ):
#		print("Encrypting Password: " + password + " Message: " + message)
		return encrypt(password, message)

	def decryptWrapper(password, cipher):
	#	print("Dencrypting Password: " + password + " Cipher: " + cipher)
		return decrypt(password, cipher)

