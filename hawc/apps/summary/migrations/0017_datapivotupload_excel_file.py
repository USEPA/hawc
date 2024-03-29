# Generated by Django 1.11.15 on 2018-10-23 02:51

import os

import numpy as np
import pandas as pd
from django.conf import settings
from django.db import migrations


def _read_tsv(fn: str, encoding: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(fn, sep="\t", encoding=encoding)
    except Exception:
        return None


def _read_excel(fn: str) -> pd.DataFrame | None:
    try:
        return pd.read_excel(fn)
    except Exception:
        return None


def rewrite_static_files(apps, schema_editor):
    """
    Iterate over all DataPivotUpload objects; for each  object, try to load as a pandas DataFrame
    and then save as an Excel file. Note that in some cases, an Excel file may not be created.
    """
    DataPivotUpload = apps.get_model("summary", "DataPivotUpload")
    excel_root = DataPivotUpload.excel_file.field.upload_to
    os.makedirs(os.path.join(settings.MEDIA_ROOT, excel_root), exist_ok=True)
    for dp in DataPivotUpload.objects.all():
        from_fn = dp.file.path
        to_fn = os.path.join(excel_root, os.path.basename(dp.file.name) + ".xlsx")
        dfs = [
            _read_tsv(from_fn, "utf-8"),
            _read_tsv(from_fn, "utf-16"),
            _read_tsv(from_fn, "latin1"),
            _read_excel(from_fn),
        ]
        dfs = [el for el in dfs if el is not None]
        if len(dfs) > 0:
            # if we couldnt load it, do nothing; otherwise save an Excel file and rewrite the CSV
            # with a UTF-8 version.
            dfs_nonnulls = [df.notnull().sum().sum() for df in dfs]
            df = dfs[np.argmax(dfs_nonnulls)]
            df.to_excel(os.path.join(settings.MEDIA_ROOT, to_fn), index=False)
            dp.excel_file.name = to_fn
            dp.save()
        else:
            print(f"Couldn't parse file: {dp.file.path}")
            print(f"Deleting data pivot: {dp.id}")
            dp.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("summary", "0016_datapivotupload_excel_file"),
    ]

    operations = [
        migrations.RunPython(rewrite_static_files, reverse_code=migrations.RunPython.noop),
    ]
