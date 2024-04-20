# Shorty

This is a URL shortener application built with Django, a powerful Python web framework. The application allows users to create short, memorable URLs that redirect to longer, more complex URLs.

## Features

- Shorten long URLs into compact and easy-to-share links
- Custom slug creation for personalized short URLs

## Technologies Used

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis/Zookeeper
- Docker

## Prerequisites

- Docker
- Docker Compose (optional, if you're using Docker Compose)

## Installation

1. Clone the repository:

```
git clone https://github.com/shuvrasish/shorty.git
```

2. Navigate to the project directory.
3. Install and run postgres on your system:

```
sudo systemctl start postgresql
```

4. Build the Docker image for zookeeper:

```
docker-compose -f docker-compose-zookeeper.yml up --build (-d if you want to run it in detached mode)
```

5. Build the Docker image for the app server:

```
docker-compose up --build (-d if you want to run it in detached mode)
```

6. Once the Docker container is running, open your web browser and navigate to `http://localhost:8000` to access the URL shortener application.

## Usage

1. Enter the long URL you want to shorten in the provided input field.
2. Click the "Shorten" button to generate the short URL.
3. Copy the generated short URL and share it with others.
4. When someone visits the short URL, they will be redirected to the original long URL.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
