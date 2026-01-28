Campus Connect: Student Complaint & Grievance Management System

Campus Connect is a full-stack web application designed to streamline campus grievance handling between students and administrators. The platform enables students to register complaints across multiple categories and provides administrators with a centralized dashboard to track, manage, and resolve issues efficiently. The project reflects real-world SaaS-style workflows, role-based access, and operational dashboards.

Features

Role-Based Access System: Separate login flows for students and administrators, ensuring secure access and role-specific functionality.

Student Complaint Portal: Students can submit complaints across categories such as infrastructure, academic issues, scholarships, book bank, and anti-ragging, with a simple and guided interface.

Admin Command Center: An admin dashboard displaying total tickets, pending issues, and resolved cases, along with detailed ticket views and resolution actions.

Real-Time Status Tracking: Complaints move through Pending and Resolved states, allowing transparent tracking for both students and administrators.

Secure Data Management: Uses Flask-SQLAlchemy with SQLite to manage student profiles, complaints, and administrative responses.

Profile Management: Students can update academic details and upload profile images, demonstrating file handling and user data management.

Responsive & Modern UI: Built with HTML, CSS, Bootstrap, and custom styling to deliver a clean, responsive, and professional user experience.

Tech Stack

Backend: Flask, Flask-SQLAlchemy, SQLite
Frontend: HTML, CSS, JavaScript, Bootstrap
Authentication & Sessions: Flask sessions and role-based access control

Getting Started

Clone the repository and install dependencies:
git clone https://github.com/Pranavrai207/new-campus-connect.git

cd new-campus-connect
pip install -r requirements.txt

Run the application:
python app.py

Open your browser and navigate to:
http://127.0.0.1:5000

Project Structure

new-campus-connect/
├── app.py – Main Flask application
├── templates/ – HTML templates for student and admin views
├── static/ – CSS, JavaScript, and uploaded files
├── requirements.txt – Project dependencies
└── complaints.db – SQLite database

Why This Project Matters

Campus Connect demonstrates practical full-stack development, database-driven workflows, and operational dashboard design. It shows how software systems can improve communication, transparency, and efficiency in real organizational environments, making it relevant for engineering, SaaS operations, and customer-facing technical roles.

License

This project is licensed under the MIT License.
