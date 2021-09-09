FROM alpine:latest
MAINTAINER Jeremy Buck <jerbuck@cisco.com>

# Install binary and remove cache
RUN apk add --no-cache iperf3 \
  && apk add --no-cache python3 \
  && apk add --no-cache bash

# Expose the iperf3 port(s)
EXPOSE 5201-5211

# Entrypoint of top ensures container starts, 
# you can then "session" to it from the cat9k
ENTRYPOINT ["top"]
