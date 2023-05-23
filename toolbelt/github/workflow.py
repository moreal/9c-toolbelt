from datetime import datetime
from typing import Optional

import structlog

from toolbelt.client.github import GithubClient, WORKFLOW_STATUS
from toolbelt.constants import LINUX, MAC, WIN, BINARY_FILENAME_MAP

logger = structlog.get_logger(__name__)

def get_artifact_urls(github_client: GithubClient, commit: str, run_id: Optional[str] = None) -> dict:
    # for status in [
    #     "completed",
    #     "action_required",
    #     "cancelled",
    #     "failure",
    #     "neutral",
    #     "skipped",
    #     "stale",
    #     "success",
    #     "timed_out",
    #     "in_progress",
    #     "queued",
    #     "requested",
    #     "waiting",
    #     "pending",
    # ]:
    #     workflow_runs = next(github_client.get_workflow_runs(status, head_sha=commit))

    #     artifacts_url = None
    #     for workflow in workflow_runs["workflow_runs"]:
    #         if workflow["name"] == "Build and Release":
    #             artifacts_url = workflow["artifacts_url"]

    #     logger.info(artifacts_url)
    #     if artifacts_url is not None:
    #         logger.info("Workflow Status", status=status)
    #         break
    # if artifacts_url is None and run_id is not None:
    #     artifacts_url = github_client.generate_artifacts_url(run_id)
    # artifacts_url = github_client.generate_artifacts_url(run_id)

    # assert artifacts_url is not None

    # artifacts_response = github_client._session.get(artifacts_url)
    # logger.info(artifacts_response)
    artifacts_response = github_client.generate_artifacts_url(run_id)
    artifacts = github_client.handle_response(artifacts_response)

    logger.info(artifacts)
    result = {
        WIN: "",
        MAC: "",
        LINUX: "",
    }

    for artifact in artifacts["value"]:
        expiresOn = datetime.fromisoformat(artifact["expiresOn"].rstrip("Z")[:-1])
        assert expiresOn > datetime.now()

        if "Window" in artifact["name"] or "win" in artifact["name"]:
            result[WIN] = f"{artifact['fileContainerResourceUrl']}?itemPath={artifact['name']}/{BINARY_FILENAME_MAP[WIN]}"
        if "OSX" in artifact["name"] or "mac" in artifact["name"]:
            # result[MAC] = artifact["fileContainerResourceUrl"]
            result[MAC] = f"{artifact['fileContainerResourceUrl']}?itemPath={artifact['name']}/{BINARY_FILENAME_MAP[MAC]}"
        if "Linux" in artifact["name"] or "linux" in artifact["name"]:
            # result[LINUX] = artifact["fileContainerResourceUrl"]
            result[LINUX] = f"{artifact['fileContainerResourceUrl']}?itemPath={artifact['name']}/{BINARY_FILENAME_MAP[LINUX]}"
        logger.info(result)

    return result
