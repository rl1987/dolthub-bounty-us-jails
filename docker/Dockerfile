FROM debian:latest
RUN apt-get update && apt-get install -y libxext-dev libxrender-dev libxtst-dev firefox-esr
RUN firefox -CreateProfile "user /root/user" -headless
ADD prefs.js /root/user/prefs.js
ADD logins.json /root/user/logins.json
CMD firefox -profile /root/user
