## \package dbr.functions
#
#  Global functions used throughout Debreate

# MIT licensing
# See: docs/LICENSE.txt


import os, re, traceback, subprocess, wx
from urllib.error   import URLError
from urllib.request import urlopen

from dbr.language        import GT
from globals.application import APP_project_gh
from globals.application import VERSION_dev
from globals.errorcodes  import dbrerrno
from globals.execute     import GetExecutable
from globals.strings     import GS
from globals.strings     import IsString
from globals.strings     import StringIsNumeric
from globals.system      import PY_VER_STRING


## Get the current version of the application
#
#  \param remote
#  Website URL to parse for update
#  \return
#  	Application's version tuple
def GetCurrentVersion(remote=APP_project_gh):
  try:
    version = os.path.basename(urlopen("{}/releases/latest".format(remote)).geturl())

    if "-" in version:
      version = version.split("-")[0]
    version = version.split(".")

    cutoff_index = 0
    for C in version[0]:
      if not C.isdigit():
        cutoff_index += 1
        continue

      break

    version[0] = version[0][cutoff_index:]
    for V in version:
      if not V.isdigit():
        return "Cannot parse release: {}".format(tuple(version))

      version[version.index(V)] = int(V)

    return tuple(version)

  except (URLError, err):
    return err


## TODO: Doxygen
def GetContainerItemCount(container):
  if wx.MAJOR_VERSION > 2:
    return container.GetItemCount()

  return len(container.GetChildren())


## TODO: Doxygen
def GetLongestLine(lines):
  if isinstance(lines, str):
    lines = lines.split("\n")

  longest = 0

  for LI in lines:
    l_length = len(LI)
    if l_length > longest:
      longest = l_length

  return longest


## Checks if the system is using a specific version of Python
#
#  FIXME: This function is currently not used anywhere in the code
#  \param version
#  	The minimal version that should be required
def RequirePython(version):
  error = "Incompatible python version"
  t = type(version)
  if t == type(""):
    if version == PY_VER_STRING[0:3]:
      return

    raise ValueError(error)

  elif t == type([]) or t == type(()):
    if PY_VER_STRING[0:3] in version:
      return

    raise ValueError(error)

  raise ValueError("Wrong type for argument 1 of RequirePython(version)")


## Checks if a string contains any alphabetic characters
#
#  \param value
#  	\b \e str : String to check
#  \return
#  	\b \e bool : Alphabet characters found
def HasAlpha(value):
  return (re.search("[a-zA-Z]", GS(value)) != None)


## Finds integer value from a string, float, tuple, or list
#
#  \param value
#  	Value to be checked for integer equivalent
#  \return
#  	\b \e int|None
def GetInteger(value):
  if isinstance(value, (int, float,)):
    return int(value)

  # Will always use there very first value, even for nested items
  elif isinstance(value,(tuple, list,)):
    # Recursive check lists & tuples
    return GetInteger(value[0])

  elif value and IsString(value):
    # Convert because of unsupported methods in str class
    value = GS(value)

    if HasAlpha(value):
      return None

    # Check for negative
    if value[0] == "-":
      if value.count("-") <= 1:
        value = GetInteger(value[1:])

        if value != None:
          return -value

    # Check for tuple
    elif "." in value:
      value = value.split(".")[0]
      return GetInteger(value)

    elif StringIsNumeric(value):
      return int(value)

  return None


## Finds a boolean value from a string, integer, float, or boolean
#
#  \param value
#  	Value to be checked for boolean equivalent
#  \return
#  	\b \e bool|None
def GetBoolean(value):
  v_type = type(value)

  if v_type == bool:
    return value

  elif v_type in (int, float):
    return bool(value)

  elif v_type == str:
    int_value = GetInteger(value)
    if int_value != None:
      return bool(int_value)

    if value in ("True", "False"):
      return value == "True"

  return None


## Finds a tuple value from a string, tuple, or list
#
#  \param value
#  	Value to be checked for tuple equivalent
#  \return
#  	\b \e tuple|None
def GetIntTuple(value):
  if isinstance(value, (tuple, list,)):
    if len(value) > 1:
      # Convert to list in case we need to make changes
      value = list(value)

      for I in value:
        t_index = value.index(I)

        if isinstance(I, (tuple, list)):
          I = GetIntTuple(I)

        else:
          I = GetInteger(I)

        if I == None:
          return None

        value[t_index] = I

      return tuple(value)

  elif IsString(value):
    # Remove whitespace & braces
    value = value.strip(" ()")
    value = "".join(value.split(" "))

    value = value.split(",")

    if len(value) > 1:
      for S in value:
        v_index = value.index(S)

        S = GetInteger(S)

        if S == None:
          return None

        value[v_index] = S

      # Convert return value from list to tuple
      return tuple(value)

  return None


def IsInteger(value):
  return GetInteger(value) != None


def IsBoolean(value):
  return GetBoolean(value) != None


def IsIntTuple(value):
  return GetIntTuple(value) != None


## Checks if file is binary & needs stripped
#
#  FIXME: Handle missing 'file' command
def FileUnstripped(file_name):
  CMD_file = GetExecutable("file")

  if CMD_file:
    output = subprocess.run([CMD_file, file_name]).stdout

    if ": " in output:
      output = output.split(": ")[1]

    output = output.split(", ")

    if "not stripped" in output:
      return True

    return False

  print("ERROR: \"file\" command does not exist on system")

  return False


def BuildBinaryPackageFromTree(root_dir, filename):
  if not os.path.isdir(root_dir):
    return dbrerrno.ENOENT

  # DEBUG
  cmd = "fakeroot dpkg-deb -v -b \"{}\" \"{}\"".format(root_dir, filename)
  print("DEBUG: Issuing command: {}".format(cmd))

  #res = subprocess.run([cmd])
  #output = (res.returncode, res.stdout)

  return 0


def UsingDevelopmentVersion():
  return VERSION_dev != 0


def BuildDebPackage(stage_dir, target_file):
  packager = GetExecutable("dpkg-deb")
  fakeroot = GetExecutable("fakeroot")

  if not fakeroot or not packager:
    return (dbrerrno.ENOENT, GT("Cannot run \"fakeroot dpkg\""))

  packager = os.path.basename(packager)

  try:
    output = subprocess.check_output([fakeroot, packager, "-b", stage_dir, target_file], stderr=subprocess.STDOUT)

  except:
    return (dbrerrno.EAGAIN, traceback.format_exc())

  return (dbrerrno.SUCCESS, output)


## Check if mouse is within the rectangle area of a window
def MouseInsideWindow(window):
  # Only need to find size because ScreenToClient method gets mouse pos
  # relative to window.
  win_size = window.GetSize().Get()
  mouse_pos = window.ScreenToClient(wx.GetMousePosition())

  # Subtracting from width & height compensates for visual boundaries
  inside_x = 0 <= mouse_pos[0] <= win_size[0]-4
  inside_y = 0 <= mouse_pos[1] <= win_size[1]-3

  return inside_x and inside_y
