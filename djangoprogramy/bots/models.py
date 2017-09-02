from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.conf import settings
from .utils import bot_directory_path

@python_2_unicode_compatible
class Bot(models.Model):

	slug = models.SlugField(
		_('Slug of Bot'), 
		blank=True, 
		max_length=255
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name=_('User'),
	)
	name = models.CharField(
		_('Name of Bot'), 
		blank=True, 
		max_length=255, 
		unique=True
	)
	port = models.PositiveSmallIntegerField(
		validators=[
		MinValueValidator(9000),
		MaxValueValidator(9999)
		],
		verbose_name=_('Name of Bot'),
	)
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('bots:bot_detail', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class Dialog(models.Model):
	
	bot = models.ForeignKey(
		'bots.Bot', 
		verbose_name=_('Bot')
	)
	name = models.CharField(
		max_length=55,
		verbose_name=_('Name of the dialog')
	)
	source = models.FileField(
		blank=True,
		verbose_name=_('Source')
	)
	aiml = models.CharField(
		verbose_name=_('AIML'),
		max_length=5000
	)

	def save(self, *args, **kwargs):
		if not self.source:
			file_path = bot_directory_path(self.bot.slug, self.name)
			new_file = open(file_path, 'w+')
			new_file.write(self.aiml)
			new_file = File(new_file)
			os.remove(file_path)
			self.source = new_file
		return super(Dialog, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('bots:dialog_detail', kwargs={'slug': self.slug})