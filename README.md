## Posts and comments API

This is a Django project that implements a simple API for managing posts and comments connected with local postgres database run on Docker and docker compose.
with a Djnago command to import 100 posts and their comments from [Json placeholder](https://jsonplaceholder.typicode.com/) it will automatically import and store data in the local database.

## Solution Description

Here goes the description how I created the app and worked on it:

- Generally I followed the shared descripton from the email.
- I added the models based on the data model in the [Json placeholder](https://jsonplaceholder.typicode.com/) tried to be close to avoid any problems with importing data.
- I implemented the import command and tried some tests with it.
- I implemented serializers and tried to make it informative as much.
- I implemented the APIs and it was a default `ModelViewSet` from django to keep it simple but it is not a best practice but for the sake of experiment nothing more.
- I added the authentication to protect the API calls.
- I implemented the tests for all functioanlity at the end.
- Wrote some docuemtation and learnings as well.

So for now the sync happens at the start of the app before it runs the import command will run and import data into local db.

I used some packages while implementing this app:

- `PyJWT`, `djangorestframework-simplejwt` for authentication and authorization.
- `psycopg2` to deal with postgres database.
- `requests` to call the fake api service and import data.

## Run the Project

To run the project locally, follow these steps:

1. Extract the compress file.
2. `cd` to the extracted directory and run `docker compose up --build`
3. Docker will take care of everything and the application will run verysoon.
4. In the `start.sh` file we got all the necessary commands to make the app run and do migrations for DB.
5. Before starting the app Importing posts and comments command from django will run, it will take sometime before start.
6. App is up and running now and you can use APIs or Django admin even though to check `posts` and `comments`.
7. You need to create a superuser to be able to access authenticated APIs so run this command `docker exec -it blog_api-backend-1 bash` or change the container name to the created name - hence check `docker ps`.
8. You are now inside docker so now create super user bu running `python manage.py createsuperuser` and fill all details required.
9. Now you are all set and you can login to Django admin.
10. In terms of use API calls you need to be authenticated so you need to authenticate using this API call with the created user.
    ```bash
    curl --location 'localhost:8000/api/token/' \
        --form 'username="<username>>"' \
        --form 'password="<password>"'
    ```
11. Output should be 2 tokens and looks like this:
    ```json
    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMzIxMzQ0MCwiaWF0IjoxNzEzMTI3MDQwLCJqdGkiOiI4NDA4N2Y2YTMzOWE0NjI5OGVhMjBhYzAxOTJlMzM4MiIsInVzZXJfaWQiOjF9.O8JnYjd7M9XSvl2QwW6C-PKKapOhifTQcZ2VL_HrX_g",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzMTI3MzQwLCJpYXQiOjE3MTMxMjcwNDAsImp0aSI6ImNiYTUwMTQ1MDlmNzRiODI5NjA4N2M4MzMzZGRhYWZjIiwidXNlcl9pZCI6MX0.7qbpzoD7D9X73ZUrjhXGFCqAeLwwHODcjXfBna_sxdM"
    }
    ```
12. Now you can use the `access` token to call APIs but if it didn't work you can generate a new one using the `refresh` token by running:
    ```bash
    curl --location 'localhost:8000/api/token/refresh/' \
        --form 'refresh="<refresh token>"'
    ```
13. Now you got the access token again in case it got expired andshould the output looks like this:
    ```json
    {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzMTM0NjA0LCJpYXQiOjE3MTMxMjcwNDAsImp0aSI6IjA4MTA1ODZmMDUwYzQyYzdiNDk5MjdiYWU0MjY1YjA1IiwidXNlcl9pZCI6MX0.jFDKptf03x_7WMI9qtdfDP84uzven7RvZlN0Zs7wpqc"
    }
    ```
14. Now you can use the access to call APIs eg:
    ```bash
        curl --location 'localhost:8000/api/v1/posts/2' \
        --header 'Authorization: Bearer <access token>'
    ```
15. Now all set and good to go!

## Improvements

    In general this is a first draft and didn't take long time, so many improvments possible here and I might not mention all of them.

- Improve the views and make it more restful by spliting it into `ListCreateAPIView` for listing and creating blogs `RetrieveUpdateDestroyAPIView` for update and delete actions from django.
- Improve the models we have and integrate with `user` model.
- Improve the import command and only use 2 hits to get `Posts` and `Comments` and do the relations in the application level.
- Improve testing from 3 points (coverage, structure and setup) where we can creat `fixtures` and auto seed for DB, better structure for test files and increase test coverage for sure.
- Add more APIs to cover more scenarios of retrieving data to make it more convieniant for the user.
- Add more documentation.
  and maybe more.
