# -*- coding: utf-8 -*-


### Version information ###
RELEASE = 0
VER_MAJ = 0
VER_MIN = 7
VER_REL = 11

VERSION = (VER_MAJ, VER_MIN, VER_REL)
VERSION_STRING = u'{}.{}.{}'.format(VER_MAJ, VER_MIN, VER_REL)

# Development version
if not RELEASE:
	VERSION_STRING = '{}-dev'.format(VERSION_STRING)

### Website & hosting information ###
HOMEPAGE = u'http://debreate.sourceforge.net/'
gh_project = u'https://github.com/AntumDeluge/debreate'
sf_project = u'https://sourceforge.net/projects/debreate'
