# TrackTrainer
#### Video Demo: (https://www.youtube.com/watch?v=2FxlBYEG5XE)
#### Description:

This CS50 final project was made to allow me to demonstrate the lessons learnt on this course in the context of one of my main interests-motorsport.

For the project my goal was to implement a web based application using Flask and SQL that would allow the user to save notes on tracks that they are driving in real world or virtually and work towards reducing their lap times.

To achieve the goal of the project I used Python Flask alongside HTML ,CSS and SQLachamy via VS Code.Python is widely used in industry today, so making it the language of choice for this project felt like the right decision as the final result will be used as part of my portfolio for job applications into software development roles.The structure of the app follows the standard Flask convention of having files divided into static,instance and template folders with a app.py file containing the code required to launch the application in browser.

Within the instance folder is the app’s database, which contains tables for registering users, allowing them to add tracks to their account and making corner by corner notes for those tracks.These tables are created by classes in the app.py using the flask sqlachemy module.

The static folder contains the images used for the promotional element of the home page for the web app alongside a style.css file that formats all of the key html elements of the web app.For ease of buildling the front end,Bootstrap styles have been used where possible.

Most of the project comprises of content within the template folder, made up of the multiple HTML files that make up the front end seen by the end user.To ensure the format is consistent across all pages, a layout .html file is used with Jinga notation to set a navigation bar and footer that is applied to all pages.

Jinga is used to alter the navigation bar based on whether a user is logged in or not as part of access restriction.Function decorators are also used within app.py to prevent users manipulating the htmls to gain access to areas without passing standard login validation.

The homepage (index.html) also uses Jinga to alter the content based on login.Registered users will see their list of saved tracks and have access to their notes along with the ability to go to a separate html to edit notes and track times direct from the home page.New users will see a carousel of promotional images and captions to entice them to register and become a user. 

The backbone of the app is its database, which needs to be updated by user interaction.For this there are front end htmls(add,notes and register.html) which give the user input forms to add tracks, notes per corner and specific driving event (braking,turn in,exit),update their best lap times as they improve and register to the app to use these features.

All input forms feature placeholders to clearly direct the user on the format in which the data should be submitted and what content they should be adding to get the most out of their experience.

In the backend, the database updates and addition of new entries are conducted by using the Flask SQLachemy framework. For updates, a query is run to find the existing information, then the new information is added using the suitable class notation (e.g class.variable) before committing to the database.Updates can be made to notes and lap times.

New entries also go through a query check to avoid duplication of data before entering the database via the creation of a new class for the given table This is usually through the creation of a variable like new_track or new_user.

All queries utilise the id of users in connection with a variable such as track_name.In terms of data types, strings are mainly used with the occasional numeric value for variables such as user ID and turn number.

During the design process, the idea of having a track comparison feature was toyed with.Whilst the concept seemed good on paper, it felt too much for an initial app launch and required major alteration to the already stable code, which was already massively bloated in size.

Perhaps this feature could be explored post launch to the public and serve as a future project to revise and improve on the skills learnt during the CS50 course.Alongside this a general review of code conciseness could be carried out to improve the readability of the code for potential future colaborators.

Overall, I am happy with how this Flask app has turned out.The scope of the project has allowed me to confirm my understanding of the concepts taught during the CS50 course and provided me with a app I can continue to develop as part of my portfolio or even launch to a customer base with enough time invested.
