# Base image
FROM python:3.9

# Zet warnings over nieuwe pip versies uit (de pip versie is onderdeel
# van het base image).
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# Environment variables. Deze worden vaak gebruikt om configuraties mee te
# geven aan de instantie van het image.
ENV SERV_URL ""

# Zet the working directory (de directory van waaruit de commandos uitgevoerd
# worden).
WORKDIR /usr/src/app

# Kopieer de requirements.txt file en installeer dependencies.
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Installeer gunicorn (production ready Python server)
RUN pip install gunicorn

# Kopieer entrypoint script. Dit script wordt gedraait wanneer we de 
# container starten. Dit script start onze applicatie.
# LET OP!: Op Linux (en mogelijk ook op Windows/Mac) moet dit bestand executable
#   zijn op de host en in de container
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Kopieer de applicatie naar het image.
COPY . /usr/src/app

# Run het entrypoint script
CMD ["/usr/src/app/entrypoint.sh"]
