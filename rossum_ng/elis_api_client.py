from __future__ import annotations

import asyncio
import typing

import aiofiles

if typing.TYPE_CHECKING:
    import pathlib
    from typing import Any, AsyncIterable, Dict, Iterable, Optional, Sequence, Tuple, Union

from rossum_ng.api_client import APIClient
from rossum_ng.models.annotation import Annotation
from rossum_ng.models.connector import Connector
from rossum_ng.models.hook import Hook
from rossum_ng.models.inbox import Inbox
from rossum_ng.models.organization import Organization
from rossum_ng.models.queue import Queue
from rossum_ng.models.schema import Schema
from rossum_ng.models.user import User
from rossum_ng.models.user_role import UserRole
from rossum_ng.models.workspace import Workspace

if typing.TYPE_CHECKING:
    APIObject = Union[
        Annotation, Connector, Hook, Inbox, Organization, Queue, Schema, UserRole, Workspace
    ]


class Sideload:
    pass


class ElisAPIClient:
    def __init__(
        self,
        username: str,
        password: str,
        base_url: Optional[str],
        http_client: Optional[APIClient] = None,
    ):
        self._http_client = http_client or APIClient(username, password, base_url)

    # ##### QUEUE #####
    async def retrieve_queue(
        self, queue_id: int, sideloads: Optional[Iterable[APIObject]] = None
    ) -> Queue:
        """https://elis.rossum.ai/api/docs/#retrieve-a-queue-2"""
        queue = await self._http_client.fetch_one("queues", queue_id)

        return Queue(**queue)

    async def list_all_queues(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[Queue]:
        """https://elis.rossum.ai/api/docs/#list-all-queues"""
        async for q in self._http_client.fetch_all("queues", ordering, **filters):
            yield Queue(**q)

    async def create_new_queue(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> Queue:
        """https://elis.rossum.ai/api/docs/#create-new-queue"""
        queue = await self._http_client.create("queues", data)

        return Queue(**queue)

    async def import_document(
        self,
        queue_id: int,
        files: Sequence[Tuple[Union[str, pathlib.Path], str]],
        values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """https://elis.rossum.ai/api/docs/#import-a-document

        arguments
        ---------
            files
                2-tuple containing current filepath and name to be used by Elis for the uploaded file
            metadata
                metadata will be set to newly created annotation object
            values
                may be used to initialize datapoint values by setting the value of rir_field_names in the schema
        """
        tasks = set()
        for file, filename in files:
            async with aiofiles.open(file) as fp:
                tasks.add(
                    asyncio.create_task(
                        self._http_client.upload("queues", queue_id, fp, filename, values, metadata)
                    )
                )

        await asyncio.gather(*tasks)

    # TODO: specific method in APICLient
    def export_annotations(self, id_: int, annotation_ids: Iterable[int], format_: str) -> dict:
        return {}

    # ##### ORGANIZATIONS #####
    async def list_all_organizations(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ):
        """https://elis.rossum.ai/api/docs/#list-all-organizations"""
        async for o in self._http_client.fetch_all("organizations", ordering, **filters):
            yield Organization(**o)

    async def retrieve_organization(
        self, org_id: int, sideloads: Optional[Iterable[APIObject]] = None
    ) -> Organization:
        """https://elis.rossum.ai/api/docs/#retrieve-an-organization"""
        organization: Dict[Any, Any] = await self._http_client.fetch_one("organizations", org_id)

        return Organization(**organization)

    # ##### SCHEMAS #####
    async def list_all_schemas(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[Schema]:
        """https://elis.rossum.ai/api/docs/#list-all-schemas"""
        async for s in self._http_client.fetch_all("schemas", ordering, **filters):
            yield Schema(**s)

    async def retrieve_schema(
        self, schema_id: int, sideloads: Optional[Iterable[APIObject]] = None
    ) -> Schema:
        """https://elis.rossum.ai/api/docs/#retrieve-a-schema"""
        schema: Dict[Any, Any] = await self._http_client.fetch_one("schemas", schema_id)

        return Schema(**schema)

    async def create_new_schema(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> Schema:
        """https://elis.rossum.ai/api/docs/#create-a-new-schema"""
        queue = await self._http_client.create("schemas", data)

        return Schema(**queue)

    # ##### USERS #####
    async def list_all_users(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[User]:
        """https://elis.rossum.ai/api/docs/#list-all-users"""
        async for u in self._http_client.fetch_all("users", ordering, **filters):
            yield User(**u)

    async def retrieve_user(
        self, user_id: int, sideloads: Optional[Iterable[APIObject]] = None
    ) -> User:
        """https://elis.rossum.ai/api/docs/#retrieve-a-user-2"""
        user = await self._http_client.fetch_one("users", user_id)

        return User(**user)

    async def create_new_user(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> User:
        """https://elis.rossum.ai/api/docs/#create-new-user"""
        user = await self._http_client.create("users", data)

        return User(**user)

    # TODO: specific method in APICLient
    def change_user_password(self, new_password: str) -> dict:
        return {}

    # TODO: specific method in APICLient
    def reset_user_password(self, email: str) -> dict:
        return {}

    # ##### ANNOTATIONS #####
    async def list_all_annotations(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[Annotation]:
        """https://elis.rossum.ai/api/docs/#list-all-annotations"""
        async for a in self._http_client.fetch_all("annotations", ordering, **filters):
            yield Annotation(**a)

    async def retrieve_annotation(
        self, annotation_id: int, sideloads: Optional[Iterable[APIObject]] = None
    ) -> Annotation:
        """https://elis.rossum.ai/api/docs/#retrieve-an-annotation"""
        annotation = await self._http_client.fetch_one("annotations", annotation_id)

        return Annotation(**annotation)

    async def update_annotation(self, annotation_id: int, data: Dict[str, Any]) -> Annotation:
        """https://elis.rossum.ai/api/docs/#update-an-annotation"""
        annotation = await self._http_client.replace("annotations", annotation_id, data)

        return Annotation(**annotation)

    async def update_part_annotation(self, annotation_id: int, data: Dict[str, Any]) -> Annotation:
        """https://elis.rossum.ai/api/docs/#update-part-of-an-annotation"""
        annotation = await self._http_client.update("annotations", annotation_id, data)

        return Annotation(**annotation)

    # ##### WORKSPACES #####
    async def list_all_workspaces(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[Workspace]:
        """https://elis.rossum.ai/api/docs/#list-all-workspaces"""
        async for w in self._http_client.fetch_all("workspaces", ordering, **filters):
            yield Workspace(**w)

    async def retrieve_workspace(
        self, workspace_id, sideloads: Optional[Iterable[APIObject]] = None
    ) -> Workspace:
        """https://elis.rossum.ai/api/docs/#retrieve-a-workspace"""
        workspace = await self._http_client.fetch_one("workspaces", workspace_id)

        return Workspace(**workspace)

    async def create_new_workspace(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> Workspace:
        """https://elis.rossum.ai/api/docs/#create-a-new-workspace"""
        workspace = await self._http_client.create("workspaces", data)

        return Workspace(**workspace)

    async def delete_workspace(
        self, workspace_id, sideloads: Optional[Iterable[APIObject]] = None
    ) -> None:
        """https://elis.rossum.ai/api/docs/#delete-a-workspace"""
        return await self._http_client.delete("workspaces", workspace_id)

    # ##### INBOX #####
    async def create_new_inbox(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> Inbox:
        """https://elis.rossum.ai/api/docs/#create-a-new-inbox"""
        inbox = await self._http_client.create("inboxes", data)

        return Inbox(**inbox)

    # ##### CONNECTORS #####
    async def list_all_connectors(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[Connector]:
        """https://elis.rossum.ai/api/docs/#list-all-connectors"""

        async for c in self._http_client.fetch_all("connectors", ordering, **filters):
            yield Connector(**c)

    async def retrieve_connector(
        self, connector_id, sideloads: Optional[Iterable[APIObject]] = None
    ) -> Connector:
        """https://elis.rossum.ai/api/docs/#retrieve-a-connector"""
        connector = await self._http_client.fetch_one("connectors", connector_id)

        return Connector(**connector)

    async def create_new_connector(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> Connector:
        """https://elis.rossum.ai/api/docs/#create-a-new-connector"""
        connector = await self._http_client.create("connectors", data)

        return Connector(**connector)

    # ##### HOOKS #####
    async def list_all_hooks(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[Hook]:
        """https://elis.rossum.ai/api/docs/#list-all-hooks"""
        async for h in self._http_client.fetch_all("hooks", ordering, **filters):
            yield Hook(**h)

    async def retrieve_hook(self, hook_id, sideloads: Optional[Iterable[APIObject]] = None) -> Hook:
        """https://elis.rossum.ai/api/docs/#retrieve-a-hook"""
        hook = await self._http_client.fetch_one("hooks", hook_id)

        return Hook(**hook)

    async def create_new_hook(
        self, data: Dict[str, Any], sideloads: Optional[Iterable[APIObject]] = None
    ) -> Hook:
        """https://elis.rossum.ai/api/docs/#create-a-new-hook"""
        hook = await self._http_client.create("hooks", data)

        return Hook(**hook)

    # ##### USER ROLES #####
    async def list_all_user_roles(
        self,
        ordering: Iterable[str] = (),
        sideloads: Optional[Iterable[APIObject]] = None,
        **filters: Dict[str, Any],
    ) -> AsyncIterable[UserRole]:
        """https://elis.rossum.ai/api/docs/#list-all-user-roles"""
        async for u in self._http_client.fetch_all("groups", ordering, **filters):
            yield UserRole(**u)
