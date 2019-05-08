#!/usr/bin/env python3
import cv2
import os
import numpy as np
import urllib.request
import platform

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

DISPLAY = 'd1'

def play_video ( V ) :
    cap = cv2.VideoCapture( V )
    
    while cap.isOpened() :
        ret, frame = cap.read()
        
        if ret == True :
            cv2.imshow( DISPLAY, frame )

            key = cv2.waitKey( 25 )
            if key & 0xFF == ord( 's' ) :
                break
            if key & 0xFF == ord( 'q' ) :
                cv2.destroyAllWindows()
                exit()
        else :
            break
    
    cap.release()

def show_img ( I, t ) :
    cv2.imshow( DISPLAY, cv2.imread( I ) )
    
    if cv2.waitKey( t * 1000 ) & 0xFF == ord( 'q' ) :
        cv2.destroyAllWindows()
        exit()

def reproducir () :
    ca = ''
    contenido = False
    files = os.popen( ( 'DIR /B' if IS_WIN else 'ls -a' ) ).read().split( '\n' )
    
    for f in files :
        if f == '.contenido' :
            contenido = True
        elif '.ca' in f :
            ca = f
    
    cv2.namedWindow( DISPLAY, cv2.WND_PROP_FULLSCREEN )
    cv2.setWindowProperty( DISPLAY, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN )
    
    if not contenido :
        if ca == '' :
            show_img( 'notfound.png', 10 )
        else :
            if IS_WIN :
                os.system( 'unzip.exe -o {}'.format( ca ) )
            else :
                os.system( 'unzip -o {}'.format( ca ) )
            contenido = True
    
    if contenido :
        f = open( '.contenido/info.ca', 'r' )
        
        for l in f :
            l = l.replace( '\n', '' )
            p = l.split( ',' )
            
            if p[2] == 'v' :
                play_video( '.contenido/{}'.format( p[1] ) )
            else :
                show_img( '.contenido/{}'.format( p[1] ), int(p[3],10))

while True :
    check_file()
    reproducir()

cv2.destroyAllWindows()
