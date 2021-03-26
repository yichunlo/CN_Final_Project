import socket
import os
import hashlib
from urllib.parse import unquote
import pandas as pd

def gen_secret(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    ret = str(m.hexdigest())
    return ret

def response_len():
    #print("response_len")
    file = open('len.html', 'rb')
    res = file.read()
    file.close()
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    ret = header.encode('utf-8') + res
    return ret

def response_plain():
    #print("response_plain")
    file = open('plain.html', 'rb')
    res = file.read()
    file.close()
    length = os.path.getsize('plain.html')
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(length) + '\r\n\r\n'
    ret = header.encode('utf-8') + res
    return ret

def handle_login(name, password):
    verify = False
    info = pd.read_csv('info.csv')
    #print(info)
    acc = list(info.account)
    pwd = list(info.password)
    #print(acc)
    #print(pwd)
    length = len(acc)
    for i in range(length):
        if name == acc[i] and password == str(pwd[i]):
            verify = True
            print("Verified!")
            break
    if verify:
        h_val = gen_secret(password)
        #print("h_val:", h_val)
        file = open('home.html', 'rb')
        res = file.read()
        file.close()
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nSet-Cookie: account=' + name + '\r\nSet-Cookie: secret=' + h_val + '\r\n\r\n'
        response = header.encode('utf-8') + res
    else:
        file_length = str(os.path.getsize('wrong.html'))
        file = open('wrong.html', 'rb')
        res = file.read()
        file.close()
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + file_length + '\r\n\r\n'
        response = header.encode('utf-8') + res
    return response

def handle_get(filename, req_list):
    #print("filename:", filename)
    #print("req_list[-1]:", req_list[-1])
    IsVideo = False
    if filename.endswith('.mp4'):
        IsVideo = True
        mimetype = 'video/mp4'
    if filename.endswith('png'):
        mimetype = 'image/png'
    elif filename.endswith('jpg'):
        mimetype = 'image/jpg'
    elif filename.endswith('gif'):
        mimetype = 'image/gif'
    else:
        mimetype = 'text/html'
    file_length = os.path.getsize(filename)
    if IsVideo:
        chunk_size = 65536
        offset_start = int(req_list[-1].split('=')[1].split('-')[0])
        #print("offset_start:", offset_start)
        file = open(filename, 'rb')
        file.seek(offset_start)
        res = file.read(chunk_size)
        file.close()
        #print("res:", res)
        if offset_start + chunk_size < file_length:
            content_range = 'Content-Range: bytes '+str(offset_start)+'-'+str(offset_start+chunk_size)+'/'+str(file_length)+'\r\n\r\n'
            header = 'HTTP/1.1 206 Partial Content\r\nContent-Type: video/mp4\r\nContent-Length: ' + str(len(res)) + '\r\n' + content_range
            #print("header:", header)
        else:
            header = 'HTTP/1.1 200 OK\r\nContent-Type: video/mp4\r\n\r\n'
            #print("header:", header)
    else:
        file = open(filename, 'rb')
        res = file.read()
        file.close()
        header = 'HTTP/1.1 200 OK\r\nContent-Type: '+str(mimetype)+'\r\nContent-Length: ' + str(file_length) + '\r\n\r\n'
    response = header.encode('utf-8') + res
    return response

def handle_comment(name_, msg_):
    name = unquote(str(name_))
    msg = unquote(str(msg_))
    name = name.replace('+', ' ')
    msg = msg.replace('+', ' ')
    if len(msg) > 50:
        response = response_len()
    else:
        response = response_plain()
        file = open('text.html', 'a')
        write_back = '\n<tr>\n<td>' + name + '</td><td>' + msg + '</td>\n</tr>'
        file.write(write_back)
        file.close()
    return response

def handle_reg(account, pwd):
    info = pd.read_csv('info.csv')
    #print(info)
    acc = list(info.account)
    #print(acc)
    if account in acc:
        file = open('exist.html', 'rb')
        res = file.read()
        file.close()
        file_length = os.path.getsize('exist.html')
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(file_length) + '\r\n\r\n'
        response = header.encode('utf-8') + res
        return response
    else:
        print("Create account")
        file = open('info.csv', 'a')
        line = account+','+pwd+'\n'
        file.write(line)
        file.close()
        file = open('finish.html', 'rb')
        res = file.read()
        file.close()
        file_length = os.path.getsize('finish.html')
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(file_length) + '\r\n\r\n'
        response = header.encode('utf-8') + res
        return response

def verify_account(account, secret):
    info = pd.read_csv('info.csv')
    password = ""
    acc = list(info.account)
    pwd = list(info.password)
    length = len(acc)
    for i in range(length):
        if acc[i] == account:
            password = pwd[i]
            print("password:", password)
            break
    my_cmp = gen_secret(password)
    if secret == my_cmp:
        print("Same!")
        return True
    else:
        print("Not the Same QQ")
        return False

def please_login():
    file = open('please_login.html', 'rb')
    res = file.read()
    file.close()
    file_length = os.path.getsize('please_login.html')
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(file_length) + '\r\n\r\n'
    response = header.encode('utf-8') + res
    return response

def you_are_evil():
    file = open('evil.html', 'rb')
    res = file.read()
    file.close()
    file_length = os.path.getsize('evil.html')
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(file_length) + '\r\n\r\n'
    response = header.encode('utf-8') + res
    return response

def clean_up_cookie(filename):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nSet-Cookie: account=\r\nSet-Cookie: secret=\r\n\r\n'
    file = open(filename, 'rb')
    res = file.read()
    file.close()
    response = header.encode('utf-8') + res
    return response

def handle_error():
    #print("handle_error")
    header = 'HTTP/1.1 404 Not Found\n\n'
    res = '<html><body><center><h3>Error 404: File not found</h3><p>Some error happens</p></center></body></html>'.encode('utf-8')
    response = header.encode('utf-8') + res
    return response

host, port = '127.0.0.1', 12724

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

print('Serving on port: ', port)

while True:
    conn, addr = s.accept()
    req = conn.recv(2048).decode('utf-8')
    req_list = req.split(' ')     # Split request from spaces
    post_list = req.split('\n')
    print(req)
    if len(req_list) <= 1:
        print("There are some error in request")
        response = handle_error()
    else:
        #print("")
        #print(req_list[-3])
        #print(req_list[-2])
        #print("")
        method   = req_list[0]
        req_file = req_list[1]

        tmp = req_file.split('?')
        myfile = tmp[0] # After the "?" symbol not relevent here
        myfile = myfile.lstrip('/')
        clean_up_cookie_flag = False
        if myfile == 'index.html':
            clean_up_cookie_flag = True
        elif myfile == '' and (req_list[-3][:9] == 'account=;'):
            print("is index.html")
            myfile = 'index.html'    # Load index file as default
        elif myfile == '' and req_list[-3][:7] == 'account':
            print("is home.html")
            myfile = 'home.html'
        elif myfile == '':
            myfile = 'index.html'
        if method == 'GET':
            try:
                if clean_up_cookie_flag:
                    response = clean_up_cookie(myfile)
                else:
                    response = handle_get(myfile, req_list)
            except Exception as e:
                response = handle_error()
        elif method == 'POST':
            try:
                data = post_list[-1]
                #print("data:", data)
                if data[:4] == 'user':
                    user, password = data.split('&')[0][5:], data.split('&')[1][4:]
                    #print("Login user:", user)
                    #print("Login password:", password)
                    response = handle_login(user, password)
                elif data[:7] == 'Comment':
                    content = data[8:]
                    #print("Comment:", content)
                    if req_list[-2][:8] == 'account=' and len(req_list[-2]) > 9:
                        user = req_list[-2][8:-1]
                        secret = req_list[-1][7:].split('\r')[0]
                        if verify_account(user, secret):
                            response = handle_comment(user, content)
                        else:
                            response = you_are_evil()
                    else:
                        response = please_login()
                elif data[:7] == 'account':
                    account, pwd = data.split('&')[0][8:], data.split('&')[1][8:]
                    #print("account:", account)
                    #print("pwd:", pwd)
                    response = handle_reg(account, pwd)

            except Exception as e:
                response = handle_error()

        conn.send(response)
        conn.close()

