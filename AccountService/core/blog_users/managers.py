from .schemas import *
from .models import *
from common.enums import AccountRole
from core.accounts.managers import AccountManager
from core.accounts.exceptions import *
from tortoise.exceptions import DoesNotExist
from uuid import UUID
from typing import List
from common.file_manager import *
from common.exceptions import InvalidFileExtension
from fastapi import UploadFile


class BlogUserManager:
    
    async def create(self, data: BlogUserCreateSchema, role: AccountRole = AccountRole.STANDARD) -> BlogUser:
        try:
            account = await AccountManager().register_account(data, role)
        except CredentialsAlreadyTaken as e:
            raise e
        
        return await BlogUser.create(account=account, **data.dict())
    
    async def get(self, id: UUID) -> BlogUser:
        try:
            instance = await BlogUser.get(account__id=id)
        except DoesNotExist:
            raise AccountNotFound()
        await instance.fetch_related('account')
        return instance
    
    async def edit(self, instance: BlogUser, data: BlogUserEditSchema) -> BlogUser:
        try:
            await AccountManager().edit_account(instance.account, data)
        except CredentialsAlreadyTaken as e:
            raise e
        
        if data.bio:
            instance.bio = data.bio
            
        await instance.save()
        return instance
    
    async def get_list(self, filters: dict = dict()) -> List[BlogUser]:
        return await BlogUser.filter(**filters).prefetch_related('account')
    
    async def save_profile_picture(self, instance: BlogUser, picture: UploadFile) -> str:
        try:
            path, url = FileManager().upload_file(
                picture, instance.account.id, 'profile_pics', ['jpg', 'png', 'jpeg'])
        except InvalidFileExtension as e:
            raise e
        
        instance.picture_path = path
        instance.picture_url = url
        await instance.save()
        return url
        
    async def delete_profile_picture(self, instance: BlogUser) -> None:
        if instance.picture_path:
            FileManager().delete_file(instance.picture_path)
        instance.picture_path = None
        instance.picture_url = None
        await instance.save()