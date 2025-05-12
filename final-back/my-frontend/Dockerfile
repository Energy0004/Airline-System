FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

# Add the line below to give execute permission to all npm binaries
RUN chmod +x node_modules/.bin/*

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]