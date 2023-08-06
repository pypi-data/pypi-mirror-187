from typing import Callable

from fastapi import Depends, APIRouter, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from facrud_router.generics import Model, IdentifierType, Authentication
from .logger import logger


class RetrieveRouterMixin:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable
    get_authentication: Callable

    retrieve_response_schema: BaseModel.__class__

    api_router: APIRouter

    @property
    def retrieve_url_pattern(self):
        return "/%s/{id}" % self.prefix

    async def perform_retrieve(self, id: IdentifierType, session: AsyncSession, *args, **kwargs) -> Model:
        query = await session.execute(select(self.model).where(self.model.id == id))
        if instance := query.scalars().first():
            return instance
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    def register_retrieve_action(self, *args, **kwargs):
        if not self.retrieve_response_schema:
            raise ValueError("retrieve_response_schema must not be None")

        async def retrieve(
                request: Request,
                id: self.identifier_type,  # type: ignore
                session: AsyncSession = Depends(self.get_session),
                authentication: Authentication = Depends(self.get_authentication)
        ) -> self.retrieve_response_schema:  # type: ignore
            logger.info(f"Received a request to retrieve an entity of type {self.model} with id {id}")
            try:
                response = await self.perform_retrieve(
                    id=id, session=session, request=request, authentication=authentication, *args, **kwargs
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(f"Error when retrieving an object of type {self.model}: {e}")
                raise e
            logger.info(f"An object of type {self.model} with id {id} was successfully retrieved: {response}")
            return response

        self.api_router.get(
            path=self.retrieve_url_pattern, response_model=self.retrieve_response_schema,
            status_code=status.HTTP_200_OK
        )(retrieve)


class ListRouterMixin:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable
    get_authentication: Callable

    list_response_schema: BaseModel.__class__

    api_router: APIRouter

    @property
    def list_url_pattern(self) -> str:
        return "/%s" % self.prefix

    async def perform_list(self, session: AsyncSession, *args, **kwargs) -> Model:
        query = await session.execute(select(self.model))
        return query.scalars().all()

    def register_list_action(self, *args, **kwargs):
        if not self.list_response_schema:
            raise ValueError("list_response_schema must not be None")

        async def list(
                request: Request,
                session: AsyncSession = Depends(self.get_session),
                authentication: Authentication = Depends(self.get_authentication)  # type: ignore
        ) -> self.list_response_schema:  # type: ignore
            logger.info(f"Received a request to get a list of entities of type {self.model}")
            try:
                response = await self.perform_list(
                    session=session, request=request, authentication=authentication, *args, **kwargs
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(f"Error when getting a list of objects of type {self.model}: {e}")
                raise e
            logger.info(f"List of objects of type {self.model} was successfully received: {response}")
            return response

        self.api_router.get(
            path=self.list_url_pattern, response_model=self.list_response_schema,
            status_code=status.HTTP_200_OK
        )(list)


class DeleteRouterMixin:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable
    get_authentication: Callable

    api_router: APIRouter

    @property
    def delete_url_pattern(self) -> str:
        return "/%s/{id}" % self.prefix

    async def perform_delete(self, id: IdentifierType, session: AsyncSession, *args, **kwargs):
        await session.execute(delete(self.model).where(self.model.id == id))
        await session.commit()

    def register_delete_action(self, *args, **kwargs):
        async def delete(
                request: Request,
                id: self.identifier_type,  # type: ignore
                session: AsyncSession = Depends(self.get_session),
                authentication: Authentication = Depends(self.get_authentication)  # type: ignore
        ):
            logger.info(f"Received a request to delete an entity of type {self.model}")
            try:
                await self.perform_delete(
                    id=id, session=session, request=request, authentication=authentication, *args, **kwargs
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(f"Error when deleting an object of type {self.model}: {e}")
                raise e
            logger.info(f"An object of type {self.model} was successfully deleted")

        self.api_router.delete(
            path=self.delete_url_pattern,
            status_code=status.HTTP_204_NO_CONTENT
        )(delete)


class CreateRouterMixin:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable
    get_authentication: Callable

    create_request_schema: BaseModel.__class__
    create_response_schema: BaseModel.__class__

    api_router: APIRouter

    @property
    def create_url_pattern(self) -> str:
        return "/%s" % self.prefix

    async def perform_create(self, data: BaseModel, session: AsyncSession, *args, **kwargs) -> Model:
        # TODO: Error if entity exists
        instance = self.model(**data.dict())
        session.add(instance)
        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Violation database constraints")
        else:
            return instance

    def register_create_action(self, *args, **kwargs):
        if not (self.create_request_schema and self.create_response_schema):
            raise ValueError("create_request_schema and create_response_schema must not be None")

        async def create(
                request: Request,
                data: self.create_request_schema,  # type: ignore
                session: AsyncSession = Depends(self.get_session),
                authentication: Authentication = Depends(self.get_authentication)  # type: ignore
        ) -> self.create_response_schema:  # type: ignore
            logger.info(f"Received a request to create an entity of type {self.model}: {data}")
            try:
                response = await self.perform_create(
                    data=data, session=session, request=request, authentication=authentication, *args, **kwargs
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(f"Error when creating an object of type {self.model}: {e}")
                raise e
            logger.info(f"An object of type {self.model} was successfully created: {response}")
            return response

        self.api_router.post(
            path=self.create_url_pattern, response_model=self.create_response_schema,
            status_code=status.HTTP_201_CREATED
        )(create)


class UpdateRouterMixin:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable
    get_authentication: Callable

    update_request_schema: BaseModel.__class__
    update_response_schema: BaseModel.__class__

    api_router: APIRouter

    @property
    def update_url_pattern(self) -> str:
        return "/%s/{id}" % self.prefix

    async def perform_update(
            self, id: IdentifierType, data: BaseModel, session: AsyncSession, *args, **kwargs
    ) -> Model:
        query = await session.execute(select(self.model).where(self.model.id == id))
        if instance := query.scalars().first():
            for key, value in data.dict().items():
                setattr(instance, key, value)
            await session.commit()
            return instance
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    def register_update_action(self, *args, **kwargs):
        if not (self.update_request_schema and self.update_response_schema):
            raise ValueError("update_request_schema and update_response_schema must not be None")

        async def update(
                request: Request,
                id: self.identifier_type,  # type: ignore
                data: self.update_request_schema,  # type: ignore
                session: AsyncSession = Depends(self.get_session),
                authentication: Authentication = Depends(self.get_authentication)  # type: ignore
        ) -> self.update_response_schema:  # type: ignore
            logger.info(f"Received a request to update an entity of type {self.model} with id{id}: {data}")
            try:
                response = await self.perform_update(
                    id=id, data=data, session=session, request=request, authentication=authentication, *args, **kwargs
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(f"Error updating an object of type {self.model} with id{id}: {e}")
                raise e
            logger.info(f"An object of type {self.model} with id {id} was successfully updated: {response}")
            return response

        self.api_router.put(
            path=self.update_url_pattern, response_model=self.update_response_schema,
            status_code=status.HTTP_200_OK
        )(update)


class PartialUpdateRouterMixin:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable
    get_authentication: Callable

    partial_update_request_schema: BaseModel.__class__
    partial_update_response_schema: BaseModel.__class__

    api_router: APIRouter

    @property
    def partial_update_url_pattern(self) -> str:
        return "/%s/{id}" % self.prefix

    async def perform_partial_update(
            self, id: IdentifierType, data: BaseModel, session: AsyncSession, *args, **kwargs
    ) -> Model:
        query = await session.execute(select(self.model).where(self.model.id == id))
        if instance := query.scalars().first():
            for key, value in data.dict(exclude_none=True, exclude_unset=True).items():
                setattr(instance, key, value)
            await session.commit()
            return instance
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    def register_partial_update_action(self, *args, **kwargs):
        if not (self.partial_update_request_schema and self.partial_update_response_schema):
            raise ValueError("partial_update_request_schema and partial_update_response_schema must not be None")

        async def partial_update(
                request: Request,
                id: self.identifier_type,  # type: ignore
                data: self.partial_update_request_schema,  # type: ignore
                session: AsyncSession = Depends(self.get_session),
                authentication: Authentication = Depends(self.get_authentication)  # type: ignore
        ) -> self.partial_update_response_schema:  # type: ignore
            logger.info(
                f"Received a request for a partial update of an entity of type {self.model} with id{id}: {data}"
            )
            try:
                response = await self.perform_partial_update(
                    id=id, data=data, session=session, request=request, authentication=authentication, *args, **kwargs
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(f"Error when partially updating an object of type {self.model} with id{id}: {e}")
                raise e
            logger.info(f"An object of type {self.model} with id {id} was successfully partial updated: {response}")
            return response

        self.api_router.patch(
            path=self.partial_update_url_pattern,
            response_model=self.partial_update_response_schema,
            status_code=status.HTTP_200_OK
        )(partial_update)
