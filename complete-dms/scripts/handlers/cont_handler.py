import docker
from docker.errors import NotFound
from fastapi import HTTPException
from scripts.utils.response_handler import handle_exception
from scripts.models.cont_model import *
from scripts.constants.app_constants import *

client = docker.from_env()

def run_container_advanced(data: ContainerRunAdvancedRequest):
    try:
        kwargs = data.dict(exclude_unset=True)
        image = kwargs.pop("image")
        command = kwargs.pop("command", None)

        container = client.containers.run(image=image, command=command, **kwargs)

        return {
            "message": CONTAINER_START_SUCCESS,
            "id": container.id,
            "status": container.status
        }
    except Exception as e:
        handle_exception(e, CONTAINER_CREATE_FAILURE)


def list_containers_with_filters(params: ContainerListRequest):
    try:
        kwargs = params.dict(exclude_unset=True)
        containers = client.containers.list(**kwargs)

        return [
            {
                "name": c.name,
                "id": c.id,
                "image": c.image.tags,
                "status": c.status
            } for c in containers
        ]
    except Exception as e:
        handle_exception(e, CONTAINER_LIST_FAILURE)


def stop_container(name: str, timeout: float = None):
    try:
        container = client.containers.get(name)
        stop_args = {"timeout": timeout} if timeout is not None else {}
        container.stop(**stop_args)
        return {"message": CONTAINER_STOP_SUCCESS}
    except Exception as e:
        handle_exception(e, CONTAINER_STOP_FAILURE)


def start_container(name: str):
    try:
        container = client.containers.get(name)
        container.start()
        return {"message": CONTAINER_START_SUCCESS}
    except Exception as e:
        handle_exception(e, CONTAINER_START_FAILURE)


def get_logs_with_params(name: str, params: ContainerLogsRequest) -> ContainerLogsResponse:
    try:
        container = client.containers.get(name)
        opts = params.dict(exclude_unset=True)

        if opts.pop("follow", False):
            # For follow=True, we stream logs (not suitable for structured return)
            raise HTTPException(status_code=400, detail="Streaming logs not supported in structured response.")

        raw_logs = container.logs(stream=False, **opts)
        logs = raw_logs.decode("utf-8", errors="ignore").splitlines()

        return ContainerLogsResponse(
            container_id=name,
            logs=logs,
            message=CONTAINER_LOGS_RETRIEVED
        )

    except NotFound:
        raise HTTPException(status_code=404, detail=CONTAINER_NOT_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{CONTAINER_LOGS_FAILURE}: {str(e)}"
        )


def remove_container_with_params(name: str, params: ContainerRemoveRequest):
    try:
        container = client.containers.get(name)
        opts = params.dict(exclude_unset=True)
        container.remove(**opts)
        return {
            "message": CONTAINER_REMOVE_SUCCESS,
            "used_options": opts
        }
    except Exception as e:
        handle_exception(e, CONTAINER_REMOVE_FAILURE)
