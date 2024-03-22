var blog_page = document.querySelector('.blog-page');
var create_blog_icon = document.querySelector('.nav_edit');

// Function to handle saving the blog content
function saveBlogContent(blogTitle, blogContent) {
    // Send a POST request to your Flask server to save the blog content
    fetch('/save_blog', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ blogTitle: blogTitle, blogContent: blogContent })
    })
    .then(response => {
        if (response.ok) {
            alert('Blog saved successfully!');
            document.getElementById('blog-title').value = '';
            document.querySelector('.create-content').value = '';
        } else {
            alert('Failed to save blog. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the blog.');
    });
}

// Attach an event listener to the "Create" button
document.getElementById('createButton').addEventListener('click', function() {
    // Extract the blog title from the input field
    var blogTitle = document.getElementById('blog-title').value;

    // Extract the blog content from the textarea
    var blogContent = document.querySelector('.create-content').value;

    // Call the function to save the blog title and content
    saveBlogContent(blogTitle, blogContent);
});


create_blog_icon.addEventListener('click', function() {
    if (document.querySelector('.home-page').classList.contains('none')) {
        document.querySelector('.home-page').classList.remove('none');
        blog_page.classList.add('none');
    } else {
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