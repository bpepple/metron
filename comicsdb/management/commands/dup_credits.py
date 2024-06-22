from django.core.management.base import BaseCommand

from comicsdb.models import Credits, Issue, Role


class Command(BaseCommand):
    """
    Duplicate issue credits for an issue to other issues.

    Explanation:
    - Retrieves base credits from a specified issue and duplicates them to other target issues.
    - Skips adding possible variant cover credits and adds new credits to target issues with
      the same creator and roles.

    Args:
    - parser: The parser for command-line arguments.
    - args: Additional command-line arguments.
    - options: Key-value pairs of command-line options.

    Returns:
    - None.

    Raises:
    - Does not raise any exceptions.

    Examples:
    - To duplicate credits from issue with ID 123 to issues with IDs 456 and 789:
        python manage.py dup_credits --from 123 --to 456 789
    """

    help = "Duplicate issue credits issue to other issues"

    def add_arguments(self, parser):
        """
        Add arguments to the parser.

        Explanation:
        - Adds command-line arguments for specifying the source issue ID and target issue IDs.

        Args:
        - parser: The parser to which arguments are added.

        Returns:
        - None.
        """

        parser.add_argument("--from", type=int, required=True)
        parser.add_argument("--to", nargs="+", type=int, required=True)

    def handle(self, *args, **options):
        """
        Handle duplicating issue credits to other issues.

        Explanation:
        - Duplicates credits from a specified issue to other target issues, skipping possible
          variant cover credits.

        Args:
        - args: Additional command-line arguments.
        - options: Key-value pairs of command-line options.

        Returns:
        - None.

        Raises:
        - Does not raise any exceptions.
        """
        max_credits = 2
        base_credits = Credits.objects.filter(issue__id=options["from"])
        cover = Role.objects.get(name="Cover")
        target_issues = []
        for target_issue in options["to"]:
            issue = Issue.objects.get(pk=target_issue)
            target_issues.append(issue)

        for issue in target_issues:
            for credit in base_credits:
                # Check if credit is possible variant cover, and if so let's slip it.
                roles = credit.role.all()
                if len(roles) < max_credits and cover in roles:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Not adding possible variant cover credit for '{credit.creator}'"
                        )
                    )
                    continue

                new_credit, create = Credits.objects.get_or_create(
                    issue=issue, creator=credit.creator
                )
                if create:
                    for role in roles:
                        new_credit.role.add(role)
                    self.stdout.write(self.style.SUCCESS(f"Added: '{new_credit}'"))
