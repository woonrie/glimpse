import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [link, setLink] = useState('');
  const [error, setError] = useState(null);
  const [blogPost, setBlogPost] = useState(null);

  const handleSubmit = () => {
    if (!link) {
      setError('Please enter a link');
    } else {
      setError(null);
      fetch('http://localhost:5000/glimpse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_link: link }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.code === 399) {
            setBlogPost(data.blog_post);
          } else if (data.code === 400) {
            setError('Invalid Link or ID');
          } else if (data.code === 401) {
            setError('Transcript not found at video');
          } else if (data.code === 402) {
            setError('OpenAI could not generate a blog');
          }
        });
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>glimpse</h1>
        <input
          type="text"
          placeholder="youtube video link"
          value={link}
          onChange={e => setLink(e.target.value)}
          className="link-input"
        />
        <button
          onClick={handleSubmit}
          className="submit-button"
        >
          Submit
        </button>
        {error && <p className="error">{error}</p>}
        {blogPost && <p className="blog-post">{blogPost}</p>}
      </header>
    </div>
  );
}

export default App;
