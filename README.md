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
![Login](https://github.com/user-attachments/assets/a7637e58-f559-41a1-9ab1-86fa598cd30a)
![SignUp](https://github.com/user-attachments/assets/f02a428d-f6ea-4578-83fe-5b2038ff1e83)

### Dashboard (After Login):
![Dashboard](https://github.com/user-attachments/assets/08c38aa2-269f-4c4e-9095-4f008f9fb171)
![Dashboard](https://github.com/user-attachments/assets/d4abc7dc-efab-48ac-90ff-0f0398732df8)

### Task Management:
![Create Task](https://github.com/user-attachments/assets/28726ea6-7f88-478f-9346-fe3a3a60c20d)
![Edit Task](https://github.com/user-attachments/assets/c411344f-dc6f-4fc0-b2ca-f64e4f3c3588)
