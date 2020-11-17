FROM kong:0.14-centos

LABEL description="Centos 7 + Kong 0.14 + kong-oidc plugin"

RUN yum install -y git unzip && yum clean all
RUN yum install -y openssl-devel -y
RUN yum install -y gcc

RUN luarocks install lua-resty-session
RUN luarocks install lua-resty-openidc
RUN luarocks install kong-oidc