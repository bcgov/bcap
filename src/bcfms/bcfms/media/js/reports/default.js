define([
        'knockout',
        'reports/bcfms-report',
        'templates/views/report-templates/bcfms_default.htm',
        'templates/views/report-templates/details/fossil_sample.htm',
], function (ko, ReportViewModel, defaultTemplate) {
    const viewModel = function(params) {
        params.configKeys = [];


        ReportViewModel.apply(this, [params]);
    };

    return ko.components.register('default-report', {
        viewModel: viewModel,
        template: defaultTemplate
    });
});