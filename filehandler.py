import os, shutil, pickle

class FileHandlingLayer(object):

	def write_list_file(hiddendirectory, filename, result):
		with open(hiddendirectory + '/' + os.path.basename(filename) + '.lst', 'wb') as listfile:
			pickle.dump(result, listfile, protocol=pickle.HIGHEST_PROTOCOL)

	def read_list_file(hiddendirectory, filename):
		with open(hiddendirectory + '/' + os.path.basename(filename) + '.lst', 'rb') as listfile:
			return pickle.load(listfile)

	def move_all_block_files(filelist, filename, hiddendirectory):
		for blockfile in filelist:
			shutil.move(os.path.split(filename)[0] + '/' + blockfile, hiddendirectory)
		for blockfile in filelist:
			shutil.move(os.path.split(filename)[0] + '/' + blockfile + '.enc', hiddendirectory)

	def remove_files_from_dir(hiddendirectory, pattern):
		filelist = [ f for f in os.listdir(hiddendirectory) if f.endswith(pattern) ]
		for f in filelist:
			os.remove(os.path.join(hiddendirectory, f))

	def create_hidden_dir(filename):
		directory = "." + os.path.basename(filename)
		if not os.path.exists(directory):
			os.makedirs(directory)
		return directory

	def check_if_lst_enc_files_exist(hiddendirectory, listfile, enc2hashfile):
		if os.path.isdir(hiddendirectory):
			if os.path.exists(listfile) and os.path.exists(enc2hashfile):
				return True
			else:
				print ("No such file, returning")
				return False
		else:
			print ("No such file, returning")
			return False

	def reconstruct_file(listfile_contents, filename):
		mainfile = open(filename,'w')
		for item in listfile_contents:
			print('Writing file: ' + item[3])
			file = open(item[3],'r')
			mainfile.write(file.read())
			file.close()
		mainfile.close()
