// Table Users
{
  "_id": ObjectId("user123"),
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password_hash": "hashed_password",
  "created_at": ISODate("2024-09-09T12:00:00Z"),
  "last_login": ISODate("2024-09-10T08:30:00Z")
}
  
// Table Projects
{
  "_id": ObjectId("project001"),
  "name": "Taskify Platform Development",
  "description": "Develop the new platform for task management",
  "status": "in-progress",  // "pending", "in-progress", "completed"
  "priority": "high",  // "low", "medium", "high"
  "created_at": ISODate("2024-09-09T12:00:00Z"),
  "deadline": ISODate("2024-12-31T23:59:59Z"),
  "team_members": [
    {
      "user_id": ObjectId("user123"),
      "role": "admin"  // "admin" o "collaborator"
    },
    {
      "user_id": ObjectId("user456"),
      "role": "collaborator"
    },
    {
      "user_id": ObjectId("user789"),
      "role": "collaborator"
    }
  ],
  "tables": [
    {
      "table_id": ObjectId("table001"),
      "name": "Tabla 1",
      "columns": [
        {
          "column_id": ObjectId("col001"),
          "name": "Estado",
          "type": "status",  // Puede ser "status", "text", "date", "number", etc.
          "options": ["pending", "in-progress", "completed"]  // Opcional para columnas de tipo 'status'
        },
        {
          "column_id": ObjectId("col002"),
          "name": "Fecha de entrega",
          "type": "date"
        },
        {
          "column_id": ObjectId("col003"),
          "name": "Asignado a",
          "type": "user"
        },
        {
          "column_id": ObjectId("col004"),
          "name": "Prioridad",
          "type": "dropdown",
          "options": ["low", "medium", "high"]
        }
      ],
      "tasks": [
        {
          "task_id": ObjectId("task001"),
          "title": "Diseñar la UI para el login",
          "description": "Diseñar la interfaz de usuario para la página de login",
          "column_values": {
            "col001": "in-progress",  // Estado
            "col002": ISODate("2024-09-15T23:59:59Z"),  // Fecha de entrega
            "col003": ObjectId("user456"),  // Asignado a
            "col004": "medium"  // Prioridad
          },
          "created_at": ISODate("2024-09-09T12:00:00Z"),
          "subtasks": [
            {
              "subtask_id": ObjectId("subtask001"),
              "title": "Crear wireframes",
              "status": "completed"
            },
            {
              "subtask_id": ObjectId("subtask002"),
              "title": "Revisión del feedback de usuarios",
              "status": "pending"
            }
          ]
        }
      ]
    }
  ]
}



// Table Task 
{
    "_id": ObjectId("task001"),
    "title": "Diseñar la UI para el login",
    "description": "Diseñar la interfaz de usuario para la página de login",
    "project_id": ObjectId("project001"),
    "table_id": ObjectId("table001"),
    "assigned_user_id": ObjectId("user456"),
    "status": "in-progress",
    "priority": "medium",
    "created_at": ISODate("2024-09-09T12:00:00Z"),
    "deadline": ISODate("2024-09-15T23:59:59Z"),
    "subtasks": [
      {
        "subtask_id": ObjectId("subtask001"),
        "title": "Crear wireframes",
        "status": "completed"
      },
      {
        "subtask_id": ObjectId("subtask002"),
        "title": "Revisión del feedback de usuarios",
        "status": "pending"
      }
    ]
  }
// SubTable of task (optional)
{
    "_id": ObjectId("subtask001"),
    "title": "Crear wireframes",
    "status": "completed",
    "task_id": ObjectId("task001"),
    "assigned_user_id": ObjectId("user456"),
    "created_at": ISODate("2024-09-09T12:00:00Z")
  }
  
// Table Task Comments
{
    "_id": ObjectId("comment001"),
    "task_id": ObjectId("task001"),
    "user_id": ObjectId("user123"),
    "comment": "I've completed the first wireframe draft.",
    "attachments": [
      {
        "file_name": "wireframe_v1.png",
        "file_url": "https://example.com/wireframes/wireframe_v1.png"
      }
    ],
    "mentions": [
      { "user_id": ObjectId("user456") }
    ],
    "created_at": ISODate("2024-09-10T12:00:00Z")
  }
// Table notifications
{
    "_id": ObjectId("notification001"),
    "user_id": ObjectId("user123"),
    "type": "task_assigned",  // Puede ser "task_assigned", "comment_mentioned", etc.
    "message": "You have been assigned a new task: Design UI for login page",
    "is_read": false,
    "created_at": ISODate("2024-09-10T12:00:00Z")
  }
  
// Table Register Activity
{
    "_id": ObjectId("log001"),
    "event": "task_created",
    "user_id": ObjectId("user123"),
    "description": "User John Doe created a task: Design UI for login page",
    "related_task_id": ObjectId("task001"),
    "created_at": ISODate("2024-09-09T12:00:00Z")
  }
  
// Structure Database in mongoDB
// Usuarios (users): Datos de los usuarios, sus roles y equipos.
// Equipos (teams): Equipos con sus miembros y proyectos asociados.
// Proyectos (projects): Proyectos que contienen tablas (fases o grupos de tareas).
// Tablas (dentro de projects): Grupos de tareas dentro de cada proyecto.
// Tareas (tasks): Las tareas dentro de cada tabla (si decides separarlas en su propia colección).
// Subtareas (subtasks): Subtareas dentro de las tareas.
// Comentarios (task_comments): Comentarios relacionados con tareas.
// Notificaciones (notifications): Notificaciones de eventos importantes.
// Registros de actividad (activity_logs): Rastreo de eventos clave en la plataforma.