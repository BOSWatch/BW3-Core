FROM alpine:latest AS build-base
RUN apk add --no-cache git make cmake g++ libusb-dev libpulse

FROM build-base AS rtl_fm
RUN git clone --depth 1 https://gitea.osmocom.org/sdr/rtl-sdr.git /opt/rtl_sdr
WORKDIR /opt/rtl_sdr/build
RUN cmake .. && make

FROM build-base AS multimon
RUN git clone --depth 1 https://github.com/EliasOenal/multimon-ng.git /opt/multimon
WORKDIR /opt/multimon/build
RUN cmake .. && make

FROM alpine:latest AS boswatch
ARG BW_VERSION=develop
RUN apk add git && \
    git clone --depth 1 --branch ${BW_VERSION} https://github.com/BOSWatch/BW3-Core.git /opt/boswatch


FROM python:alpine AS boswatch-base
LABEL maintainer="bastian@schroll-software.de"

#           for RTL    for MM
RUN apk add libusb-dev libpulse && \
    pip3 install pyyaml

COPY --from=boswatch /opt/boswatch/ /opt/boswatch/
RUN mkdir /opt/boswatch/log
COPY --from=multimon /opt/multimon/build/multimon-ng /opt/multimon/multimon-ng
COPY --from=rtl_fm /opt/rtl_sdr/build/src/ /opt/rtl_sdr/
WORKDIR /opt/boswatch

FROM boswatch-base AS client
CMD python3 /opt/boswatch/bw_client.py -c client.yaml

FROM boswatch-base AS server
CMD python3 /opt/boswatch/bw_server.py -c server.yaml
EXPOSE 8080
