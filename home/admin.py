from django.contrib import admin
from .models import Post,PostComment


class PostAdmin(admin.ModelAdmin):
    """
        #prepopulated_fields=[]
        #remember this field just active when you want to add new post for first time,
        it does not work for editing posts!!

    """
    
    list_display=['title','author','updated_date']
    list_filter=['author']
    readonly_fields=['created_date','updated_date']
    raw_id_fields=('author',)
    search_fields=['author','body','title','created_date']
    prepopulated_fields={'slug':('title','body')} 
    # list_editable=[]

admin.site.register(Post,PostAdmin)

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display=['user','post','created_date','is_reply']
    raw_id_fields=('user','post','reply')
    readonly_fields=('created_date',)

    # list_filter=[]
    # search_fields=[]