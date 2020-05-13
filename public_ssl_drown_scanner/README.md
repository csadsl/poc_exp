DROWN Scanner
=============

**Important: Some versions of this tool produce the following lines on startup:**

```
Import Error - most likely due to missing pycrypto libaries - disabling crypto functionality
ImportError('cannot import name TLSHandshake',)
```

**These lines do not prevent the tool from producing correct results.**

Learn more here: https://github.com/nimia/public_drown_scanner/issues/40


This python utility scans for vulnerability to the DROWN attack against TLS.
It is distributed under the GPLv2 license, and includes a specific version of
https://github.com/tintinweb/scapy-ssl_tls (which is also distributed under GPLv2)
and
https://github.com/hiviah/pyx509.
We are grateful to both authors for providing these useful libraries.

This utility was written in an ad-hoc manner in order to identify
only the most common vulnerable configurations.
We emphasize that **it cannot accurately detect all vulnerable servers,
and no one should rely on it to confidently determine a particular server is not vulnerable**.

In particular, the utility only detects SSLv2 support *by a single port*.
DROWN is made worse by its cross-protocol nature, i.e.
an HTTPS server that doesn't support SSLv2 may be vulnerable
because it shares its public key with an SMTP server that does.
This utility *cannot detect this scenario*, and **we strongly recommend
testing servers using our online scanner, at https://drownattack.com**.

Likewise, it may also have false positives,
i.e. it may indicate a server is vulnerable when it is in fact not.

Hubert Kario has also made different scanning scripts available here:
https://mta.openssl.org/pipermail/openssl-dev/2016-March/005602.html

Dependencies:
--------------
You need the packages listed below.
This dependency list is unfortunately a work in progress.
If you think you're missing a dependency, please read the instructions for other operating systems,
and see if they might shed light on the issue.
Pull requests clarifying the dependency list (and also general PRs) are welcome.


### On a Debian system:

`sudo apt-get install tcpdump python-pyasn1 scapy python-crypto python-pip`

On Debian Jessie also install

`sudo apt-get install python-enum`

and for all Debian versions, also run

`sudo pip install scapy-ssl_tls`

### On a Fedora/RHEL system:

`sudo yum install python-enum scapy python-crypto tcpdump`

and also run `sudo pip install scapy-ssl_tls`

### Or generally with pip:

`sudo pip install enum pycrypto scapy pyasn1 scapy-ssl_tls`

### CentOS:

Some users have encountered problems on CentOS with the asn1 package (or in general).
In addition to installing the above dependencies for Fedora/RHEL,
please see this issue for a suggested solution:

https://github.com/nimia/public_drown_scanner/issues/30

### Mac users

You may also need dnet as a dependency.

### Windows
The latest version of Scapy supports Windows out-of-the-box, with Python 2.6.
See here for installation instructions:

http://www.secdev.org/projects/scapy/doc/installation.html#windows

And here if you absolutely need to use Python 2.7:

https://stackoverflow.com/questions/5447461/running-scapy-on-windows-with-python-2-7

### Even more dependencies
One user has graciously documented setting up the dependencies
on a stripped-down installation of CentOS:
https://github.com/nimia/public_drown_scanner/issues/17

### Docker
```bash
docker build -t public-drown-scanner .
docker run -it public-drown-scanner localhost 443
```

### FreeBSD

Short version: use python libdnet from ports and install everything else inside a virtualenv.

Long version:

```bash
sudo pkg install py27-virtualenv libdnet py27-libdnet
git clone https://github.com/nimia/public_drown_scanner.git
cd public_drown_scanner
virtualenv --system-site-packages .
bin/pip install enum pycrypto scapy pyasn1 scapy-ssl_tls pcapy
```

Usage examples:
---------------
```
python scanner.py localhost 443
...
python scanner.py localhost 587 -esmtp
...
python scanner.py localhost 143 -imap
...
python scanner.py localhost 25 -esmtp
...
python scanner.py localhost 110 -pop3
...
python scanner.py localhost 443 -bare
````
