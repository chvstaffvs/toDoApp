from datetime import date
from typing import List
from fastapi import Body, Depends, Query, Path
from routes.base import CustomRouter, filter_generator
from dtos.todos import ToDosDTO, ToDosResponseDTO
from models.user import User
from controllers.auth import AuthController
from controllers.todos import ToDosController

router = CustomRouter()


@router.create("/", response_model=ToDosResponseDTO)
async def create_todo(
    todo: ToDosDTO = Body(...),
    user: User = Depends(AuthController.verify_token),
):
    return ToDosController.create(todo.dict(), user)


@router.get("/list", response_model=List[ToDosResponseDTO])
async def get_todos(
    done: bool = Query(None),
    expected_date: date = Query(None),
    active: bool = Query(None),
    user: User = Depends(AuthController.verify_token),
):
    return ToDosController.get_from_user(user, filter_generator(locals(), "user"))


@router.get("/{id}", response_model=ToDosResponseDTO)
async def get_todo(
    id: int = Path(...),
    user: User = Depends(AuthController.verify_token),
):
    return ToDosController.protected_operation("get", id, user)


@router.put("/{id}", response_model=ToDosResponseDTO)
async def edit_todo(
    id: int = Path(...),
    todo: ToDosDTO.EditSchema = Body(...),
    user: User = Depends(AuthController.verify_token),
):
    return ToDosController.protected_operation("update", id, user, schema=todo.dict())


@router.delete("/{id}")
async def delete_todo(
    id: int = Path(...),
    user: User = Depends(AuthController.verify_token),
):
    return ToDosController.protected_operation("delete", id, user)


@router.delete("/")
async def delete_all_todos(
    user: User = Depends(AuthController.verify_token),
):
    return ToDosController.wipe(user)