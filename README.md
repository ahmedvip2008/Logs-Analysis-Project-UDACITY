# Logs Analysis Project
This project was created for the *Full Stack Web Developer Nanodegree* at [**Udacity**](https://www.udacity.com/degrees/full-stack-web-developer-nanodegree--nd004).

### About the project
>You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

>In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

### How to Run the Program

#### Requirements
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Setup Project:
  1. Install Vagrant and VirtualBox, Please check [instructions to install the virtual machine](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
  2. Download or Clone this repository in the /vagrant directory **You must finish step 1 first**.
  
#### Prepare the Software and Data
 1. The virtual machine from step 1
 
       If you need to bring the virtual machine back online with `$ vagrant up`. Then log into it with `$ vagrant ssh`
 2. Download the data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
    1. Unzip this file after downloading it. The file inside is called newsdata.sql.
    2. change directory to vagrant
    3. To run the reporting tool, you'll need to load the site's data into your local database. To load the data, use the command 
        ```
        psql -d news -f newsdata.sql
        ```
    4. The database includes three tables:
        - The `authors` table includes information about the authors of articles.
        - The `articles` table includes the articles themselves.
        - The `log` table includes one entry for each time a user has accessed the site.
 3. Creating Views:
    1. Use `psql -d news` to connect to database.
    2. create views using PSQL Command :
 
 ### collect
 '''
CREATE VIEW collect AS
  SELECT articles.title AS article_title,
         articles.author AS author_id,
         authors.name AS author_name,
         count(log.path) AS views
  FROM  log, articles, authors
  WHERE log.path LIKE ('%' || articles.slug)
        AND authors.id = articles.author
  GROUP BY article_title, author_id, author_name
  ORDER BY views DESC;
'''

### total_request
'''
CREATE VIEW total_request AS
SELECT count(*) AS COUNT,
   date(TIME) AS date
FROM log
GROUP BY date
ORDER BY COUNT DESC;
'''

### error_requests
'''
 CREATE VIEW error_request AS
 SELECT count(*) AS COUNT,
   date(TIME) AS date
 FROM log
 WHERE status!='200 OK'
 GROUP BY date
 ORDER BY COUNT DESC;
'''

### error_percentage
'''
 CREATE VIEW error_percentage AS
 SELECT total_request.date,
   round((100.0*error_request.count)/total_request.count,2) AS error_percentage
 FROM error_request,
  total_request
 WHERE error_request.date=total_request.date;
 '''
 
 #### Run the Tool :
1. From the vagrant directory inside the virtual machine, run `logs_analysis.py` using: 
    ```
    $ python logs_analysis.py
    ```
    
