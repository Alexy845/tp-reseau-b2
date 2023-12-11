I. Simple bs program
1. First steps

🌞 Commandes...

Avant ça on refait nos ptites config de base sur nos vms soit l'ip hostname et tout le tralala habituel. puis on installe le git pour git clone notre projet.

```bash
[alexy@Serveur ~]$ sudo dnf install git -y
[alexy@Serveur ~]$ git clone https://gitlab.com/Alexy845/tp-dev.git
[alexy@Serveur ~]$ cd tp-dev/TP4/I.\ Simple\ bs\ program/
```

on recup les ip du client et de la machine:

```bash
[alexy@Client I. Simple bs program]$ ip a
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:73:e8:c2 brd ff:ff:ff:ff:ff:ff
    inet 10.1.2.21/24 brd 10.1.2.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe73:e8c2/64 scope link
       valid_lft forever preferred_lft forever


[alexy@Serveur I. Simple bs program]$ ip a
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:d1:38:33 brd ff:ff:ff:ff:ff:ff
    inet 10.1.2.22/24 brd 10.1.2.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fed1:3833/64 scope link
       valid_lft forever preferred_lft forever
```

Sur le serveur on a ouvert le port 13337:

```bash
[alexy@Serveur I. Simple bs program]$ sudo firewall-cmd --add-port=13337/tcp --permanent
success
[alexy@Serveur I. Simple bs program]$ sudo firewall-cmd --reload
success
```

On a choppé le repo , nos vms sont prêtes ? on peut commencer.

On lance notre serveur puis notre client:
```bash
[alexy@Serveur I. Simple bs program]$ python bs_server_I1.py

[alexy@Client I. Simple bs program]$ python bs_client_I1.py
Le serveur a répondu b'Salut mec.'
```

donc pendant que notre serveur tourne on fait notre ptit ss du serveur:

```bash
[alexy@Serveur ~]$ ss -a | grep -i 13337
tcp   LISTEN 0      1                                         0.0.0.0:13337                   0.0.0.0:*
```

