# -*- coding: utf-8 -*-

## \package globals.fileio
#  
#  File I/O operations

# MIT licensing
# See: docs/LICENSE.txt


import codecs, os

from globals.paths      import ConcatPaths
from globals.strings    import GS
from globals.strings    import IsString
from globals.strings    import TextIsEmpty


## An object that represents a file
class FileItem:
    def __init__(self, path, target=None):
        self.Path = path
        self.Target = target
    
    
    ## Checks if the file exists on the filesystem
    def Exists(self):
        return os.path.isfile(self.Path)
    
    
    ## Retrieves file's basename
    def GetBasename(self):
        return os.path.basename(self.Path)
    
    
    ## Retrieves file's full path
    def GetPath(self):
        return self.Path
    
    
    ## Retrieves file's target directory
    def GetTarget(self):
        return self.Target
    
    
    ## Checks if the file has a target installation directory
    def HasTarget(self):
        return IsString(self.Target) and not TextIsEmpty(self.Target)
    
    
    ## Checks if the item represented is a directory
    def IsDirectory(self):
        return os.path.isdir(self.Path)
    
    
    ## Checks if file is executable
    def IsExecutable(self):
        return os.access(self.Path, os.X_OK)
    
    
    ## Sets file's path & basename
    def SetPath(self, path):
        self.Path = path
    
    
    ## Sets file's target directory
    def SetTarget(self, target):
        self.Target = target


## TODO: Doxygen
def AppendFile(filename, contents, no_strip=None, input_only=False):
    contents = u'{}\n{}'.format(ReadFile(filename, no_strip=no_strip), contents)
    
    # Only strip characters from text read from file
    if input_only:
        no_strip = None
    
    WriteFile(filename, contents, no_strip)


## Retrieves the contents of a text file using utf-8 encoding
#  
#  \param filename
#    \b \e string : Path to filename to read
#  \param split
#    \b \e bool : If True, output will be split into a list or tuple
#  \param convert
#    \b \e tuple|list : Converts the output to value type if 'split' is True
def ReadFile(filename, split=False, convert=tuple, no_strip=None):
    chars = u' \t\n\r'
    if no_strip:
        for C in no_strip:
            chars = chars.replace(C, u'')
    
    if not os.path.isfile(filename):
        return
    
    FILE_BUFFER = codecs.open(filename, u'r', u'utf-8')
    contents = u''.join(FILE_BUFFER).strip(chars)
    FILE_BUFFER.close()
    
    if split:
        contents = convert(contents.split(u'\n'))
    
    # FIXME: Should return contents even if it is empty string or list
    if contents:
        return contents


## Outputs text content to file using utf-8 encoding
#  
#  FIXME: Needs exception handling
#  FIXME: Set backup & restore on error/failure
#  \param filename
#    File to write to
#  \param contents
#    Text to write to file
#  \param no_strip
#    Characters to not strip from contents
def WriteFile(filename, contents, no_strip=None):
    chars = u' \t\n\r'
    if no_strip:
        for C in no_strip:
            chars = chars.replace(C, u'')
    
    # Ensure we are dealing with a string
    if isinstance(contents, (tuple, list)):
        contents = u'\n'.join(contents)
    
    contents = contents.strip(chars)
    
    if u'/' in filename:
        target_dir = os.path.dirname(filename)
    
    else:
        target_dir = os.getcwd()
        filename = u'{}/{}'.format(target_dir, filename)
    
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    
    FILE_BUFFER = codecs.open(filename, u'w', encoding=u'utf-8')
    FILE_BUFFER.write(contents)
    FILE_BUFFER.close()
    
    if not os.path.isfile(filename):
        return False
    
    return True


## Retrieves a list of all files from the given path
#
#  \param path
#    Directory to search for license templates
def GetFiles(path, flag=None):
    file_list = []
    
    for PATH, DIRS, FILES in os.walk(path):
        for F in FILES:
            file_path = ConcatPaths((path, F))
            
            if os.path.isfile(file_path):
                # Don't add files that do not match 'flag' attributes
                if flag:
                    if not os.access(file_path, flag):
                        continue
                
                file_list.append(F)
    
    return sorted(file_list, key=GS.lower)
