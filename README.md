# Playtime Project Setup

Welcome to the Playtime project! This Django application integrates with Messenger and OpenAI. Follow the steps below to set up the project locally.

## Prerequisites

- Python 3.9 or higher installed on your system.
- Virtualenv installed globally (`pip install virtualenv`).

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Aanish97/Playtime
   cd playtime-project
   virtualenv venv --python=python3.9 // create the venv
   source venv/bin/activate // activate the venv
   pip install -r requirements.txt // install the packages
   python manage.py migrate // migrate to the DB
   python manage.py createsuperuser // follow the prompt
   python manage.py runserver // run the server







   


