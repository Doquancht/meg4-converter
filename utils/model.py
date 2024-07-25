from utils.texture import Texture

class Model:
    def __init__(self, data: dict, texture: Texture = None) -> None:
        self.elements = self.__sort_elements(data["elements"])
        self.outliner = data["outliner"]
        self.texture = texture
        self.bones = []
    
    @staticmethod
    def __get_origin(from_to: tuple[list, list]) -> list:
        origin = [-from_to[1][0], from_to[0][1], from_to[0][2]]
        return origin

    @staticmethod
    def __get_rotation(rotation: list[int]) -> list:
        if not rotation:
            return
        rotation[0] = -rotation[0]
        rotation[1] = -rotation[1]
        return rotation
    
    @staticmethod
    def __get_size(from_to: tuple[list, list]) -> list:
        return [from_to[1][i] - from_to[0][i] for i in range(3)]
    
    @staticmethod
    def __get_pivot(origin: list) -> list:
        origin[0] = -origin[0]
        return origin
    
    def __sort_elements(self, elements: list) -> dict:
        elementlist = {}
        for element in elements:
            elementlist[element["uuid"]] = element
        return elementlist

    def __get_uv(self, element) -> dict:
        return {
            "north": self.texture.get_uv("north", element["faces"]),
            "east": self.texture.get_uv("east", element["faces"]),
            "south": self.texture.get_uv("south", element["faces"]),
            "west": self.texture.get_uv("west", element["faces"]),
            "up": self.texture.get_uv("up", element["faces"]),
            "down": self.texture.get_uv("down", element["faces"])
        } if "faces" in element and self.texture else {}
    
    def __convert_element(self, element: dict = None, outliner: dict = None, parent: str = None) -> dict | None:
        if element:
            cube = {
                "rotation": Model.__get_rotation(element.get("rotation", [0, 0, 0])),
                "size": Model.__get_size((element.get("from", [0, 0, 0]), element.get("to", [0, 0, 0]))),
                "origin": Model.__get_origin((element.get("from", [0, 0, 0]), element.get("to", [0,0,0]))),
                "pivot": Model.__get_pivot(element.get("origin", [0,0,0])),
                "uv": self.__get_uv(element)
            }
            return cube if element["type"].lower() == "cube" else None
        elif outliner:
            group = {
                "name": outliner["name"],
                "pivot": Model.__get_pivot(outliner.get("origin", None)),
                "rotation": Model.__get_rotation(outliner.get("rotation", None)),
                "cubes": []
            }
            if parent:
                group["parent"] = parent
            return group

    def outliner_worker(self, bone: dict, outliners: list, parent: str = None) -> None:
        for outliner in outliners:
            if isinstance(outliner, str):
                bone["cubes"].append(self.__convert_element(self.elements[outliner]))
            elif isinstance(outliner, dict):
                group = self.__convert_element(outliner=outliner, parent=parent)
                self.outliner_worker(group, outliner.get("children", []), group["name"])
                self.bones.append(group)

    def to_geometry_bedrock(self) -> dict:
        geometry = {
            "format_version": "1.21.0",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": "geometry.meg",
                        "texture_width": self.texture.image.width if self.texture else 0,
                        "texture_height": self.texture.image.height if self.texture else 0
                     },
                    "bones": self.bones
                }
            ]
        }
        bone = {"name": "bones", "pivot": [0,0,0], "cubes": []}
        self.outliner_worker(bone, self.outliner)
        if bone["cubes"]:
            self.bones.append(bone)
        return geometry
