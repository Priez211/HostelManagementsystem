# Hostel Management System

A comprehensive Django-based web application for managing hostel operations, including student registrations, room allocations, fee management, visitor tracking, and maintenance requests.

## Features

- **Student Management**: Register and manage student information
- **Room Management**: Track room availability, allocations, and bookings
- **Staff Management**: Manage hostel staff across different categories
- **Fee Management**: Handle various types of fees and payment tracking
- **Visitor Management**: Log and track hostel visitors
- **Maintenance Requests**: Track and manage room maintenance requests
- **Inventory Management**: Keep track of room items and their conditions
- **Disciplinary Records**: Maintain records of student violations and actions taken

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation and Setup

### Quick Setup

Run the automated setup script:

```bash
chmod +x setup_mysql.sh
./setup_mysql.sh
```

This script will:
1. Start the MySQL service
2. Create the database `Hostel_Management_Db`
3. Configure the MySQL user
4. Install required Python packages
5. Run Django migrations

### Manual Setup

If you prefer to set up manually, follow these steps:

#### 1. Start MySQL Service

```bash
sudo service mysql start
```

#### 2. Create Database

```bash
mysql -u root -p
```

Then run:

```sql
CREATE DATABASE Hostel_Management_Db;
GRANT ALL PRIVILEGES ON Hostel_Management_Db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. Install Python Dependencies

```bash
pip install django mysqlclient
```

#### 4. Run Migrations

```bash
cd HMSys
python manage.py makemigrations
python manage.py migrate
```

## Running the Application

### Start the Development Server

```bash
cd HMSys
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

### Create Admin User

To access the Django admin panel, create a superuser:

```bash
cd HMSys
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials, then access the admin panel at `http://localhost:8000/admin/`

## Database Configuration

The application is configured to connect to MySQL with the following settings (in `HMSys/settings.py`):

- **Database**: `Hostel_Management_Db`
- **User**: `root`
- **Password**: `13.0.13Morna`
- **Host**: `localhost`
- **Port**: `3306`

To change these settings, modify the `DATABASES` configuration in `HMSys/HMSys/settings.py`.

## Troubleshooting

### MySQL Connection Error

If you encounter the error:
```
django.db.utils.OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)")
```

**Solution**: The MySQL service is not running. Start it with:
```bash
sudo service mysql start
```

### Database Does Not Exist

If you see:
```
django.db.utils.OperationalError: (1049, "Unknown database 'Hostel_Management_Db'")
```

**Solution**: Run the setup script or manually create the database as described in the setup instructions.

### Missing Dependencies

If you encounter `ModuleNotFoundError`:

**Solution**: Install the required packages:
```bash
pip install django mysqlclient
```

## Project Structure

```
HostelManagementsystem/
├── HMSys/
│   ├── HMSys/              # Project settings
│   │   ├── settings.py     # Django settings
│   │   ├── urls.py         # URL routing
│   │   └── wsgi.py         # WSGI configuration
│   ├── core/               # Main application
│   │   ├── models.py       # Database models
│   │   ├── views.py        # View logic
│   │   ├── urls.py         # App URLs
│   │   └── admin.py        # Admin configuration
│   ├── templates/          # HTML templates
│   ├── static/             # Static files (CSS, JS, images)
│   └── manage.py           # Django management script
├── setup_mysql.sh          # Automated setup script
└── README.md               # This file
```

## Database Models

- **Staff**: Hostel staff information
- **HostelBlock**: Building blocks in the hostel
- **Room**: Individual rooms with status tracking
- **Student**: Student information and profiles
- **Fee**: Fee management and payment tracking
- **Allocation**: Room allocation assignments
- **Booking**: Room booking reservations
- **Visitor**: Visitor logs and tracking
- **DisciplinaryRecord**: Student violation records
- **Inventory**: Room inventory and item tracking
- **MaintenanceRequest**: Maintenance request management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please open an issue in the repository.
