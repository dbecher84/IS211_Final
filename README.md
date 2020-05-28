# IS211_Final

Project Option 2: Blog Application
Details
The purpose of this web application is to give a user the ability to run their own blog. A blog is just a
series of posts made by an author. Each post has a title, a published date, an author, and textual
(HTML) content. When first loading the application at the root URL, the user should be presented with a
list of available posts listed in reverse chronological order (newest posts first). The application should
allow a user to login via the ‘/login’ URL, which gives that user the ability to make changes to the blog.
After logging in, the user should be sent to the ‘/dashboard’ page, which presents the user with an
interface that:
1. Shows a list of their posts in a table. This list just shows the title of the post, with buttons
labeled ‘Edit’ and ‘Delete’. This edit button will take the user to a page that allows them to
update the post. The delete button will simply delete that post.
2. Allows the user to add a new post (This can be done either directly on the dashboard page
or on a new page).
Extra Credit
1. Extend the application to support multiple users: You do not have to worry about supporting
a full registration workflow. Use a table in the database to store users and their credentials,
and use this table to support logins from many accounts. Please note: storing passwords
that are unencrypted is a bad idea, security wise. However, there is no need for us to delve
into that.
2. Perma­links: Most blogs have a feature called ‘permalinks’, which is a unique URL for every
blog post. Construct URLs for each blog post, and display this perma­link for each blog
post.
3. Allow a user to ‘un­publish’ a post: Lets say the user would like to make changes to a post
but would like for the post to not show up on the website. Create another button called
‘Unpublish’, which keeps the post in the database but stops it from being published on the
website.
4. Add a category feature: Posts may have an associated ‘category’ name. Allow the user to
set up their own list of categories. Update the ‘add’ and ‘edit’ forms for posts to allow the
user to create posts in that category. When displaying the post, make sure to display the
category as a link; this link should go to a view that shows only posts in that category
