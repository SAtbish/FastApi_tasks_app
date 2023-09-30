from typing import Annotated
from fastapi import Depends
from src.utils.unitofwork import IUnitOfWork, UnitOfWork
from src.utils.user_authorization import user_authorization_wrapper

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
AuthorizationDep = Annotated[dict, Depends(user_authorization_wrapper())]
