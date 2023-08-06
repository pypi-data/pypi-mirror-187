import uuid
from django.db import models
from django.http import JsonResponse
from django.contrib import admin, messages
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.db.transaction import atomic

from django_form_generator import const
from django_form_generator.common.admins import FormFilter, AdminMixin
from django_form_generator.forms import FieldForm, FormAdminForm, FormResponseFilterForm, ValidatorAdminForm
from django_form_generator.models import (
    FieldCategory,
    Form,
    Field,
    FieldValidator,
    FormFieldThrough,
    Option,
    FormResponse,
    FormAPIThrough,
    FieldOptionThrough,
    FormAPIManager,
)

# Register your models here.




class FormResponseFilter(FormFilter):

    template = "django_form_generator/filters/form_response_filter.html"
    form_class = FormResponseFilterForm

    def _create_related_fields_lookup(self, q, form, current_field_id, fields, texts, *, similar_field_index=None):
        related_fields = form.fields.filter(object_id=current_field_id, content_type__model='field', id__in=fields)
        for field in related_fields:
            try:
                if similar_field_index is not None:
                    index = fields.index(field.id)
                    query_index = similar_field_index + 1
                else:
                    query_index = index = fields.index(field.id)
                value = int(texts[query_index]) if texts[query_index].isdigit() else texts[query_index]
                if isinstance(value, int):
                    self._combine(q, models.Q(**{f"{self.field_path}__{index}__value": value}), models.Q.AND, q)
                else:
                    self._combine(q, models.Q(**{f"{self.field_path}__{index}__value__regex": value}), models.Q.AND, q)
            except IndexError:
                ...
        return q

    def clean_parameters(self, item):
        return list(filter(lambda x: x != '', item))

    def _combine(self, lookup, inner, operand, final_lookup):
        for r in inner.children:
            if str(r) not in str(final_lookup) and str(r) not in str(lookup):
                lookup.add(inner, operand)
            

    def get_lookups(self):
        lookup = models.Q()
        no_result = False
        fields_text = self.clean_parameters(self.request.GET.getlist(f'{self.field.name}-text'))
        fields_id = self.clean_parameters(self.request.GET.getlist(f'{self.field.name}-field'))
        fields_operand = self.clean_parameters(self.request.GET.getlist(f'{self.field.name}-operand'))
        form_id = self.request.GET.get(f'{self.field.name}-form_id')
        if form_id:
            form = Form.objects.prefetch_related('fields').get(id=int(form_id))
            form_fields_list = list(form.get_fields().values_list('id', flat=True))
            for i in range(len(fields_text)):
                field_id = int(fields_id[i])
                field_value = int(fields_text[i]) if fields_text[i].isdigit() else fields_text[i]
                current_operand = getattr(models.Q, fields_operand[i], models.Q.AND)
                if isinstance(field_value, int):
                    lookup_content = "{0}__{1}__value"
                else:
                    lookup_content = "{0}__{1}__value__regex"
                try:
                    index = form_fields_list.index(field_id)
                    inner_lookup = models.Q(**{lookup_content.format(self.field_path, index): field_value})
                    self._create_related_fields_lookup(inner_lookup, form, field_id, fields_id, fields_text)
                    self._combine(lookup, inner_lookup, current_operand, lookup)
                except ValueError:
                    # searching on similar fields (same names with number postfix)
                    inner_lookup = models.Q()
                    current_field = Field.objects.get(id=field_id)
                    similar_fields = form.fields.filter(name__startswith=current_field.name).exclude(pk=current_field.pk).order_by('name')
                    if similar_fields.exists():
                        for field_ in similar_fields:
                            try:
                                index = form_fields_list.index(field_.pk)
                                related_lookup = models.Q(**{lookup_content.format(self.field_path, index): field_value})
                                self._create_related_fields_lookup(related_lookup, form, field_.pk, form_fields_list, fields_text, similar_field_index=fields_id.index(str(current_field.pk)))
                                self._combine(inner_lookup, related_lookup, models.Q.OR, lookup)
                            except IndexError:
                                ...
                        self._combine(lookup, inner_lookup, current_operand, lookup)
                    else:
                        no_result = True
        elif len(fields_id) > 0 and fields_id[0] != '':
            messages.error(self.request, _("First select a form"))
        if no_result:
            return {'id': 0}
        return lookup


    def form_lookups(self):
        name = self.field.name
        return (
            ("%s-form_id" % name, "%s__exact" % name),
            ("%s-field" % name, "%s__contains" % name),
            ("%s-text" % name, "%s__contains" % name),
            ("%s-operand" % name, "%s__contains" % name),
        )


class FormFieldThroughInlineAdmin(admin.TabularInline):
    model = FormFieldThrough
    extra = 1
    raw_id_fields = ("field",)
    verbose_name = _('Field')
    verbose_name_plural = _('Fields')


class FormAPIThroughInlineAdmin(admin.TabularInline):
    model = FormAPIThrough
    extra = 1
    raw_id_fields = ("api",)
    verbose_name = _('API')
    verbose_name_plural = _('APIs')


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'get_style', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_editable = ['status']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'slug']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [FormFieldThroughInlineAdmin, FormAPIThroughInlineAdmin]
    form = FormAdminForm
    actions = ("clone_action",)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'submit_text', 'redirect_url', 'success_message', 'id', 'created_at', 'updated_at')
        }),
        ('Style', {
            'classes': ('wide',),
            'fields': ('style', 'direction'),
        }),
        ('Limitations', {
            'classes': ('wide',),
            'fields': ('limit_to', 'valid_from', 'valid_to', 'is_editable'),
        }),
    )

    @admin.display(description="Style")
    def get_style(self, obj):
        if obj.style:
            return const.FormStyle(obj.style).label

    @atomic
    def clone_action(self, request, queryset):
        for obj in queryset:
            f_through = obj.form_field_through.all().values('field_id', 'position', 'category_id', 'weight')
            a_through = obj.form_apis.all().values('api_id', 'weight')
            for field in obj._meta.local_fields:
                if field.unique:
                    if field.name in ("pk", "id"):
                        setattr(obj, field.name, None)

            setattr(obj, "slug", uuid.uuid4())
            setattr(obj, 'title', obj.title + ' (Copy)')
            setattr(obj, "status", const.FormStatus.DRAFT)
            obj.save()

            ff_through = [FormFieldThrough(form_id=obj.id, **obj_) for obj_ in f_through]
            FormFieldThrough.objects.bulk_create(ff_through, ignore_conflicts=True)
            fa_through = [FormAPIThrough(form_id=obj.id, **obj_) for obj_ in a_through]
            FormAPIThrough.objects.bulk_create(fa_through)

class FieldOptionThroughInlineAdmin(admin.TabularInline):
    model = FieldOptionThrough
    extra = 1
    raw_id_fields = ("option",)
    verbose_name = _('Option')
    verbose_name_plural = _('Options')


class FieldValidatorThroughInlineAdmin(admin.TabularInline):
    model = FieldValidator
    form = ValidatorAdminForm
    extra = 1
    verbose_name = _('Validator')
    verbose_name_plural = _('Validators')

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'genre', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at', 'genre']
    search_fields = ['label', 'name', 'forms__title']
    inlines = [FieldOptionThroughInlineAdmin, FieldValidatorThroughInlineAdmin]
    readonly_fields = ['id', 'created_at', 'updated_at']
    form = FieldForm
    prepopulated_fields = {'name': ('label',), }
    fieldsets = (
        (None, {
            'fields': ('label', 'name', 'genre', 'is_required', 'placeholder', 'default', 'help_text', 'is_active', 'read_only', 'write_only', 'id', 'created_at', 'updated_at')
        }),
        ('Dpendency', {
            'classes': ('wide',),
            'fields': ('content_type', 'object_id'),
        }),
    )

    def save_form(self, request, form, change):
        form.instance.name = slugify(form.instance.label, True).replace("-", "_")
        return super().save_form(request, form, change)


@admin.register(FormResponse)
class FormResponseAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ["id", "get_form_title", "user_ip", "show_response"]
    list_display_links = ["id", "get_form_title"]
    list_filter = [('data', FormResponseFilter)]
    search_fields = ['form__title', 'form__slug']
    readonly_fields = ['id', 'unique_id', 'created_at', 'updated_at']
    extra_views = [('fetch_options', 'options/<int:field_id>')]

    @admin.display(description="Form Title")
    def get_form_title(self, obj):
        return obj.form.title

    @admin.display(description="Response")
    def show_response(self, obj):
        return mark_safe(
            f"<a href='{reverse('django_form_generator:form_response', args=(obj.unique_id, ))}'>Response</a>"
        )
    
    def fetch_options(self, request, field_id):
        options = {}
        field = Field.objects.get(id=field_id)
        if field.genre in (const.FieldGenre.selectable_fields()):
            options = Option.objects.filter(fields__id=field_id).values('id', 'name')
        return JsonResponse(list(options), safe=False)

@admin.register(FormAPIManager)
class FormAPIManagerAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "method", "execute_time", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    list_filter = ['is_active', 'created_at', 'execute_time', 'method']
    list_editable = ['is_active']
    search_fields = ['title', 'forms__title', 'forms__slug']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(FieldCategory)
class FieldCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "parent", "weight", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "title"]
    list_filter = ['is_active', 'created_at', ('parent', admin.filters.EmptyFieldListFilter)]
    list_editable = ['is_active']
    search_fields = ['title']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['name', 'fields__name', 'fields__label']
    readonly_fields = ['id', 'created_at', 'updated_at']

