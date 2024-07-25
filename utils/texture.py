from PIL.ImageFile import ImageFile

class Texture:
    def __init__(self, image: ImageFile, textures: dict) -> None:
        self.image = image
        self.textures = textures
    
    def get_uv(self, face_name: str, faces: dict) -> dict | None:
        face = faces.get(face_name, {})
        uv = face.get("uv", None)
        if face and uv:
            try:
                return {"uv": [uv[0], uv[1] + self.textures["data"][str(faces[face_name]["texture"])]["position"]], "uv_size": [uv[2] - uv[0], uv[3] - uv[1]]}
            except:
                return None

        
        