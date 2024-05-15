# AirBnB Clone

This project is a clone of the popular vacation rental platform, AirBnB. It is a complete web application, integrating database storage, a back-end API, and front-end interface.

## The Console

The project includes a command interpreter, or console, that allows users to interact with the application's data. The console can be used to create, update, destroy, and query various objects, such as users, places, reviews, and more.

### Starting the Console

To start the console, navigate to the project directory and run the following command:


```python console.py```

This will launch the console and display a prompt where you can enter commands.

### Using the Console

The console supports a variety of commands, including:

- `create <class>`: Creates a new instance of the specified class and saves it to the database.
- `show <class> <id>`: Displays the information about the instance of the specified class with the given ID.
- `destroy <class> <id>`: Deletes the instance of the specified class with the given ID from the database.
- `all [<class>]`: Displays all instances of the specified class (or all classes if none is specified).
- `update <class> <id> <attribute> "<value>"`: Updates the specified attribute of the instance of the given class with the provided value.
- `quit`: Exits the console.

Here are some examples of how to use the console:

(hbnb) create User
(hbnb) show User Abebe-123
(hbnb) destroy Place Haile-456
(hbnb) all
(hbnb) update User Abebe-123 email "abebe@example.com"
(hbnb) quit


## Project Structure

The project follows a Model-View-Controller (MVC) architectural pattern and is organized as follows:

- `models/`: Contains the data models (e.g., `User`, `Place`, `Review`) and the database storage engine.
- `views/`: Contains the user interface components (e.g., HTML templates, CSS, JavaScript).
- `controllers/`: Contains the logic that handles user input and updates the models and views accordingly.
- `tests/`: Contains the unit tests for the various components of the application.

## Future Improvements

- Implement a web server to serve the front-end interface.
- Add authentication and authorization features.
- Enhance the search and filtering capabilities.
- Improve the overall user experience and design.