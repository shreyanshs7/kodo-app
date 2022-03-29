### Bringing up via Docker Compose ###

* For a fresh setup run to build images for services
    ```
    docker-compose build
    ```

* Now run to start services
    ```
    docker-compose up
    ```

* Or to do both the commands in one go
    ```
    docker-compose up --build
    ```

* Once the server is up and running you should see something like this
    ```
    kodo_project-kodo-app-service-1  | [2022-03-29 16:23:52 +0000] [10] [INFO] Starting gunicorn 20.1.0
    kodo_project-kodo-app-service-1  | [2022-03-29 16:23:52 +0000] [10] [INFO] Listening at: http://0.0.0.0:9000 (10)
    kodo_project-kodo-app-service-1  | [2022-03-29 16:23:52 +0000] [10] [INFO] Using worker: sync
    kodo_project-kodo-app-service-1  | [2022-03-29 16:23:52 +0000] [12] [INFO] Booting worker with pid: 12
    ```

* Once the server is running, before testing anything run the below command to load the mock data into database table.
* Also, there would be duplicate data if you call this endpoint again as there are not checks or constraints on table.
```
curl --location --request POST 'http://0.0.0.0:9000/load_mock_data'
```

### Example curl commands to test ###

* Search by name
```
curl --location --request GET 'http://0.0.0.0:9000/search?name=central'
```

* Search by exact name matching
```
curl --location --request GET 'http://0.0.0.0:9000/search?name="Central Implementation"'
```

* Ordering by name in desending order
```
curl --location --request GET 'http://0.0.0.0:9000/search?order=-name'
```

* To order by ascending order just remove `-` from `name`

```
curl --location --request GET 'http://0.0.0.0:9000/search?order=name'
```

* Search by description with results from a different page number
```
curl --location --request GET 'http://0.0.0.0:9000/search?description=Aut et&page_number=51'
```