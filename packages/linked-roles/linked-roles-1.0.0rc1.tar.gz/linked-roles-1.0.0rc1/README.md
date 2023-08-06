<h3 align="center">
	Discord Linked Roles OAuth2
</h3>
<h5 align="center">
  A basic wrapper for the Discord Linked Roles OAuth2 API.
</h5>

<p align="center">
    <img alt="Releases" src="https://img.shields.io/github/release/staciax/discord-linked-roles.svg?style=for-the-badge&logo=github&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"/></a>
	<a href="https://github.com/staciax/discord-linked-roles/stargazers"><img src="https://img.shields.io/github/stars/staciax/discord-linked-roles?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
	<a href="https://github.com/staciax/discord-linked-roles/issues"><img src="https://img.shields.io/github/issues/staciax/discord-linked-roles?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
	<a href="https://github.com/staciax/discord-linked-roles/contributors"><img src="https://img.shields.io/github/contributors/staciax/discord-linked-roles?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
</p>

<!-- https://github.com/catppuccin color style -->

## Installation:
```sh
pip install linked-roles
```

## FastAPI Examples:
```py
import logging

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

import config
from linked_roles import LinkedRolesOAuth2, OAuth2Scopes, RolePlatform, Unauthorized, NotFound

_log = logging.getLogger(__name__)

app = FastAPI(title='Linked Roles OAuth2')

client = LinkedRolesOAuth2(
    client_id=config.DISCORD_CLIENT_ID,
    client_secret=config.DISCORD_CLIENT_SECRET,
    redirect_uri=config.DISCORD_REDIRECT_URI,
    # token=config.DISCORD_TOKEN, # Optinal for Resgister
    scopes=(OAuth2Scopes.role_connection_write, OAuth2Scopes.identify),
    state=config.COOKIE_SECRET,
)


@app.on_event('startup')
async def startup():
    await client.start()
    _log.info('Startup complete')


@app.on_event('shutdown')
async def shutdown():
    await client.close()
    _log.info('Shutdown complete')


@app.get('/linked-role', status_code=status.HTTP_302_FOUND)
async def linked_roles():
    url = client.get_oauth_url()
    return RedirectResponse(url=url)


@app.get('/verified-role')
async def verified_role(code: str):

    tokens = await client.get_oauth2_tokens(code)
    user = await client.fetch_user(tokens=tokens)

    platform = RolePlatform(name='VALORANT', username='STACIA#1234')
    platform.edit_metadata(key='matches', value=50)
    platform.edit_metadata(key='winrate', value=25)
    platform.edit_metadata(key='combat_score', value=5)
    platform.edit_metadata(key='last_update', value=datetime.datetime.now())
    platform.edit_metadata(key='verified', value=False)


    await user.edit_role_metadata(platform=platform)

    return 'Verified role successfully'

@app.post('/update-role-metadata')
async def update_role_metadata(user_id: int):

    user = client.get_user(id=user_id)

    if user is None:
        raise NotFound(f'User with ID {user_id} not found')

    tokens = user.get_tokens()
    if tokens is None:
        raise Unauthorized('User is not connected to Linked Roles')

    if tokens.is_expired():
        await tokens.refresh()

    platform = user.get_role_platform()
    platform = RolePlatform(name='VALORANT', username='STACIA#1234')
    platform.edit_metadata(key='matches', value=100)
    platform.edit_metadata(key='winrate', value=50)
    platform.edit_metadata(key='combat_score', value=10)
    platform.edit_metadata(key='last_update', value=datetime.datetime.now())
    platform.edit_metadata(key='verified', value=True)


    await user.edit_role_metadata(platform=platform)
```

# Register Examples:
```py
import asyncio

import config
from linked_roles import AppRoleConnectionMetadataRecordType as RoleMetadataType, LinkedRolesOAuth2, RoleMetadataRecord


async def main():

    client = LinkedRolesOAuth2(client_id=config.DISCORD_CLIENT_ID, token=config.DISCORD_TOKEN)

    async with client:

        records = (
            RoleMetadataRecord(
                key='matches',
                name='Matches',
                description='Number of matches this season',
                type=2,
            ),
            RoleMetadataRecord(
                key='winrate',
                name='Win Rate',
                description='Win rate this season',
                type=RoleMetadataType.interger_greater_than_or_equal,
            ),
            RoleMetadataRecord(
                key='combat_score',
                name='Combat Score',
                description='Combat score this season',
                type=RoleMetadataType.interger_greater_than_or_equal,
            ),
            RoleMetadataRecord(
                key='last_update',
                name='Last Update',
                description='Last time this data was updated',
                type=RoleMetadataType.datetime_less_than_or_equal,
            ),
            RoleMetadataRecord(
                key='verified',
                name='Verified',
                description='Verified role',
                type=RoleMetadataType.boolean_equal,
            )
        )

        records = await client.register_role_metadata(records=records)
        print(records)


if __name__ == '__main__':
    asyncio.run(main())

```
## TODO:
- [ ] Add more examples
- [ ] Add more documentation
- [ ] Database support

## License
licensed under the [MIT license](LICENSE).

<!-- code style, inspiration is discord.py -->