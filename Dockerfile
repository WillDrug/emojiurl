FROM node:10 as build-deps

# build react app in docker
COPY ./front ./front
WORKDIR /front
RUN npm install
RUN npm run build

# prepare live environment

FROM python:3.6
LABEL MAINTAINER="WillDrug"

WORKDIR /app/

# copy built react app
COPY --from=build-deps /front/build ./templates

# Install python deps
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN python -c "import sqlite3; conn = sqlite3.connect('emojilinks.db'); c=  conn.cursor(); c.execute('CREATE TABLE links (url varchar, short varchar, ttl number)'); conn.commit(); conn.close()"


# Bundle python src and react build
COPY ./codebase ./codebase
COPY ./toydiscover ./toydiscover
COPY codec.py flaskapp.py ./
COPY ./templates ./templates

# ENV HOST
# ENV DEBUG
# ENV SECRET

CMD [ "python", "flaskapp.py" ]