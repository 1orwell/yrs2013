"""Config on Darwin w/ frameworks"""

import os, sys, string
from glob import glob
from distutils.sysconfig import get_python_inc

class Dependency:
    libext = '.a'
    def __init__(self, name, checkhead, checklib, libs):
        self.name = name
        self.inc_dir = None
        self.lib_dir = None
        self.libs = libs
        self.found = 0
        self.checklib = checklib + self.libext
        self.checkhead = checkhead
        self.cflags = ''

    def configure(self, incdirs, libdirs):
        incname = self.checkhead
        libnames = self.checklib, self.name.lower()
        for dir in incdirs:
            path = os.path.join(dir, incname)
            if os.path.isfile(path):
                self.inc_dir = dir
                break
        for dir in libdirs:
            for name in libnames:
                path = os.path.join(dir, name)
                if os.path.isfile(path):
                    self.lib_dir = dir
                    break
        if self.lib_dir and self.inc_dir:
            print (self.name + '        '[len(self.name):] + ': found')
            self.found = 1
        else:
            print (self.name + '        '[len(self.name):] + ': not found')

class FrameworkDependency(Dependency):
    def configure(self, incdirs, libdirs):
        BASE_DIRS = '/', os.path.expanduser('~/'), '/System/'
        for n in BASE_DIRS:
            n += 'Library/Frameworks/'
            fmwk = n + self.libs + '.framework/Versions/Current/'
            if os.path.isfile(fmwk + self.libs):
                print ('Framework ' + self.libs + ' found')
                self.found = 1
                self.inc_dir = fmwk + 'Headers'
                self.cflags = (
                    '-Xlinker "-framework" -Xlinker "' + self.libs + '"' +
                    ' -Xlinker "-F' + n + '"')
                self.origlib = self.libs
                self.libs = ''
                return
        print ('Framework ' + self.libs + ' not found')


class DependencyPython:
    def __init__(self, name, module, header):
        self.name = name
        self.lib_dir = ''
        self.inc_dir = ''
        self.libs = []
        self.cflags = ''
        self.found = 0
        self.ver = '0'
        self.module = module
        self.header = header

    def configure(self, incdirs, libdirs):
        self.found = 1
        if self.module:
            try:
                self.ver = __import__(self.module).__version__
            except ImportError:
                self.found = 0
        if self.found and self.header:
            fullpath = os.path.join(get_python_inc(0), self.header)
            if not os.path.isfile(fullpath):
                found = 0
            else:
                self.inc_dir = os.path.split(fullpath)[0]
        if self.found:
            print (self.name + '        '[len(self.name):] + ': found', self.ver)
        else:
            print (self.name + '        '[len(self.name):] + ': not found')

DEPS = [
    FrameworkDependency('SDL', 'SDL.h', 'libSDL', 'SDL'),
    FrameworkDependency('FONT', 'SDL_ttf.h', 'libSDL_ttf', 'SDL_ttf'),
    FrameworkDependency('IMAGE', 'SDL_image.h', 'libSDL_image', 'SDL_image'),
    FrameworkDependency('MIXER', 'SDL_mixer.h', 'libSDL_mixer', 'SDL_mixer'),
    FrameworkDependency('SMPEG', 'smpeg.h', 'libsmpeg', 'smpeg'),
    Dependency('PNG', 'png.h', 'libpng', ['png']),
    Dependency('JPEG', 'jpeglib.h', 'libjpeg', ['jpeg']),
    Dependency('SCRAP', '','',[]),
    Dependency('PORTMIDI', 'portmidi.h', 'libportmidi', ['portmidi']),
    FrameworkDependency('PORTTIME', 'CoreMidi.h', 'CoreMidi', 'CoreMidi'),
]


def main():
    global DEPS

    print ('Hunting dependencies...')
    incdirs = ['/usr/local/include','/opt/local/include']
    libdirs = ['/usr/local/lib','/opt/local/lib']
    newconfig = []
    for d in DEPS:
        d.configure(incdirs, libdirs)
    DEPS[0].cflags = '-Ddarwin '+ DEPS[0].cflags
    return DEPS


if __name__ == '__main__':
    print ("""This is the configuration subscript for OSX Darwin.
             Please run "config.py" for full configuration.""")
