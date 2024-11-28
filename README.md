# Bookviser

Bookviser is a web-based library management application developed as part of the Modern Application Development - II course at IIT Madras. The application leverages Flask for the backend, Vue.js for the frontend, and Celery for asynchronous task management.

## Features

- **User Authentication:** Secure login and registration system for users.
- **Book Management:** Add, edit, and delete book records.
- **Search Functionality:** Efficient search capabilities to locate books by title, author, or genre.
- **Borrowing System:** Users can borrow and return books, with real-time tracking of availability.
- **Notifications:** Automated alerts for due dates and overdue books.
- **Admin Dashboard:** Comprehensive interface for administrators to manage users and books.

## Technologies Used

- **Backend:** Python with Flask
- **Frontend:** JavaScript with Vue.js
- **Asynchronous Tasks:** Celery
- **Database:** SQLite
- **Web Server:** WSGI

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/amittkulkarni/bookviser.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd bookviser
   ```
3. **Install Backend Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Frontend Dependencies:**
   ```bash
   npm install
   ```
5. **Run the Application:**

      Backend:
      ```bash
      python wsgi.py
      ```
      Frontend:
      ```bash
      npm run dev
      ```
## Usage

- Access the application through http://localhost:5000 in your web browser.
- Register for a new account or log in with existing credentials.
- Explore the library, borrow books, and manage your account.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
