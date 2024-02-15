from questions import *

class BaseQuiz():
    def __init__(self, sections):
        assert type(sections) == list
        for section in sections:
            assert type(section) in [QuestionGroup, PassageGroup]
        
        self.sections = sections
        self.len = len(sections)
        self.curr_section = 0
        self.curr_mark = 0
        self.total_mark = sum(len(i) for i in sections)
        self.responses = []
        self.individual_grade = []
    
    def this_section(self):
        return self.sections[self.curr_section]

    def next_section(self):
        self.curr_section += 1
        if self.curr_section >= self.len:
            return None
        else:
            return self.sections[self.curr_section]

    # answers will be a list of indexes for the section
    def grade_section(self, answers):
        assert type(answers) == list
        assert len(self.sections[self.curr_section]) == len(answers)
        assert [type(i) for i in answers] == [int]*len(answers)

        self.responses += answers
        curr_section = self.sections[self.curr_section]
        score = 0
        for i in range(len(answers)):
            mark = int(curr_section[i].validate(answers[i]))
            score += mark
            self.individual_grade.append(mark)
        return score

# incomplete
"""
class AbilityQuiz():
    # questions passed should be in the format [{grade: x, questions: QuestionGroup/PassageGroup}]
    def __init__(self, questions):
        assert type(questions) == list
        for q in questions:
            assert type(q) == dict
            assert type(q["grade"]) == int
            assert type(q["questions"]) == list
            for qn in q["questions"]:
                assert type(qn) in [QuestionGroup, PassageGroup]

        self.questions = {}
        for q in questions:
            if q["grade"] not in self.questions:
                self.questions[q["grade"]] = q["questions"]
            else:
                self.questions[q["grade"]] += q["questions"]
        
        self.curr_level = None

    def this_section(self):
        

    def next_section(self):
        pass

    # MUST be called before
    def grade_section(self, answers):
        pass
"""