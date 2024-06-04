document.addEventListener('DOMContentLoaded', () => {
    let articles = []; // This will hold fetched articles
    let currentIndex = 0; // This will keep track of the current article being displayed

    function displayArticle(index) {
        // Check if there are no more articles to display
        if (index >= articles.length) {
            document.getElementById('articles-container').innerHTML = '<p>No more articles.</p>';
            return;
        }

        // Get the current article
        let article = articles[index];
        let htmlContent = `
            <div class="article-card">
                <div class="article-content">
                    <h2>${article.title}</h2>
                    <p>${article.description}</p>
                    <a href="${article.url}" target="_blank">Read more</a>
                </div>
                <div class="article-buttons">
                    <button class="btn agree" onclick="swipe('left', ${index})">✔️ Agree</button>
                    <button class="btn disagree" onclick="swipe('right', ${index})">❌ Disagree</button>
                </div>
            </div>
        `;

        // Update the articles container with the new HTML
        document.getElementById('articles-container').innerHTML = htmlContent;
    }

    function swipe(direction, index) {
        let articleCard = document.querySelector('.article-card');
        
        // Function to handle the end of the transition
        function handleTransitionEnd() {
            displayArticle(index + 1); // Display the next article
            articleCard.removeEventListener('transitionend', handleTransitionEnd); // Remove the event listener to avoid memory leaks
        }

        // Add the appropriate class to animate the swipe
        articleCard.classList.add(`swipe-${direction}`);
        articleCard.addEventListener('transitionend', handleTransitionEnd);
    }

    // Example function to call when the 'Agree' or 'Disagree' button is clicked
    function recordUserInteraction(topicId, userId, interactionType) {
        fetch('/interact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `topic_id=${topicId}&user_id=${userId}&interaction_type=${interactionType}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Interaction recorded successfully.');
            } else {
                console.log('Failed to record interaction.');
            }
        })
        .catch(error => {
            console.error('Error recording interaction:', error);
        });
    }

    // Fetch the articles from the backend and display the first one

    fetch('/get_articles')
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the data received from the server
        articles = data.articles; // Update the articles array
        displayArticle(currentIndex); // Display the first article
        
    })
    .catch(error => console.error('Error fetching articles:', error));
  
});
