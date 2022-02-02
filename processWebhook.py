import http.cookiejar as cookielib
import os, sys, re
import urllib
import urllib.request as urllib2
import json, subprocess
import base64
from Crypto.Cipher import AES

proc = None

class SafeString(str):
    def title(self):
        return self

    def capitalize(self):
        return self
    
def init_cookie_jar():
    cookie_file = 'vcpck.lwp'
    cookie_jar = cookielib.LWPCookieJar()
    if os.path.exists(cookie_file):
        print("in")
        cookie_jar.load(cookie_file, ignore_discard=True)
    TOKEN = ""
    return cookie_file, cookie_jar, TOKEN

def make_request(url, cookie_file, cookie_jar, TOKEN, key=False):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
    if key: request.add_header("x-csrf-token", KEY)
    response = opener.open(request)
    data = response.read()
    cookie_jar.save(cookie_file, ignore_discard=True)
    return data

def make_request_post(url, data, cookie_file, cookie_jar, TOKEN):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')
    request.add_header('accept', 'application/json, text/plain, */*')
    request.add_header('Content-Type', 'application/json')
    request.add_header("x-csrf-token", KEY)
    request.add_header("x-requested-with", 'XMLHttpRequest')
    request.add_header("sec-fetch-mode", 'cors')
    request.add_header("sec-fetch-site", 'same-origin')
    request.add_header("x-requested-with", 'XMLHttpRequest')
    response = opener.open(request, data)

    data = response.read()
    cookie_jar.save(cookie_file, ignore_discard=True)
    return data

def get_decrypted_data(url,uname,passwd):
    status = make_request("https://www.sunnxt.com/checkUSERSESSION", cookie_file, cookie_jar, TOKEN, True)
    print(status)
    if status == b'fail':
        print(status)
        make_request_post("https://www.sunnxt.com/login",'{"email":"'+uname+'","password":"'+passwd+'"}', cookie_file, cookie_jar, TOKEN)
        status = make_request("https://www.sunnxt.com/checkUSERSESSION", cookie_file, cookie_jar, TOKEN, True)
        if status == b'success':
            print("Signed-in successfully.")
    data = make_request(url, cookie_file, cookie_jar, TOKEN, True)
    data = decrypt(data)
    return data

def createFolder(path):
    directory = os.path.dirname(path)
    try:
        os.stat(directory)
        #print "Folder found: "+path
    except:
        os.mkdir(directory)
        #print "Folder created: "+path  


def retriveVoD(url, fname):
    global proc
    cmd = "ffmpeg -headers 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0' -i '"+url+"' -c copy -bsf:a aac_adtstoasc '"+fname+"'"
    proc = subprocess.Popen(cmd,shell=False)
    proc.wait()

def getkey():
    from bs4 import BeautifulSoup
    response = make_request("https://www.sunnxt.com", cookie_file, cookie_jar, TOKEN)
    soup = BeautifulSoup(response,features="html.parser")
    metas = soup.find_all('meta')
    return [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'csrf-token' ][0]

def decrypt(ct):
    from Crypto.Util.Padding import pad, unpad
    data = base64.b64decode(ct)
    cipher1 = AES.new("A3s68aORSgHs$71P".encode("utf8"), AES.MODE_CBC, "0000000000000000".encode("utf8"))
    pt = unpad(cipher1.decrypt(data), 16)
    return pt
    
cookie_file, cookie_jar, TOKEN = init_cookie_jar()
KEY = getkey()
print(KEY)
print(get_decrypted_data("https://www.sunnxt.com/content/detail/?content-id=14020","joesmiches@gmail.com","colombo2022"))
