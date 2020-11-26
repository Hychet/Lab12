# Lab12
## Registration
This can be found at /register. The registration page allows a user to create a username, and choose a picture. It
also allows previous users to "log in" (though log in may not be the correct term
because this website doesn't have passwords). After the user registers/logs in, they
are taken to their feed.

On the API side, when the user presses the button labeled "submit", they submit a
POST request, which goes to /submit_register. This will create a new entry in the
database table, "users". It will record the username, a profile picture, and a custom hash that is created
when the press "submit".

##Profile
The profile displays all of the users posts (in reverse chronological order), which can be found in the database table "posts". 
Each post has a link to view it individually (its title),
a link to create a new post, and a delete option. When the user clicks on delete,
javascript hides the current post, while simultaneously sending a POST request to the
server (/delete), which deletes the post from the database. 

Each post also displays the number of upvotes and downvotes, and allows the user to
upvote or downvote their own post.

## Create
This page allows users to create a new post. The form collects the post title,
content, and a timestamp. When the user hits "submit", it creates a POST
request (/submit_post), which stores all of the above information in the "posts"
table in the database, along with a unique post ID, and a foreign key connecting
the post to the user who posted it.

## Feed
The feed consists of everyone's posts other than the current user. This is done
from selecting every post other than the user's from the "posts" table in the database.
The feed allows users to upvote or downvote posts, which creates a POST request, going to /vote.

## Database Schema
Our database has three tables: "users", "posts", and "votes". The table "users" simply
has three columns: the username, the hash, and the profile picture's filename. The
table "posts" meanwhile has 6 columns. It contains the post id, a foreign key for the poster,
the post title, the post contents, the post's score (upvoted - downvotes), and
the timestamp for when the post was posted. Finally, the votes table contains 4 columns.
It contains a column for a unique vote ID (each upvote and downvote gets its own ID),
the username of the person who upvoted or downvoted, the post ID, and the actual vote
(upvote or downvote).