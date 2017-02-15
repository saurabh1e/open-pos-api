MAINTAINER "saurabh.1e1@gmail.com"
FROM python:3.5-onbuild
EXPOSE 5000
ENV PYTH_SRVR dev
CMD gunicorn -w 2 -b :5000 manager:app