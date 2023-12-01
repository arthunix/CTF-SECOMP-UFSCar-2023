#!/bin/python

import subprocess
import wget
import os

if __name__ == '__main__':
    DOWNLOAD_LINK = 'https://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz'
    wget.download(DOWNLOAD_LINK)
    DOWNLOAD_LINK = 'https://raw.githubusercontent.com/hannob/bashcheck/master/bashcheck'
    wget.download(DOWNLOAD_LINK)
    subprocess.run(['tar -xvf bash-4.3.tar.gz'], shell=True)
    subprocess.run(['chmod +x bashcheck'], shell=True)

    for i in range(1, 49):
        folder = ''
        patch = ''
        if i > 0 and i < 10:
            DOWNLOAD_LINK = 'https://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-00'+str(i)
            wget.download(DOWNLOAD_LINK)
            folder = 'bash-4.3-00'+str(i)
            patch = 'bash43-00'+str(i)
        elif i != 0:
            DOWNLOAD_LINK = 'https://ftp.gnu.org/gnu/bash/bash-4.3-patches/bash43-0'+str(i)
            wget.download(DOWNLOAD_LINK)
            folder = 'bash-4.3-0'+str(i)
            patch = 'bash43-0'+str(i)

        subprocess.run(['cp -r bash-4.3/ ' + folder + '/'], shell=True)
        os.chdir(folder+'/')
        #subprocess.run(['pwd'], shell=True)
        subprocess.run(['patch -p0 -t < ../'+ patch], shell=True)
        subprocess.run(['./configure'], shell=True)
        subprocess.run(['make'], shell=True)
        os.chdir('..')

    for i in range(1, 49):
        folder = ''
        print('testing bash with patch version: ' + str(i))
        if i > 0 and i < 10:
            folder = 'bash-4.3-00'+str(i)
        elif i != 0:
            folder = 'bash-4.3-0'+str(i)
        subprocess.run(['./bashcheck ./' + folder + '/bash'], shell=True)
