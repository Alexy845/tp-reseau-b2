☀️ **Carte réseau WiFi**

- l'adresse MAC de votre carte WiFi
    
    ``` 
    PS C:\Users\alexy> ipconfig /all
    [...]
    Carte réseau sans fil Wi-Fi :
    Adresse physique . . . . . . . . . . . : F8-B5-4D-6C-58-0E
    [...] 
    ```

- l'adresse IP de votre carte WiFi
    ``` 
    PS C:\Users\alexy> ipconfig /all
    [...]
    Carte réseau sans fil Wi-Fi :
   Adresse IPv4. . . . . . . . . . . . . .: 192.168.86.204(préféré)
    [...] 
    ```
- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi

  - en notation CIDR, par exemple `/16`
    ```
    /24
    ```
  - ET en notation décimale, par exemple `255.255.0.0`
    ``` 
    PS C:\Users\alexy> ipconfig /all
    [...]
    Carte réseau sans fil Wi-Fi :
    Masque de sous-réseau. . . . . . . . . : 255.255.255.0(préféré)
    [...] 
    ```

---

☀️ **Déso pas déso**

Pas besoin d'un terminal là, juste une feuille, ou votre tête, ou un tool qui calcule tout hihi. Déterminer...

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi
```
192.168.86.0
```
- l'adresse de broadcast
```
192.168.86.255
```
- le nombre d'adresses IP disponibles dans ce réseau
```
254
```
---

☀️ **Hostname**

- déterminer le hostname de votre PC
```
PS C:\Users\alexy> hostname
MSI
```

---

☀️ **Passerelle du réseau**

Déterminer...

- l'adresse IP de la passerelle du réseau
```

    PS C:\Users\alexy> ipconfig
    [...]
    Carte réseau sans fil Wi-Fi :
   Passerelle par défaut. . . . . . . . . : fe80::942a:9bff:fe2a:360a%30
                                       192.168.86.2
    [...]
```
- l'adresse MAC de la passerelle du réseau
```
PS C:\Users\alexy> arp -a | findstr 192.168.86.2
    [...]
    Carte réseau sans fil Wi-Fi :
  192.168.86.2          96-2a-9b-2a-36-0a     dynamique
    [...]

```

---

☀️ **Serveur DHCP et DNS**

Déterminer...

- l'adresse IP du serveur DHCP qui vous a filé une IP
```
   PS C:\Users\alexy> ipconfig /all
    [...]
    Carte réseau sans fil Wi-Fi :
     Serveur DHCP . . . . . . . . . . . . . : 192.168.86.2
    [...]

```
- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet

```
   PS C:\Users\alexy> ipconfig /all
    [...]
    Carte réseau sans fil Wi-Fi :
     Serveurs DNS. . .  . . . . . . . . . . : 192.168.86.2
    [...]

```

---

☀️ **Table de routage**

Déterminer...

- dans votre table de routage, laquelle est la route par défaut
```
PS C:\Users\alexy> route print
    [...]
    IPv4 Table de routage
=============================================================
Itinéraires actifs :
Destination réseau    Masque réseau  Adr. passerelle   Adr. interface Métrique
          0.0.0.0          0.0.0.0     192.168.86.2   192.168.86.204     55
    [...]

```


# II. Go further

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1`
```
C:\Windows\System32>echo 1.1.1.1 b2.hello.vous
```
- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`
```
C:\Windows\System32>ping b2.hello.vous

Envoi d’une requête 'ping' sur b2.hello.vous [1.1.1.1] avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=809 ms TTL=55
Réponse de 1.1.1.1 : octets=32 temps=93 ms TTL=55

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 2, reçus = 2, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 93ms, Maximum = 809ms, Moyenne = 451ms
Ctrl+C
^C
```

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo

- le port du serveur auquel vous êtes connectés
- le port que votre PC a ouvert en local pour se connecter au port du serveur distant
```
PS C:\Users\alexy> netstat -b -a -n -o | Select-String 443 -Context 0,1

>   UDP    0.0.0.0:60384          0.0.32.14:443                          10180
   [opera.exe]
```
---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`

> Ca s'appelle faire un "lookup DNS".
```
PS C:\Users\alexy> nslookup www.ynov.com
Serveur :   UnKnown
Address:  192.168.220.251

Réponse ne faisant pas autorité :
Nom :    www.ynov.com
Addresses:  2606:4700:20::ac43:4ae2
          2606:4700:20::681a:be9
          2606:4700:20::681a:ae9
          104.26.10.233
          172.67.74.226
          104.26.11.233
```

- à quel nom de domaine correspond l'IP `174.43.238.89`

> Ca s'appelle faire un "reverse lookup DNS".
```
PS C:\Users\alexy> nslookup 174.43.238.89
Serveur :   UnKnown
Address:  192.168.220.251

Nom :    89.sub-174-43-238.myvzw.com
Address:  174.43.238.89
```
---

☀️ **Hop hop hop**

Déterminer...

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```
PS C:\Users\alexy> tracert www.ynov.com

Détermination de l’itinéraire vers www.ynov.com [2606:4700:20::681a:ae9]
avec un maximum de 30 sauts :

  1     4 ms     3 ms     6 ms  2a02-8440-6441-5f0d-0000-0000-0000-0027.rev.sfr.net [2a02:8440:6441:5f0d::27]
  2    74 ms    24 ms    43 ms  2a02-8440-6441-5f0d-0000-0047-998d-9a40.rev.sfr.net [2a02:8440:6441:5f0d:0:47:998d:9a40]
  3    87 ms    27 ms    41 ms  fdff:8440:6006:1054::96
  4     *      105 ms    29 ms  2a02-8400-1001-fc0e-0000-0000-0001-0002.rev.sfr.net [2a02:8400:1001:fc0e::1:2]
  5     *       56 ms     *     2a02-8400-0000-0003-0000-0000-0000-6d2e.rev.sfr.net [2a02:8400:0:3::6d2e]
  6    65 ms    70 ms    70 ms  fc00:0:0:101::437
  7   111 ms    63 ms    69 ms  fc00:0:0:101::431
  8     *       70 ms     *     fc00:0:0:101::6bc
  9    70 ms    58 ms    70 ms  2400:cb00:19:200::48
 10    53 ms    72 ms    76 ms  2400:cb00:534:3::
 11    72 ms    57 ms    61 ms  2606:4700:20::681a:ae9

Itinéraire déterminé.
```

---

☀️ **IP publique**

Déterminer...

- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)
```
PS C:\Users\alexy> ipconfig /all | Select-String Wi-Fi -Context 0,9

Carte réseau sans fil Wi-Fi :

     Passerelle par défaut. . . . . . . . . : 10.33.79.254
```
---

☀️ **Scan réseau**

Déterminer...

- combien il y a de machines dans le LAN auquel vous êtes connectés

> Allez-y mollo, on va vite flood le réseau sinon. :)

```
PS C:\Users\alexy> arp -a

Interface : 10.4.1.20 --- 0x15
  Adresse Internet      Adresse physique      Type
  10.4.1.255            ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique

Interface : 10.3.2.16 --- 0x1d
  Adresse Internet      Adresse physique      Type
  10.3.2.255            ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique

Interface : 192.168.220.204 --- 0x1e
  Adresse Internet      Adresse physique      Type
  192.168.220.251       d6-84-b5-89-cb-4e     dynamique
  192.168.220.255       ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique

Interface : 192.168.56.1 --- 0x1f
  Adresse Internet      Adresse physique      Type
  192.168.56.255        ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique

Interface : 10.3.1.15 --- 0x20
  Adresse Internet      Adresse physique      Type
  10.3.1.255            ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
```

![Stop it](./img/stop.png)

# III. Le requin

Faites chauffer Wireshark. Pour chaque point, je veux que vous me livrez une capture Wireshark, format `.pcap` donc.

Faites *clean* 🧹, vous êtes des grands now :

- livrez moi des captures réseau avec uniquement ce que je demande et pas 40000 autres paquets autour
  - vous pouvez sélectionner seulement certains paquets quand vous enregistrez la capture dans Wireshark
- stockez les fichiers `.pcap` dans le dépôt git et côté rendu Markdown, vous me faites un lien vers le fichier, c'est cette syntaxe :

```markdown
[Lien vers capture ARP](./captures/arp.pcap)
```

---

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
- capturez un échange ARP entre votre PC et la passerelle du réseau

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

[Arp.pcapng](./arp.pcap)

---

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
- capturez une requête DNS vers le domaine de votre choix et la réponse
- vous effectuerez la requête DNS en ligne de commande

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
- effectuez une connexion qui sollicite le protocole TCP
- je veux voir dans la capture :
  - un 3-way handshake
  - un peu de trafic
  - la fin de la connexion TCP

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

![Packet sniffer](img/wireshark.jpg)

> *Je sais que je vous l'ai déjà servi l'an dernier lui, mais j'aime trop ce meme hihi 🐈*