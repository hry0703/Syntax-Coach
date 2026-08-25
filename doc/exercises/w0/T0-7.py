
import json
from pathlib import Path


def load_scenes(path: str) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_scene_by_id(scenes:list[dict[str,str]],id:str)->dict[str,str] | None:
    for scene in scenes:
        if scene["id"] == id:
            return scene
    return None

if __name__ == "__main__":
    data_file = Path(__file__).resolve().parents[3] / "backend" / "data" / "scenes.json"
    scenes = load_scenes(str(data_file))
    print(get_scene_by_id(scenes, "coffee_shop"))