#!/usr/bin/env python3
import platform
import os
import urllib.request

IS_WIN = platform.system() is 'Windows'
HOST = ''

with open( 'host.conf', 'r' ) as f :
    HOST = f.read().replace( '\n', '' )

SAVED_FILE = './copay.ca'
CHECK_FILE = './check.txt'
FTP_URL = 'http://{}:8000/download'.format( HOST )
HTTP_URL = 'http://{}:8080'.format( HOST )

print( FTP_URL )
print( HTTP_URL )


def download_file () :
    print( 'Downloading...' )
    if IS_WIN :
        os.system( 'DEL {}'.format( SAVED_FILE ) )
        os.system( 'RMDIR /S /Q .contenido' )
    else :
        os.system( 'rm {}'.format( SAVED_FILE ) )
        os.system( 'rm -r .contenido' )
    
    file = urllib.request.urlopen( FTP_URL ).read()
    
    with open( SAVED_FILE, 'wb' ) as f :
        f.write( file )

def check_file () :
    if not os.path.isfile( CHECK_FILE ) :
        with open( CHECK_FILE, 'w' ) as f :
            f.write( '-1' )
    
    code = urllib.request.urlopen( '{}/check'.format( HTTP_URL ) ).read().decode( 'utf-8' )
    actual = ''
    
    with open( CHECK_FILE, 'r' ) as f :
        actual = f.read()
    
    if not actual == code :
        download_file()
        
        with open( CHECK_FILE, 'w' ) as f :
            f.write( code )


check_file()