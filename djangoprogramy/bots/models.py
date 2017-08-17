from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify


@python_2_unicode_compatible
class Bot(models.Model):

	# First Name and Last Name do not cover name patterns
	# around the globe.
	slug = models.SlugField(_('Slug of Bot'), blank=True, max_length=255)
	name = models.CharField(_('Name of Bot'), blank=True, max_length=255)
	port = models.PositiveSmallIntegerField(
		validators=[
		MinValueValidator(9000),
		MaxValueValidator(9999)
		])

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('bots:detail', kwargs={'slug': self.slug})