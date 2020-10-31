from datetime import date
from typing import List
from fastapi import Body, Path, Query
from fastapi.param_functions import Depends
from controllers import UserController
from controllers.auth import AuthController
from dtos import ResponseUserDTO, RegisterUserDTO
from dtos.user import UserDTO
from models.user import User
from routes.base import CustomRouter, filter_generator

router = CustomRouter()


@router.create("/", response_model=ResponseUserDTO)
async def register_user(user_data: RegisterUserDTO = Body(...)):
    return UserController.create(user_data.dict())


@router.get("/id/{id}", response_model=ResponseUserDTO)
async def get_user(user: User = Depends(AuthController.verify_token)):
    return UserController.get(user.id)


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


@router.put("/edit", response_model=ResponseUserDTO)
async def edit_user(
    user_data: UserDTO.EditSchema = Body(...),
    user: User = Depends(AuthController.verify_token),
):
    return UserController.update(user.id, user_data.dict())


@router.put("/password/", response_model=ResponseUserDTO)
async def change_password(
    password: str = Body(..., embed=True),
    user: User = Depends(AuthController.verify_token),
):
    return UserController.change_password(user.id, password)


@router.delete("/")
async def delete(user: User = Depends(AuthController.verify_token)):
    return UserController.delete(user.id)