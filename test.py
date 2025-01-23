import pytest
from file import AutoAdd

add = AutoAdd()
section = {
    "name": "test",
}
add.Addsection("test",section)
case = [
    {
     "title": "test_sum_two_decimals",
     "refs": "123",
     "custom_automation_id" : "New Test Case Example",
     "custom_preconds": "123",
     "custom_steps": "My test steps",
     "custom_expected": "My expected final results"
    }
    ,
    {
     "title": "test_sum_two_decimals",
     "refs": "123",
     "custom_automation_id" : "New Test Case Example",
     "custom_preconds": "123",
     "custom_steps": "My test steps",
     "custom_expected": "My expected final results"
    },
    {
     "title": "test_sum_multiple_numbers[3+5-8]",
     "refs": "123",
     "custom_automation_id" : "New Test Case Example",
     "custom_preconds": "123",
     "custom_steps": "My test steps",
     "custom_expected": "My expected final results"
    },
    {
     "title": "test_sum_multiple_numbers[2+4-6]",
     "refs": "123",
     "custom_automation_id" : "New Test Case Example",
     "custom_preconds": "123",
     "custom_steps": "My test steps",
     "custom_expected": "My expected final results"
    }
]
for i in case:
    print(add.Addcase('test','test',i))

# def test_sum_two_numbers():
#     assert 1 + 1 == 2

# def test_sum_two_decimals(record_property):
#     record_property("testrail_attachment", "sample_reports/testrail.jpg")
#     assert 0.8 + 0.3 == 1.2

# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6)])
# def test_sum_multiple_numbers(test_input, expected):
#     assert eval(test_input) == expected