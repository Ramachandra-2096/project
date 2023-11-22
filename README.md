# Virtual Event Management System

Welcome to the Virtual Event Management System! This Django project allows you to organize virtual events, collect participant data, generate QR codes, and manage event logistics.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Admin Panel](#admin-panel)
6. [Contributing](#contributing)
7. [License](#license)

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.x
- Django (install using `pip install -r requirements.txt`)
- Git

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/<your-username>/<your-project-name>.git
    cd <your-project-name>
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

2. **Create a superuser account for the admin panel:**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to enter a username, email, and password for the superuser.

3. Start the development server:

    ```bash
    python manage.py runserver
    ```

4. Access the application in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Features

...

## Admin Panel

**Access the Django Built-in Admin Panel:**

1. Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your browser.

2. Log in using the superuser credentials you created earlier.

**Scan QR Code:**
    - In the Admin panel, scan the QR code to retrieve participant details.

**Update Participant Details:**
    - In the Admin panel, add payment details and mark participants as checked in.

**Admin Dashboard:**
    - View the list of participants who have arrived and those yet to arrive.

## Contributing

Feel free to contribute by opening issues or creating pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
