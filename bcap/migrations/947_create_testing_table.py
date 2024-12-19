# Generated by Django 4.2.13 on 2024-06-14 11:10
"""
BCAP Release 1.1.0 Note

This migration is not meant to run for a clean database.
The reason being is because the majority of the materialzed views require data
population for other views to be created based on the data entries, layman's
terms 'chicken or egg' problem.

The database must be pre-seeded with all the data population beforehand.

"""
from django.db import migrations
from bcgov_arches_common.migrations.operations.privileged_sql import RunPrivilegedSQL


class Migration(migrations.Migration):

    dependencies = [
        ("bcap", "0003_create_databc_proxy_role"),
    ]

    operations = [
        # The reverse of the databc.V_HISTORIC_ENVIRO_ONEROW_SITE  needs to be done after all the MVs have been created
        migrations.RunSQL(
            """
        begin;
        call refresh_materialized_views();
        commit;
        """,
            "",
        ),
        RunPrivilegedSQL(
            """
            begin;
            drop table if exists databc.testing_947_v_historic_enviro_onerow_site_pre_update;
            create table databc.testing_947_v_historic_enviro_onerow_site_pre_update as
                select * from databc.v_historic_enviro_onerow_site;
            commit;
             """,
            """
             drop table if exists databc.testing_947_v_historic_enviro_onerow_site_pre_update;
             """,
        ),
    ]
