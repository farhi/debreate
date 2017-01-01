# -*- coding: utf-8 -*-

## \package dbr.cursor

# MIT licensing
# See: docs/LICENSE.txt


import wx

from dbr.image import GetImagePath


## Retrieves an image from bitmaps dir & creates a wx.Cursor
#  
#  \param name
#    \b \e string : Base filename of the image
#  \param size
#    \b \e int : Image size (denotes subfolder to search)
#  \param img_type
#    \b \e string : Image type / filename suffix
#  \return
#    \b \e wx.Cursor : Either a new cursor using the retrieved image, or wx.NullCursor
def GetCursor(name, size=16, img_type=u'png'):
    cursor_bitmap = GetImagePath(name, size, img_type)
    
    if not cursor_bitmap:
        return wx.NullCursor
    
    return wx.Cursor(cursor_bitmap, wx.BITMAP_TYPE_PNG)
