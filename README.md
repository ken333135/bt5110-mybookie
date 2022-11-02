## Flask Sandbox

A sandbox application with Flask, SQLAlchemy and PostgreSQL

### Usage

- Install Git Bash
- Open Git Bash, go to the directory containing this project, and run `./deploy.sh`
- A directory called `.venv` will be created. If there is any error, delete this folder and run `./deploy.sh` again

### Requirements

- Python 3
- Flask
- Flask-SQLAlchemy
- flask-WTF

### Prog startup sequence

- app.py
  - models.py
  - .createModels() // this creates all the tables
- utils.readDbfile -> reads from data.sql
  - executes the file line by line
  - creates, student, book, assignment


### Pages
- index
  - signup
  - signin

- books
  - 


### Ajax calls are in views.py, data is passed directly into the page

# showing different logging levels
app.logger.debug("debug log info")
app.logger.info("Info log information")
app.logger.warning("Warning log info")
app.logger.error("Error log info")
app.logger.critical("Critical log info")
