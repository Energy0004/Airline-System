FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN chmod +x node_modules/.bin/*

EXPOSE 5173

CMD ["npx", "vite", "--host"]