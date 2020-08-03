from telegram import ChatPermissions

initial_permission = ChatPermissions(can_send_messages=False)
standard_permissions = ChatPermissions(can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False)