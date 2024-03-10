import string
from faker import Faker

faker_instance = Faker()


class DataGenerator:
    """
    Faker for data generation
    """

    @staticmethod
    def fake_project_id():
        first_letter = faker_instance.random.choice(string.ascii_letters)
        rest_characters = "".join(faker_instance.random.choices(string.ascii_letters + string.digits, k=10))
        project_id = first_letter + rest_characters
        return project_id

    @staticmethod
    def fake_name():
        return faker_instance.word()

    @staticmethod
    def fake_build_id():
        first_letter = faker_instance.random.choice(string.ascii_letters)
        rest_characters = "".join(faker_instance.random.choices(string.ascii_letters + string.digits, k=10))
        build_id = first_letter + rest_characters
        return build_id

    @staticmethod
    def fake_user_email():
        return faker_instance.email()
