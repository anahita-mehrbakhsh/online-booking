# online-booking
Online Booking is our university's project. The Backend is implemented with Django and the Frontend is with React. There are still many bugs in the code, so look at it as a sample project.

## T‍‍‍‍‍o run the frontend server:

1. Install npm
  ```bash
  npm install
  ```
2. Everytime you want to run the server, just use this command:
  ```bash
  npm run dev
  ```

## To run the backend server:
### Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework django-cors-headers
cd backend
```
To start the backend server:
```bash
python manage.py runserver
```
### Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install django djangorestframework django-cors-headers
cd backend
```
To start the backend server:
```bash
python3 manage.py runserver
```
