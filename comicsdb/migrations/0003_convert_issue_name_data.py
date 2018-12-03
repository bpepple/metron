from django.db import migrations

def change_to_array(apps, schema_editor):
    Issue = apps.get_model('comicsdb', 'Issue')
    for i in Issue.objects.all():
        story = []
        story.append(i.name)
        i.tmp_name = story
        i.save()

class Migration(migrations.Migration):

    dependencies = [
        ('comicsdb', '0002_add_issue_arrayfield'),
    ]

    operations = [
        migrations.RunPython(change_to_array),
    ]