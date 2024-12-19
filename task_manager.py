# task_manager.py
import streamlit as st
import json
from datetime import datetime
from db_config import SessionLocal, Task

class TaskManager:
    def __init__(self):
        self.session = SessionLocal()
    
    def add_task(self, title, description=""):
        try:
            task = Task(title=title, description=description)
            self.session.add(task)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            st.error(f"Error al agregar tarea: {str(e)}")
            return False
    
    def list_tasks(self):
        return self.session.query(Task).all()
    
    def complete_task(self, task_id):
        try:
            task = self.session.query(Task).filter(Task.id == task_id).first()
            if task:
                task.completed = True
                self.session.commit()
                return True
        except Exception as e:
            self.session.rollback()
            st.error(f"Error al completar tarea: {str(e)}")
        return False
    
    def delete_task(self, task_id):
        try:
            task = self.session.query(Task).filter(Task.id == task_id).first()
            if task:
                self.session.delete(task)
                self.session.commit()
                return True
        except Exception as e:
            self.session.rollback()
            st.error(f"Error al eliminar tarea: {str(e)}")
        return False
    
    def export_tasks(self, filename):
        try:
            tasks = self.session.query(Task).all()
            tasks_dict = [task.to_dict() for task in tasks]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tasks_dict, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.error(f"Error al exportar tareas: {str(e)}")
            return False
    
    def import_tasks(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks_dict = json.load(f)
            
            for task_data in tasks_dict:
                task = Task(
                    title=task_data['title'],
                    description=task_data['description'],
                    completed=task_data['completed'],
                    created_at=datetime.fromisoformat(task_data['created_at'])
                )
                self.session.add(task)
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            st.error(f"Error al importar tareas: {str(e)}")
            return False
        
        