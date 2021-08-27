# iperf3 in a container
#
# Run as Server:
# docker run  -it --rm --name=iperf3-srv -p 5201:5201 iperf3 -s
#
# Run as Client (first get server IP address):
# docker inspect --format "{{ .NetworkSettings.IPAddress }}" iperf3-srv
# docker run  -it --rm iperf3 -c <SERVER_IP>
#
FROM debian:latest
MAINTAINER Jeremy Buck <jerbuck@cisco.com>

# Install binary and remove cache
RUN apt-get update \
    && apt-get install -y iperf3 \
    && apt-get install -y python3 \
    && rm -rf /var/lib/apt/lists/*

# Copy python scripts for application
ADD iperf3_args.py /app/iperf3_args.py

# Expose the default iperf3 server port
EXPOSE 5201

# entrypoint allows you to pass your arguments to the container at runtime
# very similar to a binary you would run. For example, in the following
# docker run -it <IMAGE> --help' is like running 'iperf3 --help'
CMD ["/app/iperf3_args.py"]
ENTRYPOINT ["python3"]
