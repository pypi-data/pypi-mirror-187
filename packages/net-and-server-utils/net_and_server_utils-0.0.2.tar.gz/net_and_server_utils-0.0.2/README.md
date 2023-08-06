# net_and_server_utils

The project aims at creating a library for following 7 functionalities using Python standard libraries only: -
- API to access various services via HTTP as a client. For example, downloadingdata or interacting with a REST-based API -> urlib
- API to implement a server that communicates with clients using the TCP Internet protocol -> socketserver
- API to implement a server that communicates with clients using the UDP Internet protocol -> socketserver
- API to generate a range of all the IP addresses that it represents (in a given range) for ipv4 and ipv6 you have a  CIDR network -> ipaddress
- API to control or interact with your program remotely over the network using a simple REST-based interface -> cgi
- API to execute functions or methods in Python programs running on remote machines -> xmlrpc
- API to implement a network service involving sockets where servers and clients authenticate themselves and encrypt the transmitted data using SSL - socket

The library with the above functionalities is published on PyPI and can be installed in your environment as: -
```
pip3 install net-and-server-utils
```

The structure of the repo is as follows: -
- src/docs - contains the html documentation created using sphinx. Open module.html in the browser to see the main page.
- src/net_and_server_utils - contains the code for various functionalities.
- tests - contains unit tests for the project.
