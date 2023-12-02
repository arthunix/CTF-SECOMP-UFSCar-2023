FROM ubuntu:mantic

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update -y && apt-get dist-upgrade -y
RUN apt-get install sudo gcc gdb python3 openssh-server file nano python3-pwntools libc6-i386 -y

RUN useradd -rm -d /home/secomp -s /bin/bash secomp
#RUN echo 'root:root' | chpasswd
RUN echo 'secomp:secomp' | chpasswd

ADD sys_login /sys_login
ADD flag /flag

RUN chown -R root:root /sys_login
RUN chown -R root:root /flag
RUN chmod +s /sys_login
RUN chmod 660 /flag

RUN apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#RUN mkdir /var/run/sshd

RUN echo "MaxAuthTries 25" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
