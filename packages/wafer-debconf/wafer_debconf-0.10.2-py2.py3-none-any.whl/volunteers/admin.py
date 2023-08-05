from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, F, Q

from volunteers.models import Volunteer, Task, TaskCategory, TaskTemplate


def duplicate(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


duplicate.short_description = "Duplicate selected record"


class DayListFilter(admin.SimpleListFilter):
    title = _('day')
    parameter_name = 'day'

    def lookups(self, request, model_admin):
        return (
            (1, 'Sunday'),
            (2, 'Monday'),
            (3, 'Tuesday'),
            (4, 'Wednesday'),
            (5, 'Thursday'),
            (6, 'Friday'),
            (7, 'Saturday'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start__week_day=self.value())


class NumTasksListFilter(admin.SimpleListFilter):
    title = _('tasks')
    parameter_name = 'tasks'

    def lookups(self, request, model_admin):
        return (
            (0, _('No tasks')),
            (1, _('1 - 5 tasks')),
            (2, _('More than 5 tasks')),
        )

    def queryset(self, request, queryset):
        query = queryset.annotate(num_tasks=Count('tasks'))

        if self.value() == '0':
            return query.filter(num_tasks__lte=0)
        if self.value() == '1':
            return query.filter(num_tasks__gte=1, num_tasks__lte=5)
        if self.value() == '2':
            return query.filter(num_tasks__gte=6)


class HasVolunteersListFilter(admin.SimpleListFilter):
    title = _('volunteers')
    parameter_name = 'volunteers'

    def lookups(self, request, model_admin):
        return (
            ('full', _('No more needed')),
            ('some', _('More needed')),
            ('none', _('None')),
        )

    def queryset(self, request, queryset):
        query = queryset.annotate(nbr_volunteers=Count('volunteers'))

        if self.value() == 'full':
            return query.filter(nbr_volunteers=F('nbr_volunteers_max'))
        elif self.value() == 'some':
            return query.filter(nbr_volunteers__lt=F('nbr_volunteers_max'))
        elif self.value() == 'none':
            return query.filter(nbr_volunteers=0)


class CategoryFilter(admin.SimpleListFilter):
    title = _('Category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return [(cat.pk, cat.name) for cat in TaskCategory.objects.all()]

    def queryset(self, request, queryset):
        pk = self.value()
        return queryset.filter(
            Q(category__pk=pk) | Q(template__category__pk=pk)
        )


class VolunteerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal information', {
            'fields': ('user', 'full_name', 'email', 'contact_number', 'timezone'),
        }),
        (None, {
            'fields': ('preferred_categories',),
        }),
        ('For staff', {
            'classes': ('collapse',),
            'fields': ('staff_rating', 'staff_notes'),
        }),
    )

    list_display = ('user', 'full_name', 'email', 'contact_number',
                    'num_tasks', 'staff_rating')
    list_editable = ('staff_rating',)
    list_filter = ('staff_rating', NumTasksListFilter)

    readonly_fields = ('full_name', 'email', 'contact_number', 'num_tasks')

    def full_name(self, volunteer):
        return u'%s %s' % (volunteer.user.first_name, volunteer.user.last_name)

    def email(self, volunteer):
        return volunteer.user.email

    def contact_number(self, volunteer):
        return volunteer.user.userprofile.contact_number

    def num_tasks(self, volunteer):
        return volunteer.tasks.count()


class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('template',),
        }),
        ('Task data', {
            'fields': ('category', 'name', 'description'),
        }),
        ('Space-time considerations', {
            'fields': ('schedule_item', 'venue', 'start', 'end'),
        }),
        ('Volunteers', {
            'fields': ('volunteers',
                       'nbr_volunteers_min', 'nbr_volunteers_max'),
        }),
    )

    list_display = (
        'get_name', 'template', 'start', 'end', 'venue',
        'nbr_volunteers', 'get_nbr_volunteers_min', 'get_nbr_volunteers_max',
        'volunteers_', 'get_category', 'schedule_item',
    )
    list_editable = ('venue', 'template')
    list_filter = (CategoryFilter, DayListFilter, HasVolunteersListFilter)
    search_fields = ('name', 'template__name', 'description',
                     'template__description')

    actions = [duplicate]

    def volunteers_(self, instance):
        return format_html('<ul>{0}</ul>', format_html_join(
            '',
            '<li>{}</li>',
            ((volunteer.user.get_full_name(),)
             for volunteer in instance.volunteers.all())
        ))
    volunteers_.short_description = 'Volunteers'


class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'nbr_volunteers_min', 'nbr_volunteers_max',
                    'video_task')


admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)
admin.site.register(TaskTemplate, TaskTemplateAdmin)
