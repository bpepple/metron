from sorl.thumbnail import delete


def pre_delete_image(sender, instance, **kwargs):
    if (instance.image):
        delete(instance.image)
