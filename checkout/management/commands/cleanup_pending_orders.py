from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from checkout.models import CheckoutSubmission


class Command(BaseCommand):
    help = 'Clean up old pending/failed payment submissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Delete submissions older than this many hours (default: 24)'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        # Find old unpaid submissions
        old_submissions = CheckoutSubmission.objects.filter(
            is_paid=False,
            created_at__lt=cutoff_time
        )
        
        count = old_submissions.count()
        
        if count > 0:
            old_submissions.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} old pending submission(s) '
                    f'older than {hours} hours'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No old pending submissions to clean up')
            )
