FROM nginx:stable-alpine

# -- Remove old configuration -- #
RUN rm -f /etc/nginx/conf.d/*

# -- Custom NGINX configuration -- #
COPY nginx-dev.conf /etc/nginx/conf.d/app.conf
