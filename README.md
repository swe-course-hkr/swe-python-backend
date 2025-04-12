# SWE-Python-Backend

## To create a docker:
first command to pull and build an image:
```bash
docker pull ibmoh/client-server
```
<br />

second command to run a container:
```bash
docker run -d -p 5000:5000 ibmoh/client-server
```
<br />

Docker's default timezone is UTC in order to change it use `-e TZ=Prefered/TimeZone`
```
docker run -e TZ=Europe/Stockholm -d -p 5000:5000 ibmoh/client-server
```
<br />

This command will run a container in Sweden's timezone. Timezone is important as two columns in the database depend on it: `created_at` and `modified_at`
