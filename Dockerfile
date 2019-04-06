FROM gorialis/discord.py:3.7.2-stretch-rewrite-extras

WORKDIR /app

RUN sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl && \
 sudo chmod a+rx /usr/local/bin/youtube-dl && \
 sudo pip3 install feedparser markovify && \
 sudo apt-get update && \
 sudo apt-get install units -y



COPY . .

CMD ["./run-owl.sh"]
