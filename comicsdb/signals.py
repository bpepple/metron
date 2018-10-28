def pre_delete_image(sender, instance, **kwargs):
    if (instance.image):
        instance.image.delete(False)