# app.py
import streamlit as st
from task_manager import TaskManager

def main():
    st.title("Gestor de Tareas")
    
    # Inicializar TaskManager
    task_manager = TaskManager()
    
    # Sidebar para acciones principales
    action = st.sidebar.selectbox(
        "Seleccione una acción",
        ["Agregar Tarea", "Listar Tareas", "Exportar/Importar Tareas"]
    )
    
    if action == "Agregar Tarea":
        st.header("Agregar Nueva Tarea")
        title = st.text_input("Título de la tarea")
        description = st.text_area("Descripción (opcional)")
        
        if st.button("Agregar"):
            if title:
                if task_manager.add_task(title, description):
                    st.success("Tarea agregada exitosamente!")
            else:
                st.warning("Por favor ingrese un título para la tarea")
    
    elif action == "Listar Tareas":
        st.header("Lista de Tareas")
        tasks = task_manager.list_tasks()
        
        if not tasks:
            st.info("No hay tareas pendientes")
        
        for task in tasks:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if task.completed:
                    st.markdown(f"~~{task.title}~~")
                else:
                    st.write(task.title)
                if task.description:
                    st.write(f"*{task.description}*")
            
            with col2:
                if not task.completed and st.button("Completar", key=f"complete_{task.id}"):
                    if task_manager.complete_task(task.id):
                        st.rerun()
            
            with col3:
                if st.button("Eliminar", key=f"delete_{task.id}"):
                    if task_manager.delete_task(task.id):
                        st.rerun()
    
    else:  # Exportar/Importar Tareas
        st.header("Exportar/Importar Tareas")
        
        # Exportar
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Exportar Tareas")
            export_filename = st.text_input("Nombre del archivo para exportar", "tareas.json")
            if st.button("Exportar"):
                if task_manager.export_tasks(export_filename):
                    st.success(f"Tareas exportadas a {export_filename}")
        
        # Importar
        with col2:
            st.subheader("Importar Tareas")
            import_filename = st.text_input("Nombre del archivo para importar", "tareas.json")
            if st.button("Importar"):
                if task_manager.import_tasks(import_filename):
                    st.success(f"Tareas importadas desde {import_filename}")

if __name__ == "__main__":
    main()

    