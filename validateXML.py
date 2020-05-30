import datetime
import os
import sys

from lxml import etree


ROOT_DIRECTORY = os.path.dirname(sys.argv[0])
PATH_TO_XSD_SCHEME = '{}\\{}'.format(ROOT_DIRECTORY, 'XSD\V02_STD_Cadastral_Cost\STD_Cadastral_Cost.xsd')
PATH_TO_FOLDER_WITH_XML = '{}\\{}'.format(ROOT_DIRECTORY, 'xml')
LOG_NAME = 'errors.log'
PATH_TO_LOG = '{}\\{}'.format(ROOT_DIRECTORY, LOG_NAME)

class Validator:

    def __init__(self, xsd_path: str):
        xmlschema_doc = etree.parse(xsd_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_path: str) -> bool:
        xml_doc = etree.parse(xml_path)
        try:
            self.xmlschema.assertValid(xml_doc)
            return 'Ok'
        except etree.DocumentInvalid as e:
            with open(PATH_TO_LOG, 'a') as f:
                for error in self.xmlschema.error_log:
                    f.write('File name: {} Error: {} Line: {}.\n'.format(xml_path, error.message, error.line))
            return 'Error'


if __name__ == '__main__':
    if not os.path.exists(PATH_TO_XSD_SCHEME):
        print('ERROR - xsd scheme not found')
        sys.exit(404)
    if not os.path.exists(PATH_TO_FOLDER_WITH_XML):
        print('ERROR - folder with xml not found')
        sys.exit(404)
    if os.path.exists(PATH_TO_LOG):
        os.remove(PATH_TO_LOG)
    validator = Validator(PATH_TO_XSD_SCHEME)
    files = os.listdir(PATH_TO_FOLDER_WITH_XML)
    t = 'files' if len(files) > 1 else 'file'
    print('Scanning %s %s' % (len(files), t))
    timeBegin = datetime.datetime.now()
    for file in files:
        print('{}: '.format(file), end='')
        path_to_file = '{}\\{}'.format(PATH_TO_FOLDER_WITH_XML, file)
        print(validator.validate(path_to_file))
    timeEnd = datetime.datetime.now()
    delta = timeEnd - timeBegin
    print('Scanning complete. Total time: {} seconds'.format(delta.seconds))
