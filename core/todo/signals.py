from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, TaskActivity
from django.db.models.signals import pre_save

# Temporary place to store previous values
_pre_save_instance_cache = {}

@receiver(pre_save, sender=Task)
def cache_old_instance(sender, instance, **kwargs):
    if instance.pk:
        try:
            _pre_save_instance_cache[instance.pk] = Task.objects.get(pk=instance.pk)
        except Task.DoesNotExist:
            pass

@receiver(post_save, sender=Task)
def log_task_activity(sender, instance, created, **kwargs):
    from .signals import _pre_save_instance_cache

    if created:
        TaskActivity.objects.create(
            task=instance,
            user=instance.user,
            action="Created",
            changes={"message": "Task created."}
        )
    else:
        old_instance = _pre_save_instance_cache.pop(instance.pk, None)
        if not old_instance:
            return

        field_labels = {
            "title": "Title",
            "description": "Description",
            "priority": "Priority",
            "deadline": "Deadline",
            "status": "Status",
            "is_completed": "Completion",
            "category": "Category" 
        }

        def display_value(val):
            if hasattr(val, 'strftime'):
                return val.strftime('%Y-%m-%d %H:%M')
            elif hasattr(val, 'name'):
                return val.name  # For category or other FK objects
            return str(val).capitalize()

        messages = []
        for field in field_labels:
            old_value = getattr(old_instance, field)
            new_value = getattr(instance, field)

            if old_value != new_value:
                messages.append(
                    f"{field_labels[field]} changed from **{display_value(old_value)}** to **{display_value(new_value)}**"
                )

        if messages:
            TaskActivity.objects.create(
                task=instance,
                user=instance.user,
                action="Updated",
                changes={"message": "\n".join(messages)}
            )



