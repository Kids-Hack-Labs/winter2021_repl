import csv
import json

class SceneManager():
    instance = None
    class __SceneManager():
        is_init = False
        SCENE_TYPES = ()
        current_scene_index = 0
        def __init__(self):
            self.question_data = []
            self.layout_data = None
            with open("./engine/data/scene_types.csv", newline="") as types:
                t_reader = csv.reader(types)
                temp = []
                for row in t_reader:
                    temp.extend(row)
                SceneManager.__SceneManager.SCENE_TYPES = tuple(temp)
            with open("./src/data/questions.csv", newline="") as questions,\
                 open("./src/data/scene_data.json") as scene_info:
                q_reader = csv.reader(questions)
                self.question_data.extend([row for row in q_reader])
                self.layout_data = json.load(scene_info)
            SceneManager.__SceneManager.is_init = self.question_data[0] != [] and\
                                                  self.layout_data != {}
            
        def get_init(self):
            return SceneManager.instance.is_init

        def request_scene_data(self, index, scene_type):
            if scene_type not in SceneManager.instance.SCENE_TYPES:
                raise ValueError("Unknown scene type")
            elif scene_type == SceneManager.instance.SCENE_TYPES[0]:
                temp = {"question":"QUIZ START","next":"NEXT"}
                return (temp, self.layout_data[scene_type])
            elif scene_type == SceneManager.instance.SCENE_TYPES[1]:
                if index >= len(self.question_data):
                    raise IndexError("Question line index out of range")
                else:
                    temp = {"question"  :self.question_data[index][0],
                            "answer1"   :self.question_data[index][1],
                            "answer2"   :self.question_data[index][2],
                            "answer3"   :self.question_data[index][3],
                            "answer4"   :self.question_data[index][4],
                            "timer"     :int(self.question_data[index][5])*1000,
                            "correct"   :int(self.question_data[index][6]),
                            "next"      :"NEXT"
                           }
                    return(temp, self.layout_data[scene_type])
            else:
                return({"question":"END"}, self.layout_data[scene_type])

        def next_scene(self):
            if SceneManager.instance.current_scene_index < len(self.question_data):
                SceneManager.instance.current_scene_index += 1
                return self.request_scene_data(SceneManager.instance.current_scene_index-1,
                                               SceneManager.instance.SCENE_TYPES[1])
            else:
                return self.request_scene_data({}, SceneManager.instance.SCENE_TYPES[2])

    def __init__(self):
        if not SceneManager.instance:
            SceneManager.instance = SceneManager.__SceneManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)
