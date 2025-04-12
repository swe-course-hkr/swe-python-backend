# SWE-Python-Backend

## To create a docker:
first command to pull and build an image:
```docker pull ibmoh/client-server ```

second command to run a container:
```docker run -d -p 5000:5000 ibmoh/client-server```

Docker's default timezone is UTC in order to change it use ```-e TZ=Prefered/TimeZone```

for example: ```docker run -e TZ=Europe/Stockholm -d -p 5000:5000 ibmoh/client-server```
This command will run a container in Sweden's timezone. Timezone is important as two columns in the database depend on it: ```Created_at``` and ```modified_at```
