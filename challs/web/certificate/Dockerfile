FROM php:7.4-fpm


# Install necessary dependencies
RUN apt-get update
RUN apt-get --yes install libfreetype6-dev \
                          libjpeg62-turbo-dev \
                          libpng-dev \
                          libwebp-dev 

RUN set -e; \
    docker-php-ext-configure gd --with-jpeg --with-webp --with-freetype; \
    docker-php-ext-install -j$(nproc) gd

COPY ./flag /
WORKDIR /var/www/html
COPY ./img.png .
COPY ./index.php .
COPY ./dompdf ./dompdf

CMD ["php", "-S", "0.0.0.0:7000"]

# docker build -t certificate-web-chall .
# docker tag certificate-web-chall:latest registry.ctf.secompufscar.com.br/certificate-web-chall:latest
# docker push registry.ctf.secompufscar.com.br/certificate-web-chall:latest
