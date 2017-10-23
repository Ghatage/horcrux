import os, shutil, pickle

class FileHandlingLayer(object):

	def write_list_file(self, directory, filename, result):
		with open(directory + '/' + os.path.basename(filename) + '.lst', 'wb') as listfile:
			pickle.dump(result, listfile, protocol=pickle.HIGHEST_PROTOCOL)

	def read_list_file(self, directory, filename):
		with open(directory + '/' + os.path.basename(filename) + '.lst', 'rb') as listfile:
			return pickle.load(listfile)

	def move_all_block_files(self, filelist, filename, directory):
		for blockfile in filelist:
			shutil.move(os.path.split(filename)[0] + '/' + blockfile, directory)
		for blockfile in filelist:
			shutil.move(os.path.split(filename)[0] + '/' + blockfile + '.enc', directory)

	def remove_files_from_dir(self, directory, pattern):
		filelist = [ f for f in os.listdir(directory) if f.endswith(pattern) ]
		for f in filelist:
			os.remove(os.path.join(directory, f))

	def create_hidden_dir(self, filename):
		directory = "." + os.path.basename(filename)
		if not os.path.exists(directory):
			os.makedirs(directory)
		return directory

	def check_if_lst_enc_files_exist(self, directory, listfile, enc2hashfile):
		if os.path.isdir(directory):
			if os.path.exists(listfile) and os.path.exists(enc2hashfile):
				return True
			else:
				print ("No such file, returning")
				return False
		else:
			print ("No such file, returning")
			return False

	def reconstruct_file(self, listfile_contents, filename):
		reconstructed_file = open(filename,'w')
		for item in listfile_contents:
			print('Writing file: ' + item[3])
			file = open(item[3],'r')
			reconstructed_file.write(file.read())
			file.close()
		reconstructed_file.close()
