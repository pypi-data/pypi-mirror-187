# Copyright (c) 2023-present staciax
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.
from __future__ import annotations

from enum import Enum
from datetime import datetime
from typing import Tuple, TypeVar

__all__: Tuple[str, ...] = ('AppRoleConnectionMetadataRecordType', 'OAuth2Scopes')

T = TypeVar('T')


class AppRoleConnectionMetadataRecordType(int, Enum):
    interger_less_than_or_equal = 1
    interger_greater_than_or_equal = 2
    interger_equal = 3
    interger_not_equal = 4
    datetime_less_than_or_equal = 5
    datetime_greater_than_or_equal = 6
    boolean_equal = 7
    boolean_not_equal = 8
    int = interger_equal
    bool = boolean_equal

    def __int__(self):
        return self.value

    @property
    def data_type(self) -> T:
        if self.value <= 4:
            return int
        elif self.value <= 6:
            return datetime
        elif self.value <= 8:
            return bool


class OAuth2Scopes(str, Enum):
    email = 'email'
    guilds = 'guilds'
    identify = 'identify'
    role_connection_write = 'role_connections.write'
    # https://discord.com/developers/docs/topics/oauth2
