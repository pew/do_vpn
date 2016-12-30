# DigitalOcean VPN VPS

This little webapp just starts a plain image in a given region and installs OpenVPN so you can watch netflix if abroad. Since DO charges by the hour you can spin up an instance in the evening, watch some series and shut it down a few hours later by paying just for three hours intead of a month.

You can create, start, stop and destroy an instance through this webapp.

# TODO

* [ ] you should make sure to have your own dockerfile in case the repo or github is down etc.
* [ ] fix your intercoolerjs stuff
* [ ] create a mobile template

# setup
O RLY?


## config.py

create a `config.py` with your API Key:

```
headers = {"Authorization":"Bearer 2342"}
```

## userdata.txt

create a `userdata.txt` file to install docker and start a ipsec vpn server container. Also, please adjust the environment variables

```
#cloud-config
package_upgrade: true
package_reboot_if_required: true
runcmd:
- apt-get update
- curl -fsSL https://get.docker.com/ | sh
- curl -fsSL https://get.docker.com/gpg | sudo apt-key add -
- modprobe af_key
- /usr/bin/docker run --name ipsec-vpn-server --env-file /root/vpn.env --restart=always -p 500:500/udp -p 4500:4500/udp -v /lib/modules:/lib/modules:ro -d --privileged hwdsl2/ipsec-vpn-server

write_files:
-   content: |
        VPN_IPSEC_PSK=asdf1234
        VPN_USER=netflix
        VPN_PASSWORD=l0l0l
    path: /root/vpn.env
```

# Licenses

* [docker-ipsec-vpn-server](https://github.com/hwdsl2/docker-ipsec-vpn-server/blob/master/LICENSE.md)
* [jQuery](https://github.com/jquery/jquery/blob/master/LICENSE.txt)
* [bootstrap](https://github.com/twbs/bootstrap/blob/master/LICENSE)
