# Setup latest image of nginx
FROM nginx:latest
COPY static-html-directory /usr/share/nginx/html

# $ docker run --name some-nginx -d some-content-nginx
# $ docker run --name some-nginx -d -p 8080:80 some-content-nginx

# Complex config

# $ docker run --name my-custom-nginx-container -v /host/path/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx

COPY nginx.conf /etc/nginx/nginx.conf

# Run nginx in read-only mode
#$ docker run -d -p 80:80 --read-only -v $(pwd)/nginx-cache:/var/cache/nginx -v $(pwd)/nginx-pid:/var/run nginx

# Run as non-root user
#$ docker run -d -v $PWD/nginx.conf:/etc/nginx/nginx.conf nginx