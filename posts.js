// This file fetches the posts from the server
fetch('http://example.com/movies.json')
  .then(response => response.json())
  .then(data => console.log(data));


/* Post structure: 
<details>
  <summary>title</summary>
  <time>time</time>
  <article>content</article>
</details> 
*/

function response_status(response) {
  if (response.status >= 200 && response.status < 300) {
    return Promise.resolve(response)
  } else {
    return Promise.reject(new Error(response.statusText))
  }
}

function gettext(response) {
  return response.text()
}

window.onload = function() {
  // let p_data = localStorage.getItem("post");
  // if (p_data === null) {

    fetch('posts/*')
    .then(response_status)
    .then(gettext)
    .then(function(data) {
      console.log('Request succeeded with text response', data);
      localStorage.setItem("post", data);
      document.getElementById("posts")
    }).catch(function(error) {
      console.log('Request failed', error);
    });
  // } else {
    // console.log('Already loaded', p_data);
  // }
}

  // post hello world to console when the window loads