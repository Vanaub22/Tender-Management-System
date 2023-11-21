
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

 1. Install VS Code (Assuming you have python, Flask and pip installed)
 2. Open Terminal in VS Code and type: `protender\Scripts\activate.bat` to launch the Virtual Environment.
 3. In your terminal, type in: `python -m pip install flask_bcrypt flask_login flask_wtf`
 4. After that simply type in `python
    run.py` in the terminal, this should get your web application up and running at `http://127.0.0.1:5000/home`.
