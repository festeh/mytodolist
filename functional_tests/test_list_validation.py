import unittest

from functional_tests.base import FunctionalTest


class TaskValidationTest(FunctionalTest):

    def test_cannot_add_empty_task(self):
        # I'm misclicking Enter with empty field

        # No task is added, warning is shown

        # I'm correcting myself this time and add vaild task, which is shown

        # Then I again misclick and nothing happens, except for warning

        # TODO: finish test
        self.fail("TBD")