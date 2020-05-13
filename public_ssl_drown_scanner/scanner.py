#!/usr/bin/env python2

import sys
from enum import Enum
import time
import datetime
import socket
# In case your pip install pycrypto has placed the module in lowercase directories
try:
    import Crypto.Cipher
except ImportError:
    import crypto
    sys.modules['Crypto'] = crypto
import signal
from binascii import hexlify
import base64
import os

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy
from scapy.all import *
from scapy_ssl_tls.ssl_tls import *

from pyx509.pkcs7.asn1_models.X509_certificate import Certificate
from pyx509.pkcs7_models import X509Certificate, PublicKeyInfo, ExtendedKeyUsageExt
from pyx509.pkcs7.asn1_models.decoder_workarounds import decode

import select

SOCKET_TIMEOUT = 15
SOCKET_RECV_SIZE = 80 * 1024

CON_FAIL = "con fail"
NO_STARTTLS = "no starttls"
NO_TLS = "no tls"
VULN = "vuln"

def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)

    return result

CHALLENGE    = 'a' * 16
CLEAR_KEY    = '\0' * 11
KEY_ARGUMENT = '\0' * 8

class CipherSuite(object):
    @classmethod
    def get_string_description(cls):
        raise NotImplementedError()

    @classmethod
    def get_constant(cls):
        return eval("SSLv2CipherSuite." + cls.get_string_description())

    @classmethod
    def get_client_master_key(cls, encrypted_pms):
        raise NotImplementedError()

    @classmethod
    def verify_key(cls, connection_id, server_finished):
        raise NotImplementedError()

    @classmethod
    def get_encrypted_pms(cls, public_key, secret_key):
        pkcs1_pubkey = Crypto.Cipher.PKCS1_v1_5.new(public_key)
        encrypted_pms = pkcs1_pubkey.encrypt(secret_key)
        return encrypted_pms

class RC4Export(CipherSuite):
    SECRET_KEY = 'b' * 5

    @classmethod
    def get_string_description(cls):
        return "RC4_128_EXPORT40_WITH_MD5"

    @classmethod
    def get_client_master_key(cls, public_key):
        client_master_key = SSLv2ClientMasterKey(cipher_suite=cls.get_constant(),
                                                 encrypted_key=cls.get_encrypted_pms(public_key, cls.SECRET_KEY),
                                                 clear_key=CLEAR_KEY)
        return client_master_key

    @classmethod
    def verify_key(cls, connection_id, server_finished):
        md5 = MD5.new(CLEAR_KEY + cls.SECRET_KEY + '0' + CHALLENGE + connection_id).digest()
        rc4 = Crypto.Cipher.ARC4.new(md5)
        if not rc4.decrypt(server_finished[2:]).endswith(CHALLENGE):
            return False
        return True

class RC4(CipherSuite):
    SECRET_KEY = 'b' * 16
    CLEAR_KEY  = 'a' * 15

    @classmethod
    def get_string_description(cls):
        return "RC4_128_WITH_MD5"

    @classmethod
    def get_client_master_key(cls, public_key):
        client_master_key = SSLv2ClientMasterKey(cipher_suite=cls.get_constant(),
                                                 encrypted_key=cls.get_encrypted_pms(public_key, cls.SECRET_KEY),
                                                 clear_key=cls.CLEAR_KEY)
        return client_master_key

    @classmethod
    def verify_key(cls, connection_id, server_finished):
        md5 = MD5.new((cls.CLEAR_KEY + cls.SECRET_KEY)[:16] + '0' + CHALLENGE + connection_id).digest()
        rc4 = Crypto.Cipher.ARC4.new(md5)
        if not rc4.decrypt(server_finished[2:]).endswith(CHALLENGE):
            return False
        return True

class RC2Export(CipherSuite):
    SECRET_KEY = 'b' * 5

    @classmethod
    def get_string_description(cls):
        return "RC2_128_CBC_EXPORT40_WITH_MD5"

    @classmethod
    def get_client_master_key(cls, public_key):
        client_master_key = SSLv2ClientMasterKey(cipher_suite=cls.get_constant(),
                                                 encrypted_key=cls.get_encrypted_pms(public_key, cls.SECRET_KEY),
                                                 key_argument=KEY_ARGUMENT,
                                                 clear_key=CLEAR_KEY)
        return client_master_key

    @classmethod
    def verify_key(cls, connection_id, server_finished):
        md5 = MD5.new(CLEAR_KEY + cls.SECRET_KEY + '0' + CHALLENGE + connection_id).digest()
        rc2 = Crypto.Cipher.ARC2.new(md5, mode=Crypto.Cipher.ARC2.MODE_CBC, IV=KEY_ARGUMENT, effective_keylen=128)
        try:
            decryption = rc2.decrypt(server_finished[3:])
        except ValueError, e:
            return False
        if decryption[17:].startswith(CHALLENGE):
            return True
        return False

class DES(CipherSuite):
    SECRET_KEY = 'b' * 8

    @classmethod
    def get_string_description(cls):
        return "DES_64_CBC_WITH_MD5"

    @classmethod
    def get_client_master_key(cls, public_key):
        client_master_key = SSLv2ClientMasterKey(cipher_suite=cls.get_constant(),
                                                 encrypted_key=cls.get_encrypted_pms(public_key, cls.SECRET_KEY),
                                                 key_argument=KEY_ARGUMENT)
        return client_master_key

    @classmethod
    def verify_key(cls, connection_id, server_finished):
        md5 = MD5.new(cls.SECRET_KEY + '0' + CHALLENGE + connection_id).digest()
        des = Crypto.Cipher.DES.new(md5[:8], mode=Crypto.Cipher.DES.MODE_CBC, IV=KEY_ARGUMENT)
        try:
            decryption = des.decrypt(server_finished[3:])
        except ValueError, e:
            return False
        if decryption[17:].startswith(CHALLENGE):
            return True
        return False

cipher_suites = [RC2Export, RC4Export, RC4, DES]

def parse_certificate(derData):
    cert = decode(derData, asn1Spec=Certificate())[0]
    x509cert = X509Certificate(cert)
    tbs = x509cert.tbsCertificate

    algType = tbs.pub_key_info.algType
    algParams = tbs.pub_key_info.key

    if (algType != PublicKeyInfo.RSA):
        print 'Certificate algType is not RSA'
        raise Exception()

    return RSA.construct((long(hexlify(algParams["mod"]), 16), long(algParams["exp"])))

class Protocol(Enum):
    BARE_SSLv2 = 1
    ESMTP      = 2
    IMAP       = 3
    POP3       = 4
    PROXY      = 3128
    XMPP       = 5222
    FTP        = 21

def sslv2_connect(ip, port, protocol, cipher_suite, result_additional_data):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(SOCKET_TIMEOUT)
    try:
        s.connect((ip, port))
    except socket.error, e:
        try:
            s.connect((ip, port))
        except socket.error, e:
            try:
                s.connect((ip, port))
            except socket.error, e:
                print '%s: Case 1 - port is apparently closed (after 3 tries); Connect failed' % ip
                return CON_FAIL

    starttls_response = "n/a"
    try:
        if protocol == Protocol.ESMTP:
            banner = s.recv(SOCKET_RECV_SIZE)
            s.send("EHLO testing\r\n")
            ehlo_response = s.recv(SOCKET_RECV_SIZE)
            if "starttls" not in ehlo_response.lower():
                print "%s: Case 2a; Server apparently doesn't support STARTTLS" % ip
                return NO_STARTTLS
            s.send("STARTTLS\r\n")
            starttls_response = s.recv(SOCKET_RECV_SIZE)
        elif protocol == Protocol.IMAP:
            banner = s.recv(SOCKET_RECV_SIZE)
            s.send(". CAPABILITY\r\n")
            banner = s.recv(SOCKET_RECV_SIZE)
            if "starttls" not in banner.lower():
                print "%s: Case 2b; Server apparently doesn't support STARTTLS" % ip
                return NO_STARTTLS
            s.send(". STARTTLS\r\n")
            starttls_response = s.recv(SOCKET_RECV_SIZE)
        elif protocol == Protocol.POP3:
            banner = s.recv(SOCKET_RECV_SIZE)
            s.send("STLS\r\n")
            starttls_response = s.recv(SOCKET_RECV_SIZE)
        elif protocol == Protocol.PROXY:
            to = "github.com:443" if not ':' in sys.argv[-1] else sys.argv[-1]
            print "%s: connecting to target %s" % (ip, to)
            s.send("CONNECT %s HTTP/1.1\r\n\r\n" % to)
            starttls_response = s.recv(SOCKET_RECV_SIZE)
        elif protocol == Protocol.XMPP:
            to = ip
            s.send("<?xml version='1.0' ?><stream:stream to='%s' xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams' version='1.0'>"%to)
            banner = ''
            while not "</stream:features>" in banner: # get all the chunks
                banner += s.recv(SOCKET_RECV_SIZE)
                if not "<stream:" in banner:
                   break 
            if not '</starttls>' in banner:
                print "%s: Case 2b; Server apparently doesn't support STARTTLS" % ip
                return NO_STARTTLS
            s.send("<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>")
            starttls_response = s.recv(SOCKET_RECV_SIZE)
        elif protocol == Protocol.FTP:
            banner = s.recv(SOCKET_RECV_SIZE)
            s.send("AUTH TLS\r\n")
            starttls_response = s.recv(SOCKET_RECV_SIZE)
    except socket.error, e:
        print "Errorx: " + str(e) + " - starttls_response: '" + starttls_response + "'"
        print '%s: Case 2c; starttls negotiation failed' % ip
        return NO_STARTTLS


    client_hello = SSLv2Record()/SSLv2ClientHello(cipher_suites=SSL2_CIPHER_SUITES.keys(),challenge=CHALLENGE)
    s.sendall(str(client_hello))

    rlist, wlist, xlist = select.select([s], [], [s], SOCKET_TIMEOUT)
    if s in xlist or not s in rlist:
        print '%s: Case 3a; Server did not response properly to client hello' % ip
        s.close()
        return "3a: %s" % NO_TLS

    try:
        server_hello_raw = s.recv(SOCKET_RECV_SIZE)
    except socket.error, e:
        print '%s: Case 3b; Connection reset by peer when waiting for server hello' % ip
        s.close()
        return "3b: %s" % NO_TLS

    server_hello = timeout(SSL, (server_hello_raw,), timeout_duration=SOCKET_TIMEOUT)
    if server_hello == None:
        print '%s: Case 3c; Timeout on parsing server hello' % ip
        s.close()
        return "3c: %s" % NO_TLS

    if not SSLv2ServerHello in server_hello:
        print '%s: Case 3d; Server hello did not contain SSLv2' % ip
        s.close()
        return "3d: %s" % NO_TLS

    parsed_server_hello = server_hello[SSLv2ServerHello]
    connection_id = parsed_server_hello.connection_id
    cert = parsed_server_hello.certificates

    try:
        public_key = parse_certificate(cert)
    except:
        # Server could still be vulnerable, we just can't tell, so we assume it isn't
        print '%s: Case 4a; Could not extract public key from DER' % ip
        s.close()
        return "4a: %s" % NO_TLS

    server_advertised_cipher_suites = parsed_server_hello.fields["cipher_suites"]
    cipher_suite_advertised = cipher_suite.get_constant() in server_advertised_cipher_suites

    client_master_key = cipher_suite.get_client_master_key(public_key)
    client_key_exchange = SSLv2Record()/client_master_key

    s.sendall(str(client_key_exchange))

    rlist, wlist, xlist = select.select([s], [], [s], SOCKET_TIMEOUT)
    if s in xlist:
        print '%s: Case 4b; Exception on socket after sending client key exchange' % ip
        s.close()
        return "4b: %s" % NO_TLS
    if not s in rlist:
        print '%s: Case 5; Server did not send finished in time' % ip
        s.close()
        return "5: %s" % NO_TLS
    try:
        server_finished = s.recv(SOCKET_RECV_SIZE)
    except socket.error, e:
        print '%s: Case 4c; Connection reset by peer when waiting for server finished' % ip
        s.close()
        return "4c: %s" % NO_TLS

    if server_finished == '':
        print '%s: Case 4d; Empty server_finished' % ip
        s.close()
        return "4d: %s" % NO_TLS

    if not cipher_suite.verify_key(connection_id, server_finished):
        print '%s: Case 7; Symmetric key did not successfully verify on server finished message' % ip
        return "7: %s" % NO_TLS

    s.close()

    result_additional_data['cipher_suite_advertised'] = cipher_suite_advertised
    return "%s:%s" % (VULN, base64.b64encode(public_key.exportKey(format='DER')))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: %s <hostname> <port> [-xmpp|-ftp|-proxy|-esmtp|-imap|-pop3|-bare]' % sys.argv[0])

    ip = sys.argv[1]
    port = int(sys.argv[2])
    scan_id = os.getcwd()
    dtime = datetime.datetime.now()
    print 'Testing %s on port %s' % (ip, port)

    protocol = Protocol.BARE_SSLv2
    if len(sys.argv) >= 4:
        if sys.argv[3] == '-esmtp':
            protocol = Protocol.ESMTP
        elif sys.argv[3] == '-imap':
            protocol = Protocol.IMAP
        elif sys.argv[3] == '-pop3':
            protocol = Protocol.POP3
        elif sys.argv[3] == '-bare':
            protocol = Protocol.BARE_SSLv2
        elif sys.argv[3] == '-proxy':
            protocol = Protocol.PROXY
        elif sys.argv[3] == '-ftp':
            protocol = Protocol.FTP
        elif sys.argv[3] == '-xmpp':
            protocol = Protocol.XMPP
        else:
            print 'You gave 3 arguments, argument 3 is not a recognized protocol. Bailing out'
            sys.exit(1)

    vulns = []
    for cipher_suite in cipher_suites:

        string_description = cipher_suite.get_string_description()
        ret_additional_data = {}
        ret = sslv2_connect(ip, port, protocol, cipher_suite, ret_additional_data)

        if ret.startswith(VULN):
            pub_key = ret.replace('%s:' % VULN, '')

            cve_string = ""
            if not ret_additional_data['cipher_suite_advertised']:
                cve_string = " to CVE-2015-3197"
            if string_description == "RC4_128_WITH_MD5":
                if cve_string == "":
                    cve_string = " to CVE-2016-0703"
                else:
                    cve_string += " and CVE-2016-0703"

            print '%s: Server is vulnerable%s, with cipher %s\n' % (ip, cve_string, string_description)
        else:
            print '%s: Server is NOT vulnerable with cipher %s, Message: %s\n' % (ip, string_description, ret)
