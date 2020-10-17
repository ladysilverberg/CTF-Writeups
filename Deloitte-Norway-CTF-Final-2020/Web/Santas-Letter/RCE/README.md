## WEB250 - Santa's Letter (RCE)
By using the LFI vulnerability from the Vulnerability task, we can also get the source code for send.php:

```
inc=php://filter/convert.base64-encode/resource=send
```

Decoding the source code shows that another file called translit.php is included. We can use LFI once again to get the source code. Putting these together, we can see that translit is simply a library to convert letters and symbols from foreign languages to ASCII/the roman alphabet. We also see that when we submit a letter and drawing, the file extension of the drawing is checked to filter out *php, php3, php4, phtml, ini, htaccess*, which makes it troublesome to upload a webshell. The MIME-type of the drawing is also check if it contains "image/". Then the filename calls translit to translate foreign symbols and uploads the file.

There is one vulnerability here though. By posting a letter with a drawing, intercepting the request in burp and sending it to the repeater we can tamper with the MIME type, content and filename. We ensure that the MIME type contains *image/*, set the contents to contains a webshell and then we set the filename to *webshell.пhp*. By doing so, we will passe the MIME type validation, pass the file extension validation and finally the russian п will be converted to a 'p' by translit. Then the file webshell.php is uploaded and we have remote code execution.

I also uploaded another PHP-file containing the code:

```php=
<?php
    ($handle = opendir('../.')) {
        while (false !== ($entry = readdir($handle))) {
            if ($entry != "." && $entry != "..") {
                echo "$entry\n";
            }
        }
        closedir($handle);
    }
?>
```

The script prints all files in the directory above /uploads, and we see a file called MAGIC-FLAG-FILE.php. Using LFI again:

```
inc=php://filter/convert.base64-encode/resource=MAGIC-FILE-FLAG
```

And decoding it, we get the flag.