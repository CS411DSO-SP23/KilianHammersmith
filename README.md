Title: Dashboard App to Rule the Academic World


Purpose: The purpose of this dashboard is to give students and other professors the ability to find out more information about the professors at a number of universities in the computer science department. The dashboard allows students to see where professors focus their time and in what area they are the strongest. Also a professor can be added to the database and a keyword could be added to a publication if one sees fit.


Demo: Demo video can be found on the University of Illinois media sharing website. Link:https://mediaspace.illinois.edu/media/t/1_dim3ep53


Usage: Use of the dahsboard is meant for faculty and students in computer science at universities. One may use this dashboard to see what professors work in certain specailities. This may be for research, studies, or general interest. The dahsboard will allow users to learn about the focus of publications and faculty at listed universities.


Design: The dashboard is design using Plotly Dash. The dahsboard includes elements from html and dash core components that interact with the backend functionality using callbacks. Callback will take input from either a dropdwon or inout widget then using the utililities and connection to the different databases to query and return the desired information in a new component that could be a graph, table, or text. 


Implementation: The libraries used where Dash from plotly for the dashboard itself, pymysql for the connection to the mysql database, neo4j for the connection to the neo4j database, MongoClient from pymonog for the connection to MongoDB, plotly express for creating vizulaizations in the user interface, and pandas for orginizing and handling data. For implementation, I first created the utilities for each database type, then using dahs and html elements created the widgets, using callbacks to facilitate widgets interacting with the utlities.


Database Techniques: Within the dashboard app, three database models where implemented: MySQL for relational data, MongoDB for key-value/document data, and Neo4j for graph data. Added to the functionality of the MySQL database was a contraint on the faculty table and a trigger on inserts to prohibit unfit information to be added to the faculty table; the two techniques were both added to add some redunacny and protection in case of a use case where one might fail. Also added was an index on university name, becuase this is a large component of most of the queries, to speed up query time. Finally a view was created that stored faculty score information in a more accessible way and this view was used on a widget.


Contributions: Kilian Hammersmith is the only member who worked on this project. Roughly 25 hours was spent on the project and completing all tasks involved.
