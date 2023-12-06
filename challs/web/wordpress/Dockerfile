FROM wordpress:5.6.2

COPY flag /flag
COPY wpdiscuz /var/www/html/wp-content/plugins/wpdiscuz/

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["apache2-foreground"]

# docker build -t wordpress-rev-shell . -f Dockerfile.wordpress-rev-shell
# docker tag wordpress-rev-shell:latest registry.ctf.secompufscar.com.br/wordpress-rev-shell:latest
# docker push registry.ctf.secompufscar.com.br/wordpress-rev-shell:latest

# docker buildx build --platform linux/amd64,linux/arm64 -t registry.example.com/wordpress-rev-shell --push .
