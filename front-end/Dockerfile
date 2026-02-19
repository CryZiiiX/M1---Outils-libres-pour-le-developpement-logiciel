# Image front-end Vue : Vite dev server
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Port exposé : 5173 (Vite)
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
