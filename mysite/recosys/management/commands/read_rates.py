from django.core.management.base import BaseCommand, CommandError
from recosys.models import User
from recosys.models import Movie

# -*- coding: utf_8 -*-
from itertools import islice
import time

class Command(BaseCommand):
    args = "<file>"
    help = "Add Users from a text file"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')
        n = 10000
        n_comments = 0
        rate_list = args[0]
        start_time = time.time()
        with open(rate_list) as f:
            while True:
                next_n_lines = list(islice(f,n))
                if not next_n_lines:
                    break
                for line in next_n_lines:
                    n_comments += 1
                    user_id,movie_id,rate = line.split()
                    rate = float(rate)
                    try:
                        user = User.objects.get(index=user_id)
                    except User.DoesNotExist:
                        self.stderr.write("User %s does not exist" % user_id)
                        continue
                    try: 
                        movie = Movie.objects.get(index=movie_id)
                    except Movie.DoesNotExist:
                        self.stderr.write("Movie %s does not exist" % movie_id)
                        continue
                    user.rated = dict([(movie_id,rate)])
                    user.watched.add(movie)
                    user.save()
                    movie.watched_users += 1
                    movie.avg_rate2 = (movie.avg_rate2*(movie.watched_users-1)+\
                                       rate)/movie.watched_users
                    movie.save()

        self.stdout.write('Successfully added %d rates' % n_comments)
        self.stdout.write('time takes: %s seconds' % (time.time()-start_time))
