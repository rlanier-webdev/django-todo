# Todo App with Django

A simple Todo App built with Django where users can manage tasks, mark them as complete, and organize them into active and completed categories. This app provides a dashboard where users can interact with tasks, view active tasks, and move them to a completed section.

## Features

### 1. **User Authentication**
   - **Registration**: Users can sign up to create an account.
   - **Login/Logout**: Users can log in to their account and log out when needed.
   - **Dashboard**: After logging in, users are directed to their personal dashboard.

### 2. **Task Management**
   - **Add Task**: Users can create new tasks by providing a title, description, priority, and deadline.
   - **Edit Task**: Users can edit the details of a task (e.g., change the title, description, or priority).
   - **Delete Task**: Users can delete a task they no longer need.

### 3. **Task Status**
   - **Mark as Complete**: Users can mark a task as completed by clicking a checkbox. When checked, the task moves from the "Active Tasks" table to the "Completed Tasks" table.
   - **Move Back to Active**: If a user unchecks the "complete" checkbox, the task moves back to the active section.
   
### 4. **Task Prioritization**
   - **Priority Color Coding**: Tasks are color-coded based on their priority. Possible priorities:
     - **Low**: Green
     - **Medium**: Blue
     - **High**: Yellow
     - **Urgent**: Red
   - Priority can be set when creating or editing a task.

### 5. **Task Sorting**
   - Tasks are displayed in descending order of their creation date.
   - The dashboard shows two separate tables:
     - **Active Tasks**: Tasks that are still pending or in-progress.
     - **Completed Tasks**: Tasks that have been marked as completed.
  
### 6. **Responsive UI**
   - The app is fully responsive and works well on both mobile and desktop devices.
   - Bootstrap is used to style the UI, providing a clean, modern design.

### 7. **Table Pagination**
   - Active and completed tasks are paginated, with a maximum of 10 tasks displayed per page.

### 8. **📅 Calendar View**
- Visual overview of all tasks using FullCalendar.
- Tasks appear on their respective due dates.
- Hover or click to view task details.
- Access from the dashboard via the **Calendar View** button.
- Built with [FullCalendar](https://fullcalendar.io/) for rich interaction and styling.

## Cloning the Project

To clone this project to your local machine and get started, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rlanier-webdev/django-todo.git
   ```

2. **Navigate to the project folder:**

   ```bash
   cd django-todo/core
   ```

3. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**
   - For **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - For **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

5. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (to log in and access the admin interface):**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

9. Open your browser and go to `http://127.0.0.1:8000/` to view the app.

## Screenshots

Here are some screenshots of the app in action:

### Home Page (Login Screen):
![Login Screen](https://github.com/user-attachments/assets/7735adf1-a934-4ba9-b938-33f90f3ab7b5)
![Sign Up Screen](https://github.com/user-attachments/assets/f10d2099-6961-4304-843e-bcb57e0d2708)

### Dashboard (After Login):
![Empty Dashboard](https://github.com/user-attachments/assets/fa436cbf-623c-4f65-a52c-c7632ddf7b02)
![Dashboard with Tasks](https://github.com/user-attachments/assets/ae5facd9-7a81-467c-a12f-20a6b5d972d4)

### Task Management:
![Create Task](https://github.com/user-attachments/assets/28726ea6-7f88-478f-9346-fe3a3a60c20d)
![View Task](https://github.com/user-attachments/assets/26f22960-f701-490a-8e9c-cad2e29ebf46)
![Edit Task](https://github.com/user-attachments/assets/d3cfc721-f78e-49b8-a91b-4b2c122d6fe1)

### Calendar View:
![Calendar](https://github.com/user-attachments/assets/483ef950-877a-4dbc-b3f4-fd00d978a490)

