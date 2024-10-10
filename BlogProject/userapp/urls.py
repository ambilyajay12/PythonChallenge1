from django.urls import path
from . import views

urlpatterns = [

    path("",views.userRegistration,name='Register'),
    path("list/", views.listBlogPosts, name='list'),
    path("blogdetailsview/<int:blogpost_id>/", views.blogdetailsView, name='blogdetails'),
    path("updateview/<int:blogpost_id>/", views.updateBlog, name='updateblog'),
    path("deleteview/<int:blogpost_id>/", views.deleteBlog, name='deleteblog'),
    path("postlist/", views.postcomment, name='postlist'),
    path("postcomment/<int:alluserposts_id>", views.userpostcomment, name='postcomments'),
    path("login/",views.loginPage,name='Login'),
    path("logout/", views.logout_view, name='logout'),
    path("reset/",views.resetPassword, name='ResetPassword'),
    path("userprofileview/", views.profiledetails, name='profiledetails'),
    path("updateprofile/", views.updateProfile, name='updateprofile'),
    path("admin_view/",views.adminView,name='admin_view'),
    path("admin_selectuserview/<int:user_id>", views.admin_selectedUserView, name='admin_selUserview'),
    path("admin_blockuser/<int:user_id>", views.blockUser, name='blockuser'),
    path("user_view/", views.userView, name='user_view'),
    path("blogpost/",views.createPost,name='create'),
]