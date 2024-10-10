from django.contrib import auth, messages
from django.contrib.auth import logout
from django.core.paginator import Paginator,EmptyPage

from django.shortcuts import render,redirect
from .models import UserProfile,loginTable,BlogPost, UserPosts, BlogComment, BlockedUsers

from .forms import BlogPostForm

def userRegistration(request):
    login_table=loginTable()
    userprofile=UserProfile()
    if request.method=='POST':
        userprofile.username=request.POST['username']
        userprofile.firstname=request.POST['firstname']
        userprofile.lastname = request.POST['lastname']
        userprofile.email = request.POST['email']
        userprofile.contactno = request.POST['contactno']
        userprofile.password = request.POST['password']
        userprofile.confpassword = request.POST['confpassword']

        login_table.username = request.POST['username']
        login_table.firstname = request.POST['firstname']
        login_table.lastname = request.POST['lastname']
        login_table.email = request.POST['email']
        login_table.contactno = request.POST['contactno']
        login_table.password = request.POST['password']
        login_table.confpassword = request.POST['confpassword']
        login_table.type='user'

        if request.POST['password']== request.POST['confpassword']:
            if UserProfile.objects.filter(username=userprofile.username).exists():
                messages.info(request,'This username already exists')
            elif UserProfile.objects.filter(email=userprofile.email).exists():
                messages.info(request,'This email already exists')
            elif UserProfile.objects.filter(contactno=userprofile.contactno).exists():
                messages.info(request, 'This contactno already exists')
            else:
                userprofile.save()
                login_table.save()
                messages.info(request,'Registration Successful')
                return redirect('Login')
        else:
            messages.info(request,'Password not matching')
            return redirect('Register')
    return render(request,'user/Register.html')

# Create your views here.

def loginPage(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        user=loginTable.objects.filter(username=username,password=password,type='user').exists()
        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                #blockeduser=BlockedUsers.objects.filter(username=user_details.username).exists()
                if BlockedUsers.objects.filter(username=user_details.username).exists():
                    messages.info(request, 'Blocked User')
                else:

                    messages.info(request, 'inside')
                    user_name = user_details.username
                    type = user_details.type
                    # messages.info(request,type)
                    if type == 'user':
                        request.session['username'] = user_name
                        return redirect('user_view')
                    elif type == 'admin':
                        request.session['username'] = user_name
                        return redirect('admin_view')
            else:
                messages.error(request,'Invalid username or password')
        except:
            messages.error(request, 'Invalid role')
    return render(request,'user/login.html')

def createPost(request):
    user_name = request.session['username']
    blogpost=BlogPost.objects.all()
    userposts=UserPosts()
    if request.method=='POST':
        form=BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            image=form.cleaned_data["image"]
            userposts.title=title
            userposts.content=content
            userposts.username=user_name
            userposts.image=image
            userposts.save()
            form.save()
            return redirect('list')

    else:
        form=BlogPostForm()
    return render(request,'user/postblog.html',{'form':form,'blogpost':blogpost})

def listBlogPosts(request):
    # books=Book.objects.all()
    # return render(request,'listbook.html',{'books':books})
    user_name = request.session['username']
    # blogpost=BlogPost.objects.all()
    blogpost = UserPosts.objects.filter(username=user_name)
    #Pagination
    paginator=Paginator(blogpost,2)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)


    return render(request, 'user/listpostblog.html', {'blogpost': blogpost,'page':page})

def blogdetailsView(request,blogpost_id):
    blogpost=BlogPost.objects.get(id=blogpost_id)
    return render(request,'user/blogdetailsview.html',{'blogpost':blogpost})

def updateBlog(request,blogpost_id):
    user_name = request.session['username']
    blogpost=BlogPost.objects.get(id=blogpost_id)
    userposts = UserPosts.objects.filter(username=user_name,id=blogpost_id)[0]
    if request.method=="POST":
        form=BlogPostForm(request.POST,request.FILES,instance=blogpost)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            image = form.cleaned_data["image"]
            userposts.title = title
            userposts.content = content
            userposts.username = user_name
            userposts.image = image
            userposts.save()
            form.save()
            return redirect('list')
    else:
        form=BlogPostForm(instance=blogpost)
    return render(request,'user/blogupdateview.html',{'form':form})



def deleteBlog(request,blogpost_id):
    user_name = request.session['username']
    blogpost=BlogPost.objects.get(id=blogpost_id)
    userposts = UserPosts.objects.filter(username=user_name, id=blogpost_id)[0]
    if request.method=="POST":
        blogpost.delete()
        userposts.delete()
        return redirect('list')
    return render(request,'user/blogdeleteview.html',{'blogpost':blogpost})
def adminView(request):
    user_name=request.session['username']
    return render(request,'user/admin_view.html',{'user_name':user_name})

def userView(request):
    user_name=request.session['username']
    return render(request,'user/user_view.html',{'user_name':user_name})

def logout_view(request):
    logout(request)
    return redirect('Login')
    # return render(request,'user/login.html')

def profiledetails(request):
    user_name = request.session['username']
    userdetails=UserProfile.objects.get(username=user_name)
    # blogpost=BlogPost.objects.get(id=blogpost_id)
    # userposts = UserPosts.objects.get(username=user_name)
    context={'userdetails':userdetails,
             'username':user_name}
    return render(request,'user/UserProfile.html',context)

def updateProfile(request):
    user_name = request.session['username']
    userdetails = UserProfile.objects.get(username=user_name)
    if request.method=="POST":
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        userdetails.firstname = firstname
        userdetails.lastname = lastname
        userdetails.email = email
        userdetails.contactno = contactno

        userdetails.save()
        return redirect('profiledetails')
    return render(request,'user/updateUserProfile.html',{'userdetails':userdetails})

def resetPassword(request):


    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        confpassword = request.POST['confpassword']
        if request.POST['password'] == request.POST['confpassword']:
            if UserProfile.objects.filter(username=username).exists():
                userdetails = UserProfile.objects.get(username=username)
                logindetails = loginTable.objects.get(username=username,type='user')
                userdetails.password = password
                logindetails.password = password
                userdetails.save()
                logindetails.save()
                return redirect('Login')
            else:
                messages.info(request, 'This username doesnot exists')
        else:
            messages.info(request, 'Password not matching')
        return redirect('Login')
    return render(request, 'user/resetpassword.html')

# def postComment(request):
#     if request.method == "POST":
#         comment=request.POST.get('comment')
#         user=request.user
#         postSno =request.POST.get('postSno')
#         post= Post.objects.get(sno=postSno)
#         parentSno= request.POST.get('parentSno')
#         if parentSno=="":
#             comment=BlogComment(comment= comment, user=user, post=post)
#             comment.save()
#             messages.success(request, "Your comment has been posted successfully")
#         else:
#             parent= BlogComment.objects.get(sno=parentSno)
#             comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
#             comment.save()
#             messages.success(request, "Your reply has been posted successfully")

def postcomment(request):
    user_name = request.session['username']
    alluserposts = UserPosts.objects.all()
    user_details = loginTable.objects.get(username=user_name)
    blog_userdetails=UserProfile.objects.all()
    user_comments=BlogComment.objects.all()
    paginator = Paginator(alluserposts, 2)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    if(user_details.type=='user'):
        return render(request, 'user/comment.html', {'alluserposts': alluserposts,'page':page,'user_comments':user_comments,'blog_userdetails':blog_userdetails})
    else:
        return render(request, 'user/admincomment.html', {'alluserposts': alluserposts, 'page': page,'user_comments':user_comments,'blog_userdetails':blog_userdetails})

def userpostcomment(request,alluserposts_id):
    user_name = request.session['username']
    userposts = UserPosts.objects.get(id=alluserposts_id)
    userdetails= UserProfile.objects.get(username=user_name)
    postpersondetails=UserProfile.objects.get(username=userposts.username)
    blogcomment = BlogComment()
    if request.method=="POST":
        blogcomment.blogid = alluserposts_id
        blogcomment.username = userposts.username
        blogcomment.firstname= userdetails.firstname
        blogcomment.lastname= userdetails.lastname
        blogcomment.postedby_username = user_name
        blogcomment.comment = request.POST['comment']
        # if (blogcomment.comment):
        blogcomment.save()
        return redirect('postlist')
    return render(request,'user/postcomments.html',{'userdetails':userdetails,'userposts':userposts,'postpersondetails':postpersondetails})

def admin_selectedUserView(request,user_id):
    userdetailsview=UserProfile.objects.get(id=user_id)
    return render(request,'user/adminSelectedUserview.html',{'userdetailsview':userdetailsview})

def blockUser(request,user_id):
    user_name = request.session['username']
    userdetails=UserProfile.objects.get(id=user_id)
    blockedusers=BlockedUsers()
    if request.method=="POST":
        blockedusers.blocked_status='blocked'
        blockedusers.username=userdetails.username
        blockedusers.adminname = user_name
        blockedusers.save()
        return redirect('postlist')
    return render(request,'user/blockuser.html',{'userdetails':userdetails})