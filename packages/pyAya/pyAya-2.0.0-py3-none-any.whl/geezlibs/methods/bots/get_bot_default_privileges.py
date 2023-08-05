#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

import geezlibs
from geezlibs import raw
from geezlibs import types


class GetBotDefaultPrivileges:
    async def get_bot_default_privileges(
        self: "geezlibs.Client",
        for_channels: bool = None
    ) -> Optional["types.ChatPrivileges"]:
        """Get the current default privileges of the bot.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            for_channels (``bool``, *optional*):
                Pass True to get default privileges of the bot in channels. Otherwise, default privileges of the bot
                for groups and supergroups will be returned.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                privileges = await app.get_bot_default_privileges()
        """

        bot_info = await self.invoke(
            raw.functions.users.GetFullUser(
                id=raw.types.InputUserSelf()
            )
        )

        field = "bot_broadcast_admin_rights" if for_channels else "bot_group_admin_rights"

        admin_rights = getattr(bot_info.full_user, field)

        return types.ChatPrivileges._parse(admin_rights) if admin_rights else None
