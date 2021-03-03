import json
from engine.game_env import Game

def main():
    with open("./engine/data/config.json", "r") as config:
        cfg = json.load(config)
        g = Game(cfg)
    g.run()

if __name__ == "__main__":
    main()
    
