from datetime import date
from typing import List
from fastapi import Body, Path, Query
from controllers import UserController
from dtos import ResponseUserDTO, RegisterUserDTO
from dtos.user import UserDTO
from routes.base import CustomRouter, filter_generator

router = CustomRouter()


@router.create("/", response_model=ResponseUserDTO)
async def register_user(user_data: RegisterUserDTO = Body(...)):
    return UserController.create(user_data.dict())


@router.get("/id/{id}", response_model=ResponseUserDTO)
async def get_user_by_id(id: int = Path(...)):
    return UserController.get(id)


@router.get("/username/{username}", response_model=ResponseUserDTO)
async def get_user_by_username(username: str):
    return UserController.get_by_username(username)


@router.get("/", response_model=List[ResponseUserDTO])
async def list_users(
    first_name: str = Query(None),
    last_name: str = Query(None),
    birth_date: date = Query(None),
):
    return UserController.list(filter_generator(locals()))


@router.put("/edit/{id}", response_model=ResponseUserDTO)
async def edit_user(id: int = Path(...), user_data: UserDTO.EditSchema = Body(...)):
    return UserController.update(id, user_data.dict())


@router.put("/password/{id}", response_model=ResponseUserDTO)
async def change_password(id: int = Path(...), password: str = Body(..., embed=True)):
    return UserController.change_password(id, password)


@router.delete("/{id}")
async def delete(id: int = Path(...)):
    return UserController.delete(id)