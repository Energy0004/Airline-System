FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

# Make sure npm binaries are executable
RUN chmod +x node_modules/.bin/*

COPY . .

EXPOSE 5173

CMD ["npx", "vite", "--host"]
