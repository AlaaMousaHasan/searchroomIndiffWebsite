def detect_changes(current_rooms, previous_rooms):
    """Detects added and removed rooms."""
    added_rooms = [room for room in current_rooms if room not in previous_rooms]
    removed_rooms = [room for room in previous_rooms if room not in current_rooms]
    return added_rooms, removed_rooms


def format_email_body(website_name, added_rooms, removed_rooms):
    """Formats the email body based on added and removed rooms."""
    message_body = f"Website: {website_name}\n\n"
    if added_rooms:
        if len(added_rooms) == 1:
            message_body += "1 new room has been added:\n"
        else:
            message_body += f"{len(added_rooms)} new rooms have been added:\n"
        message_body += "\n".join([f"{room['title']} - {room['link']}" for room in added_rooms])
        message_body += "\n\n"
    if removed_rooms:
        if len(removed_rooms) == 1:
            message_body += "1 room has been removed:\n"
        else:
            message_body += f"{len(removed_rooms)} rooms have been removed:\n"
        message_body += "\n".join([f"{room['title']} - {room['link']}" for room in removed_rooms])
        message_body += "\n\n"
    return message_body.strip()
