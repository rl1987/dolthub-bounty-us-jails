#!/bin/bash

set -x

apt-get update
apt-get install -y python3 python3-pip tmux git vim visidata default-jre
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh > /tmp/install.sh && bash /tmp/install.sh
dolt config --global --add user.email rimantas@keyspace.lt
dolt config --global --add user.name "rl1987"
pip3 install openpyxl requests lxml js2xml doltpy xlrd TableauScraper PyPDF2 tabula-py googlemaps

curl -sSL https://repos.insights.digitalocean.com/install.sh -o /tmp/install.sh
bash /tmp/install.sh

mkdir /root/go

wget https://golang.org/dl/go1.18.1.linux-amd64.tar.gz -O /tmp/go1.18.1.linux-amd64.tar.gz
tar -C /usr/local -xzf /tmp/go1.18.1.linux-amd64.tar.gz
echo "export PATH=\$PATH:/usr/local/go/bin" >> /etc/profile
echo "export GOPATH=/root/go" >> /etc/profile

pushd /bin
ln -s /usr/local/go/bin/go go
popd

pushd /tmp
git clone https://github.com/dolthub/bounties.git
pushd /tmp/bounties/go/payments/cmd/calc_payments
go install .
popd
popd

pushd /bin
ln -s /root/go/bin/calc_payments calc_payments
popd

apt-get install -y python3-pdfminer

