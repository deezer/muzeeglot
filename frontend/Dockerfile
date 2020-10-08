# ----
# build image
FROM node:alpine as build-stage

RUN mkdir -p /application
WORKDIR /application
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# ----
# production stage
FROM nginx:alpine AS muzeeglot
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/muzeeglot.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /application/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# ----
# production stage
FROM nginx:alpine AS muzeeglot-ssl
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/muzeeglot-ssl.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /application/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]