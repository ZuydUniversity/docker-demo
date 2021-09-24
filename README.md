# docker-demo
Voorbeelden en uitleg m.b.t. het gebruik van Docker.

## Wat is Docker
Docker is een platform dat een geïsoleerde omgeving bied voor (server)applicaties. De applicatie wordt samen met de dependencies/libraries geïnstalleerd in een Docker image. Dit zorgt voor een consistente omgeving voor development, testen en productie. Hiermee wordt dus "it works on my machine" voorkomen.

### Dockerfile > Image > Container
1. Een Dockerfile beschrijft de opbouw van een Image.
2. Een Image is een gebouwde Dockerfile en wordt gebruikt voor het maken van containers
3. Een Container is een instantie van een Image.
    - Het is dus mogelijk om meerdere instanties van hetzelfde Image naast elkaar te draaien

### Docker tegenover Virtual Machines
Let op, Docker containers zijn geen virtuele machines. Bij VMs wordt in iedere machine een apart operating system geïnstalleerd. Dit is bij Docker niet het geval. Alleen de applicatie en de dependencies worden geïsoleerd.

![docker-vs-vms](https://i2.wp.com/www.docker.com/blog/wp-content/uploads/Blog.-Are-containers-..VM-Image-1.png?resize=1024%2C435&ssl=1)

## Basis Commandos
- `docker --help` of `docker <subcommand> --help`: Geeft informatie over de beschikbare (sub-)commandos
- Containers draaien en stoppen gebeurt met: `run`: (nieuwe container maken), `start`: (bestaande container starten), `stop`, `kill`, `rm`
- Informatie over een of meer containers: `ps`, `stats`, `logs`
- (Linux) commandos runnen in een container: `exec`
- Builden Image: `build`

### Run
`run` wordt gebruikt bij het aanmaken van een nieuwe container. Hierbij kunnen verschillende opties meegegeven worden:
- Poorten, `-p`: Forward een poort van de host naar de docker container. Neem bijvoorbeeld `-p 8000:5000`, dan wordt poort 8000 van de host (zoals je laptop/pc) doorverbonden naar poort 5000 binnen de container.
- Volumes, `-v`: Verbind een lokale folder op de host naar een folder in de container. Bijvoorbeeld `-v /some/host/folder:/some/container/folder`. Wanneer nu een file in `/some/host/folder` aangepast wordt, is deze automatisch ook in `/some/container/folder` aangepast (en andersom).
- Environment variabelen, `-e`: Geeft een variabele mee naar de container. Dit wordt meestal gebruikt voor configuratie, bijvoorbeeld `-e MYSQL_DATABASE=SomeDb`. Deze variabelen worden gespecificeerd in de Dockerfile.
- Naam, `--name`: De naam van de container, bijvoorbeeld `--name app1_db`. Wanneer deze optie niet gebruikt wordt, genereerd Docker zelf een random naam.
- Detach, `-d`: Zorgt dat de container op de achtergrond gedraait wordt.

**LET OP!** gebruik je geen volume en verwijder je een container, dan is alle data in de container weg. Door gebruik te maken van volumes kun je deze data bewaren (en/of delen) tussen verschillende instanties van een container.

Een voorbeeld voor het `run` command:
```docker
docker run -e MYSQL_DATABASE=AppDb -e MARIADB_ROOT_PASSWORD=secret_pass --name app_db -v /some/dir:/var/lib/mysql -p 8000:3306 -d mariadb:latest
```
### Start/Stop/Kill/Rm
De `start`/`stop`/`kill`/`rm` commandos worden gebruikt om de containers aan en uit te zetten en om containers te verwijderen. Deze commandos hebben altijd het patroon `docker <command> <container_name/container_id>`. Bijvoorbeeld `docker start app_db`.

Het `stop` commando en het `kill` commando worden beiden gebruikt om containers af te sluiten. Het verschil is dat `stop` containers "gracefully" afsluit, waar `kill` de container geforceerd stopt (denk aan het sluiten van een applicatie met de Task Manager).

Om een container te verwijderen met `rm` moet de container eerst afgesloten zijn of moet de force optie (`-f`) gebruikt worden (dus `docker rm -f app_db`).

### ps
`ps` geeft een overzicht van alle actieve containers. Door gebruik te maken van de `-a` optie worden ook de niet actieve containers getoond.
```bash
$ docker ps -a
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS                    PORTS                                       NAMES
9a013891e3eb   dockerdemo_front   "/usr/src/app/entryp…"   4 seconds ago   Up 4 seconds              0.0.0.0:9002->5000/tcp, :::9002->5000/tcp   dockerdemo_front_1
eaaa5e3b5a31   dockerdemo_serv    "/usr/src/app/entryp…"   5 seconds ago   Up 4 seconds              0.0.0.0:9001->5000/tcp, :::9001->5000/tcp   dockerdemo_serv_1
4317a8acfa5f   postgres           "docker-entrypoint.s…"   23 hours ago    Exited (0) 23 hours ago                                               app_db_1
580fafc334aa   redis              "docker-entrypoint.s…"   23 hours ago    Exited (0) 23 hours ago                                               app_redis_1

```

### stats
Het `stats` commando geeft het resource gebruikt van de actieve containers weer.
```bash
$ docker stats
CONTAINER ID   NAME                 CPU %     MEM USAGE / LIMIT    MEM %     NET I/O       BLOCK I/O       PIDS
9a013891e3eb   dockerdemo_front_1   0.02%     37.77MiB / 14.6GiB   0.25%     19kB / 0B     4.1kB / 549kB   3
eaaa5e3b5a31   dockerdemo_serv_1    0.01%     35.59MiB / 14.6GiB   0.24%     19.8kB / 0B   467kB / 545kB   3
```

### logs
Het `logs` commando geeft de logs weer van een specifieke container. Hiervoor wordt de naam van de container of het ID gebruikt.
```bash
$ docker logs dockerdemo_front_1
[2021-09-24 08:22:14 +0000] [7] [INFO] Starting gunicorn 20.1.0
[2021-09-24 08:22:14 +0000] [7] [INFO] Listening at: http://0.0.0.0:5000 (7)
[2021-09-24 08:22:14 +0000] [7] [INFO] Using worker: sync
[2021-09-24 08:22:14 +0000] [8] [INFO] Booting worker with pid: 8
```

### exec
`exec` kan worden gebruikt om (Linux) commandos te draaien in de container. Het onderstaande voorbeeld draait het `ls` (print folder inhoud) commando in de container:
```bash
$ docker exec dockerdemo_front_1 ls  
Dockerfile
__pycache__
app.py
entrypoint.sh
files
requirements.txt
```

`exec` kan ook worden gebruikt om interactieve sessies te starten in de container, bijvoorbeeld een Python shell:
```bash
$ docker exec -it dockerdemo_front_1 python 
Python 3.9.7 (default, Sep  3 2021, 20:10:26) 
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
Of een interactieve bash shell:
```bash
$ docker exec -it dockerdemo_front_1 /bin/sh    
# ls
Dockerfile  __pycache__  app.py  entrypoint.sh	files  requirements.txt
# 
```

### build
Om van een Dockerfile een image te maken, kan het `build` commando worden gebruikt. Door de `-t` optie te gebruiken kan dit image ook voorzien worden van een naam. Hierbij wordt ook de output getoond van iedere stap in het build proces.
```bash
$ docker build -t some_demo_img .        
Sending build context to Docker daemon   7.68kB
Step 1/11 : FROM python:3.8
3.8: Pulling from library/python
955615a668ce: Already exists 
2756ef5f69a5: Already exists 
911ea9f2bd51: Already exists 
27b0a22ee906: Already exists 
8584d51a9262: Already exists 
524774b7d363: Already exists 
9460f6b75036: Pull complete 
9bc548096c18: Pull complete 
1d87379b86b8: Pull complete 
Digest: sha256:c2842aababbe377f9c76f172d9eb39487e23f306b2f29f020f3f6654cb0876e9
Status: Downloaded newer image for python:3.8
 ---> ff08f08727e5
Step 2/11 : ENV PIP_DISABLE_PIP_VERSION_CHECK=on
 ---> Running in 8124f3a93305
Removing intermediate container 8124f3a93305
 ---> 01eec1f31e01
Step 3/11 : ENV SERV_URL ""
 ---> Running in 0ef983a27739
Removing intermediate container 0ef983a27739
 ---> 1edd320cf359
Step 4/11 : WORKDIR /usr/src/app
 ---> Running in 23fe9284aef9
Removing intermediate container 23fe9284aef9
 ---> d6f952c5b3d2
Step 5/11 : COPY ./requirements.txt /usr/src/app/requirements.txt
 ---> 20e5ab1acb46
Step 6/11 : RUN pip install -r requirements.txt
 ---> Running in 85bc781bdc74
Collecting flask
  Downloading Flask-2.0.1-py3-none-any.whl (94 kB)
Collecting requests
  Downloading requests-2.26.0-py2.py3-none-any.whl (62 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.1-py3-none-any.whl (133 kB)
Collecting click>=7.1.2
  Downloading click-8.0.1-py3-none-any.whl (97 kB)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.1-py3-none-any.whl (288 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.7-py2.py3-none-any.whl (138 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.2-py3-none-any.whl (59 kB)
Collecting charset-normalizer~=2.0.0
  Downloading charset_normalizer-2.0.6-py3-none-any.whl (37 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2021.5.30-py2.py3-none-any.whl (145 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (30 kB)
Installing collected packages: MarkupSafe, Werkzeug, urllib3, Jinja2, itsdangerous, idna, click, charset-normalizer, certifi, requests, flask
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Successfully installed Jinja2-3.0.1 MarkupSafe-2.0.1 Werkzeug-2.0.1 certifi-2021.5.30 charset-normalizer-2.0.6 click-8.0.1 flask-2.0.1 idna-3.2 itsdangerous-2.0.1 requests-2.26.0 urllib3-1.26.7
Removing intermediate container 85bc781bdc74
 ---> 4b9c978a30a8
Step 7/11 : RUN pip install gunicorn
 ---> Running in 29223580e5ac
Collecting gunicorn
  Downloading gunicorn-20.1.0-py3-none-any.whl (79 kB)
Requirement already satisfied: setuptools>=3.0 in /usr/local/lib/python3.8/site-packages (from gunicorn) (57.5.0)
Installing collected packages: gunicorn
Successfully installed gunicorn-20.1.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 29223580e5ac
 ---> 91906dbf2c5a
Step 8/11 : COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
 ---> d1402be41095
Step 9/11 : RUN chmod +x /usr/src/app/entrypoint.sh
 ---> Running in c16f1f599b57
Removing intermediate container c16f1f599b57
 ---> 0050c168ca98
Step 10/11 : COPY . /usr/src/app
 ---> cdfc853b9eeb
Step 11/11 : CMD ["/usr/src/app/entrypoint.sh"]
 ---> Running in c7776d1cd441
Removing intermediate container c7776d1cd441
 ---> 8d31eb0d50fe
Successfully built 8d31eb0d50fe
Successfully tagged some_demo_img:latest
```

Wanneer een Dockerfile al eens eerder gebouwd is worden alleen de veranderede onderdelen, en de onderdelen erna opnieuw uitgevoerd:
```bash
docker build -t some_demo_img .    
Sending build context to Docker daemon   7.68kB
Step 1/11 : FROM python:3.8
 ---> a5210955ee89
Step 2/11 : ENV PIP_DISABLE_PIP_VERSION_CHECK=on
 ---> Using cache
 ---> 800e0c2a134a
Step 3/11 : ENV SERV_URL ""
 ---> Using cache
 ---> d0fd5ed099c4
Step 4/11 : WORKDIR /usr/src/app
 ---> Using cache
 ---> 4fb23f82a91e
Step 5/11 : COPY ./requirements.txt /usr/src/app/requirements.txt
 ---> Using cache
 ---> 126a424cafd7
Step 6/11 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 3b659e3684a6
Step 7/11 : RUN pip install gunicorn
 ---> Using cache
 ---> 33f3b3ecf8b3
Step 8/11 : COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
 ---> Using cache
 ---> 0c8d39dd8d99
Step 9/11 : RUN chmod +x /usr/src/app/entrypoint.sh
 ---> Using cache
 ---> c540990f15b3
Step 10/11 : COPY . /usr/src/app
 ---> Using cache
 ---> cf1285b4b95c
Step 11/11 : CMD ["/usr/src/app/entrypoint.sh"]
 ---> Using cache
 ---> b6029b1bf3c7
Successfully built b6029b1bf3c7
Successfully tagged some_demo_img:latest
```

## Dockerfile
De Dockerfile beschrijft hoe een image opgebouwd wordt. Zie de Dockerfiles in deze repository.

## Docker-Compose
Docker-compose wordt gebruikt om meerdere containers samen te laten draaien. Deze worden gespecificeerd door middel van YAML files. De meeste opties die gebruikt worden in docker-compose komen overeen met de opties van het `run` commando (o.a. volumes, ports, etc.). Voor meer details zie de docker-compose.yml in deze repository.

De containers kunnen gestart worden door het commando `docker-compose up -d`.

## Docker & Python/Flask
Er zijn bestaande docker images beschikbaar voor Python ([link](https://hub.docker.com/_/python/)). Ook zijn er specifiekere images beschikbaar, zoals bijv. van Tensorflow. Gebruik deze waar toepasselijk. Naast Python zijn er ook bestaande containers voor de meeste databases en andere systemen waarmee de demonstrators gekoppeld worden.

Voor het installeren van dependencies, gebruikt een `requirements.txt` file. Deze kan handmatig worden bijgehouden of worden gegenereerd door middel van `pip freeze`. Let op! dit installeerd alleen de Python packages van een dependency. Voor sommige libraries (zoals OpenCV) moeten ook nog packages handmatig worden geïnstalleerd (bijv. met `apt`).

Maak gebruik van een entrypoint script (zie demo entrypoint.sh). Dit is het script wat gedraait wordt wanneer de container start. Let op! dit script moet zowel in de container als op de host de juiste rechten hebben.

Voor Flask (of Django) applicaties, gebruik een production-ready Python web-server zoals Gunicorn ([link](https://gunicorn.org/)).

## Valkuilen gebruik Docker
Er zijn een aantal punten waar je op moet letten bij het gebruik van Docker:
- Docker containers zijn Linux omgevingen (Windows containers zijn technisch gezien mogelijk. Echter werken deze alleen wanneer de host ook Windows draait. Binnen het lectoraat gebruiken we voornamelijk Linux servers, dus zijn Windows containers geen optie).
- Docker containers (en de servers van het lectoraat) hebben geen GUI, alles moet dus aangeboden worden over het netwerk (bijv. als web-applicatie).
- Directe toegang tot hardware kan lastig zijn (het doel is immer om applicaties te isoleren).
- Docker containers draaien op de server, niet op de client (voor client-side interactie moeten dus extra stappen gezet worden, bijv. client-side Javascript voor web-applicaties).
- Servers hebben meestal geen GPU, houd hier rekening mee (voor het trainen van modellen).

## Handige links
- Documentatie: https://docs.docker.com/
- Docker op Windows: https://hub.docker.com/editions/community/docker-ce-desktop-windows
- Bestaande images: https://hub.docker.com/search?type=image
