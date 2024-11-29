from app.models import Task, User
from app import db
from typing import List, Dict
from datetime import datetime

class TaskManager:
    @staticmethod
    def create_task(title: str, description: str, user_id: int) -> Task:
        """
        Create a new task
        
        Args:
            title: Task title
            description: Task description
            user_id: ID of the user creating the task
            
        Returns:
            Task: Created task object
        """
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_user_tasks(user_id: int) -> List[Task]:
        """
        Get all tasks for a specific user
        
        Args:
            user_id: ID of the user
            
        Returns:
            List[Task]: List of user's tasks
        """
        return Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()

    @staticmethod
    def get_task(task_id: int) -> Task:
        """
        Get a specific task
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task: Task object if found, None otherwise
        """
        return Task.query.get(task_id)

    @staticmethod
    def update_task(task_id: int, **kwargs) -> Dict:
        """
        Update a task's attributes
        
        Args:
            task_id: ID of the task to update
            **kwargs: Attributes to update
            
        Returns:
            dict: Operation result
        """
        task = Task.query.get(task_id)
        if not task:
            return {'error': 'Task not found'}

        try:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.session.commit()
            return {'success': True, 'task': task}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}

    @staticmethod
    def delete_task(task_id: int) -> Dict:
        """
        Delete a task
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            dict: Operation result
        """
        task = Task.query.get(task_id)
        if not task:
            return {'error': 'Task not found'}

        try:
            db.session.delete(task)
            db.session.commit()
            return {'success': True}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}

    @staticmethod
    def mark_completed(task_id: int) -> Dict:
        """
        Mark a task as completed
        
        Args:
            task_id: ID of the task
            
        Returns:
            dict: Operation result
        """
        return TaskManager.update_task(task_id, completed=True)
