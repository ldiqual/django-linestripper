from django.conf import settings
from django.template.loaders import app_directories

import re

# To be set in settings.py
STRIPPER_TAG = getattr(settings, 'STRIPPER_TAG', '__STRIPPER_TAG__')
STRIPPER_CLEAR_LINE = getattr(settings, 'STRIPPER_CLEAR_LINE', False)

# Finders
FIND_BLANK_LINE = r'\n(\s*)\n'
FIND_START_BLANK_LINE = r'^(\s*)\n'
FIND_TAG = STRIPPER_TAG

# Replacers
REPLACE_WITH_TAG = r'\n'+ STRIPPER_TAG +'\n' if STRIPPER_CLEAR_LINE else r'\n\1'+ STRIPPER_TAG +'\n'
REPLACE_START_WITH_TAG = STRIPPER_TAG +'\n' if STRIPPER_CLEAR_LINE else r'\n\1'+ STRIPPER_TAG +'\n'

# Deleters
DELETE_BLANK_LINE = r'\n'
DELETE_START_BLANK_LINE = r''
DELETE_TAG = ''

'''
This is called AFTER the template generation.
It suppresses blank lines and deletes STRIPPER_TAG
'''
class StripperMiddleware(object):
	def process_response(self, request, response):
		# Suppress a blank line at the beginning of the document
		response.content = re.sub(FIND_START_BLANK_LINE, DELETE_START_BLANK_LINE, response.content)
		# Suppress blank lines
		response.content = re.sub(FIND_BLANK_LINE, DELETE_BLANK_LINE, response.content)
		# Delete STRIPPER_TAG
		response.content = re.sub(FIND_TAG, DELETE_TAG, response.content)
		return response

	def process_request(self, request):
		pass

'''
This is called BEFORE the template generation.
It replaces blank lines by STRIPPER_TAG
'''
class Loader(app_directories.Loader):
    is_usable = True

    def process_content(self, content):
        content = re.sub(FIND_BLANK_LINE, REPLACE_WITH_TAG, content)
        content = re.sub(FIND_START_BLANK_LINE, REPLACE_WITH_TAG, content)
        return content

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        return self.process_content(source), origin