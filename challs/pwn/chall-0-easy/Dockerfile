FROM debian:bookworm

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update -y && apt-get dist-upgrade -y
RUN apt-get install -y wget apache2 libtinfo5

RUN wget http://snapshot.debian.org/archive/debian/20131228T034846Z/pool/main/b/bash/bash_4.3~rc1-1_amd64.deb -O /tmp/bash_43.deb && \
 apt install /tmp/bash_43.deb --allow-downgrades -y

ADD index.html /var/www/html/
ADD stats /usr/lib/cgi-bin/
RUN cd /etc/apache2/mods-enabled && ln -s ../mods-available/cgi.load
RUN chown www-data:www-data /usr/lib/cgi-bin/stats && chmod u+x /usr/lib/cgi-bin/stats
RUN echo '!$_th3r3_st1ll_0l|)_$erv3r$_runn1ng_th@t_bullsh!t?' > flag

RUN apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80
CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]