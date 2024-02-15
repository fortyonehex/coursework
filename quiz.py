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
class AbilityQuiz(BaseQuiz):
    def __init__(self):
        pass

    def this_section(self):
        return self.sections[self.curr_section]

    def next_section(self):
        self.curr_section += 1
        if self.curr_section >= self.len:
            return None
        else:
            return self.sections[self.curr_section]

    # MUST be called before
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