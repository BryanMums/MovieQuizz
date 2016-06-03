import pytest
import random
import codecs
import json
import os


@pytest.fixture()
def questions_file_exists():
    """Test whether the question file exists or not"""
    assert os.path.exists("../moviequizz/ressources/questions.json")

def test_questions_are_valid(questions_file_exists):
    """Test if questions are valid (interrogation mark)"""
    json_data = codecs.open("../moviequizz/ressources/questions.json", "r", "utf-8")
    questions =  json.load(json_data)  # Read the json questions file and create a dict

    questionIntegrity = True

    for q in questions:
        if "?" not in q["question"]:
            questionIntegrity = False

    assert questionIntegrity == True


def test_bad_answers_are_valid(questions_file_exists):
    """Test if the good answer is valid (there are two answers)."""
    json_data = codecs.open("../moviequizz/ressources/questions.json", "r", "utf-8")
    questions = json.load(json_data)  # Read the json questions file and create a dict

    answersIntegrity = True

    for q in questions:
        if len(q["badAnswers"]) != 2:
            answersIntegrity = False

    assert answersIntegrity == True
