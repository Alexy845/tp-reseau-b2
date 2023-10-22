# TP2 : Environnement virtuel

Dans ce TP, on remanipule toujours les mêmes concepts qu'au TP1, mais en environnement virtuel avec une posture un peu plus orientée administrateur qu'au TP1.

- [TP2 : Environnement virtuel](#tp2--environnement-virtuel)
- [0. Prérequis](#0-prérequis)
- [I. Topologie réseau](#i-topologie-réseau)
  - [Topologie](#topologie)
  - [Tableau d'adressage](#tableau-dadressage)
  - [Hints](#hints)
  - [Marche à suivre recommandée](#marche-à-suivre-recommandée)
  - [Compte-rendu](#compte-rendu)
- [II. Interlude accès internet](#ii-interlude-accès-internet)
- [III. Services réseau](#iii-services-réseau)
  - [1. DHCP](#1-dhcp)
  - [2. Web web web](#2-web-web-web)

# 0. Prérequis

![One IP 2 VM](./img/oneip.jpg)

La même musique que l'an dernier :

- VirtualBox
- Rocky Linux
  - préparez une VM patron, prête à être clonée
  - système à jour (`dnf update`)
  - SELinux désactivé
  - préinstallez quelques paquets, je pense à notamment à :
    - `vim`
    - `bind-utils` pour la commande `dig`
    - `traceroute`
    - `tcpdump` pour faire des captures réseau

La ptite **checklist** que vous respecterez pour chaque VM :

- [ ] carte réseau host-only avec IP statique
- [ ] pas de carte NAT, sauf si demandée
- [ ] connexion SSH fonctionnelle
- [ ] firewall actif
- [ ] SELinux désactivé
- [ ] hostname défini

Je pardonnerai aucun écart de la checklist côté notation. 🧂🧂🧂

> Pour rappel : une carte host-only dans VirtualBox, ça permet de créer un LAN entre votre PC et une ou plusieurs VMs. La carte NAT de VirtualBox elle, permet de donner internet à une VM.

# I. Topologie réseau

Vous allez dans cette première partie préparer toutes les VMs et vous assurez que leur connectivité réseau fonctionne bien.

On va donc parler essentiellement IP et routage ici.

## Topologie

![Topologie](./img/topo.png)

## Tableau d'adressage

| Node             | LAN1 `10.1.1.0/24` | LAN2 `10.1.2.0/24` |
| ---------------- | ------------------ | ------------------ |
| `node1.lan1.tp2` | `10.1.1.11`        | x                  |
| `node2.lan1.tp2` | `10.1.1.12`        | x                  |
| `node1.lan2.tp2` | x                  | `10.1.2.11`        |
| `node2.lan2.tp2` | x                  | `10.1.2.12`        |
| `router.tp2`     | `10.1.1.254`       | `10.1.2.254`       |

## Hints

➜ **Sur le `router.tp2`**

Il sera nécessaire d'**activer le routage**. Par défaut Rocky n'agit pas comme un routeur. C'est à dire que par défaut il ignore les paquets qu'il reçoit s'il l'IP de destination n'est pas la sienne. Or, c'est précisément le job d'un routeur.

> Dans notre cas, si `node1.lan1.tp2` ping `node1.lan2.tp2`, le paquet a pour IP source `10.1.1.11` et pour IP de destination `10.1.2.11`. Le paquet passe par le routeur. Le routeur reçoit donc un paquet qui a pour destination `10.1.2.11`, une IP qui n'est pas la sienne. S'il agit comme un routeur, il comprend qu'il doit retransmettre le paquet dans l'autre réseau. Par défaut, la plupart de nos OS ignorent ces paquets, car ils ne sont pas des routeurs.

Pour activer le routage donc, sur une machine Rocky :

```bash
$ firewall-cmd --add-masquerade
$ firewall-cmd --add-masquerade --permanent
$ sysctl -w net.ipv4.ip_forward=1
```

---

➜ **Les switches sont les host-only de VirtualBox pour vous**

Vous allez donc avoir besoin de créer deux réseaux host-only. Faites bien attention à connecter vos VMs au bon switch host-only.

---

➜ **Aucune carte NAT**

## Marche à suivre recommandée

Dans l'ordre, je vous recommande de :

**1.** créer les VMs dans VirtualBox (clone du patron)  
**2.** attribuer des IPs statiques à toutes les VMs  
**3.** vous connecter en SSH à toutes les VMs  
**4.** activer le routage sur `router.tp2`  
**5.** vous assurer que les membres de chaque LAN se ping, c'est à dire :

- `node1.lan1.tp2`
  - doit pouvoir ping `node2.lan1.tp2`
  - doit aussi pouvoir ping `router.tp2` (il a deux IPs ce `router.tp2`, `node1.lan1.tp2` ne peut ping que celle qui est dans son réseau : `10.1.1.254`)
- `router.tp2` ping tout le monde
- les membres du LAN2 se ping aussi

**6.** ajouter les routes statiques

- sur les deux machines du LAN1, il faut ajouter une route vers le LAN2
- sur les deux machines du LAN2, il faut ajouter une route vers le LAN1

## Compte-rendu

☀️ Sur **`node1.lan1.tp2`**

- afficher ses cartes réseau
```
[alexy@node1Lan1 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:7b:49:43 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe7b:4943/64 scope link
       valid_lft forever preferred_lft forever
```
- afficher sa table de routage
```
[alexy@node1Lan1 ~]$ ip route show
10.1.1.0/24 dev enp0s8 proto kernel scope link src 10.1.1.11 metric 100
10.1.2.0/24 via 10.1.1.254 dev enp0s8 proto static metric 100
```
- prouvez qu'il peut joindre `node2.lan2.tp2`
```
[alexy@node1Lan1 ~]$ ping 10.1.2.12
PING 10.1.2.12 (10.1.2.12) 56(84) bytes of data.
64 bytes from 10.1.2.12: icmp_seq=1 ttl=63 time=2.43 ms
64 bytes from 10.1.2.12: icmp_seq=2 ttl=63 time=1.35 ms
^C
--- 10.1.2.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1016ms
rtt min/avg/max/mdev = 1.353/1.890/2.428/0.537 ms
```
- prouvez avec un `traceroute` que le paquet passe bien par `router.tp2`
```
[alexy@node1Lan1 ~]$ traceroute -n 10.1.1.254
traceroute to 10.1.1.254 (10.1.1.254), 30 hops max, 60 byte packets
 1  10.1.1.254  1.075 ms !X  0.979 ms !X  0.945 ms !X
```

# II. Interlude accès internet

![No internet](./img/no%20internet.jpg)

**On va donner accès internet à tout le monde.** Le routeur aura un accès internet, et permettra à tout le monde d'y accéder : il sera la passerelle par défaut des membres du LAN1 et des membres du LAN2.

**Ajoutez une carte NAT au routeur pour qu'il ait un accès internet.**

☀️ **Sur `router.tp2`**

- prouvez que vous avez un accès internet (ping d'une IP publique)
```
[alexy@router ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=24.9 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=115 time=24.3 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1003ms
rtt min/avg/max/mdev = 24.269/24.579/24.889/0.310 ms
```
- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)
```
[alexy@router ~]$ ping www.google.com
PING www.google.com (216.58.214.164) 56(84) bytes of data.
64 bytes from mad01s26-in-f164.1e100.net (216.58.214.164): icmp_seq=1 ttl=116 time=19.5 ms
64 bytes from mad01s26-in-f164.1e100.net (216.58.214.164): icmp_seq=2 ttl=116 time=23.5 ms
64 bytes from mad01s26-in-f164.1e100.net (216.58.214.164): icmp_seq=3 ttl=116 time=24.5 ms
^C
--- www.google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2008ms
rtt min/avg/max/mdev = 19.467/22.469/24.469/2.161 ms
```

☀️ **Accès internet LAN1 et LAN2**

- ajoutez une route par défaut sur les deux machines du LAN1
- ajoutez une route par défaut sur les deux machines du LAN2
- configurez l'adresse d'un serveur DNS que vos machines peuvent utiliser pour résoudre des noms
- dans le compte-rendu, mettez-moi que la conf des points précédents sur `node2.lan1.tp2`
```
[alexy@node2Lan1 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.12
NETMASK=255.255.255.0
GATEWAY=10.1.1.254
[alexy@node2Lan1 ~]$ sudo systemctl restart NetworkManager
[alexy@node2Lan1 ~]$ sudo cat /etc/resolv.conf
# Generated by NetworkManager
nameserver 8.8.8.8
nameserver 1.1.1.1
```
- prouvez que `node2.lan1.tp2` a un accès internet :
  - il peut ping une IP publique
```
[alexy@node2Lan1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=114 time=23.1 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=114 time=28.9 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1128ms
rtt min/avg/max/mdev = 23.142/26.036/28.930/2.894 ms
```
  - il peut ping un nom de domaine public
```
[alexy@node2Lan1 ~]$ ping google.com
PING google.com (142.250.179.78) 56(84) bytes of data.
64 bytes from par21s19-in-f14.1e100.net (142.250.179.78): icmp_seq=1 ttl=116 time=22.0 ms
64 bytes from par21s19-in-f14.1e100.net (142.250.179.78): icmp_seq=2 ttl=116 time=20.3 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 20.337/21.147/21.957/0.810 ms
```

# III. Services réseau

**Adresses IP et routage OK, maintenant, il s'agirait d'en faire quelque chose nan ?**

Dans cette partie, on va **monter quelques services orientés réseau** au sein de la topologie, afin de la rendre un peu utile que diable. Des machines qui se `ping` c'est rigolo mais ça sert à rien, des machines qui font des trucs c'est mieux.

## 1. DHCP

![Dora](./img/dora.jpg)

Petite **install d'un serveur DHCP** dans cette partie. Par soucis d'économie de ressources, on recycle une des machines précédentes : `node2.lan1.tp2` devient `dhcp.lan1.tp2`.

**Pour rappel**, un serveur DHCP, on en trouve un dans la plupart des LANs auxquels vous vous êtes connectés. Si quand tu te connectes dans un réseau, tu n'es pas **obligé** de saisir une IP statique à la mano, et que t'as un accès internet wala, alors il y a **forcément** un serveur DHCP dans le réseau qui t'a proposé une IP disponible.

> Le serveur DHCP a aussi pour rôle de donner, en plus d'une IP disponible, deux informations primordiales pour l'accès internet : l'adresse IP de la passerelle du réseau, et l'adresse d'un serveur DNS joignable depuis ce réseau.

**Dans notre TP, son rôle sera de proposer une IP libre à toute machine qui le demande dans le LAN1.**

> Vous pouvez vous référer à [ce lien](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=dhcp&f=1) ou n'importe quel autre truc sur internet (je sais c'est du Rocky 8, m'enfin, la conf de ce serveur DHCP ça bouge pas trop).

---

Pour ce qui est de la configuration du serveur DHCP, quelques précisions :

- vous ferez en sorte qu'il propose des adresses IPs entre `10.1.1.100` et `10.1.1.200`
- vous utiliserez aussi une option DHCP pour indiquer aux clients que la passerelle du réseau est `10.1.1.254` : le routeur
- vous utiliserez aussi une option DHCP pour indiquer aux clients qu'un serveur DNS joignable depuis le réseau c'est `1.1.1.1`

---

☀️ **Sur `dhcp.lan1.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan1.tp2` devient `dhcp.lan1.tp2`)
```
[alexy@node2Lan1 ~]$ echo 'dhcpLan1.tp2' | sudo tee /etc/hostname
[alexy@node2Lan1 ~]$ sudo systemctl restart NetworkManager
```
- changez son adresse IP en `10.1.1.253`

```	
[alexy@dhcpLan1 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
[sudo] password for alexy:
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.253
NETMASK=255.255.255.0
GATEWAY=10.1.1.254
DNS1=1.1.1.1

[alexy@dhcpLan1 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a7:05:34 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fea7:534/64 scope link
       valid_lft forever preferred_lft forever
```

- setup du serveur DHCP
  - commande d'installation du paquet
  ```
  [alexy@dhcpLan1 ~]$ sudo dnf -y install dhcp-server
  ```
  - fichier de conf
```
[alexy@dhcpLan1 ~]$ sudo cat /etc/dhcp/dhcpd.conf
# create new
# specify domain name
option domain-name     "srv.world";
# specify DNS server's hostname or IP address
option domain-name-servers     dlp.srv.world;
# default lease time
default-lease-time 600;
# max lease time
max-lease-time 7200;
# this DHCP server to be declared valid
authoritative;
# specify network address and subnetmask
subnet 10.1.1.0 netmask 255.255.255.0 {
    # specify the range of lease IP address
    range dynamic-bootp 10.1.1.100 10.1.1.200;
    # specify broadcast address
    option broadcast-address 10.1.1.255;
    # specify gateway
    option routers 10.1.1.254;
}
```
  - service actif
```
[alexy@dhcpLan1 ~]$ sudo systemctl enable --now dhcpd
Created symlink /etc/systemd/system/multi-user.target.wants/dhcpd.service → /usr/lib/systemd/system/dhcpd.service.

[alexy@dhcpLan1 ~]$ systemctl status dhcpd
● dhcpd.service - DHCPv4 Server Daemon
     Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
     Active: active (running) since Sun 2023-10-22 17:30:10 CEST; 1min 43s ago
       Docs: man:dhcpd(8)
             man:dhcpd.conf(5)
   Main PID: 1719 (dhcpd)
     Status: "Dispatching packets..."
      Tasks: 1 (limit: 4609)
     Memory: 5.2M
        CPU: 15ms
     CGroup: /system.slice/dhcpd.service
             └─1719 /usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid

Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Config file: /etc/dhcp/dhcpd.conf
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Database file: /var/lib/dhcpd/dhcpd.leases
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: PID file: /var/run/dhcpd.pid
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Source compiled to use binary-leases
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Wrote 0 leases to leases file.
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Listening on LPF/enp0s8/08:00:27:a7:05:34/10.1.1.0/24
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Sending on   LPF/enp0s8/08:00:27:a7:05:34/10.1.1.0/24
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Sending on   Socket/fallback/fallback-net
Oct 22 17:30:10 dhcpLan1.tp2 dhcpd[1719]: Server starting service.
Oct 22 17:30:10 dhcpLan1.tp2 systemd[1]: Started DHCPv4 Server Daemon.
```

☀️ **Sur `node1.lan1.tp2`**

- demandez une IP au serveur DHCP
```
[alexy@node1Lan1 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
[sudo] password for alexy:
DEVICE=enp0s8

BOOTPROTO=dhcp
ONBOOT=yes
```
- prouvez que vous avez bien récupéré une IP *via* le DHCP
- prouvez que vous avez bien récupéré l'IP de la passerelle
```
[alexy@node1Lan1 ~]$ ip route
default via 10.1.1.254 dev enp0s8 proto dhcp src 10.1.1.100 metric 100
10.1.1.0/24 dev enp0s8 proto kernel scope link src 10.1.1.100 metric 100
10.1.2.0/24 via 10.1.1.254 dev enp0s8 proto static metric 100
```

- prouvez que vous pouvez `ping node1.lan2.tp2`
```
[alexy@node1Lan1 ~]$ ping 10.1.2.11
PING 10.1.2.11 (10.1.2.11) 56(84) bytes of data.
64 bytes from 10.1.2.11: icmp_seq=1 ttl=63 time=1.37 ms
64 bytes from 10.1.2.11: icmp_seq=2 ttl=63 time=1.29 ms
^C
--- 10.1.2.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.294/1.334/1.374/0.040 ms
```

## 2. Web web web

Un petit serveur web ? Pour la route ?

On recycle ici, toujours dans un soucis d'économie de ressources, la machine `node2.lan2.tp2` qui devient `web.lan2.tp2`. On va y monter un serveur Web qui mettra à disposition un site web tout nul.

---

La conf du serveur web :

- ce sera notre vieil ami NGINX
- il écoutera sur le port 80, port standard pour du trafic HTTP
- la racine web doit se trouver dans `/var/www/site_nul/`
  - vous y créerez un fichier `/var/www/site_nul/index.html` avec le contenu de votre choix
- vous ajouterez dans la conf NGINX **un fichier dédié** pour servir le site web nul qui se trouve dans `/var/www/site_nul/`
  - écoute sur le port 80
  - répond au nom `site_nul.tp2`
  - sert le dossier `/var/www/site_nul/`
- n'oubliez pas d'ouvrir le port dans le firewall 🌼

---

☀️ **Sur `web.lan2.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan2.tp2` devient `web.lan2.tp2`)
```
[alexy@node2Lan2 ~]$ echo 'web.lan2.tp2' | sudo tee /etc/hostname
```
- setup du service Web
  - installation de NGINX
  ```
  [alexy@web ~]$ sudo dnf install nginx
  
  ```
  - gestion de la racine web `/var/www/site_nul/`
  ```
  [alexy@web ~]$ sudo mkdir -p /var/www/site_nul/html
  [alexy@web ~]$ sudo chown -R alexy:alexy /var/www/site_nul/html
  [alexy@web ~]$ sudo cat /var/www/site_nul/html/index.html
  <html>
      <head>
          <title>Mon super site nul</title>
      </head>
      <body>
          <h1>MEOW MEOW<em>site_nul</em>. </h1>
  <p>rhasoul sa passe</p>
      </body>
  </html>

  [alexy@web ~]$ sudo cat /etc/nginx/conf.d/site_nul.conf
  server {
        listen 80;
        listen [::]:80;

        root /var/www/site_nul/html;
        index index.html index.htm index.nginx-debian.html;

        server_name site_nul www.site_nul;

        location / {
                try_files $uri $uri/ =404;
        }
  }
  [alexy@web ~]$ sudo nginx -t
  nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
  nginx: configuration file /etc/nginx/nginx.conf test is successful
  sudo systemctl restart nginx
  [alexy@web ~]$ sudo chcon -vR system_u:object_r:httpd_sys_content_t:s0 /var/www/site_nul/
  changing security context of '/var/www/site_nul/html/index.html'
  changing security context of '/var/www/site_nul/html'
  changing security context of '/var/www/site_nul/'
  ```
  - configuration NGINX
```
[alexy@web ~]$ sudo systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
[alexy@web ~]$ sudo systemctl start nginx
```
  - service actif
```
[alexy@web ~]$ sudo systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: disabled)
     Active: active (running) since Sun 2023-10-22 18:01:21 CEST; 7s ago
    Process: 1504 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
    Process: 1505 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
    Process: 1506 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
   Main PID: 1507 (nginx)
      Tasks: 3 (limit: 4609)
     Memory: 2.8M
        CPU: 32ms
     CGroup: /system.slice/nginx.service
             ├─1507 "nginx: master process /usr/sbin/nginx"
             ├─1508 "nginx: worker process"
             └─1509 "nginx: worker process"

Oct 22 18:01:21 web.lan2.tp2 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Oct 22 18:01:21 web.lan2.tp2 nginx[1505]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Oct 22 18:01:21 web.lan2.tp2 nginx[1505]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Oct 22 18:01:21 web.lan2.tp2 systemd[1]: Started The nginx HTTP and reverse proxy server.
```
  - ouverture du port firewall
```
  [alexy@web ~]$ sudo firewall-cmd --add-port=80/tcp      --permanent
  success
  [alexy@web ~]$ sudo firewall-cmd --reload
  success
```
- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)
```
[alexy@web ~]$ sudo ss -lutnp | grep nginx
tcp   LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=1574,fd=6),("nginx",pid=1573,fd=6),("nginx",pid=1572,fd=6))
tcp   LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=1574,fd=7),("nginx",pid=1573,fd=7),("nginx",pid=1572,fd=7))
```
- prouvez que le firewall est bien configuré
```
[alexy@web ~]$ sudo firewall-cmd --list-all
[sudo] password for alexy:
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s8
  sources:
  services: cockpit dhcpv6-client ssh
  ports: 80/tcp
  protocols:
  forward: yes
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```
☀️ **Sur `node1.lan1.tp2`**

- éditez le fichier `hosts` pour que `site_nul.tp2` pointe vers l'IP de `web.lan2.tp2`
```
[alexy@node1Lan1 ~]$ sudo cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.2.12 site_nul.tp2
```
- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp2`
```
10.1.2.12 site_nul.tp2
[alexy@node1Lan1 ~]$ curl site_nul.tp2
<html>
    <head>
        <title>Mon super site nul</title>
    </head>
    <body>
        <h1>MEOW MEOW<em>site_nul</em>. </h1>
<p>rhasoul sa passe</p>
    </body>
</html>
```	

![That's all folks](./img/thatsall.jpg)
