# Dongi

This project is a **Django** web application running inside a **Docker** container with **PostgreSQL** as the database. It includes a **Makefile** to simplify setup.

---

## 🚀 Features
- Django + PostgreSQL database
- Dockerized environment
- Makefile for easy project management

---

## 📦 Prerequisites
Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/) (if you are on linux you already have this)

---

## 🔧 Setup & Usage

### 1️⃣ Clone the repository
```sh
git clone https://github.com/ArtA110/Dongi.git
cd Dongi
```

### 2️⃣ Build and run the project
Use the **Makefile** to build and start the project:
```sh
make build   # Build the Docker images
make up      # Start the containers
```

### 3️⃣ Run migrations & create superuser
```sh
make migrate       # Apply database migrations
make createsuperuser  # Create Django superuser
```

### 4️⃣ Access the app
- Open **http://localhost:8000/** in your browser
- Log in to the Django admin at **http://localhost:8000/admin/**

---

## 📜 Makefile Commands

| Command         | Description                          |
|--------------- |---------------------------------- |
| `make build`   | Build the Docker containers       |
| `make up`      | Start the containers              |
| `make down`    | Stop and remove containers       |
| `make restart` | restart container              |
| `make logs`    | View container logs               |
| `make shell`   | Open a shell inside the container |
| `make migrate` | Apply database migrations        |
| `make createsuperuser` | Create a Django superuser |
| `make format`  | Format code using `ruff`          |
| `make lint`    | Lint code using `ruff`            |
| `make reset-db`    | remove databse and create a fresh database            |

---

## 🔨 Project Architecture
### ERD
You can see project **ERD** below:  
[![DongiERD.png](https://i.postimg.cc/jq3xPYCL/Dongi.png)](https://dbdiagram.io/d/Dongi-679cf9ed263d6cf9a0a8af96)
