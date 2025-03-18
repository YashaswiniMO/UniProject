# UniProject – Digital Project Hub for Universities 
Offers a transformative solution. 
It is a platform designed to leverage the power of technology to create an integrated digital ecosystem for students from diverse academic institutions. 
The platform enables students to upload, showcase, and share their academic projects, fostering a culture of innovation and collaboration.

# Problem Statement Details

      “Online Integrated Platform for Projects Taken up by the Students of Various Universities/Colleges” 

# Objectives
• To develop a centralized platform for project uploads and showcases. 
• To facilitate inter-university collaboration through forums, chat, and file sharing. 
• To implement plagiarism detection to ensure submission originality. 
• To develop a recommendation system for personalized project and resource suggestions. 
• To utilize data analytics to monitor activity and provide insights via admin dashboards. 

# Functinal Requirements
1. Login & Registration -- Role-based access for students, universities, and admins. 
2. Project Upload -- Students can upload projects with metadata like tags, categories, and files. 
3. Recommendation System --Personalized project suggestions based on history and preferences.
4. Plagiarism Checker -- Detect copied content with detailed plagiarism score. 
5. Dashboards -- Analytics for users, universities, and admins to track performance. 
6. CRD Space --Collaborative workspaces for multi-university projects.

# Technology Stack
| Python |
|--------|
| Django|
|Sqlite3 / Mysql|
|Bootstrap v4.5.0|

# Main Idea
- The primary objective is to bring together students and their projects exclusively from various colleges, universities, schools, and institutions.
- Students can register and log in, or they can try the demo user to explore all available projects.
- Form Teams: Assign Team Leaders and Team Members.
- Create Projects: Specify Project Details, Deadline, Plagiriasm detection, Technology Stack, and Progress.
- Create Tasks: Team leaders can assign tasks to everyone, while members can self-assign tasks.
- View all projects and their details created by students across all Universities.
- Comment Section


# Installion & Usage
## Make sure you have the following installed:
- Python3

## 1. **Clone the repository:**
   ```
   git clone https://github.com/YashaswiniMO/UniProject.git
   cd National-Project-Management
   ```
## 2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
## 3. Install dependencies:
```
pip install -r requirements.txt
```
## 4. Apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```
## 5. Create Super user aka admin:
```
python manage.py createsuperuser
```
## 6. Run the App
Start the development server:
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/admin in your browser login with admin and in users add new user with username and password 

Now make click on edit this user and click on checkbox which says Demo User.
## 7. Logout 
## 8. Home Page
Visit http://127.0.0.1:8000/ in your browser (This page is for users aka students).


# Modules

## Teams
Teams are made up of members, and every team has a leader. Team leaders have
special privileges like being able to assign tasks to other team members and
changing the members of the team. 

## Projects
Every project is assigned to a team and thus has members and a leader associated
with it. A project can only be assigned to one team but a team can have many
projects. Once a project is over it can be marked as completed.

## Plagiarism Detection: 
Integration of plagiarism detection tools (e.g., Cosine Similarity, Levenshtein Distance) to 
check project submissions for originality. 
Provide feedback to students on possible plagiarism and offer recommendations for revision 
 
## Tasks
Tasks are assigned to projects. Once a task has been assigned to a project it
can be assigned to a member of the project's team, it will then appear on a list
of their active tasks. Tasks can be assigned by team members to themselves or by
the team leader to anyone on the team. Any member of a project's team can create
a task for the project. Every task is given a unique number that can be used to
refer to it independent of the project or user it is assigned to. Tasks can also
be marked as completed, this is generally done by the user that the task is
assigned to, but may also be done by the team leader.

## The Dashboard
One of the main features of the site is the user's dashboard.
Currently this shows six key tables, though this may change in the
future.

### 1 & 2 ) Graphs
There are two graphs , 1st one shows technologies used in all projects and the 2nd one shows all active v/s completed projects.
Note: Graph data is independent of user, i.e it shows graphs for all available projects in database.

### 3) Top tasks
This is a list of the user's top seven tasks, tasks are ranked firstly by due
date and then by priority (in other words the highest priority task that is due
today is at the top).

### 4) Unassigned tasks
A list of the top seven unassigned tasks from projects where the user is the
team leader, again sorted by due date and priority.

### 5) User's projects
A list of all active projects the user is a part of.

### 6) User's teams
A list of teams the user is a part of.

## Real-Time Communication: Forums
Integrated chat functionality for students to communicate with team members and mentors.
