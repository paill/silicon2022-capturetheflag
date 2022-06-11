1. Build docker image `docker build . -t silicon-mongodb-nosqli`
2. Run container (passwords here are just examples)
```
docker run -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin -e MONGO_FLASK_DATABASE=nosqli -e MONGO_FLASK_USER_NAME=flask -e MONGO_FLASK_USER_PASSWORD=flask --name mongodb-test -p 27017:27017 silicon-mongodb-nosqli
```