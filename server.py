#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        # Initializing variables to be used later:
        content = ''
        contentType = ''
        location = ''

        # Handling recieved data:
        self.data = self.request.recv(1024).strip().decode('utf-8')
        data = self.data.splitlines()[0].split()
        method, ogIndex, version = data[0], data[1], data[2]
        print ('Got a request of: %s\n' % self.data)

        # Handling method; and main chunk of code:
        if method != 'GET':
            statusCode = '405 Method Not Allowed'
        else:
            # Serving from www and serving index.html from directories:
            index = ogIndex
            if index[-1] == '/':
                index += 'index.html'
            index = 'www' + index

            # Try to open valid file/directory:
            try:
                # Opening requested file to get its contents:
                content = open(index, 'r').read()
                # Getting current working directory and the absolute path of requested index:
                cwd = os.getcwd()
                absPath = os.path.abspath(ogIndex)
                path = cwd + '/www/' + absPath
                # Checking if the path is not a directory:
                if os.path.isdir(path) == False:
                    # Checking if the path is not a file:
                    if os.path.isfile(path) == False:  
                        statusCode = '404 Page Not Found'
                        # ** Need these next two lines or else we get a max header error, not sure why. Should ask prof **                         
                        content = ''
                        contentType = ''
                    else:
                        statusCode = '200 OK'
                else:
                    statusCode = '200 OK'

                # Handling the mime-types for html and css:
                if index.endswith('.html'):
                    contentType = 'Content-Type: text/html'
                if index.endswith('.css'):
                    contentType = 'Content-Type: text/css'

            # If the try block fails then we just update status code to 404 OR check to see if we need to handle a 301 code:
            except:
                statusCode = '404 Page Not Found' 
                # If there's no '/' at the end of the requested index then we must give 301 code and route the url properly:
                if ogIndex[-1] != '/':
                    statusCode = '301 Moved Permanently'
                    location = 'Location: ' + ogIndex + '/' +'\n'

        response = self.respond(version, statusCode, location, contentType, content)
        print(response)
        self.request.sendall(bytearray(response, 'utf-8'))


    def respond(self, version, statusCode, location, contentType, content):
        response = version + ' ' + statusCode + '\n' + location + contentType + '\n\n' + content + '\n'
        return response

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()