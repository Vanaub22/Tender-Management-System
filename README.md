# Tender Management System

This is the Beta Version of the Tender Management System which I had to prepare as a part of my **Software Engineering Course** **(ESC501)** in my **3rd Year (5th Semester)** of **B.Tech** in **CSE**.

## Key Functionalities Offered So Far:

 1. **Login / Sign Up / Authentication:** Account Creation has been implemented with sessions.
 2. **Setting Bids for Tenders**
 3. **Selling Tenders**
 4. **Displaying Available Balance after Selling / Purchasing**
 5. **Delete Tenders from Listing**
 6. **Adding Tenders to Listing**
 7. **Admin Panel with full access to User, Bidding and Tender Databases**
 8. **Contact Admin Section with Automated E-mail Facility**

## Tech used:

 - **Front-End:** HTML, CSS, JavaScript, Bootstrap-4
 - **Back-End:** Flask, SQLAlchemy, SQLite3

The project is still in its nascent stage and runs only on a Virtual Environment on the local host.

## The steps to start this project are as follows (For Windows Machines Only):

 1. Install VS Code
 2. Assuming you have flask and Python installed, open Terminal in VS Code and simply type in: `run_protender.bat` to run the scripts inside the file and launch the Virtual Environment.
 3. If you encounter any errors related to undefined python packages, make sure to install all of them. Notably, `flask_bcrypt`, `flask_login` and `flask_wtf` using `pip`. For eg: `python -m pip install flask_bcrypt flask_login flask_wtf`.
 
 This should get your web application up and running at `http://127.0.0.1:5000`.