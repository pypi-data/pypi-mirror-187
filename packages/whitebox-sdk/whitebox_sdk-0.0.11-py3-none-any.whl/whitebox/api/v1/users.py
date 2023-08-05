from whitebox.schemas.user import User, UserCreateDto
from fastapi import APIRouter, Depends, status
from whitebox import crud
from sqlalchemy.orm import Session
from whitebox.core.db import get_db
from whitebox.schemas.utils import StatusCode
from whitebox.utils.passwords import hash_password
from whitebox.utils.errors import add_error_responses

users_router = APIRouter()


@users_router.post(
    "/users",
    tags=["Users"],
    response_model=User,
    summary="Create user",
    status_code=status.HTTP_201_CREATED,
    responses=add_error_responses([400, 409]),
)
async def create_user(body: UserCreateDto, db: Session = Depends(get_db)) -> User:
    """Creates an admin user during testing"""
    body.api_key = hash_password(body.api_key)
    new_user = crud.users.create(db=db, obj_in=body)
    return new_user


@users_router.delete(
    "/users/{user_id}",
    tags=["Users"],
    response_model=StatusCode,
    summary="Delete user",
    status_code=status.HTTP_200_OK,
    responses=add_error_responses([404]),
)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> StatusCode:
    """Deletes the admin user during testing"""
    crud.users.remove(db=db, _id=user_id)
    return {"status_code": status.HTTP_200_OK}
