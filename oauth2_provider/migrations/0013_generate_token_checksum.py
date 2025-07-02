import oauth2_provider
import oauth2_provider.models as oa
from django.db import migrations, models
from oauth2_provider.settings import oauth2_settings

def forwards_func(apps, schema_editor):
    """
    Forward migration touches every "old" accesstoken.token which will cause the checksum to be computed.
    """
    AccessToken = apps.get_model(oauth2_settings.ACCESS_TOKEN_MODEL)
    print(f"DEBUG: AccessToken model : {oauth2_settings.ACCESS_TOKEN_MODEL}")
    print(f"DEBUG: AccessToken model fields: {[f.name for f in AccessToken._meta.get_fields() if f.concrete]}")
    print(f"DEBUG: AccessToken model fields: {[f.name for f in oa.AccessToken._meta.get_fields() if f.concrete]}")
    accesstokens = AccessToken._default_manager.iterator()
    for accesstoken in accesstokens:
        accesstoken.save(update_fields=['token_checksum'])


class Migration(migrations.Migration):
    dependencies = [
        ("oauth2_provider", "0012_add_token_checksum"),
        migrations.swappable_dependency(oauth2_settings.ACCESS_TOKEN_MODEL),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='accesstoken',
            name='token_checksum',
            field=oauth2_provider.models.TokenChecksumField(blank=False, max_length=64,  db_index=True, unique=True),
        ),
    ]
