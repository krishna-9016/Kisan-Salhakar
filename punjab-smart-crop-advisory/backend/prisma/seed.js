// The complete code for: backend/prisma/seed.js

import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('--- Start seeding database ---');

  // --- Clean up the database ---
  console.log('Deleting existing data...');
  await prisma.order.deleteMany();
  await prisma.farm.deleteMany();
  await prisma.farmer.deleteMany();
  await prisma.extensionOfficer.deleteMany();
  await prisma.buyer.deleteMany();
  console.log('✅ Existing data deleted.');

  // --- 1. Create an Extension Officer ---
  const officerPassword = await bcrypt.hash('password123', 10);
  const officer = await prisma.extensionOfficer.create({
    data: {
      email: 'officer@punjab.gov',
      name: 'Officer Singh',
      password: officerPassword,
    },
  });
  console.log(`✅ Created officer: ${officer.name}`);

  // --- 2. Create a Test Buyer ---
  const buyerPassword = await bcrypt.hash('password123', 10);
  const buyer = await prisma.buyer.create({
    data: {
      email: 'buyer@example.com',
      name: 'Test Buyer',
      password: buyerPassword,
    }
  });
  console.log(`✅ Created buyer: ${buyer.name}`);

  // --- 3. Create Farmers with YOUR Verified Twilio Numbers ---
  const farmer1 = await prisma.farmer.create({
    data: {
      name: 'Ranjit Singh (DB)',
      // IMPORTANT: REPLACE THIS WITH YOUR OWN VERIFIED NUMBER
      phone: '+919016988925', 
      district: 'Ludhiana',
      farms: { create: [{ plotGeoJson: {} }] },
    },
  });
  console.log(`✅ Created farmer: ${farmer1.name} in ${farmer1.district}`);

  const farmer2 = await prisma.farmer.create({
    data: {
      name: 'Gurpreet Kaur (DB)',
      // IMPORTANT: REPLACE THIS WITH YOUR OWN VERIFIED NUMBER
      phone: '+919727645016', 
      district: 'Amritsar',
      farms: { create: [{ plotGeoJson: {} }] },
    },
  });
  console.log(`✅ Created farmer: ${farmer2.name} in ${farmer2.district}`);
  
  console.log('--- Seeding finished successfully! ---');
}

main()
  .catch((e) => {
    console.error('❗️ Seeding script failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
