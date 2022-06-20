# How To Run

## web-log-server
1. `cd web-log-server`
2. `mkdir httpd`
3. `docker run -v ${PWD}/httpd:/log -it --rm mingrammer/flog -t log -f apache_combined -o log/apache.log -p 512000 -b 20480000 -w`
    * Check out [mingrammer/flog](https://github.com/mingrammer/flog) for how to use
4. `sed -i '' -E 's/^[0-9]{1,3}\.[0-9]{1,3}\.([0-9]{1,3})\.([0-9]{1,3}) - .* \[/192.168.\1.\2 - - [/g' httpd/apache*.log`
5. Find a line in file and put the IP you want folks to find.
6. `tar czfv apache.log.tar.gz httpd/apache*.log`
7. `rm -rf httpd/apache*.log`
8. `docker build . -t silicon/level-0-web-log-server`
9. `docker run -it --rm silicon/level-0-web-log-server`

## c2-server
1. `cd c2-server`
2. `sqlite3 src/database/c2.db < schema.sql`
3. `docker build . -t silicon/level-0-c2-server --build-arg http_proxy=http://yourproxy.com:1337`
4. `docker run -it --rm -p 8080:8080 silicon/level-0-c2-server`
5. Open browser and go to `http://localhost:8080`

You can also deploy to K8S, see [k8s-deployment](./k8s-deployment/)