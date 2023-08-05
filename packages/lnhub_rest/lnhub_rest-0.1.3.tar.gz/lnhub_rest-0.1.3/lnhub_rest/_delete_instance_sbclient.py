from datetime import datetime, timedelta
from typing import Union

from lamin_logger import logger

from lnhub_rest._sbclient import connect_hub_with_auth


def delete_ci_instances() -> None:
    try:
        hub = connect_hub_with_auth()
        # Delete instances created by the CI more than one hour ago
        data = (
            hub.table("instance")
            .delete()
            .like("name", "lamin.ci.instance.%")
            .lt("created_at", datetime.now() - timedelta(hours=1))
            .execute()
            .data
        )
        instance_count = len(data)
        logger.info(f"{instance_count} instances deleted")
    finally:
        hub.auth.sign_out()


def delete_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
) -> Union[None, str]:
    try:
        hub = connect_hub_with_auth()

        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

        data = (
            hub.table("instance")
            .delete()
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
            .data
        )
        if len(data) == 0:
            return "instance-does-not-exist-on-hub"

        # TODO: delete storage if no other instances use it
        return None
    finally:
        hub.auth.sign_out()
