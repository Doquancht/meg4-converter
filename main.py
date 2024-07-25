import os
import re
import glob
import json
import base64
import shutil
from PIL import Image
from io import BytesIO
from utils.model import Model
from utils.texture import Texture
from utils.animation import Animation

shutil.rmtree("output") if os.path.exists("output") else None
os.makedirs("output")
for modelfile in glob.glob("blueprints/**/*.bbmodel", recursive=True):
    with open(modelfile, "r") as f:
        data = json.load(f)
    
    textures = {"width": 0, "height": 0, "data": {}}
    name = os.path.splitext(os.path.basename(modelfile))[0]
    os.makedirs(f"output/{name}/")

    for slot, texture in enumerate(data.get("textures", [])):
        texture_data = re.sub('^data:image/.+;base64,', '', texture["source"])
        texture_image = Image.open(BytesIO(base64.b64decode(texture_data)))
        
        #Remove Animtion Frame
        if texture.get("frame_time", 1)> 1:
            height = texture_image.height // texture["frame_time"]
            texture_image.crop(0, 0, texture_image.width, height)
        
        textures["data"][str(slot)] = {"image": texture_image,"position": textures["height"]}
        textures["width"] = max(textures["width"], texture_image.width)
        textures["height"] += texture_image.height

    if data.get("textures", None):
        model_texture = Image.new("RGBA", (textures["width"], textures["height"]))
        model_texture_height = 0
        for k, texture_img in textures["data"].items():
            model_texture.paste(texture_img["image"], (0, model_texture_height))
            model_texture_height += texture_img["image"].height
        model_texture.save(f"output/{name}/{name}.png")

    texture = Texture(model_texture, textures) if data.get("textures", None) else None
    animations = Animation(data["animations"]).to_bedrock()
    model = Model(data, texture).to_geometry_bedrock()
    with open(f"output/{name}/{name}.json", "w") as f:
        json.dump(model, f, indent=4)
    with open(f"output/{name}/animation.{name}.json", 'w') as f:
        json.dump(animations, f, indent=4)
    