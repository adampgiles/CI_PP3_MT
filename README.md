# Mini Tales (Short Story Sharing)

**Developer: Adam Giles**

[Live website](https://mini-tales-project.herokuapp.com/)

## Table of Content

- [Project Goals](#project-goals)
- [User Experience](#user-experience)
    - [Target Audience](#target-audience)
    - [User Stories](#user-stories)
- [Design](#design)
    - [Colour](#colour)
    - [Fonts](#font)
    - [Structure](#structure)
- [Technologies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks, Libraries & Tools](#frameworks-libraries--tools)

## Project Goals
Mini Tales is a short story sharing website. Users can create an account to share, read, search for and upvote short stories.

Mini Tales has the following goals;
- Give users a platform to submit and share short stories.
- Give users a platform to search for and read short stories.

Users of Mini Tales have the following goals;
- To create an account to submit short stories.
- To submit short stories for other users to read and upvote.
- To edit or delete their existing short story submissions.
- To search/filter for short stories by keywords.

## User Experience

### Target Audience
- Individuals interested in sharing short stories.
- Individuals interested in reading short stories.

### User Stories
User stories have been separated into two groups; Site Users and Site Owner. 

#### Site Users
1. I would like to create an account to share my short stories with other users.
2. I would like to submit a short story to the website.
3. I would like to edit my short story submission.
4. I would like to delete my short story submission.
5. I would like to search and filter for other user's short stories.
6. I would like to upvote short stories that I enjoy.

#### Site Owner
7. I would like users to have the ability to create a unique account on the website.
8. I would like users to be able to "Log in" to the website.
9. I would like users to be able to "Log out" of the website.
10. I would like the user to be able to search and filter for other user's short stories using keywords.
11. I would like the website to be responsive, so I can be accessed via mobile, tablet and desktop.

## Design

### Colour
The site's colour scheme consists of four key colours; White, black, yellow and red. White is used for input fields and text background. Black is used for text, icons and borders. Yellow is for buttons, links and key information. Red is used for delete buttons and alert messages.
<details><summary>Key Colours</summary>
</details>

### Font

One font was used on the site; Quicksand, which is a clear and legible font.

### Structure

The website structure consists of the main "Base" page, with the following sections being added to this page dependant on the URL; an "Explore Tales" page, a Log in page, a Register page, a Tale page, a My Tales page, a New Tale page, an Edit Tale page, a Delete Tale page and 404 page.

The pages are detailed below;

<details><summary>Base Page</summary>
<img src="">
</details>
- This page contains a header; consisting of Site Logo and Navigation Bar (Links change if the user is logged in). Also a footer; consisting of a credits link, disclaimer and copyright notice. 

<details><summary>Explore Tales Page</summary>
<img src="">
</details>
- This page contains a search bar and a block for each submitted tales. Each block shows all the tales details, except for the tale story. Users can also click the like link when logged in, to like/unlike a tale. A clear search button displays if a search is conducted.

<details><summary>Log in Page</summary>
<img src="">
</details>
- This page contains a form for the user to complete that will log them into the site.

<details><summary>Register Page</summary>
<img src="">
</details>
- This page contains a form for the user to complete that will create an account and log them into the site.

<details><summary>Tale Page</summary>
<img src="">
</details>
- This page displays all the content of a tale for a user to read. If the user is logged in and this tale is theirs, a button to edit/delete the tale is displayed.

<details><summary>My Tales Page</summary>
<img src="">
</details>
- This page displays all the currently logged in user's tales. A button to edit/delete the tale is displayed on each tales. Also a button is displayed for the user to submit a new tale.

<details><summary>New Tale Page</summary>
<img src="">
</details>
- This page contains a form for the user to complete that will submit a tale to the site.

<details><summary>Edit Tale Page</summary>
<img src="">
</details>
- This page contains a form for the user to complete that will allow them to edit an existing submitted tale. Also a button is displayed for the user to delete the tale.

<details><summary>Delete Tale Page</summary>
<img src="">
</details>
- This page contains buttons for the user to confirm or cancel a deletion request.

<details><summary>404 Page</summary>
<img src="">
</details>
- A 404 page was created to ensure that a user can easily navigate back to the main site if they encounter a page which does not exist.

## Technologies Used

### Languages

- HTML
- CSS
- Javascript
- Python
- Jinja

### Frameworks, Libraries & Tools

- [Am I Responsive](http://ami.responsivedesign.is/), used to create a devices mock-up image. 
- [Balsamiq](https://balsamiq.com/), used to create wireframes.
- [Favicon.io](https://favicon.io), used to create the site favicon.
- [Font Awesome](https://fontawesome.com/), used for all site icons.
- [Git](https://git-scm.com/), used for version control within VSCode to push the code to GitHub.
- [GitHub](https://github.com/), used to store project code.
- [Google Fonts](https://fonts.google.com/), used to acquire the site's font.
- [Lucidchart](http://lucidchart.com), used to create database design diagrams.
- [WC3 Validator](https://validator.w3.org/), [Jigsaw W3 Validator](https://jigsaw.w3.org/css-validator/), [Wave Validator](https://wave.webaim.org/), [Lighthouse](https://developers.google.com/web/tools/lighthouse/) and [Am I Responsive](http://ami.responsivedesign.is/), used to test the site's code, performance, accessibility and responsiveness. 