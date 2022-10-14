FROM harbor.cicd.s15m.nl/ocw-lsp-pub/nginxinc/nginx-unprivileged:1.21.6-alpine_lsp
USER root
RUN apk update
RUN apk upgrade
COPY ./dist /app
COPY nginx.conf /etc/nginx/nginx.conf