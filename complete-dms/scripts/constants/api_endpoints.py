class Endpoints:

 AUTH_SIGNUP = "/auth/signup"
 AUTH_LOGIN = "/auth/login"

 DOCKER_LOGIN = "/docker/login"

 IMAGE_BUILD_ADV = "/docker/images/build"
 IMAGE_PUSH = "/docker/images/push"
 IMAGE_PULL = "/docker/images/pull"
 IMAGE_LIST = "/docker/images/list"
 IMAGE_DETAILS = "/docker/images/details"
 IMAGE_DELETE = "/docker/images/delete"

 CONTAINER_RUN = "/docker/containers"
 CONTAINER_RUN_ADV = "/docker/containers/advanced"
 CONTAINER_START = "/docker/containers/{name}/start"
 CONTAINER_STOP = "/docker/containers//{name}/stop"
 CONTAINER_LOGS = "/docker/containers/{name}/logs"
 CONTAINER_LIST = "/docker/containers"
 CONTAINER_DETAILS = "/docker/containers/{name}"
 CONTAINER_REMOVE = "/docker/containers/{name}"

 VOLUME_CREATE = "/create"
 VOLUME_DELETE = "/delete/{name}"
 VOLUME_LIST = "/list"
 VOLUME_DETAILS = "/details/{name}"