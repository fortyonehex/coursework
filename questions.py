import json

# Question class -- represents a singular question
# We assume all text is in UTF-8
class Question():
    def __init__(self, question_name, question_options, correct_answer, correct_answer_index):
        # check that all inputs are valid
        # i.e. question_name, correct_answer --> str,
        #      question_options              --> list(str),
        #      correct_answer_index          --> int
        assert type(question_name) == str
        assert type(question_options) == list
        assert [type(i) for i in question_options] == [str]*len(question_options)
        assert type(correct_answer) == str
        assert type(correct_answer_index) == int
        assert 0 <= correct_answer_index < len(question_options)

        self.name = question_name
        self.options = question_options
        self.correct = correct_answer
        self.correct_index = correct_answer_index
    
    # allow for the response or an index to be passed
    # to check if it is correct
    def correct(self, response):
        assert type(response) in [str, int]
        if type(response) == int:
            assert 0 <= response < len(self.options)
            return response == self.correct_index
        else:
            assert response in self.options
            return response == self.correct

    def __repr__(self):
        return "<Question name={} options={} ans={}>".format(self.name, self.options, self.correct)
    
# Questions class -- represents a collection of questions
# might be OOP bloat, but who cares
class QuestionGroup():
    def __init__(self, questions_object, name, instructions):
        # check that questions_object --> list(dict)
        assert type(questions_object) == list
        assert [type(i) for i in questions_object] == [dict]*len(questions_object)

        self.name = name
        self.instructions = instructions
        self._store = []
        for qn in questions_object:
            self._store.append(Question(qn["question"], qn["options"], qn["options"][qn["answer"]], qn["answer"]))
        
    def __len__(self):
        return len(self._store)

    def __getitem__(self, key):
        return self._store[key]
    
    def __iter__(self):
        return self._store

    def __repr__(self):
        return "<QuestionGroup len={}>".format(self.__len__())

# Passage class -- for reading comprehension questions with passage
# definitely OOP bloat
class PassageGroup(QuestionGroup):
    def __init__(self, questions_object, name, instructions, passage_text):
        assert type(passage_text) == str
        super().__init__(questions_object, name, instructions)

        self.text = passage_text
    
    def __repr__(self):
        return "<PassageGroup len={} passage_len={}>".format(self.__len__(), len(self.text))

def parse_qn_data(filename):
    with open(filename, "r") as jsonfile:
        raw = json.load(jsonfile)
    
    raw = raw["data"]
    processed = []
    for raw_entry in raw:
        entry = {}
        entry["language"] = raw_entry["language"]
        entry["stream"] = raw_entry["stream"]
        entry["grade"] = raw_entry["grade"]
        entry["sections"] = []
        for section in raw_entry["sections"]:
            if section["type"] == "passage":
                entry["sections"].append(PassageGroup(section["questions"], section["name"], section["instructions"], section["passage"]))
            elif section["type"] == "single":
                entry["sections"].append(QuestionGroup(section["questions"], section["name"], section["instructions"]))
            else:
                raise ValueError
        processed.append(entry)
    
    return processed