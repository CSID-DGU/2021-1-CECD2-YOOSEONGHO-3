import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "jangoback.settings")

django.setup()
from welfare.models import Welfare


if __name__=='__main__':
    test=Welfare.objects.filter(domain='교육').count()
    print(test)