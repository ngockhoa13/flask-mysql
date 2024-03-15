window.addEventListener('hashchange', function() {
    var hash = window.location.hash;
    var homePage = document.querySelector('.home-page');
    var blog_page = this.document.querySelector('.blog-page');
    if (hash === '#blog') {
        homePage.classList.add('none');
        blog_page.classList.remove('none');
    } else {
        homePage.classList.remove('none');
        blog_page.classList.add('none');

    }
    console.log(hash)
    // Kiểm tra nếu không có hash hoặc hash là một hash rỗng thì hiển thị trang chính
    if (!hash || hash === '#') {
        homePage.classList.remove('none');
        this.document.querySelector('.blog-page').classList.add('none');
    }
});

// Đảm bảo rằng trạng thái ban đầu của trang được xử lý đúng
window.addEventListener('DOMContentLoaded', function() {
    var hash = window.location.hash;
    var homePage = document.querySelector('.home-page');

    if (!hash || hash === '#') {
        homePage.classList.remove('none');
        this.document.querySelector('.blog-page').classList.add('none');
    } else if (hash === '#blog') {
        homePage.classList.add('none');
        this.document.querySelector('.blog-page').classList.remove('none');
    }
});
// Event for display notification
window.addEventListener('hashchange', function() {
    var hash = window.location.hash;
    var homePage = document.querySelector('.blog-user-info');
    var blog_page = this.document.querySelector('.notification');
    if (hash === '#notification') {
        homePage.classList.add('none');
        blog_page.classList.remove('none');
    } else {
        homePage.classList.remove('none');
        blog_page.classList.add('none');

    }
    console.log(hash)
    // Kiểm tra nếu không có hash hoặc hash là một hash rỗng thì hiển thị trang chính
    if (!hash || hash === '#') {
        homePage.classList.remove('none');
        this.document.querySelector('.notification').classList.add('none');
    }
});

// Đảm bảo rằng trạng thái ban đầu của trang được xử lý đúng
window.addEventListener('DOMContentLoaded', function() {
    var hash = window.location.hash;
    var homePage = document.querySelector('.blog-user-info');

    if (!hash || hash === '#') {
        homePage.classList.remove('none');
        this.document.querySelector('.notification').classList.add('none');
    } else if (hash === '#notification') {
        homePage.classList.add('none');
        this.document.querySelector('.notification').classList.remove('none');
    }
});
