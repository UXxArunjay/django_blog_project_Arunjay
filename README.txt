# Django Blog Project

This is a simple blog project built using Django, designed to allow users to create, edit, and view blog posts.

## Features

- User authentication (login/logout/signup)
- Create, update, and delete blog posts
- Commenting system for blog posts
- Responsive design

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.11+
- pip
- virtualenv
- Django 5.x

### Steps to Run the Project

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/django_blog_project.git
   cd django_blog_project
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server:**

   ```sh
   python manage.py runserver
   ```

   Open `http://127.0.0.1:8000/` in your browser.

## Configuration

- Update `settings.py` for database configuration.
- Add your static and media files in the appropriate folders.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Contact

If you have any questions, feel free to contact me at `contact.arunjayail@gmail.com`.

