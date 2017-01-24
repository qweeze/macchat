# macchat
A toy serverless LAN instant messenger.

<p align="center">
  <img src="https://github.com/qweeze/macchat/raw/master/doc/screenshot.png?raw=true" width=75% alt="screenshot"/>
</p>

Messages are transported in raw ethernet frames' payload; therefore their length is limited to 1500 bytes and 
communication is restricted to broadcast domain.

Command line interface is implemented with [Python Prompt Toolkit](https://github.com/jonathanslenders/python-prompt-toolkit/).
Network interactions rely on [Scapy](https://github.com/secdev/scapy) package.

## Installation
```
$ git clone https://github.com/qweeze/macchat.git
$ cd macchat
$ sudo python setup.py install
```
Start it by typing `macchat`.

## Features
- both Python 2 and 3 compatible
- symmetric AES encryption with HMAC
- is basically a REPL that prints messages to stdout
