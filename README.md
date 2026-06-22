 а если сделать так приходит запрос на API
 POST /repositories
{
  "repo_url": "https://github.com/user/project",
  "branch": "main"
}
 
ми сохраняем в БД реляционую или в nosql и кидаем пользователю uuid 
и ставмим задачу на индексацию (видаем в воркер).ну а там дальше
GET /repositories/{repo_id}/status
POST /repositories/{repo_id}/ask
{
  "question": "де реалізовано auth?"
}