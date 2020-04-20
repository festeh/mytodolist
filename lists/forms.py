from django.core.exceptions import ValidationError
from django.forms import TextInput, ModelForm

from lists.models import Task

EMPTY_TASK_ERROR = 'Cannot add an empty task'
DUPLICATING_TASK_ERROR = 'Cannot add a duplicating task'


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('text',)
        widgets = {
            'text': TextInput({
                'placeholder': 'Enter a task',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_TASK_ERROR
            }
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListTaskForm(TaskForm):
    def __init__(self, for_list, *args, **kwargs):
        super(ExistingListTaskForm, self).__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATING_TASK_ERROR]}
            self._update_errors(e)

    def save(self):
        return ModelForm.save(self)
