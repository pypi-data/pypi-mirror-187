from collections import OrderedDict

import django.forms
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.translation import gettext_lazy as _

from wagtail.admin.forms import WagtailAdminPageForm


class BaseForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")

        self.user = kwargs.pop("user", None)
        self.page = kwargs.pop("page", None)

        super().__init__(*args, **kwargs)


class FormBuilder:
    def __init__(self, fields):
        self.fields = fields

    def create_singleline_field(self, field, options):
        # TODO: This is a default value - it may need to be changed
        options["max_length"] = 255
        return django.forms.CharField(**options)

    def create_multiline_field(self, field, options):
        return django.forms.CharField(widget=django.forms.Textarea, **options)

    def create_date_field(self, field, options):
        return django.forms.DateField(**options)

    def create_datetime_field(self, field, options):
        return django.forms.DateTimeField(**options)

    def create_email_field(self, field, options):
        return django.forms.EmailField(**options)

    def create_url_field(self, field, options):
        return django.forms.URLField(**options)

    def create_number_field(self, field, options):
        return django.forms.DecimalField(**options)

    def create_dropdown_field(self, field, options):
        options["choices"] = self.get_formatted_field_choices(field)
        return django.forms.ChoiceField(**options)

    def create_multiselect_field(self, field, options):
        options["choices"] = self.get_formatted_field_choices(field)
        return django.forms.MultipleChoiceField(**options)

    def create_radio_field(self, field, options):
        options["choices"] = self.get_formatted_field_choices(field)
        return django.forms.ChoiceField(widget=django.forms.RadioSelect, **options)

    def create_checkboxes_field(self, field, options):
        options["choices"] = self.get_formatted_field_choices(field)
        options["initial"] = self.get_formatted_field_initial(field)
        return django.forms.MultipleChoiceField(
            widget=django.forms.CheckboxSelectMultiple, **options
        )

    def create_checkbox_field(self, field, options):
        return django.forms.BooleanField(**options)

    def create_hidden_field(self, field, options):
        return django.forms.CharField(widget=django.forms.HiddenInput, **options)

    def get_create_field_function(self, type):
        """
        Takes string of field type and returns a Django Form Field Instance.
        Assumes form field creation functions are in the format:
        'create_fieldtype_field'
        """
        create_field_function = getattr(self, "create_%s_field" % type, None)
        if create_field_function:
            return create_field_function
        else:
            import inspect

            method_list = [
                f[0]
                for f in inspect.getmembers(self.__class__, inspect.isfunction)
                if f[0].startswith("create_") and f[0].endswith("_field")
            ]
            raise AttributeError(
                "Could not find function matching format \
                create_<fieldname>_field for type: "
                + type,
                "Must be one of: " + ", ".join(method_list),
            )

    def get_formatted_field_choices(self, field):
        """
        Returns a list of choices [(string, string),] for the field.
        Split the provided choices into a list, separated by new lines.
        If no new lines in the provided choices, split by commas.
        """

        if "\n" in field.choices:
            choices = (
                (
                    x.strip().rstrip(",").strip(),
                    x.strip().rstrip(",").strip(),
                )
                for x in field.choices.split("\r\n")
            )
        else:
            choices = ((x.strip(), x.strip()) for x in field.choices.split(","))

        return choices

    def get_formatted_field_initial(self, field):
        """
        Returns a list of initial values [string,] for the field.
        Split the supplied default values into a list, separated by new lines.
        If no new lines in the provided default values, split by commas.
        """

        if "\n" in field.default_value:
            values = [
                x.strip().rstrip(",").strip() for x in field.default_value.split("\r\n")
            ]
        else:
            values = [x.strip() for x in field.default_value.split(",")]

        return values

    @property
    def formfields(self):
        formfields = OrderedDict()

        for field in self.fields:
            options = self.get_field_options(field)
            create_field = self.get_create_field_function(field.field_type)

            # If the field hasn't been saved to the database yet (e.g. we are previewing
            # a FormPage with unsaved changes) it won't have a clean_name as this is
            # set in FormField.save.
            clean_name = field.clean_name or field.get_field_clean_name()
            formfields[clean_name] = create_field(field, options)

        return formfields

    def get_field_options(self, field):
        options = {}
        options["label"] = field.label
        if getattr(settings, "WAGTAILFORMS_HELP_TEXT_ALLOW_HTML", False):
            options["help_text"] = field.help_text
        else:
            options["help_text"] = conditional_escape(field.help_text)
        options["required"] = field.required
        options["initial"] = field.default_value
        return options

    def get_form_class(self):
        return type(str("WagtailForm"), (BaseForm,), self.formfields)


class SelectDateForm(django.forms.Form):
    date_from = django.forms.DateTimeField(
        required=False,
        widget=django.forms.DateInput(attrs={"placeholder": _("Date from")}),
    )
    date_to = django.forms.DateTimeField(
        required=False,
        widget=django.forms.DateInput(attrs={"placeholder": _("Date to")}),
    )


class WagtailAdminFormPageForm(WagtailAdminPageForm):
    def clean(self):
        super().clean()

        # Check for duplicate form fields by comparing their internal clean_names
        if "form_fields" in self.formsets:
            forms = self.formsets["form_fields"].forms
            for form in forms:
                form.is_valid()

            # Use existing clean_name or generate for new fields.
            # clean_name is set in FormField.save
            clean_names = [
                f.instance.clean_name or f.instance.get_field_clean_name()
                for f in forms
            ]
            duplicate_clean_name = next(
                (n for n in clean_names if clean_names.count(n) > 1), None
            )
            if duplicate_clean_name:
                duplicate_form_field = next(
                    f
                    for f in self.formsets["form_fields"].forms
                    if f.instance.get_field_clean_name() == duplicate_clean_name
                )
                duplicate_form_field.add_error(
                    "label",
                    django.forms.ValidationError(
                        _(
                            "There is another field with the label %(label_name)s, please change one of them."
                        )
                        % {"label_name": duplicate_form_field.instance.label}
                    ),
                )
