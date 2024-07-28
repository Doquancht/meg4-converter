
class Animation:
    def __init__(self, animations: list) -> None:
        self.animations = animations
    
    @staticmethod
    def __get_loop(loop: str) -> bool | str:
        if loop == "loop" or loop == "once":
            return True
        elif loop == "hold":
            return "hold_on_last_frame"

    @staticmethod
    def __get_datapoint(datapoint: dict) -> list:
        return [float(datapoint["x"]), float(datapoint["y"]), float(datapoint["z"])] if all(a in datapoint for a in ("x", "y", "z")) else None

    @staticmethod
    def __get_animator(animators: dict) -> dict:
        bedrock_animators = {}
        for _, animator in animators.items():
            if not animator["name"] in bedrock_animators:
                bedrock_animators[animator["name"]] = {}
            for keyframe in animator["keyframes"]:
                if not keyframe["channel"] in bedrock_animators[animator["name"]]:
                    bedrock_animators[animator["name"]][keyframe["channel"]] = {}
                bedrock_animators[animator["name"]][keyframe["channel"]][str(float(keyframe["time"]))] = Animation.__get_datapoint(keyframe["data_points"][0])
        return bedrock_animators

    def to_bedrock(self) -> None:
        data = {"format_version": "1.8.0","animations": {}}
        for animation in self.animations:
            data["animations"][animation["name"]] = {
                "loop": Animation.__get_loop(animation["loop"]),
                "animation_length": animation.get("length"),
                "anim_time_update": animation.get("anim_time_update"),
                "blend_weight": animation.get("blend_weight"),
                "start_delay": animation.get("start_delay"),
                "loop_delay": animation.get("loop_delay"),
                "bones": Animation.__get_animator(animation.get("animators", {}))
            }
        return data
            
