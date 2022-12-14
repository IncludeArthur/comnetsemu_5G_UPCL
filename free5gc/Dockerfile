FROM golang:1.14.4-stretch AS builder

LABEL maintainer="Free5GC <support@free5gc.org>"

ENV DEBIAN_FRONTEND noninteractive

# Install dependencies
RUN apt-get update \
    && apt-get -y install gcc cmake autoconf libtool pkg-config libmnl-dev libyaml-dev apt-transport-https ca-certificates \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y nodejs yarn

# Clean apt cache
RUN apt-get clean

# Get Free5GC
RUN cd $GOPATH/src \
    && git clone --recursive -b v3.2.1 -j `nproc` https://github.com/free5gc/free5gc.git

# Build Free5GC NFs & WebUI
RUN cd $GOPATH/src/free5gc \
    && make all

# Final image
FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    	bash \
    	iproute2 \
        libmnl0 \
        libyaml-0-2 \
    	nano \
        curl \
        net-tools \
        tcpdump \
        iptables \
        mongodb \
        iperf3 && \
    apt-get autoremove -y && apt-get autoclean

RUN mkdir -p config/TLS/ public

# Copy executables
COPY --from=builder /go/src/free5gc/bin /free5gc/bin
COPY --from=builder /go/src/free5gc/NFs /free5gc/NFs
COPY --from=builder /go/src/free5gc/webconsole /free5gc/webconsole

# Copy configuration files
COPY --from=builder /go/src/free5gc/config /free5gc/config

WORKDIR /free5gc
