import 'dotenv/config'; // Loads .env file
import app from './app.js'; // Note the .js extension

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
