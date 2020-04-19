from django.forms import CharField, TextInput, ModelForm

from lists.models import Task

EMPTY_TASK_ERROR = 'Cannot add an empty task'


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
