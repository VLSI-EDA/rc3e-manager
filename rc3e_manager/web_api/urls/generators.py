import sys
from collections import namedtuple

from django.conf.urls import url
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import ListView


def model_class_pythonic_name(model_entity):
    """
    A helper function to generate names for urls and folders from a model entity.
    It uses the verbose name of the entity but replaces spaces with underscores.
    :param model_entity:
    :return:
    """
    # I found no way to do this without violating the protected status of _meta
    verbose_name = model_entity._meta.verbose_name
    return verbose_name.replace(" ", "_")


def deduce_generator_parameters(
        model_entity,
        operation_name,
        url_param_pattern="",
        is_multi_element_operation=False,
        verbose=False
):
    GeneratorParameters = namedtuple(
        "GeneratorParameters",
        [
            "url_pattern_name",
            "url_pattern",
            "context_object_name",
            "form_name",
            "template_name",
            "success_url"
        ])

    class_name = model_class_pythonic_name(model_entity)

    # Set static values
    context_object_name = "object"
    form_name = "form"

    # Generate the url pattern name
    url_pattern_name = "{operation_name}_{class_name}".format(
        class_name=class_name,
        operation_name=operation_name
    )

    if is_multi_element_operation:
        url_pattern_name += "s"

    # Generate the url pattern
    url_pattern = "^{class_name}s/{operation_name}".format(
        class_name=class_name,
        operation_name=operation_name
    )

    if url_param_pattern:
        url_pattern += "/{url_param_pattern}".format(url_param_pattern=url_param_pattern)
    url_pattern += "/$"

    # Generate the template file name
    template_name = "{class_name}s/{operation_name}.html".format(
        class_name=class_name,
        operation_name=operation_name
    )
    success_url = "list_{class_name}s".format(class_name=class_name)

    # Verify that the referenced html files exist.
    try:
        get_template(template_name)
    except TemplateDoesNotExist as error:
        print("WARNING Template is referenced, but missing: {0}".format(error), file=sys.stderr)

    if verbose:
        print("Generating url pattern {0} where {1} -> {2}".format(url_pattern_name, url_pattern, template_name))

    return GeneratorParameters(
        url_pattern_name,
        url_pattern,
        context_object_name,
        form_name,
        template_name,
        success_url
    )


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

    generator_parameters = deduce_generator_parameters(
        model_entity,
        operation_name="list",
        is_multi_element_operation=True,
        verbose=verbose)

    return url(
        generator_parameters.url_pattern,
        ListView.as_view(
            model=model_entity,
            context_object_name=generator_parameters.context_object_name,
            template_name=generator_parameters.template_name
        ),
        name=generator_parameters.url_pattern_name
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

    generator_parameters = deduce_generator_parameters(
        model_entity,
        operation_name="delete",
        url_param_pattern="(?P<pk>[\d]+)",
        is_multi_element_operation=False,
        verbose=verbose)

    return url(
        generator_parameters.url_pattern,
        DeleteView.as_view(
            model=model_entity,
            context_object_name=generator_parameters.context_object_name,
            template_name=generator_parameters.template_name,
            success_url=reverse_lazy(generator_parameters.success_url),
        ),
        name=generator_parameters.url_pattern_name
    )
