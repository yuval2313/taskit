import http from "./httpService";

const apiEndpoint = "/api/tasks";

function taskUrl(taskId) {
  return `${apiEndpoint}/${taskId}`;
}

export async function getTasks() {
  const { data } = await http.get(apiEndpoint);
  return data.map((task) => mapToViewModel(task));
}

export async function deleteTask(taskId) {
  const { data } = await http.delete(taskUrl(taskId));
  return mapToViewModel(data);
}

export async function saveTask(task) {
  const body = mapToApiModel(task);
  delete body.id;
  let response;

  if (task.id) response = await http.put(taskUrl(task.id), body);
  else response = await http.post(apiEndpoint, body);

  return mapToViewModel(response.data);
}

function mapToViewModel(task) {
  return {
    id: task.id,
    title: task.title,
    body: task.body,
    statusDone: task.status_done,
    createdAt: task.created_at,
    updatedAt: task.updated_at,
  };
}

function mapToApiModel(task) {
  return {
    id: task.id,
    title: task.title,
    body: task.body,
    status_done: task.statusDone,
  };
}
