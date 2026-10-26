const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

const Reviews = require('./review');
const Dealerships = require('./dealership');

mongoose.connect('mongodb://mongo_db:27017/', {
  dbName: 'dealershipsDB'
});

async function initializeData() {
  try {
    const dataDir = path.join(__dirname, 'data');
    const reviewsData = JSON.parse(
      fs.readFileSync(path.join(dataDir, 'reviews.json'), 'utf8')
    );
    const dealershipsData = JSON.parse(
      fs.readFileSync(path.join(dataDir, 'dealerships.json'), 'utf8')
    );

    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);
    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);

    console.log('Sample data loaded successfully');
  } catch (error) {
    console.error('Error loading sample data:', error.message);
  }
}

mongoose.connection.once('open', initializeData);

app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

app.get('/fetchReviews', async (req, res) => {
  try {
    res.json(await Reviews.find());
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    res.json(await Reviews.find({ dealership: Number(req.params.id) }));
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

app.get('/fetchDealers', async (req, res) => {
  try {
    res.json(await Dealerships.find());
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const documents = await Dealerships.find({
      state: { $regex: `^${state}$`, $options: 'i' }
    });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealerships.findOne({
      id: Number(req.params.id)
    });

    if (!dealer) {
      return res.status(404).json({ error: 'Dealership not found' });
    }

    res.json(dealer);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership details' });
  }
});

app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;
    const latestReview = await Reviews.findOne().sort({ id: -1 });
    const newId = latestReview ? latestReview.id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year
    });

    res.status(201).json(await review.save());
  } catch (error) {
    console.error('Error inserting review:', error.message);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on port ${port}`);
});
