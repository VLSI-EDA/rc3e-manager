import sys

from django.conf.urls import url
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import ListView


def generate_list_view(model_entity, verbose=False):
    """
    Generates a default list view for a given class.
    The model class' class_name will be extracted and lower cased.
    The generated url pattern will be '^{class_name}s/list/'.
    The generated pattern name will be 'list_{class_name}s'.
    The generated html template file will be searched as  '{class_name}s/list.html'.
    The context object will be named 'object_list'

    :param model_entity: Is the model class you want to generate a list view for
    :param verbose: dictates whether you want additional output printed to see what gets generated.
    :return: a url object containing the generated list view
    """

    # I found no way to do this without violating the protected status of _meta
    class_name = model_entity._meta.model_name

    url_pattern = "^{class_name}s/list/".format(class_name=class_name)
    context_object_name = "object_list"
    template_name = "{class_name}s/list.html".format(class_name=class_name)
    name = "list_{class_name}s".format(class_name=class_name)

    # Verify that the referenced html files exist.
    try:
        get_template(template_name)
    except TemplateDoesNotExist as error:
        print("WARNING Template is referenced, but missing: {0}".format(error), file=sys.stderr)

    if verbose:
        print("Generating url pattern {0} where {1} -> {2}".format(name, url_pattern, template_name))

    return url(
        url_pattern,
        ListView.as_view(
            model=model_entity,
            context_object_name=context_object_name,
            template_name=template_name
        ),
        name=name
    )


def generate_delete_view(model_entity, verbose=False):
    """
    Generates a default delete view for a given class.
    The model class' class_name will be extracted and lower cased.
    The generated url pattern will be '^{class_name}s/delete/(?P<pk>[\d]+)/$'.
    The generated pattern name will be 'delete_{class_name}'.
    The generated html template file will be searched as  '{class_name}s/delete.html'.
    The context object will be named 'object'
    The success url will be 'list_{class_name}s'

    :param model_entity: Is the model class you want to generate a list view for
    :param verbose: dictates whether you want additional output printed to see what gets generated.
    :return: a url object containing the generated delete view
    """

    # I found no way to do this without violating the protected status of _meta
    class_name = model_entity._meta.model_name

    url_pattern = "^{class_name}s/delete/(?P<pk>[\d]+)/$".format(class_name=class_name)
    context_object_name = "object"
    template_name = "{class_name}s/delete.html".format(class_name=class_name)
    name = "delete_{class_name}".format(class_name=class_name)
    success_url = "list_{class_name}s".format(class_name=class_name)

    # Verify that the referenced html files exist.
    try:
        get_template(template_name)
    except TemplateDoesNotExist as error:
        print("WARNING Template is referenced, but missing: {0}".format(error), file=sys.stderr)

    if verbose:
        print("Generating url pattern {0} where {1} -> {2}".format(name, url_pattern, template_name))

    return url(
        url_pattern,
        DeleteView.as_view(
            model=model_entity,
            context_object_name=context_object_name,
            template_name=template_name,
            success_url=reverse_lazy(success_url),
        ),
        name=name
    )
