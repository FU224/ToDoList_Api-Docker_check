## To build containers
docker compose up --build

## апишка
http://localhost:8000

## Доки (для проверки)
http://localhost:8000/docs

## endp
GET /tasks
GET /tasks/unfinished
POST /tasks
PATCH /tasks/{task_id}/status
DELETE /tasks/{task_id}
GET /joke
