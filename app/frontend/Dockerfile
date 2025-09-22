FROM harbor.cicd.s15m.nl/ictu-devops-pub/nginxinc/nginx-unprivileged:1.21.6-alpine_devops
USER root
RUN apk update
RUN apk upgrade
COPY ./dist /app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080:8080