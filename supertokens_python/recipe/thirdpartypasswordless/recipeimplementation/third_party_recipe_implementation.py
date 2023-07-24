# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from supertokens_python.recipe.thirdparty.interfaces import (
    GetProviderOkResult,
    ManuallyCreateOrUpdateUserOkResult,
    RecipeInterface,
    SignInUpOkResult,
)
from supertokens_python.recipe.thirdparty.types import RawUserInfoFromProvider, User

from ..interfaces import RecipeInterface as ThirdPartyPasswordlessRecipeInterface


class RecipeImplementation(RecipeInterface):
    def __init__(self, recipe_implementation: ThirdPartyPasswordlessRecipeInterface):
        super().__init__()
        self.recipe_implementation = recipe_implementation

    async def get_user_by_id(
        self, user_id: str, user_context: Dict[str, Any]
    ) -> Union[User, None]:
        user = await self.recipe_implementation.get_user_by_id(user_id, user_context)
        if user is None or user.third_party_info is None:
            return None

        if user.email is None:
            raise Exception("Should never come here")

        return User(
            user_id=user.user_id,
            email=user.email,
            time_joined=user.time_joined,
            tenant_ids=user.tenant_ids,
            third_party_info=user.third_party_info,
        )

    async def get_users_by_email(
        self, email: str, tenant_id: str, user_context: Dict[str, Any]
    ) -> List[User]:
        users = await self.recipe_implementation.get_users_by_email(email, user_context)
        users_result: List[User] = []

        for user in users:
            if user.third_party_info is not None:
                if user.email is None:
                    raise Exception("Should never come here")

                users_result.append(
                    User(
                        user_id=user.user_id,
                        email=user.email,
                        time_joined=user.time_joined,
                        tenant_ids=user.tenant_ids,
                        third_party_info=user.third_party_info,
                    )
                )

        return users_result

    async def get_user_by_thirdparty_info(
        self,
        third_party_id: str,
        third_party_user_id: str,
        tenant_id: str,
        user_context: Dict[str, Any],
    ) -> Union[User, None]:
        user = await self.recipe_implementation.get_user_by_thirdparty_info(
            third_party_id, third_party_user_id, user_context
        )
        if user is None or user.third_party_info is None:
            return None

        if user.email is None:
            raise Exception("Should never come here")

        return User(
            user_id=user.user_id,
            email=user.email,
            time_joined=user.time_joined,
            tenant_ids=user.tenant_ids,
            third_party_info=user.third_party_info,
        )

    async def sign_in_up(
        self,
        third_party_id: str,
        third_party_user_id: str,
        email: str,
        oauth_tokens: Dict[str, Any],
        raw_user_info_from_provider: RawUserInfoFromProvider,
        tenant_id: str,
        user_context: Dict[str, Any],
    ) -> SignInUpOkResult:
        return await self.recipe_implementation.thirdparty_sign_in_up(
            third_party_id,
            third_party_user_id,
            email,
            oauth_tokens,
            raw_user_info_from_provider,
            user_context,
        )

    async def manually_create_or_update_user(
        self,
        third_party_id: str,
        third_party_user_id: str,
        email: str,
        tenant_id: str,
        user_context: Dict[str, Any],
    ) -> ManuallyCreateOrUpdateUserOkResult:
        return (
            await self.recipe_implementation.thirdparty_manually_create_or_update_user(
                third_party_id, third_party_user_id, email, user_context
            )
        )

    async def get_provider(
        self,
        third_party_id: str,
        client_type: Optional[str],
        tenant_id: str,
        user_context: Dict[str, Any],
    ) -> GetProviderOkResult:
        return await self.recipe_implementation.thirdparty_get_provider(
            third_party_id, tenant_id, client_type, user_context
        )
