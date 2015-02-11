from django.core.management.base import BaseCommand, CommandError
from recosys.models import User

# -*- coding: utf_8 -*-
from itertools import islice

class Command(BaseCommand):
    args = "<file>"
    help = "Add Users from a text file"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')
        user_list = args[0]
        n = 10000
        counter = 0
        with open(user_list) as f:
            while True:
                next_n_lines = list(islice(f,n))
                if not next_n_lines:
                    break
                for line in next_n_lines:
                    all_iterms = line.split()
                    index = all_iterms[0]
                    if len(all_iterms) > 1:
                        name = all_iterms[1]
                    else:
                        name = "user"+str(counter)
                    q = User.objects.create_user(index, name)
                    q.save()
                    counter += 1
        self.stdout.write('Successfully added %d Users' % counter)
