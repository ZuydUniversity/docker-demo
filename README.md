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
docker run -e MYSQL_DATABASE=AppDb --name app_db -v /some/dir:/var/lib/mysql -p 8000:3306 -d mariadb:latest
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
docker stats
CONTAINER ID   NAME                 CPU %     MEM USAGE / LIMIT    MEM %     NET I/O       BLOCK I/O       PIDS
9a013891e3eb   dockerdemo_front_1   0.02%     37.77MiB / 14.6GiB   0.25%     19kB / 0B     4.1kB / 549kB   3
eaaa5e3b5a31   dockerdemo_serv_1    0.01%     35.59MiB / 14.6GiB   0.24%     19.8kB / 0B   467kB / 545kB   3
```

### logs
Het `logs` commando geeft de logs weer van een specifieke container. Hiervoor wordt de naam van de container of het ID gebruikt.
```bash
docker logs dockerdemo_front_1
[2021-09-24 08:22:14 +0000] [7] [INFO] Starting gunicorn 20.1.0
[2021-09-24 08:22:14 +0000] [7] [INFO] Listening at: http://0.0.0.0:5000 (7)
[2021-09-24 08:22:14 +0000] [7] [INFO] Using worker: sync
[2021-09-24 08:22:14 +0000] [8] [INFO] Booting worker with pid: 8
```
