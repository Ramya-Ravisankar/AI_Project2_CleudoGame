def move_to_room(player, destination, rooms):
    for room in rooms:
        if room.name == player.position:
            if destination in [r.name for r in room.connected_rooms]:
                player.position = destination
                return True
    return False
