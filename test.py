from questions import *
from quiz import *

# proof of concept
qnd = parse_qn_data("format.json")
qni = QuizInterface(qnd[0]["sections"])
print(qni.grade_section([2, 3, 3]))
print(qni.individual_grade)
qni.next_section()
print(qni.grade_section([2, 3, 3]))
print(qni.individual_grade)
print(qni.curr_mark)