# Setup offcial image for go language
FROM golang:latest

WORKDIR /go/src/app
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

CMD ["app"]

# Setup official centos image
#FROM centos:latest
#RUN wget https://dl.google.com/go/go1.13.linux-amd64.tar.gz
#RUN echo "68a2297eb099d1a76097905a2ce334e3155004ec08cdea85f24527be3c48e856  go1.13.linux-amd64.tar.gz
#" | sha256sum -c
#RUN false
## Untar downloaded go package
#RUN sudo tar -C /usr/local -xzf go1.13.linux-amd64.tar.gz
#
#ENV PATH /usr/local/go/bin
## Test installed go package
#COPY src .
#WORKDIR ~/src/hello
#RUN go build
#RUN ./hello
