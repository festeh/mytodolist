from django.core.exceptions import ValidationError
from django.forms import TextInput, ModelForm

from lists.models import Task, List

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


class NewListTaskForm(TaskForm):
    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_task_text=self.cleaned_data["text"], owner=owner)
        else:
            return List.create_new(first_task_text=self.cleaned_data["text"])


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
