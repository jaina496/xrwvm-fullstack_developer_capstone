import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Header from '../Header/Header';

const DealerDetails = () => {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const dealerResponse = await fetch(`/djangoapp/get_dealer_details/${id}`);
        if (!dealerResponse.ok) {
          throw new Error('Could not load dealer details.');
        }

        const dealerData = await dealerResponse.json();
        setDealer(dealerData);

        const reviewsResponse = await fetch(`/djangoapp/get_dealer_reviews/${id}`);
        if (reviewsResponse.ok) {
          const reviewsData = await reviewsResponse.json();
          setReviews(Array.isArray(reviewsData) ? reviewsData : []);
        }
      } catch (err) {
        console.error(err);
        setError('Unable to load dealer details. Please try again.');
      }
    };

    loadData();
  }, [id]);

  return (
    <div>
      <Header />
      <main className="container mt-4">
        <Link to="/">← Back to Dealerships</Link>

        {error && <p role="alert">{error}</p>}
        {!dealer && !error && <p>Loading dealer details...</p>}

        {dealer && (
          <>
            <h2 className="mt-3">{dealer.full_name}</h2>
            <p><strong>Dealer ID:</strong> {dealer.id}</p>
            <p><strong>City:</strong> {dealer.city}</p>
            <p><strong>State:</strong> {dealer.state}</p>
            <p><strong>Address:</strong> {dealer.address}</p>
            <p><strong>ZIP:</strong> {dealer.zip}</p>

            <h3 className="mt-4">Customer Reviews</h3>
            {reviews.length === 0 ? (
              <p>No reviews yet for this dealership.</p>
            ) : (
              reviews.map((review, index) => (
                <article key={review.id || review._id || index} className="border rounded p-3 mb-3">
                  <p><strong>Reviewer:</strong> {review.name || review.reviewer || review.username || 'Customer'}</p>
                  <p><strong>Vehicle:</strong> {[review.car_make, review.car_model, review.car_year].filter(Boolean).join(' ') || 'Not specified'}</p>
                  <p>{review.review || review.review_text || review.comment || 'Review submitted.'}</p>
                </article>
              ))
            )}
          </>
        )}
      </main>
    </div>
  );
};

export default DealerDetails;
