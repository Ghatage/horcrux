from simplecrypt import encrypt, decrypt

class EncryptLayer(object):

	def encryptWrapper(password, message ):
		return encrypt(password, message)

	def decryptWrapper(password, cipher):
		return decrypt(password, cipher)

