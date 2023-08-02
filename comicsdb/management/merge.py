from django.db.models import ManyToManyField, ManyToManyRel, ManyToOneRel


def update_related(canonical, obj):
    """update all the models with fk to the object being removed"""
    # move related models to canonical
    related_models = [
        (r.remote_field.name, r.related_model) for r in canonical._meta.related_objects
    ]
    for related_field, related_model in related_models:
        # Skip the ManyToMany fields that aren`t auto-created. These
        # should have a corresponding OneToMany field in the model for
        # the linking table anyway. If we update it through that model
        # instead then we won`t lose the extra fields in the linking
        # table.
        related_field_obj = related_model._meta.get_field(related_field)
        if isinstance(related_field_obj, ManyToManyField):
            through = related_field_obj.remote_field.through
            if not through._meta.auto_created:
                continue
        related_objs = related_model.objects.filter(**{related_field: obj})
        for related_obj in related_objs:
            print(
                f"Replacing in '{related_model.__name__}' model '{related_field}' "
                f"field with ID '{related_obj.id}'"
            )
            try:
                setattr(related_obj, related_field, canonical)
                related_obj.save()
            except TypeError:
                getattr(related_obj, related_field).add(canonical)
                getattr(related_obj, related_field).remove(obj)


def copy_data(canonical, obj):
    """try to get the most data possible"""
    for data_field in obj._meta.get_fields():
        if isinstance(data_field, ManyToManyRel | ManyToOneRel):
            continue
        # Skip any images in the other obj since it will be remove
        # when the object is deleted.
        if data_field.name == "image":
            continue
        data_value = getattr(obj, data_field.name)
        if not data_value:
            continue
        if not getattr(canonical, data_field.name):
            print(f"Setting field '{data_field.name}' to '{data_value}")
            setattr(canonical, data_field.name, data_value)
    canonical.save()


def remove_attribution(obj):
    # For now let's remove any attribution records on the dup obj.
    att_count = obj.attribution.count()
    if att_count > 0:
        print(f"Removed {att_count} attribution records for {obj}")
        obj.attribution.clear()


def merge_objects(canonical, obj):
    copy_data(canonical, obj)
    update_related(canonical, obj)
    remove_attribution(obj)
    # remove the outdated entry
    obj.delete()
