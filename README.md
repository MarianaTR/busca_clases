# busca_clases

Al correr el proyecto solo con docker-compose up --build no se conectara con kubernetes pero funcionara todo perfectamente dado que opensourse esta en AWS.
Junto con esto la bbdd esta en heroku (postgresql).

Cuando opensourse no se conecta la pagina se debe correr el comando: (esto ocurria al correr opensourse de manera local dentro del docker-compose, ya no deberia ocurrir)
'curl -XPUT "http://34.222.58.202:9200/iaps-index" '


## Instalación
Funciona todo de manera correcta, pero con kubernete puede dar error al crear un usuario.
Un usuario para probar es:
  user: cveralyon@gmail.com
  pass: 123456789
Este usuario tiene un par de cursos creados y se pueden crear mas si lo desea.

Para correrlo con kubernetes se debe estar en el directorio web-project y ejecutar el comando ** kubectl apply -f deployment.yaml ** con esto se subira la web
