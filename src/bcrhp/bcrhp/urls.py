from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls.resolvers import RegexPattern
from bcrhp.views.api import BordenNumber, MVT, LegislativeAct
from bcrhp.views.crhp import CRHPXmlExport
from bcrhp.views.search import export_results as bcrhp_export_results
from bcrhp.views.resource import ResourceReportView
from .views.map import BCTileserverProxyView
import re

uuid_regex = settings.UUID_REGEX

path_prefix_re = re.compile(r'^(\^)(.*)$')

def bc_path_prefix(path):
    if not settings.BCGOV_PROXY_PREFIX:
        return path
    else:
        new_path = path_prefix_re.sub(r"\1%s\2",path)
        return new_path % settings.BCGOV_PROXY_PREFIX

class BCRegexPattern(RegexPattern):
    def __init__(self, regexpattern):
        super().__init__(bc_path_prefix(regexpattern.regex.pattern), regexpattern.name, regexpattern._is_endpoint)


bc_url_resolver = re_path((r'^'), include('arches.urls'))


for pattern in bc_url_resolver.url_patterns:
    # print("Before: %s" % pattern.pattern)
    pattern.pattern = BCRegexPattern(pattern.pattern)
    # print("After: %s" % pattern.pattern)

urlpatterns = [
                  re_path(bc_path_prefix(r"^bctileserver/(?P<path>.*)$"), BCTileserverProxyView.as_view(),
                             name="bcrhp_tile_server"),
                  re_path(
                      bc_path_prefix(r"^borden_number/(?P<resourceinstanceid>%s)$" % uuid_regex),
                      BordenNumber.as_view(),
                      name="borden_number",
                      ),
                  re_path(
                      r"^legislative_act/(?P<act_id>%s)$" % uuid_regex, LegislativeAct.as_view(),
                      name="legislative_act",
                      ),
                  re_path(
                      bc_path_prefix(r"^crhp_export/(?P<resourceinstanceid>%s)$" % uuid_regex),
                      CRHPXmlExport.as_view(),
                      name="crhp_export",
                      ),
                  re_path(
                      bc_path_prefix(r"^mvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % uuid_regex),
                      MVT.as_view(),
                      name="mvt",
                      ),
                  re_path(
                      bc_path_prefix(r"^report/(?P<resourceid>%s)$" % uuid_regex),
                      ResourceReportView.as_view(),
                      name="resource_report"),
                  # Override base export results
                  re_path(
                      bc_path_prefix(r"^search/export_results$"),
                      bcrhp_export_results,
                      name="export_results"),
                  bc_url_resolver,
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
