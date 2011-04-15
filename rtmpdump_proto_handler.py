""" 
    Protocol handler for rtmpdump:// urls
    Version 0.0.1
    
    Copyright (C) 2011 Adam Malcontenti-Wilson
    Licenced under GNU Lesser General Public License (GNU LGPL)
    <http://www.gnu.org/copyleft/lesser.html>
    
    Requires pygtk, subprocess, re, os, sys, urlparse and urllib2 modules.
    Requires rtmpdump installed in your system's PATH, 
    or add a path to RTMPDUMP_EXECUTABLE variable.
    Also requires manual installation as a default protocol handler
    for rtmpdump:// urls - this may vary by system.
"""
import gtk, subprocess, re, os, sys
from urlparse import parse_qs
from urllib2 import unquote
VERSION = "0.0.1"
PROMPT_FILENAME = True
IGNORE_O_PARAM = False
RTMPDUMP_EXECUTEABLE = 'rtmpdump'
DEFAULT_DIRECTORY = os.getcwd()
ALLOWED_ARGS = ['r','n','c','l','S','a','t','p','s','f','u','C','y','Y','v','d','e','k','A','B','b','m','T','w','x','W','X','#','q','V','z']
outputDirectory = DEFAULT_DIRECTORY 
outputFile = 'video.f4v'
execArgs = [RTMPDUMP_EXECUTEABLE]

print "rtmpdump:// protocol handler, Version", VERSION,"\n"
    
if len(sys.argv) != 2 or sys.argv[1][:11] != 'rtmpdump://':
    print "Invalid call"
else:
    args = parse_qs(sys.argv[1][11:], True)
    for arg in args:
        if not IGNORE_O_PARAM and arg == 'o':
            outputFile = re.sub(r'[^a-zA-Z0-9]',r'_',re.sub(r'(.+)\.[a-zA-Z0-9]{1,4}$',r'\1',unquote(args[arg][0]))) + '.f4v'
            continue
        if arg not in ALLOWED_ARGS:
            print "WARNING: Argument \"%s\" not allowed" % arg
            continue
        execArgs.append('-' + arg)
        if args[arg][0] != '':
            for c in '`\'\";':
                if c in args[arg][0] or c in unquote(args[arg][0]):
                    print "ERROR: Invalid characters found in url"
                    sys.exit(0)
            execArgs.append(unquote(args[arg][0]))
    if PROMPT_FILENAME:
        dialog = gtk.FileChooserDialog(title="Save Video As...", action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_current_name(outputFile)
        f4vfilter = gtk.FileFilter()
        f4vfilter.set_name("Flash Video files")
        f4vfilter.add_mime_type("video/flv")
        f4vfilter.add_pattern("*.f4v")
        dialog.add_filter(f4vfilter)
        anyfilter = gtk.FileFilter()
        anyfilter.set_name("Any files")
        anyfilter.add_pattern("*")
        dialog.add_filter(anyfilter)
        dialog.set_do_overwrite_confirmation(True)
        dialog_response = dialog.run()
        if dialog_response != gtk.RESPONSE_OK:
            sys.exit(0)
        outputFile = dialog.get_filename()
        dialog.destroy()
        while gtk.events_pending():
            gtk.main_iteration(block=False)
    else:
        outputFile = outputDirectory + '/' + outputFile
    execArgs.extend(['-o',outputFile])
    print "Executing:"," ".join(execArgs),"\n"
    subprocess.call(execArgs)
    raw_input("Press ENTER to exit")
