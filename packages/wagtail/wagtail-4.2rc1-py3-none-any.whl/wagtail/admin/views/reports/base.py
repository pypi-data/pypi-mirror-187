from django.utils.translation import gettext_lazy as _

from wagtail.admin.views.generic.models import IndexView
from wagtail.admin.views.mixins import SpreadsheetExportMixin


class ReportView(SpreadsheetExportMixin, IndexView):
    header_icon = ""
    page_kwarg = "p"
    template_name = "wagtailadmin/reports/base_report.html"
    title = ""
    paginate_by = 50

    def get_filtered_queryset(self):
        return self.filter_queryset(self.get_queryset())

    def decorate_paginated_queryset(self, object_list):
        # A hook point to allow rewriting the object list after pagination has been applied
        return object_list

    def get(self, request, *args, **kwargs):
        self.filters, self.object_list = self.get_filtered_queryset()
        self.is_export = self.request.GET.get("export") in self.FORMATS
        if self.is_export:
            self.paginate_by = None
            self.object_list = self.decorate_paginated_queryset(self.object_list)
            return self.as_spreadsheet(self.object_list, self.request.GET.get("export"))
        else:
            context = self.get_context_data()
            context["object_list"] = self.decorate_paginated_queryset(
                context["object_list"]
            )
            return self.render_to_response(context)

    def get_context_data(self, *args, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        context = super().get_context_data(*args, object_list=queryset, **kwargs)
        context["title"] = self.title
        context["header_icon"] = self.header_icon
        context["filters"] = self.filters
        return context


class PageReportView(ReportView):
    template_name = "wagtailadmin/reports/base_page_report.html"
    export_headings = {
        "latest_revision_created_at": _("Updated"),
        "status_string": _("Status"),
        "content_type.model_class._meta.verbose_name.title": _("Type"),
    }
    list_export = [
        "title",
        "latest_revision_created_at",
        "status_string",
        "content_type.model_class._meta.verbose_name.title",
    ]
