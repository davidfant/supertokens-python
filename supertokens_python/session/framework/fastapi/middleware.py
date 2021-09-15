"""
Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.

This software is licensed under the Apache License, Version 2.0 (the
"License") as published by the Apache Software Foundation.

You may not use this file except in compliance with the License. You may
obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""
from typing import Union

from supertokens_python.normalised_url_path import NormalisedURLPath
from supertokens_python.session import SessionRecipe, Session
from supertokens_python.utils import FRAMEWORKS, normalise_http_method


def verify_session(recipe: SessionRecipe, anti_csrf_check: Union[bool, None] = None, session_required: bool = True):
    from fastapi.requests import Request
    async def func(request: Request) -> Union[Session, None]:
        if not hasattr(request, 'wrapper_used') or not request.wrapper_used:
            request = FRAMEWORKS[recipe.app_info.framework].wrap_request(request)
        method = normalise_http_method(request.method())
        if method == 'options' or method == 'trace':
            return None
        incoming_path = NormalisedURLPath(recipe, request.get_path())
        refresh_token_path = recipe.config.refresh_token_path
        if incoming_path.equals(refresh_token_path) and method == 'post':
            session = await recipe.refresh_session(request)
        else:
            session = await recipe.get_session(request, anti_csrf_check, session_required)

        request.set_session(session)
        return request.get_session()

    return func
