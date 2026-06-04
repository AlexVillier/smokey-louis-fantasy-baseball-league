# Stage 1: build the React app
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
COPY vite.config.js .
COPY tsconfig.json* .
COPY public ./public
COPY src ./src

RUN npm install
RUN npm run build

# Stage 2: serve with nginx
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
