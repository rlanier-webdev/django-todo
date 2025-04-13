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