var blog_page = this.document.querySelector('.blog-page');
create_blog_icon = document.querySelector('.nav_edit');
create_blog_icon.addEventListener('click', function() {
    if (document.querySelector('.home-page').classList.contains('none')) {
        document.querySelector('.home-page').classList.remove('none');
        blog_page.classList.add('none');
    } else if(!document.querySelector('.home-page').classList.contains('none')) {
        document.querySelector('.home-page').classList.add('none');
        blog_page.classList.remove('none');
    }
});



var noti_icon = document.querySelector('.nav_noti');
noti_icon.addEventListener('click', function() {
    if (document.querySelector('.blog-user-info').classList.contains('none')) {
        document.querySelector('.blog-user-info').classList.remove('none');
        document.querySelector('.notification').classList.add('none');
    } else if(!document.querySelector('.blog-user-info').classList.contains('none')) {
        document.querySelector('.blog-user-info').classList.add('none');
        document.querySelector('.notification').classList.remove('none');
    }
});

document.querySelector('.nav_home').addEventListener('click',function(){
    document.querySelector('.home-page').classList.remove('none');
    blog_page.classList.add('none');
})