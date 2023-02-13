# Pocket Monsters
#### Video Demo:  https://youtu.be/4RXl8HP7AZM
#### Description: A website connected to multiple databases which can be utilised to display information based on user input.
##### Homepage:
From the homepage you can access all subpages. The homepage is a very simple design which explains the different aspects and features of the website. By using Bootstap I was able to implement a number of useful features including the nav bar to get to the other pages. As Jinja was used in this project, it meant that I could have the same layout on all html pages ensuring consistancy.

##### Search/Results:
On the search page it shows over 700 Pokemon which are pulled through a database. You can refine which Pokemon are shown by searching by Pokemon name or type. Even if you don't know the whole name you can search by using just a few letters and it will bring up anything similar. The search function works by using the button or pressing enter on your keyboard. If there are no matches, the table will show an error message. If this happens you can press 'go back' at the top of the page. To complete this page it required importing SLQLITE rather than relying on CS50s SQL function. Due to this I used documentation (https://docs.python.org/3/library/sqlite3.html?highlight=sqlite) to learn new functions and commands I had not previously used in CS50.

##### Compare/Comparison:
On the compare page you can search two pokemon to compare their stats. Similarly to the search function, this pulls data from the same database on the search page, but presents the results differently. Instead of looking up any Pokemon based on name or type, it searches just on name and presents one Pokemon per column on the table. Ensuring that even if the Pokemon is two different types, both types are shown on the same row rather than excluding a type and not showing all the information.

##### Types:
Finally, on the types page you can find which is the best Pokemon type in a battle depending on the attacking and defending Pokemon. This page pulls from an entirly different database and presents the data in a pivot table style rather than outputting the data as imported. Again, this relied on SQL searches to pull the data from the database in a different format.

##### Overall:
The project required me to learn new skills and build on the ones I already had. As I completed this project alone, I feel that I have shown a great use of my skills and the range in programming languages I have learnt over CS50.
From the homepage you can access all subpages. The homepage is a very simple design which explains the different aspects and features of the website.
