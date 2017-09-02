import sys
import os


import logging
import io
from logging import StreamHandler, DEBUG
from os.path import dirname, abspath
from tempfile import mkstemp
from docopt import docopt
import shutil
import errno
from pathlib import Path
import subprocess


# If you add #{project} in a file, add the file ext here
REWRITE_FILE_EXTS = ('.html', '.conf', '.py', '.json', '.md', '.yaml', '.sh')
BASE_DIR = Path(__file__).parents[1]

logger = logging.getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


def bot_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/<bot>/<filename>,aiml
	return os.path.join(dirname(BASE_DIR), 'program-y/bots', '{0}/{1}.aiml'.format(instance.bot.slug, instance.name))


def _mkdir_p(path):
	"""mkdir -p path"""
	try:
		os.makedirs(path)
		print(os.makedirs(path))
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

	else:
		logger.info("New: %s%s", path, os.path.sep)


def _rewrite_and_copy(src_file, dst_file, project_name):
	"""Replace vars and copy."""
	# Create temp file
	fh, abs_path = mkstemp()

	with io.open(abs_path, 'w', encoding='utf-8') as new_file:
		with io.open(src_file, 'r', encoding='utf-8') as old_file:
			for line in old_file:
				new_line = line.replace('#{project}', project_name). \
					replace('#{project|title}', project_name.title())
				new_file.write(new_line)

	# Copy to new file
	shutil.copy(abs_path, dst_file)
	os.close(fh)


def _relative_path(absolute_path):
	current_path = os.getcwd()
	return absolute_path.split(current_path)[1][1:]


def run_client(project_name):
	with open(os.path.join(dirname(BASE_DIR), 'program-y/bots', project_name, '{}-rest.sh'.format(project_name)), 'rb') as file:
		script = file.read()
		rc = subprocess.call(script, shell=True)


def generate_bot(data):
	src = os.path.join(dirname(BASE_DIR),'program-y/bots/bot-template')
	
	slug = data['slug']
	port = data['port']
	
	project_name = slug

	if not project_name:
		logger.warning('Project name cannot be empty.')
		return

	# Destination project path
	dst = os.path.join(dirname(BASE_DIR), 'program-y/bots', project_name)
	print(dst)	
	
	if os.path.isdir(dst):
		logger.warning('Project directory already exists.')
		return

	logger.info('Start generating project files.')

	_mkdir_p(dst)
	
	for src_dir, sub_dirs, filenames in os.walk(src):
	
		# Build and create destination directory path
		relative_path = src_dir.split(src)[1].lstrip(os.path.sep)
		
		dst_dir = os.path.join(dst, relative_path)

		if src != src_dir:
			_mkdir_p(dst_dir)

		# Copy, rewrite and move project files
		for filename in filenames:
			
			if filename in ['development.py', 'production.py']:
				continue

			src_file = os.path.join(src_dir, filename)
			dst_file = os.path.join(dst_dir, filename)

			if filename.endswith(REWRITE_FILE_EXTS):
				_rewrite_and_copy(src_file, dst_file, project_name)			
			else:
				shutil.copy(src_file, dst_file)
			logger.info("New: %s" % dst_file)

			if filename in ['development_sample.py', 'production_sample.py']:
				dst_file = os.path.join(dst_dir, "%s.py" % filename.split('_')[0])
				_rewrite_and_copy(src_file, dst_file, project_name)
				logger.info("New: %s" % dst_file)

			with open(
				os.path.join(src_file, dst_file

					), 'r') as file :
				filedata = file.read()
				filedata = filedata.replace('{{ project.slug }}', slug)
				filedata = filedata.replace('{{ project.port }}', str(port))
			
			with open(
				os.path.join(src_file, dst_file
					), 'w') as file :
				file.write(filedata)				

			if '{{ project.slug }}' in filename:
				print('FILENAME IS: ' + str(filename))
				print(dst_file.split('/')[-1])
				repalced_filename = filename.replace('{{ project.slug }}', slug)
				print(repalced_filename)
				os.rename(
					os.path.join('/'.join(dst_file.split('/')[0:-1]), filename), 
					os.path.join('/'.join(dst_file.split('/')[0:-1]), repalced_filename)
				)

	logger.info('Finish generating project files.')
	run_client(project_name)