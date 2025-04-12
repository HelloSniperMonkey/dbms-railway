import { Sequelize } from 'sequelize';

// Initialize Sequelize with your database credentials
const sequelize = new Sequelize({
  dialect: 'mysql', // or 'postgres', 'sqlite', 'mariadb', etc.
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '3306'),
  username: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'railway_db',
  logging: console.log,
});

// Connection function for Next.js API routes
export async function connectToDatabase() {
  try {
    await sequelize.authenticate();
    console.log('Database connection established successfully');
    return sequelize;
  } catch (error) {
    console.error('Unable to connect to the database:', error);
    throw error;
  }
}

// Export the sequelize instance for models
export { sequelize };