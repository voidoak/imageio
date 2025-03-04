from .imopen import imopen as imopen_core
import numpy as np


# create name in this namespace to allow ``import imageio.v3 as iio``
imopen = imopen_core()


def imread(uri, *, index: int = None, plugin: str = None, **kwargs):
    """Read an ndimage from a URI.

    Opens the given URI and reads an ndimage from it. The exact behavior
    depends on both the file type and plugin used to open the file. To learn
    about the exact behavior, check the documentation of the relevant plugin.
    Typically, imread attempts to read all data stored in the URI.

    Parameters
    ----------
    uri : {str, pathlib.Path, bytes, file}
        The resource to load the image from, e.g. a filename, pathlib.Path,
        http address or file object, see the docs for more info.
    index : {int, None}
        If the URI contains multiple ndimages, select the index-th ndimage
        from among them and return it. The exact behavior is plugin dependent.
    plugin : {str, None}
        The plugin to be used. If None, performs a search for a matching plugin.
    **kwargs :
        Additional keyword arguments will be passed to the plugin's read call.

    Returns
    -------
    image : ndimage
    """

    plugin_kwargs = {"search_legacy_only": False, "plugin": plugin}

    with imopen_core()(uri, "r", **plugin_kwargs) as img_file:
        return np.asarray(img_file.read(index=index, **kwargs))


def imiter(uri, *, plugin: str = None, **kwargs):
    """Read a sequence of ndimages from a URI.

    Returns an iterable that yields ndimages from the given URI. The exact
    behavior depends on both, the file type and plugin used to open the file.
    To learn about the exact behavior, check the documentation of the relevant
    plugin.

    Parameters
    ----------
    uri : {str, pathlib.Path, bytes, file}
        The resource to load the image from, e.g. a filename, pathlib.Path,
        http address or file object, see the docs for more info.
    plugin : {str, None}
        The plugin to be used. If None, performs a search for a matching
        plugin.
    **kwargs :
        Additional keyword arguments will be passed to the plugin's ``iter``
        call.

    Returns
    -------
    image : ndimage
    """

    plugin_kwargs = {"search_legacy_only": False, "plugin": plugin}

    with imopen_core()(uri, "r", **plugin_kwargs) as img_file:
        for image in img_file.iter(**kwargs):
            # Note: casting to ndarray here to ensure compatibility
            # with the v2.9 API
            yield np.asarray(image)


def imwrite(uri, image: np.ndarray, *, plugin: str = None, **kwargs):
    """Write an ndimage to the given URI.

    The exact behavior depends on the file type and plugin used. To learn about
    the exact behavior, check the documentation of the relevant plugin.

    Parameters
    ----------
    uri : {str, pathlib.Path, bytes, file}
        The resource to save the image to, e.g. a filename, pathlib.Path,
        http address or file object, check the docs for more info.
    image : np.ndarray
        The image to write to disk.
    plugin : {str, None}
        The plugin to be used. If None, performs a search for a matching
        plugin.
    **kwargs :
        Additional keyword arguments will be passed to the plugin's ``write``
        call.

    Returns
    -------
    None
    """
    plugin_kwargs = {"search_legacy_only": False, "plugin": plugin}

    with imopen_core()(uri, "w", **plugin_kwargs) as img_file:
        img_file.write(image, **kwargs)
