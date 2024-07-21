FROM node:22-alpine

COPY --chown=node:node package*.json ./
RUN npm install

WORKDIR /usr/src/frontend

EXPOSE 3000

CMD ["npm", "run", "dev"]