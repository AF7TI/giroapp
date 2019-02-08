# giroapp

Frontend for https://github.com/AF7TI/girotick. Display latest ionosphere metrics for each station as datatable and render to .json for other stuff like [contour maps](https://github.com/AF7TI/giroviz). Docker based on tiangolo uwsgi-nginx-flask-docker.

## Installation
Run the official postgres Docker image then build this image from Dockerfile, tag with giroapp   
    `docker build -t giroapp .`

## Configuration
Pass database connection info through environment variables:  
    `docker run -e "DB_USER=postgres" -e "DB_HOST=localhost" -e "DB_NAME=postgres" -e "DB_PASSWORD=mysecretpassword" -d -p 80:80 giroapp`
    
Optionally, configure nginx in [nginx.conf](app/nginx.conf)

## Running Code
- Tabular data online at https://prop.kc2g.com/stations and http://metrics.af7ti.com
- JSON data sources online at https://prop.kc2g.com/stations.json and http://metrics.af7ti.com/stations.json
