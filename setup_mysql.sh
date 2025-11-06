#!/bin/bash
# MySQL Setup Script for Hostel Management System
# This script starts MySQL, creates the database, and runs Django migrations

echo "=========================================="
echo "Hostel Management System - MySQL Setup"
echo "=========================================="

# Start MySQL service
echo "Starting MySQL service..."
sudo service mysql start
sleep 3

# Check if MySQL is running
if ! sudo service mysql status | grep -q "active (running)"; then
    echo "Error: Failed to start MySQL service"
    exit 1
fi
echo "✓ MySQL service started successfully"

# Create database and configure user
echo "Creating database and configuring MySQL user..."
mysql -u debian-sys-maint -p$(sudo grep password /etc/mysql/debian.cnf | head -1 | awk '{print $3}') <<EOF
CREATE DATABASE IF NOT EXISTS Hostel_Management_Db;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '13.0.13Morna';
GRANT ALL PRIVILEGES ON Hostel_Management_Db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo "✓ Database created and user configured successfully"
else
    echo "Error: Failed to create database or configure user"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
cd HMSys
pip install -q django mysqlclient

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed successfully"
else
    echo "Error: Failed to install Python dependencies"
    exit 1
fi

# Run Django migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

if [ $? -eq 0 ]; then
    echo "✓ Database migrations completed successfully"
else
    echo "Error: Failed to run migrations"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  cd HMSys"
echo "  python manage.py runserver"
echo ""
echo "To create an admin user, run:"
echo "  cd HMSys"
echo "  python manage.py createsuperuser"
echo ""
