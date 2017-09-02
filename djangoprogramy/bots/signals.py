from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import Bot, Dialog
from .utils import generate_bot, run_client


@receiver(post_save, sender=Bot)
def schedule_task(sender, instance, created, **kwargs):
	if created:
		generate_bot(
			{
			'slug': instance.slug,
			'port': instance.port
			}
		)
	else:
		run_client(instance.slug)


@receiver(post_save, sender=Dialog)
def schedule_task(sender, instance, created, **kwargs):
	run_client(instance.slug)