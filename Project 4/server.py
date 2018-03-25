#!/usr/bin/env python3

# See https://docs.python.org/3.2/library/socket.html
# for a description of python socket and its parameters
#
# Copyright 2018, Shaden Smith, Koorosh Vaziri,
# Niranjan Tulajapure, Ambuj Nayab, Akash Kulkarni, and Daniel J. Challou
# for use by students enrolled in Csci 4131 at the University of
# Minnesota-Twin Cities only. Do not reuse or redistribute further
# without the express written consent of the authors.
#
import socket
#add the following
import socket
import os
import stat
import sys
import urllib.parse
import datetime
import time
import sys

from threading import Thread
from argparse import ArgumentParser


BUFSIZE = 4096
#add the following
CRLF = '\r\n'
CREATED = 'HTTP/1.1 201 CREATED{}{}{}'.format(CRLF, CRLF, CRLF)
METHOD_NOT_ALLOWED = 'HTTP/1.1 405  METHOD NOT ALLOWED{}Allow: GET, HEAD{}Connection: close{}{}'.format(CRLF, CRLF, CRLF, CRLF)
OK = 'HTTP/1.1 200 OK{}{}{}'.format(CRLF, CRLF, CRLF)
NOT_FOUND = 'HTTP/1.1 404 NOT FOUND{}Connection: close{}{}'.format(CRLF, CRLF, CRLF)
FORBIDDEN = 'HTTP/1.1 403 FORBIDDEN{}Connection: close{}{}'.format(CRLF, CRLF, CRLF)
MOVED_PERMANENTLY = 'HTTP/1.1 301 MOVED PERMANENTLY{}Location:  https://www.cs.umn.edu/{}Connection: close{}{}'.format(CRLF, CRLF, CRLF, CRLF)
NOT_ACCEPTABLE = 'HTTP/1.1 406 NOT ACCEPTABLE{}'.format(CRLF)

def get_contents(fname):
    with open(fname, 'r') as f:
        return f.read()

def check_perms(resource):
    """Returns True if resource has read permissions set on 'others'"""
    stmode = os.stat(resource).st_mode
    return (getattr(stat, 'S_IROTH') & stmode) > 0


def client_talk(client_sock, client_addr):
    print('talking to {}'.format(client_addr))
    data = client_sock.recv(BUFSIZE)
    while data:
      print(data.decode('utf-8'))
      data = client_sock.recv(BUFSIZE)

    # clean up
    client_sock.shutdown(1)
    client_sock.close()
    print('connection closed.')

class HTTP_HeadServer:  #A re-worked version of EchoServer
  def __init__(self, host, port):
    print('listening on port {}'.format(port))
    self.host = host
    self.port = port

    self.setup_socket()

    self.accept()

    self.sock.shutdown()
    self.sock.close()

  def setup_socket(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.host, self.port))
    self.sock.listen(128)

  def accept(self):
    while True:
      (client, address) = self.sock.accept()
      #th = Thread(target=client_talk, args=(client, address))
      th = Thread(target=self.accept_request, args=(client, address))
      th.start()

  # here, we add a function belonging to the class to accept
  # and process a request
  def accept_request(self, client_sock, client_addr):
    print("accept request")
    data = client_sock.recv(BUFSIZE)
    req = data.decode('utf-8') #returns a string
    response = self.process_request(req)
    #once we get a response, we chop it into utf encoded bytes
    #and send it (like EchoClient)
    #print(response)
    for resp in response:
            client_sock.sendall(bytes(resp,'utf-8'))

    #clean up the connection to the client
    #but leave the server socket for recieving requests open
    client_sock.shutdown(1)
    client_sock.close()

  def process_request(self, request):
    print('######\nREQUEST:\n{}######'.format(request))
    linelist = request.strip().split(CRLF)
    reqline = linelist[0]
    rlwords = reqline.split()

    ## Select http method based on the request
    if len(rlwords) == 0:
        return ''
    elif 'csumn'  in request:
        return [MOVED_PERMANENTLY, 'Location', 'https://cs.umn.edu']
    elif rlwords[0] == 'HEAD':
        resource = rlwords[1]
        return self.head_request(resource)
    elif rlwords[0] == 'GET':
        resource = rlwords[1]
        return self.get_request(resource)
    elif rlwords[0] == 'PUT':
        resource = rlwords[1]
        return self.put_request(resource)
    elif rlwords[0] == 'DELETE':
        resource = rlwords[1]
        return self.delete_request(resource)
    elif rlwords[0] == 'OPTIONS':
        resource = rlwords[1]
        return self.options_request(resource)
    elif rlwords[0] == 'POST':
        resource = linelist[len(linelist)-1]
        return self.post_request(resource)
    else:
        return METHOD_NOT_ALLOWED

  ## Creates the response for HEAD request
  def head_request(self, resource):
    """Handles HEAD requests."""
    #path = os.path.join('.', resource) #look in directory where server is running
    p = os.getcwd()
    pth = os.path.join(p,resource[1:])
    if 'csumn' in resource:
      ret = [MOVED_PERMANENTLY, 'Location', 'https://cs.umn.edu']
    elif not os.path.exists(pth):
      get = get_contents(os.path.join(p, '404.html'))
      ret = [NOT_FOUND,get]
    elif not check_perms(pth):
      get = get_contents(os.path.join(p, '403.html'))
      ret = [FORBIDDEN, get]
    else:
      ret = OK
    return ret

  ## Creates the response for GET request
  def get_request(self,resource):
    ret = []
    p = os.getcwd()
    pth = os.path.join(p,resource[1:])
    if not os.path.exists(pth):
        get = get_contents(os.path.join(p, '404.html'))
        ret = NOT_FOUND + get
    elif not check_perms(pth):
        get = get_contents(os.path.join(p, '404.html'))
        ret = FORBIDDEN + get
    else:
        get = get_contents(pth)
        ret.append(OK)
        #ret.append(content)
        ret.append(get)
    return ret

  ## Creates the response for PUT request
  def put_request(self,resource):
    p = os.getcwd()
    if not os.path.isfile(resource[1:]) and open(resource[1:], "w") :
        content = 'Content-Location: {}{}'.format(resource, CRLF)
        ret = CREATED + content
    elif os.path.isfile(resource[1:]):
        content = 'Content-Location: {}{}'.format(resource, CRLF)
        ret = OK +  content
    else:
        get = get_contents(p + '/403.html')
        ret = FORBIDDEN + get
    return ret

  ## Creates the response for DELETE request
  def delete_request(self,resource):
    p = os.getcwd()
    if os.path.isfile(resource[1:]):
        os.remove(resource[1:])
        dt = 'Date:' + str(datetime.datetime.now()) + '{}'.format(CRLF)
        ret = OK + dt
    else:
        get = get_contents(os.path.join(p, '404.html'))
        ret = NOT_FOUND + get
    return ret

  ## Creates the response for OPTIONS request
  def options_request(self, resource):
      p = os.getcwd()
      pth = p + '/' + resource[1:]
      if resource == '/calendar.html':
          allow = 'Allow: OPTIONS, GET, HEAD {}'.format(CRLF)
          cache = 'Cache-Control: max-age= 604800 {}'.format(CRLF)
          dt = 'Date:' + str(datetime.datetime.now()) + '{}'.format(CRLF)
          leng = 'Content-Length: ' + str(len(get_contents(pth))) + '{}'.format(CRLF)
          ret = OK + allow + cache + dt + leng
      elif resource == '/form.html':
          allow = 'Allow: OPTIONS, GET, HEAD, POST {}'.format(CRLF)
          cache = 'Cache-Control: max-age= 604800 {}'.format(CRLF)
          dt = 'Date:' + str(datetime.datetime.now()) + '{}'.format(CRLF)
          leng = 'Content-Length: ' + str(len(get_contents(pth))) + '{}'.format(CRLF)
          ret = OK + allow + cache + dt + leng
      elif resource == '/':
          allow = 'Allow: OPTIONS, GET, HEAD, POST, PUT {}'.format(CRLF)
          cache = 'Cache-Control: max-age= 604800 {}'.format(CRLF)
          dt = 'Date:' + str(datetime.datetime.now()) + '{}'.format(CRLF)
          leng = 'Content-Length: ' + str(os.path.getsize(pth)) + '{}'.format(CRLF)
          ret = OK + allow + cache + dt + leng
      else:
          get = get_contents(os.path.join(p, '404.html'))
          ret = NOT_FOUND + get
      return ret

  ## Creates the response for POST request
  def post_request(self,resource):
      ret = [];
      lst = resource.split('&')
      for i in range(len(lst)):
          lst[i] = lst[i].split('=')
      html = """
            <html>
            <body>
            <h2> Following Form Data Submitted Successfully </h2>
            <p> Place Name: {} </p><p>
            </p><p>Address Line1: {} </p><p>
            <p> Address Line2: {} </p><p>
            </p><p> Open Time: {} </p><p>
            </p><p> Close Time: {} </p><p>
            </p><p> Additional Info Text: {} </p><p>
            </p><p> Additional Info URL: {} <p/>
            <div style="font-weight: normal; clear: both; margin-top: 25px; font-size: small; font-style: italic;">
            <p>The views and opinions expressed in this page are strictly those of the page author.
            <br>The contents of this page have not been reviewed or approved by the University of Minnesota.
            </p>
            </div>
            </body>
            </html>""".format(lst[0][1], lst[1][1], lst[2][1], lst[3][1], lst[4][1], lst[5][1], lst[6][1])

      #os.remove(pth)
      content = "Content-type:text/html\r\n\r\n"
      ret.append(OK)
      #ret.append(content)
      ret.append(html)
      return ret

def parse_args():
  parser = ArgumentParser()
  parser.add_argument('--host', type=str, default='localhost',
                      help='specify a host to operate on (default: localhost)')
  parser.add_argument('-p', '--port', type=int, default=9001,
                      help='specify a port to operate on (default: 9001)')
  args = parser.parse_args()
  return (args.host, args.port)


if __name__ == '__main__':
  (host, port) = parse_args()
  HTTP_HeadServer(host, port) #Formerly EchoServer

