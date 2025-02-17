import random
import pickle


class Map():
    def __init__(self, width, height, room_number, room_width, room_height, max_doors):
        self.width = width
        self.height = height
        self.room_number = room_number
        self.room_width = room_width
        self.room_height = room_height
        self.max_doors = max_doors
        self.map = [[{"tile": 'void'} for x in range(width)] for y in range(height)]
        self.room_dictionary = {}
        self.generate_rooms()
        self.generate_corridors()

    def generate_rooms(self):
        current_room_number = 0
        while current_room_number < self.room_number:
            # Random size
            while True:
                room_width = random.randint(3, self.room_width)
                room_height = random.randint(3, self.room_height)
                if abs(room_width-room_height) < 4:
                    break
            # Random coordinate
            x = random.randint(1, self.width-1-room_width)
            y = random.randint(1, self.height-1-room_height)
            # Check space for room
            valid = True
            for y_check in range(room_height+2):
                for x_check in range(room_width+2):
                    if self.map[y+y_check-1][x+x_check-1]["tile"] == 'floor':
                        valid = False
            if not valid:
                continue
            current_room_number += 1
            # Build walls
            for y_build in range(room_height+2):
                for x_build in range(room_width+2):
                    self.map[y+y_build-1][x+x_build-1]["tile"] = 'wall'
            # Build floors
            for y_build in range(room_height):
                for x_build in range(room_width):
                    self.map[y+y_build][x+x_build]["tile"] = 'floor'
            # Add room to dictionary with its center coordinates
            self.room_dictionary.update({f"room{current_room_number}":{"center":[y+(room_height//2), x+(room_width//2)]}})

    def generate_corridors(self):
        # Find room closest to top left corner of the map for rhe first corridor
        # Then the main_room will be the previous room
        main_room = "room1"
        for room in self.room_dictionary.keys():
            if (self.room_dictionary[main_room]["center"][0] + self.room_dictionary[main_room]["center"][1]) > \
                    (self.room_dictionary[room]["center"][0] + self.room_dictionary[room]["center"][1]):
                main_room = room
        connected_rooms = []
        for i in range(self.room_number-1):
            connected_rooms.append(main_room)
            # Find room closest to main room
            secondary_room = "room1"
            for room in self.room_dictionary.keys():
                if room in connected_rooms:
                    continue
                distance1 = abs(self.room_dictionary[main_room]["center"][0]-self.room_dictionary[secondary_room]["center"][0])+\
                    abs(self.room_dictionary[main_room]["center"][1]-self.room_dictionary[secondary_room]["center"][1])
                distance2 = abs(
                    self.room_dictionary[main_room]["center"][0] - self.room_dictionary[room]["center"][0]) + \
                            abs(self.room_dictionary[main_room]["center"][1] -
                                self.room_dictionary[room]["center"][1])
                if secondary_room in connected_rooms:
                    secondary_room = room
                if distance1 == 0:   # Distance 1 is distance from already chosen secondary room to the main room
                    secondary_room = room
                if distance2 < distance1:
                    secondary_room = room

            # Build corridor
            doors_built = 0
            for x_build in range(min(self.room_dictionary[main_room]["center"][1], self.room_dictionary[secondary_room]["center"][1]),
                                 max(self.room_dictionary[main_room]["center"][1], self.room_dictionary[secondary_room]["center"][1])):
                if self.map[self.room_dictionary[main_room]["center"][0]][x_build]["tile"] == "wall" and doors_built < self.max_doors and\
                        self.map[self.room_dictionary[main_room]["center"][0]+1][x_build]["tile"] == "wall" and\
                        self.map[self.room_dictionary[main_room]["center"][0]-1][x_build]["tile"] == "wall":
                    self.map[self.room_dictionary[main_room]["center"][0]][x_build]["tile"] = "door"
                    doors_built += 1
                    print("door built")
                else:
                    self.map[self.room_dictionary[main_room]["center"][0]][x_build]["tile"] = "floor"
                if self.map[self.room_dictionary[main_room]["center"][0]+1][x_build]["tile"] == "void":
                    self.map[self.room_dictionary[main_room]["center"][0] + 1][x_build]["tile"] = "wall"
                if self.map[self.room_dictionary[main_room]["center"][0]-1][x_build]["tile"] == "void":
                    self.map[self.room_dictionary[main_room]["center"][0] - 1][x_build]["tile"] = "wall"
            for y_build in range(
                    min(self.room_dictionary[main_room]["center"][0], self.room_dictionary[secondary_room]["center"][0]),
                    max(self.room_dictionary[main_room]["center"][0], self.room_dictionary[secondary_room]["center"][0])+1):
                if self.map[y_build][self.room_dictionary[secondary_room]["center"][1]]["tile"] == "wall" and\
                        doors_built < self.max_doors and\
                        self.map[y_build][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] == "wall" and\
                        self.map[y_build][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] == "wall":
                    self.map[y_build][self.room_dictionary[secondary_room]["center"][1]]["tile"] = "door"
                    doors_built += 1
                    print("door built")
                else:
                    self.map[y_build][self.room_dictionary[secondary_room]["center"][1]]["tile"] = "floor"
                # building the walls
                if self.map[y_build][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] == "void":
                    self.map[y_build][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] = "wall"
                if self.map[y_build][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] == "void":
                    self.map[y_build][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] = "wall"
                if self.map[y_build-1][self.room_dictionary[secondary_room]["center"][1]]["tile"] == "void":
                    self.map[y_build-1][self.room_dictionary[secondary_room]["center"][1]]["tile"] = "wall"
                if self.map[y_build+1][self.room_dictionary[secondary_room]["center"][1]]["tile"] == "void":
                    self.map[y_build+1][self.room_dictionary[secondary_room]["center"][1]]["tile"] = "wall"
                if self.map[y_build-1][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] == "void":
                    self.map[y_build-1][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] = "wall"
                if self.map[y_build-1][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] == "void":
                    self.map[y_build-1][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] = "wall"
                if self.map[y_build+1][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] == "void":
                    self.map[y_build+1][self.room_dictionary[secondary_room]["center"][1]-1]["tile"] = "wall"
                if self.map[y_build+1][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] == "void":
                    self.map[y_build+1][self.room_dictionary[secondary_room]["center"][1]+1]["tile"] = "wall"

            print(f"{main_room} connected to {secondary_room}")
            main_room = secondary_room

        connected_rooms.append(main_room)
        print(*sorted(connected_rooms))

    def save_map(self):
        with open("map_data1.pkl", "wb") as file:
            pickle.dump(self.map, file)
            print("Map saved to 'map_data1.pkl'")
