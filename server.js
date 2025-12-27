// import express from "express";
// import cors from "cors";
// import mysql from "mysql2";
// import dotenv from "dotenv";
// import bcrypt from "bcryptjs";
// import jwt from "jsonwebtoken";
// import axios from "axios";

// dotenv.config();
// const app = express();

// // ===============================
// //  CORS Configuration
// // ===============================
// app.use(
//   cors({
//     origin: ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"], 
//     methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
//     allowedHeaders: ["Content-Type", "Authorization"],
//     credentials: true
//   })
// );

// app.use(express.json());

// // ===============================
// //  MySQL Connection
// // ===============================
// const db = mysql.createConnection({
//   host: "localhost",
//   user: "root",
//   password: "koye20@%",
//   database: "crime_system",
// });

// db.connect((err) => {
//   if (err) {
//     console.error("❌ Database connection failed:", err);
//     process.exit(1);
//   } else {
//     console.log("✅ Connected to MySQL Database (crime_system)");
//   }
// });

// db.on('error', (err) => {
//   console.error('❌ Database error:', err);
//   if (err.code === 'PROTOCOL_CONNECTION_LOST') {
//     console.error('Database connection was closed.');
//   }
// });

// // ===============================
// //  JWT Secret
// // ===============================
// const JWT_SECRET = process.env.JWT_SECRET || "some_long_secret_key";

// // ===============================
// //  ML API Configuration
// // ===============================
// const ML_API_URL = "http://127.0.0.1:8000/predict";
// const ML_TIMEOUT = 15000;

// // ===============================
// //  Register Officer (Signup)
// // ===============================
// app.post("/api/auth/signup", (req, res) => {
//   const { name, badge_number, department, password } = req.body;

//   if (!name || !badge_number || !department || !password) {
//     return res.status(400).json({ error: "All fields are required" });
//   }

//   const checkSql = "SELECT * FROM officers WHERE badge_number = ?";
//   db.query(checkSql, [badge_number], (err, results) => {
//     if (err) {
//       console.error("Database error:", err);
//       return res.status(500).json({ error: "Database error" });
//     }

//     if (results.length > 0)
//       return res.status(400).json({ error: "Badge number already exists" });

//     const hashedPassword = bcrypt.hashSync(password, 10);
//     const sql =
//       "INSERT INTO officers (name, badge_number, department, password) VALUES (?, ?, ?, ?)";

//     db.query(sql, [name, badge_number, department, hashedPassword], (err) => {
//       if (err) {
//         console.error("Database error:", err);
//         return res.status(500).json({ error: "Database error" });
//       }
//       res.json({ message: "✅ Officer registered successfully" });
//     });
//   });
// });

// // ===============================
// //  Login Officer
// // ===============================
// app.post("/api/auth/login", (req, res) => {
//   const { badge_number, password } = req.body;

//   if (!badge_number || !password)
//     return res.status(400).json({ error: "All fields required" });

//   const sql = "SELECT * FROM officers WHERE badge_number = ?";
//   db.query(sql, [badge_number], (err, results) => {
//     if (err) {
//       console.error("Database error:", err);
//       return res.status(500).json({ error: "Database error" });
//     }
//     if (results.length === 0)
//       return res.status(401).json({ error: "Officer not found" });

//     const officer = results[0];
//     const isMatch = bcrypt.compareSync(password, officer.password);
//     if (!isMatch) return res.status(401).json({ error: "Invalid password" });

//     const token = jwt.sign(
//       { id: officer.id, badge_number: officer.badge_number },
//       JWT_SECRET,
//       { expiresIn: "1h" }
//     );

//     res.json({
//       message: "✅ Login successful",
//       token,
//       officer: {
//         id: officer.id,
//         name: officer.name,
//         badge_number: officer.badge_number,
//         department: officer.department,
//       },
//     });
//   });
// });

// // ===============================
// //  Report Crime (with ML support)
// // ===============================
// app.post("/api/report", async (req, res) => {
//   console.log("🔥 Received report request:", req.body);

//   const { officer_id, date_time, place, location, city, country, description } =
//     req.body;

//   if (!officer_id || !description) {
//     console.error("❌ Missing required fields");
//     return res.status(400).json({ error: "Missing required fields: officer_id and description" });
//   }

//   try {
//     console.log("🔗 Calling ML API at:", ML_API_URL);
    
//     const mlResponse = await axios.post(
//       ML_API_URL,
//       { description: description },
//       { 
//         timeout: ML_TIMEOUT,
//         headers: {
//           'Content-Type': 'application/json'
//         }
//       }
//     );

//     console.log("✅ ML API Response:", mlResponse.data);

//     const { crime_type, ipc_section } = mlResponse.data;

//     if (!crime_type || !ipc_section) {
//       console.error("❌ Invalid ML response format");
//       return res.status(500).json({ error: "Invalid response from ML model" });
//     }

//     const sql = `
//       INSERT INTO crime_reports 
//       (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
//       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
//     `;

//     db.query(
//       sql,
//       [
//         officer_id,
//         date_time || new Date().toISOString().slice(0, 19).replace('T', ' '),
//         place || "Unknown",
//         location || "Unknown",
//         city || "Unknown",
//         country || "India",
//         description,
//         crime_type,
//         ipc_section,
//       ],
//       (err, result) => {
//         if (err) {
//           console.error("❌ Database error:", err);
//           return res.status(500).json({ error: "Failed to save report to database" });
//         }
        
//         console.log("✅ Report saved successfully. ID:", result.insertId);
        
//         res.json({
//           message: "✅ Report saved successfully",
//           crime_type,
//           ipc_section,
//           report_id: result.insertId,
//           success: true
//         });
//       }
//     );
//   } catch (error) {
//     console.error("❌ Error details:", {
//       message: error.message,
//       code: error.code,
//       response: error.response?.data
//     });

//     if (error.code === 'ECONNREFUSED') {
//       return res.status(503).json({
//         error: "ML model is not running. Please start FastAPI server at http://127.0.0.1:8000",
//         details: "Run: uvicorn app:app --reload --port 8000"
//       });
//     }

//     if (error.code === 'ETIMEDOUT') {
//       return res.status(504).json({
//         error: "ML model request timed out. Please try again.",
//       });
//     }

//     if (error.response) {
//       return res.status(error.response.status).json({
//         error: "ML model returned an error",
//         details: error.response.data
//       });
//     }

//     res.status(500).json({
//       error: "Failed to process report",
//       details: error.message
//     });
//   }
// });

// // ===============================
// //  Fetch all Reports
// // ===============================
// app.get("/api/reports", (req, res) => {
//   const sql = `
//     SELECT 
//       r.id,
//       r.officer_id,
//       r.date_time,
//       r.place,
//       r.location,
//       r.city,
//       r.country,
//       r.description,
//       r.crime_type,
//       r.ipc_section,
//       o.name AS officer_name,
//       o.department
//     FROM crime_reports r
//     JOIN officers o ON r.officer_id = o.id
//     ORDER BY r.date_time DESC
//   `;
  
//   db.query(sql, (err, results) => {
//     if (err) {
//       console.error("❌ Database error:", err);
//       return res.status(500).json({ error: "Database error" });
//     }
//     res.json(results);
//   });
// });

// // ===============================
// //  Dashboard Statistics - FIXED FOR ACTUAL SCHEMA
// // ===============================
// app.get("/api/reports/stats", async (req, res) => {
//   console.log("\n📊 ============================================");
//   console.log("📊 Dashboard Stats Endpoint Called");
//   console.log("📊 ============================================");
//   console.log("📅 Current Date:", new Date().toLocaleString());

//   try {
//     // Promise-based query executor
//     const executeQuery = (queryName, sql, params = []) => {
//       return new Promise((resolve, reject) => {
//         console.log(`\n🔍 Executing: ${queryName}`);
//         const startTime = Date.now();
        
//         db.query(sql, params, (err, results) => {
//           const duration = Date.now() - startTime;
          
//           if (err) {
//             console.error(`❌ ${queryName} Error:`, err.message);
//             reject(err);
//           } else {
//             console.log(`✅ ${queryName} completed in ${duration}ms`);
//             console.log(`   Returned ${Array.isArray(results) ? results.length : 1} row(s)`);
//             resolve(results);
//           }
//         });
//       });
//     };

//     // Query 1: Overall Statistics (no status column, so all are "pending")
//     const statsSql = `
//       SELECT 
//         COUNT(*) as total,
//         COUNT(*) as pending,
//         0 as resolved,
//         SUM(CASE 
//           WHEN crime_type LIKE '%Murder%' 
//           OR crime_type LIKE '%Assault%' 
//           OR crime_type LIKE '%Robbery%' 
//           OR crime_type LIKE '%Rape%'
//           THEN 1 ELSE 0 
//         END) as high_priority
//       FROM crime_reports
//     `;

//     // Query 2: City Distribution (ALL TIME)
//     const citySql = `
//       SELECT 
//         city, 
//         COUNT(*) as count 
//       FROM crime_reports 
//       GROUP BY city
//       ORDER BY count DESC
//       LIMIT 10
//     `;

//     // Query 3: Crime Categories
//     const categorySql = `
//       SELECT 
//         crime_type, 
//         COUNT(*) as count 
//       FROM crime_reports 
//       GROUP BY crime_type
//       ORDER BY count DESC
//       LIMIT 10
//     `;

//     // Query 4: Recent Reports (mapping to available columns only)
//     const recentSql = `
//       SELECT 
//         r.id,
//         r.date_time as date,
//         r.crime_type as crimeType,
//         r.city,
//         r.location,
//         r.place,
//         r.ipc_section,
//         CASE 
//           WHEN r.crime_type LIKE '%Murder%' 
//           OR r.crime_type LIKE '%Assault%' 
//           OR r.crime_type LIKE '%Robbery%'
//           OR r.crime_type LIKE '%Rape%'
//           THEN 'high'
//           WHEN r.crime_type LIKE '%Theft%' 
//           OR r.crime_type LIKE '%Burglary%'
//           OR r.crime_type LIKE '%Kidnapping%'
//           THEN 'medium'
//           ELSE 'low'
//         END as severity,
//         'pending' as status
//       FROM crime_reports r
//       ORDER BY r.date_time DESC
//       LIMIT 10
//     `;

//     // Query 5: Monthly Trend (Last 6 months) - FIXED
//     const trendSql = `
//       SELECT 
//         DATE_FORMAT(date_time, '%b') as month,
//         YEAR(date_time) as year,
//         MONTH(date_time) as month_num,
//         COUNT(*) as count
//       FROM crime_reports
//       WHERE date_time >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
//       GROUP BY YEAR(date_time), MONTH(date_time), DATE_FORMAT(date_time, '%b')
//       ORDER BY year, month_num
//     `;

//     // Execute all queries in parallel
//     console.log("\n⏳ Executing all queries in parallel...");
//     const [statsResults, cityResults, categoryResults, recentResults, trendResults] = await Promise.all([
//       executeQuery("Overall Statistics", statsSql),
//       executeQuery("City Distribution", citySql),
//       executeQuery("Crime Categories", categorySql),
//       executeQuery("Recent Reports", recentSql),
//       executeQuery("Monthly Trend", trendSql)
//     ]);

//     console.log("\n📊 Processing Results...");

//     // Process results
//     const stats = statsResults[0];
//     console.log("📈 Stats:", stats);
    
//     // City intensity map
//     const byCityIntensity = {};
//     cityResults.forEach((row) => {
//       byCityIntensity[row.city] = row.count;
//     });
//     console.log("🏙️  Cities:", Object.keys(byCityIntensity).length);

//     // Category map
//     const byCategory = {};
//     categoryResults.forEach((row) => {
//       byCategory[row.crime_type] = row.count;
//     });
//     console.log("📋 Categories:", Object.keys(byCategory).length);

//     // Monthly trend map
//     const monthlyTrend = {};
//     trendResults.forEach((row) => {
//       monthlyTrend[row.month] = row.count;
//     });
//     console.log("📅 Months with data:", Object.keys(monthlyTrend).length);
//     console.log("📈 Recent Reports:", recentResults.length);

//     const response = {
//       totalCases: stats.total || 0,
//       pendingCases: stats.pending || 0,
//       resolvedCases: stats.resolved || 0,
//       highPriorityCases: stats.high_priority || 0,
//       byCityIntensity,
//       byCategory,
//       monthlyTrend,
//       recentReports: recentResults
//     };

//     console.log("\n✅ ============================================");
//     console.log("✅ Response Summary:");
//     console.log(`   Total Cases: ${response.totalCases}`);
//     console.log(`   Pending: ${response.pendingCases}`);
//     console.log(`   Resolved: ${response.resolvedCases}`);
//     console.log(`   High Priority: ${response.highPriorityCases}`);
//     console.log(`   Cities: ${Object.keys(response.byCityIntensity).length}`);
//     console.log(`   Categories: ${Object.keys(response.byCategory).length}`);
//     console.log(`   Monthly Data Points: ${Object.keys(response.monthlyTrend).length}`);
//     console.log(`   Recent Reports: ${response.recentReports.length}`);
//     console.log("✅ ============================================\n");

//     res.json(response);

//   } catch (error) {
//     console.error("\n❌ ============================================");
//     console.error("❌ Stats Endpoint FATAL Error:");
//     console.error("❌ ============================================");
//     console.error("Error Message:", error.message);
//     console.error("Error Stack:", error.stack);
//     console.error("❌ ============================================\n");
    
//     res.status(500).json({ 
//       error: "Failed to fetch statistics",
//       details: error.message,
//       hint: "Check server console for detailed error logs"
//     });
//   }
// });

// // ===============================
// //  Health Check
// // ===============================
// app.get("/", (req, res) => {
//   res.json({ 
//     message: "✅ Crime Classification Backend API is running!",
//     timestamp: new Date().toISOString(),
//     endpoints: {
//       auth: ["/api/auth/signup", "/api/auth/login"],
//       reports: ["/api/report", "/api/reports", "/api/reports/stats"],
//       debug: ["/api/debug/count", "/api/debug/sample", "/api/debug/schema"]
//     }
//   });
// });

// // ===============================
// //  DEBUG: Check database records count
// // ===============================
// app.get("/api/debug/count", (req, res) => {
//   console.log("🔍 Debug: Checking total records...");
//   db.query("SELECT COUNT(*) as total FROM crime_reports", (err, results) => {
//     if (err) {
//       console.error("❌ Debug error:", err);
//       return res.status(500).json({ error: err.message });
//     }
//     const total = results[0].total;
//     console.log(`✅ Total records in database: ${total}`);
//     res.json({ 
//       totalRecords: total,
//       message: total === 0 ? "⚠️ No records in database!" : `✅ Found ${total} records`,
//       timestamp: new Date().toISOString()
//     });
//   });
// });

// // ===============================
// //  DEBUG: Get sample data
// // ===============================
// app.get("/api/debug/sample", (req, res) => {
//   console.log("🔍 Debug: Fetching sample data...");
//   db.query("SELECT * FROM crime_reports LIMIT 5", (err, results) => {
//     if (err) {
//       console.error("❌ Debug error:", err);
//       return res.status(500).json({ error: err.message });
//     }
//     console.log(`✅ Retrieved ${results.length} sample records`);
//     res.json({ 
//       count: results.length,
//       samples: results,
//       timestamp: new Date().toISOString()
//     });
//   });
// });

// // ===============================
// //  DEBUG: Check table schema
// // ===============================
// app.get("/api/debug/schema", (req, res) => {
//   console.log("🔍 Debug: Checking table schema...");
//   db.query("DESCRIBE crime_reports", (err, results) => {
//     if (err) {
//       console.error("❌ Debug error:", err);
//       return res.status(500).json({ error: err.message });
//     }
//     console.log(`✅ Table schema retrieved`);
//     res.json({ 
//       columns: results,
//       timestamp: new Date().toISOString()
//     });
//   });
// });

// // ===============================
// //  Error Handler Middleware
// // ===============================
// app.use((err, req, res, next) => {
//   console.error("❌ Unhandled error:", err);
//   res.status(500).json({
//     error: "Internal server error",
//     details: err.message,
//     timestamp: new Date().toISOString()
//   });
// });

// // ===============================
// //  Start Server
// // ===============================
// const PORT = process.env.PORT || 5000;
// app.listen(PORT, () => {
//   console.log("\n🎉 ============================================");
//   console.log("🚀 Backend Server Started Successfully!");
//   console.log("============================================");
//   console.log(`📡 Server URL: http://localhost:${PORT}`);
//   console.log(`📊 Dashboard Stats: http://localhost:${PORT}/api/reports/stats`);
//   console.log(`🔍 Debug Count: http://localhost:${PORT}/api/debug/count`);
//   console.log(`🔍 Debug Sample: http://localhost:${PORT}/api/debug/sample`);
//   console.log(`🔍 Debug Schema: http://localhost:${PORT}/api/debug/schema`);
//   console.log(`🤖 ML API URL: ${ML_API_URL}`);
//   console.log("============================================\n");
// });

//// FINAL

// import express from "express";
// import cors from "cors";
// import mysql from "mysql2";
// import dotenv from "dotenv";
// import bcrypt from "bcryptjs";
// import jwt from "jsonwebtoken";
// import axios from "axios";

// dotenv.config();
// const app = express();

// // ===============================
// //  CORS Configuration
// // ===============================
// app.use(
//   cors({
//     origin: ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"], 
//     methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
//     allowedHeaders: ["Content-Type", "Authorization"],
//     credentials: true
//   })
// );

// app.use(express.json());

// // ===============================
// //  MySQL Connection
// // ===============================
// const db = mysql.createConnection({
//   host: "localhost",
//   user: "root",
//   password: "koye20@%",
//   database: "crime_system",
// });

// db.connect((err) => {
//   if (err) {
//     console.error("❌ Database connection failed:", err);
//     process.exit(1);
//   } else {
//     console.log("✅ Connected to MySQL Database (crime_system)");
//   }
// });

// db.on('error', (err) => {
//   console.error('❌ Database error:', err);
//   if (err.code === 'PROTOCOL_CONNECTION_LOST') {
//     console.error('Database connection was closed.');
//   }
// });

// // ===============================
// //  JWT Secret
// // ===============================
// const JWT_SECRET = process.env.JWT_SECRET || "some_long_secret_key";

// // ===============================
// //  ML API Configuration
// // ===============================
// const ML_API_URL = "http://127.0.0.1:8000/predict";
// const ML_TIMEOUT = 15000;

// // ===============================
// //  Register Officer (Signup)
// // ===============================
// app.post("/api/auth/signup", (req, res) => {
//   const { name, badge_number, department, password } = req.body;

//   if (!name || !badge_number || !department || !password) {
//     return res.status(400).json({ error: "All fields are required" });
//   }

//   const checkSql = "SELECT * FROM officers WHERE badge_number = ?";
//   db.query(checkSql, [badge_number], (err, results) => {
//     if (err) {
//       console.error("Database error:", err);
//       return res.status(500).json({ error: "Database error" });
//     }

//     if (results.length > 0)
//       return res.status(400).json({ error: "Badge number already exists" });

//     const hashedPassword = bcrypt.hashSync(password, 10);
//     const sql =
//       "INSERT INTO officers (name, badge_number, department, password) VALUES (?, ?, ?, ?)";

//     db.query(sql, [name, badge_number, department, hashedPassword], (err) => {
//       if (err) {
//         console.error("Database error:", err);
//         return res.status(500).json({ error: "Database error" });
//       }
//       res.json({ message: "✅ Officer registered successfully" });
//     });
//   });
// });

// // ===============================
// //  Login Officer
// // ===============================
// app.post("/api/auth/login", (req, res) => {
//   const { badge_number, password } = req.body;

//   if (!badge_number || !password)
//     return res.status(400).json({ error: "All fields required" });

//   const sql = "SELECT * FROM officers WHERE badge_number = ?";
//   db.query(sql, [badge_number], (err, results) => {
//     if (err) {
//       console.error("Database error:", err);
//       return res.status(500).json({ error: "Database error" });
//     }
//     if (results.length === 0)
//       return res.status(401).json({ error: "Officer not found" });

//     const officer = results[0];
//     const isMatch = bcrypt.compareSync(password, officer.password);
//     if (!isMatch) return res.status(401).json({ error: "Invalid password" });

//     const token = jwt.sign(
//       { id: officer.id, badge_number: officer.badge_number },
//       JWT_SECRET,
//       { expiresIn: "1h" }
//     );

//     res.json({
//       message: "✅ Login successful",
//       token,
//       officer: {
//         id: officer.id,
//         name: officer.name,
//         badge_number: officer.badge_number,
//         department: officer.department,
//       },
//     });
//   });
// });

// // ===============================
// //  Report Crime (with ML support)
// // ===============================
// app.post("/api/report", async (req, res) => {
//   console.log("🔥 Received report request:", req.body);

//   const { officer_id, date_time, place, location, city, country, description } =
//     req.body;

//   if (!officer_id || !description) {
//     console.error("❌ Missing required fields");
//     return res.status(400).json({ error: "Missing required fields: officer_id and description" });
//   }

//   try {
//     console.log("🔗 Calling ML API at:", ML_API_URL);
    
//     const mlResponse = await axios.post(
//       ML_API_URL,
//       { description: description },
//       { 
//         timeout: ML_TIMEOUT,
//         headers: {
//           'Content-Type': 'application/json'
//         }
//       }
//     );

//     console.log("✅ ML API Response:", mlResponse.data);

//     const { crime_type, ipc_section } = mlResponse.data;

//     if (!crime_type || !ipc_section) {
//       console.error("❌ Invalid ML response format");
//       return res.status(500).json({ error: "Invalid response from ML model" });
//     }

//     const sql = `
//       INSERT INTO crime_reports 
//       (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
//       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
//     `;

//     db.query(
//       sql,
//       [
//         officer_id,
//         date_time || new Date().toISOString().slice(0, 19).replace('T', ' '),
//         place || "Unknown",
//         location || "Unknown",
//         city || "Unknown",
//         country || "India",
//         description,
//         crime_type,
//         ipc_section,
//       ],
//       (err, result) => {
//         if (err) {
//           console.error("❌ Database error:", err);
//           return res.status(500).json({ error: "Failed to save report to database" });
//         }
        
//         console.log("✅ Report saved successfully. ID:", result.insertId);
        
//         res.json({
//           message: "✅ Report saved successfully",
//           crime_type,
//           ipc_section,
//           report_id: result.insertId,
//           success: true
//         });
//       }
//     );
//   } catch (error) {
//     console.error("❌ Error details:", {
//       message: error.message,
//       code: error.code,
//       response: error.response?.data
//     });

//     if (error.code === 'ECONNREFUSED') {
//       return res.status(503).json({
//         error: "ML model is not running. Please start FastAPI server at http://127.0.0.1:8000",
//         details: "Run: uvicorn app:app --reload --port 8000"
//       });
//     }

//     if (error.code === 'ETIMEDOUT') {
//       return res.status(504).json({
//         error: "ML model request timed out. Please try again.",
//       });
//     }

//     if (error.response) {
//       return res.status(error.response.status).json({
//         error: "ML model returned an error",
//         details: error.response.data
//       });
//     }

//     res.status(500).json({
//       error: "Failed to process report",
//       details: error.message
//     });
//   }
// });

// // ===============================
// //  Fetch all Reports
// // ===============================
// app.get("/api/reports", (req, res) => {
//   const sql = `
//     SELECT 
//       r.id,
//       r.officer_id,
//       r.date_time,
//       r.place,
//       r.location,
//       r.city,
//       r.country,
//       r.description,
//       r.crime_type,
//       r.ipc_section,
//       o.name AS officer_name,
//       o.department
//     FROM crime_reports r
//     JOIN officers o ON r.officer_id = o.id
//     ORDER BY r.date_time DESC
//   `;
  
//   db.query(sql, (err, results) => {
//     if (err) {
//       console.error("❌ Database error:", err);
//       return res.status(500).json({ error: "Database error" });
//     }
//     res.json(results);
//   });
// });

// // ===============================
// //  Dashboard Statistics - FIXED
// // ===============================
// app.get("/api/reports/stats", async (req, res) => {
//   console.log("\n📊 ============================================");
//   console.log("📊 Dashboard Stats Endpoint Called");
//   console.log("📊 ============================================");
//   console.log("📅 Current Date:", new Date().toLocaleString());

//   try {
//     // Promise-based query executor
//     const executeQuery = (queryName, sql, params = []) => {
//       return new Promise((resolve, reject) => {
//         console.log(`\n🔍 Executing: ${queryName}`);
//         const startTime = Date.now();
        
//         db.query(sql, params, (err, results) => {
//           const duration = Date.now() - startTime;
          
//           if (err) {
//             console.error(`❌ ${queryName} Error:`, err.message);
//             reject(err);
//           } else {
//             console.log(`✅ ${queryName} completed in ${duration}ms`);
//             console.log(`   Returned ${Array.isArray(results) ? results.length : 1} row(s)`);
//             resolve(results);
//           }
//         });
//       });
//     };

//     // Query 1: Overall Statistics - REMOVED HIGH PRIORITY
//     const statsSql = `
//       SELECT 
//         COUNT(*) as total,
//         COUNT(*) as pending,
//         0 as resolved
//       FROM crime_reports
//     `;

//     // Query 2: City Distribution
//     const citySql = `
//       SELECT 
//         city, 
//         COUNT(*) as count 
//       FROM crime_reports 
//       WHERE city IS NOT NULL AND city != ''
//       GROUP BY city
//       ORDER BY count DESC
//       LIMIT 10
//     `;

//     // Query 3: Crime Categories
//     const categorySql = `
//       SELECT 
//         crime_type, 
//         COUNT(*) as count 
//       FROM crime_reports 
//       WHERE crime_type IS NOT NULL AND crime_type != ''
//       GROUP BY crime_type
//       ORDER BY count DESC
//       LIMIT 10
//     `;

//     // Query 4: Recent Reports
//     const recentSql = `
//       SELECT 
//         r.id,
//         r.date_time as date,
//         r.crime_type as crimeType,
//         r.city,
//         r.location,
//         r.place,
//         r.ipc_section,
//         CASE 
//           WHEN r.crime_type LIKE '%Murder%' 
//           OR r.crime_type LIKE '%Assault%' 
//           OR r.crime_type LIKE '%Robbery%'
//           OR r.crime_type LIKE '%Rape%'
//           THEN 'high'
//           WHEN r.crime_type LIKE '%Theft%' 
//           OR r.crime_type LIKE '%Burglary%'
//           OR r.crime_type LIKE '%Kidnapping%'
//           THEN 'medium'
//           ELSE 'low'
//         END as severity,
//         'pending' as status
//       FROM crime_reports r
//       ORDER BY r.date_time DESC
//       LIMIT 10
//     `;

//     // Query 5: Monthly Trend (Last 6 months)
//     const trendSql = `
//       SELECT 
//         DATE_FORMAT(date_time, '%b') as month,
//         YEAR(date_time) as year,
//         MONTH(date_time) as month_num,
//         COUNT(*) as count
//       FROM crime_reports
//       WHERE date_time >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
//       GROUP BY YEAR(date_time), MONTH(date_time), DATE_FORMAT(date_time, '%b')
//       ORDER BY year, month_num
//     `;

//     // Execute all queries in parallel
//     console.log("\n⏳ Executing all queries in parallel...");
//     const [statsResults, cityResults, categoryResults, recentResults, trendResults] = await Promise.all([
//       executeQuery("Overall Statistics", statsSql),
//       executeQuery("City Distribution", citySql),
//       executeQuery("Crime Categories", categorySql),
//       executeQuery("Recent Reports", recentSql),
//       executeQuery("Monthly Trend", trendSql)
//     ]);

//     console.log("\n📊 Processing Results...");

//     // Process results
//     const stats = statsResults[0];
//     console.log("📈 Stats:", stats);
    
//     // City intensity map
//     const byCityIntensity = {};
//     cityResults.forEach((row) => {
//       byCityIntensity[row.city] = row.count;
//     });
//     console.log("🏙️ Cities:", Object.keys(byCityIntensity).length);

//     // Category map
//     const byCategory = {};
//     categoryResults.forEach((row) => {
//       byCategory[row.crime_type] = row.count;
//     });
//     console.log("📋 Categories:", Object.keys(byCategory).length);

//     // Monthly trend map
//     const monthlyTrend = {};
//     trendResults.forEach((row) => {
//       monthlyTrend[row.month] = row.count;
//     });
//     console.log("📅 Months with data:", Object.keys(monthlyTrend).length);
//     console.log("📈 Recent Reports:", recentResults.length);

//     const response = {
//       totalCases: stats.total || 0,
//       pendingCases: stats.pending || 0,
//       resolvedCases: stats.resolved || 0,
//       highPriorityCases: 0,
//       byCityIntensity,
//       byCategory,
//       monthlyTrend,
//       recentReports: recentResults
//     };

//     console.log("\n✅ ============================================");
//     console.log("✅ Response Summary:");
//     console.log(`   Total Cases: ${response.totalCases}`);
//     console.log(`   Pending: ${response.pendingCases}`);
//     console.log(`   Resolved: ${response.resolvedCases}`);
//     console.log(`   High Priority: ${response.highPriorityCases}`);
//     console.log(`   Cities: ${Object.keys(response.byCityIntensity).length}`);
//     console.log(`   Categories: ${Object.keys(response.byCategory).length}`);
//     console.log(`   Monthly Data Points: ${Object.keys(response.monthlyTrend).length}`);
//     console.log(`   Recent Reports: ${response.recentReports.length}`);
//     console.log("✅ ============================================\n");

//     res.json(response);

//   } catch (error) {
//     console.error("\n❌ ============================================");
//     console.error("❌ Stats Endpoint FATAL Error:");
//     console.error("❌ ============================================");
//     console.error("Error Message:", error.message);
//     console.error("Error Stack:", error.stack);
//     console.error("❌ ============================================\n");
    
//     res.status(500).json({ 
//       error: "Failed to fetch statistics",
//       details: error.message,
//       hint: "Check server console for detailed error logs"
//     });
//   }
// });

// // ===============================
// //  Health Check
// // ===============================
// app.get("/", (req, res) => {
//   res.json({ 
//     message: "✅ Crime Classification Backend API is running!",
//     timestamp: new Date().toISOString(),
//     endpoints: {
//       auth: ["/api/auth/signup", "/api/auth/login"],
//       reports: ["/api/report", "/api/reports", "/api/reports/stats"],
//       debug: ["/api/debug/count", "/api/debug/sample", "/api/debug/schema"]
//     }
//   });
// });

// // ===============================
// //  DEBUG: Check database records count
// // ===============================
// app.get("/api/debug/count", (req, res) => {
//   console.log("🔍 Debug: Checking total records...");
//   db.query("SELECT COUNT(*) as total FROM crime_reports", (err, results) => {
//     if (err) {
//       console.error("❌ Debug error:", err);
//       return res.status(500).json({ error: err.message });
//     }
//     const total = results[0].total;
//     console.log(`✅ Total records in database: ${total}`);
//     res.json({ 
//       totalRecords: total,
//       message: total === 0 ? "⚠️ No records in database!" : `✅ Found ${total} records`,
//       timestamp: new Date().toISOString()
//     });
//   });
// });

// // ===============================
// //  DEBUG: Get sample data
// // ===============================
// app.get("/api/debug/sample", (req, res) => {
//   console.log("🔍 Debug: Fetching sample data...");
//   db.query("SELECT * FROM crime_reports LIMIT 5", (err, results) => {
//     if (err) {
//       console.error("❌ Debug error:", err);
//       return res.status(500).json({ error: err.message });
//     }
//     console.log(`✅ Retrieved ${results.length} sample records`);
//     res.json({ 
//       count: results.length,
//       samples: results,
//       timestamp: new Date().toISOString()
//     });
//   });
// });

// // ===============================
// //  DEBUG: Check table schema
// // ===============================
// app.get("/api/debug/schema", (req, res) => {
//   console.log("🔍 Debug: Checking table schema...");
//   db.query("DESCRIBE crime_reports", (err, results) => {
//     if (err) {
//       console.error("❌ Debug error:", err);
//       return res.status(500).json({ error: err.message });
//     }
//     console.log(`✅ Table schema retrieved`);
//     res.json({ 
//       columns: results,
//       timestamp: new Date().toISOString()
//     });
//   });
// });

// // ===============================
// //  Error Handler Middleware
// // ===============================
// app.use((err, req, res, next) => {
//   console.error("❌ Unhandled error:", err);
//   res.status(500).json({
//     error: "Internal server error",
//     details: err.message,
//     timestamp: new Date().toISOString()
//   });
// });

// // ===============================
// //  Start Server
// // ===============================
// const PORT = process.env.PORT || 5000;
// app.listen(PORT, () => {
//   console.log("\n🎉 ============================================");
//   console.log("🚀 Backend Server Started Successfully!");
//   console.log("============================================");
//   console.log(`📡 Server URL: http://localhost:${PORT}`);
//   console.log(`📊 Dashboard Stats: http://localhost:${PORT}/api/reports/stats`);
//   console.log(`🔍 Debug Count: http://localhost:${PORT}/api/debug/count`);
//   console.log(`🔍 Debug Sample: http://localhost:${PORT}/api/debug/sample`);
//   console.log(`🔍 Debug Schema: http://localhost:${PORT}/api/debug/schema`);
//   console.log(`🤖 ML API URL: ${ML_API_URL}`);
//   console.log("============================================\n");
// });



import express from "express";
import cors from "cors";
import mysql from "mysql2";
import dotenv from "dotenv";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import axios from "axios";

dotenv.config();
const app = express();

// ===============================
//  CORS Configuration
// ===============================
app.use(
  cors({
    origin: ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"], 
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization"],
    credentials: true
  })
);

app.use(express.json());

// ===============================
//  MySQL Connection
// ===============================
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "koye20@%",
  database: "crime_system",
});

db.connect((err) => {
  if (err) {
    console.error("❌ Database connection failed:", err);
    process.exit(1);
  } else {
    console.log("✅ Connected to MySQL Database (crime_system)");
  }
});

db.on('error', (err) => {
  console.error('❌ Database error:', err);
  if (err.code === 'PROTOCOL_CONNECTION_LOST') {
    console.error('Database connection was closed.');
  }
});

// ===============================
//  JWT Secret
// ===============================
const JWT_SECRET = process.env.JWT_SECRET || "some_long_secret_key";

// ===============================
//  ML API Configuration
// ===============================
const ML_API_URL = "http://127.0.0.1:8000/predict";
const ML_TIMEOUT = 15000;

// ===============================
//  Register Officer (Signup)
// ===============================
app.post("/api/auth/signup", (req, res) => {
  const { name, badge_number, department, password } = req.body;

  if (!name || !badge_number || !department || !password) {
    return res.status(400).json({ error: "All fields are required" });
  }

  const checkSql = "SELECT * FROM officers WHERE badge_number = ?";
  db.query(checkSql, [badge_number], (err, results) => {
    if (err) {
      console.error("Database error:", err);
      return res.status(500).json({ error: "Database error" });
    }

    if (results.length > 0)
      return res.status(400).json({ error: "Badge number already exists" });

    const hashedPassword = bcrypt.hashSync(password, 10);
    const sql =
      "INSERT INTO officers (name, badge_number, department, password) VALUES (?, ?, ?, ?)";

    db.query(sql, [name, badge_number, department, hashedPassword], (err) => {
      if (err) {
        console.error("Database error:", err);
        return res.status(500).json({ error: "Database error" });
      }
      res.json({ message: "✅ Officer registered successfully" });
    });
  });
});

// ===============================
//  Login Officer
// ===============================
app.post("/api/auth/login", (req, res) => {
  const { badge_number, password } = req.body;

  if (!badge_number || !password)
    return res.status(400).json({ error: "All fields required" });

  const sql = "SELECT * FROM officers WHERE badge_number = ?";
  db.query(sql, [badge_number], (err, results) => {
    if (err) {
      console.error("Database error:", err);
      return res.status(500).json({ error: "Database error" });
    }
    if (results.length === 0)
      return res.status(401).json({ error: "Officer not found" });

    const officer = results[0];
    const isMatch = bcrypt.compareSync(password, officer.password);
    if (!isMatch) return res.status(401).json({ error: "Invalid password" });

    const token = jwt.sign(
      { id: officer.id, badge_number: officer.badge_number },
      JWT_SECRET,
      { expiresIn: "1h" }
    );

    res.json({
      message: "✅ Login successful",
      token,
      officer: {
        id: officer.id,
        name: officer.name,
        badge_number: officer.badge_number,
        department: officer.department,
      },
    });
  });
});

// ===============================
//  Report Crime (with ML support)
// ===============================
app.post("/api/report", async (req, res) => {
  console.log("📥 Received report request:", req.body);

  const { officer_id, date_time, place, location, city, country, description } =
    req.body;

  if (!officer_id || !description) {
    console.error("❌ Missing required fields");
    return res.status(400).json({ error: "Missing required fields: officer_id and description" });
  }

  try {
    console.log("🔗 Calling ML API at:", ML_API_URL);
    
    const mlResponse = await axios.post(
      ML_API_URL,
      { description: description },
      { 
        timeout: ML_TIMEOUT,
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    console.log("✅ ML API Response:", mlResponse.data);

    const { crime_type, ipc_section } = mlResponse.data;

    if (!crime_type || !ipc_section) {
      console.error("❌ Invalid ML response format");
      return res.status(500).json({ error: "Invalid response from ML model" });
    }

    const sql = `
      INSERT INTO crime_reports 
      (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    `;

    db.query(
      sql,
      [
        officer_id,
        date_time || new Date().toISOString().slice(0, 19).replace('T', ' '),
        place || "Unknown",
        location || "Unknown",
        city || "Unknown",
        country || "India",
        description,
        crime_type,
        ipc_section,
      ],
      (err, result) => {
        if (err) {
          console.error("❌ Database error:", err);
          return res.status(500).json({ error: "Failed to save report to database" });
        }
        
        console.log("✅ Report saved successfully. ID:", result.insertId);
        
        res.json({
          message: "✅ Report saved successfully",
          crime_type,
          ipc_section,
          report_id: result.insertId,
          success: true
        });
      }
    );
  } catch (error) {
    console.error("❌ Error details:", {
      message: error.message,
      code: error.code,
      response: error.response?.data
    });

    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        error: "ML model is not running. Please start FastAPI server at http://127.0.0.1:8000",
        details: "Run: uvicorn app:app --reload --port 8000"
      });
    }

    if (error.code === 'ETIMEDOUT') {
      return res.status(504).json({
        error: "ML model request timed out. Please try again.",
      });
    }

    if (error.response) {
      return res.status(error.response.status).json({
        error: "ML model returned an error",
        details: error.response.data
      });
    }

    res.status(500).json({
      error: "Failed to process report",
      details: error.message
    });
  }
});

// ===============================
//  🆕 NEW: Mark Report as Resolved
// ===============================
app.put("/api/reports/:id/status", (req, res) => {
  const reportId = req.params.id;
  const { status } = req.body;

  console.log(`🔄 Updating report #${reportId} status to: ${status}`);

  if (!status) {
    return res.status(400).json({ error: "Status is required" });
  }

  if (status !== "resolved" && status !== "pending" && status !== "investigating") {
    return res.status(400).json({ error: "Invalid status value" });
  }

  const sql = "UPDATE crime_reports SET status = ? WHERE id = ?";

  db.query(sql, [status, reportId], (err, result) => {
    if (err) {
      console.error("❌ Database error:", err);
      return res.status(500).json({ error: "Failed to update status" });
    }

    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Report not found" });
    }

    console.log(`✅ Report #${reportId} status updated successfully`);

    res.json({
      message: "✅ Status updated successfully",
      reportId: reportId,
      newStatus: status,
      success: true
    });
  });
});

// ===============================
//  Fetch all Reports
// ===============================
app.get("/api/reports", (req, res) => {
  const sql = `
    SELECT 
      r.id,
      r.officer_id,
      r.date_time,
      r.place,
      r.location,
      r.city,
      r.country,
      r.description,
      r.crime_type,
      r.ipc_section,
      r.status,
      o.name AS officer_name,
      o.department
    FROM crime_reports r
    JOIN officers o ON r.officer_id = o.id
    ORDER BY r.date_time DESC
  `;
  
  db.query(sql, (err, results) => {
    if (err) {
      console.error("❌ Database error:", err);
      return res.status(500).json({ error: "Database error" });
    }
    res.json(results);
  });
});

// ===============================
//  Dashboard Statistics - UPDATED
// ===============================
app.get("/api/reports/stats", async (req, res) => {
  console.log("\n📊 ============================================");
  console.log("📊 Dashboard Stats Endpoint Called");
  console.log("📊 ============================================");
  console.log("📅 Current Date:", new Date().toLocaleString());

  try {
    const executeQuery = (queryName, sql, params = []) => {
      return new Promise((resolve, reject) => {
        console.log(`\n🔍 Executing: ${queryName}`);
        const startTime = Date.now();
        
        db.query(sql, params, (err, results) => {
          const duration = Date.now() - startTime;
          
          if (err) {
            console.error(`❌ ${queryName} Error:`, err.message);
            reject(err);
          } else {
            console.log(`✅ ${queryName} completed in ${duration}ms`);
            console.log(`   Returned ${Array.isArray(results) ? results.length : 1} row(s)`);
            resolve(results);
          }
        });
      });
    };

    // Query 1: Overall Statistics with status tracking
    const statsSql = `
      SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'pending' OR status IS NULL THEN 1 ELSE 0 END) as pending,
        SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) as resolved
      FROM crime_reports
    `;

    const citySql = `
      SELECT 
        city, 
        COUNT(*) as count 
      FROM crime_reports 
      WHERE city IS NOT NULL AND city != ''
      GROUP BY city
      ORDER BY count DESC
      LIMIT 10
    `;

    const categorySql = `
      SELECT 
        crime_type, 
        COUNT(*) as count 
      FROM crime_reports 
      WHERE crime_type IS NOT NULL AND crime_type != ''
      GROUP BY crime_type
      ORDER BY count DESC
      LIMIT 10
    `;

    const recentSql = `
      SELECT 
        r.id,
        r.date_time as date,
        r.crime_type as crimeType,
        r.city,
        r.location,
        r.place,
        r.ipc_section,
        COALESCE(r.status, 'pending') as status,
        CASE 
          WHEN r.crime_type LIKE '%Murder%' 
          OR r.crime_type LIKE '%Assault%' 
          OR r.crime_type LIKE '%Robbery%'
          OR r.crime_type LIKE '%Rape%'
          THEN 'high'
          WHEN r.crime_type LIKE '%Theft%' 
          OR r.crime_type LIKE '%Burglary%'
          OR r.crime_type LIKE '%Kidnapping%'
          THEN 'medium'
          ELSE 'low'
        END as severity
      FROM crime_reports r
      ORDER BY r.date_time DESC
      LIMIT 10
    `;

    const trendSql = `
      SELECT 
        DATE_FORMAT(date_time, '%b') as month,
        YEAR(date_time) as year,
        MONTH(date_time) as month_num,
        COUNT(*) as count
      FROM crime_reports
      WHERE date_time >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
      GROUP BY YEAR(date_time), MONTH(date_time), DATE_FORMAT(date_time, '%b')
      ORDER BY year, month_num
    `;

    console.log("\n⏳ Executing all queries in parallel...");
    const [statsResults, cityResults, categoryResults, recentResults, trendResults] = await Promise.all([
      executeQuery("Overall Statistics", statsSql),
      executeQuery("City Distribution", citySql),
      executeQuery("Crime Categories", categorySql),
      executeQuery("Recent Reports", recentSql),
      executeQuery("Monthly Trend", trendSql)
    ]);

    console.log("\n📊 Processing Results...");

    const stats = statsResults[0];
    console.log("📈 Stats:", stats);
    
    const byCityIntensity = {};
    cityResults.forEach((row) => {
      byCityIntensity[row.city] = row.count;
    });
    console.log("🏙️ Cities:", Object.keys(byCityIntensity).length);

    const byCategory = {};
    categoryResults.forEach((row) => {
      byCategory[row.crime_type] = row.count;
    });
    console.log("📋 Categories:", Object.keys(byCategory).length);

    const monthlyTrend = {};
    trendResults.forEach((row) => {
      monthlyTrend[row.month] = row.count;
    });
    console.log("📅 Months with data:", Object.keys(monthlyTrend).length);
    console.log("📈 Recent Reports:", recentResults.length);

    const response = {
      totalCases: stats.total || 0,
      pendingCases: stats.pending || 0,
      resolvedCases: stats.resolved || 0,
      highPriorityCases: 0,
      byCityIntensity,
      byCategory,
      monthlyTrend,
      recentReports: recentResults
    };

    console.log("\n✅ ============================================");
    console.log("✅ Response Summary:");
    console.log(`   Total Cases: ${response.totalCases}`);
    console.log(`   Pending: ${response.pendingCases}`);
    console.log(`   Resolved: ${response.resolvedCases}`);
    console.log(`   Cities: ${Object.keys(response.byCityIntensity).length}`);
    console.log(`   Categories: ${Object.keys(response.byCategory).length}`);
    console.log(`   Monthly Data Points: ${Object.keys(response.monthlyTrend).length}`);
    console.log(`   Recent Reports: ${response.recentReports.length}`);
    console.log("✅ ============================================\n");

    res.json(response);

  } catch (error) {
    console.error("\n❌ ============================================");
    console.error("❌ Stats Endpoint FATAL Error:");
    console.error("❌ ============================================");
    console.error("Error Message:", error.message);
    console.error("Error Stack:", error.stack);
    console.error("❌ ============================================\n");
    
    res.status(500).json({ 
      error: "Failed to fetch statistics",
      details: error.message,
      hint: "Check server console for detailed error logs"
    });
  }
});

// ===============================
//  Health Check
// ===============================
app.get("/", (req, res) => {
  res.json({ 
    message: "✅ Crime Classification Backend API is running!",
    timestamp: new Date().toISOString(),
    endpoints: {
      auth: ["/api/auth/signup", "/api/auth/login"],
      reports: ["/api/report", "/api/reports", "/api/reports/stats", "/api/reports/:id/status"],
      debug: ["/api/debug/count", "/api/debug/sample", "/api/debug/schema"]
    }
  });
});

// ===============================
//  DEBUG: Check database records count
// ===============================
app.get("/api/debug/count", (req, res) => {
  console.log("🔍 Debug: Checking total records...");
  db.query("SELECT COUNT(*) as total FROM crime_reports", (err, results) => {
    if (err) {
      console.error("❌ Debug error:", err);
      return res.status(500).json({ error: err.message });
    }
    const total = results[0].total;
    console.log(`✅ Total records in database: ${total}`);
    res.json({ 
      totalRecords: total,
      message: total === 0 ? "⚠️ No records in database!" : `✅ Found ${total} records`,
      timestamp: new Date().toISOString()
    });
  });
});

// ===============================
//  DEBUG: Get sample data
// ===============================
app.get("/api/debug/sample", (req, res) => {
  console.log("🔍 Debug: Fetching sample data...");
  db.query("SELECT * FROM crime_reports LIMIT 5", (err, results) => {
    if (err) {
      console.error("❌ Debug error:", err);
      return res.status(500).json({ error: err.message });
    }
    console.log(`✅ Retrieved ${results.length} sample records`);
    res.json({ 
      count: results.length,
      samples: results,
      timestamp: new Date().toISOString()
    });
  });
});

// ===============================
//  DEBUG: Check table schema
// ===============================
app.get("/api/debug/schema", (req, res) => {
  console.log("🔍 Debug: Checking table schema...");
  db.query("DESCRIBE crime_reports", (err, results) => {
    if (err) {
      console.error("❌ Debug error:", err);
      return res.status(500).json({ error: err.message });
    }
    console.log(`✅ Table schema retrieved`);
    res.json({ 
      columns: results,
      timestamp: new Date().toISOString()
    });
  });
});

// ===============================
//  Error Handler Middleware
// ===============================
app.use((err, req, res, next) => {
  console.error("❌ Unhandled error:", err);
  res.status(500).json({
    error: "Internal server error",
    details: err.message,
    timestamp: new Date().toISOString()
  });
});

// ===============================
//  Start Server
// ===============================
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log("\n🎉 ============================================");
  console.log("🚀 Backend Server Started Successfully!");
  console.log("============================================");
  console.log(`📡 Server URL: http://localhost:${PORT}`);
  console.log(`📊 Dashboard Stats: http://localhost:${PORT}/api/reports/stats`);
  console.log(`🔄 Update Status: PUT http://localhost:${PORT}/api/reports/:id/status`);
  console.log(`🔍 Debug Count: http://localhost:${PORT}/api/debug/count`);
  console.log(`🔍 Debug Sample: http://localhost:${PORT}/api/debug/sample`);
  console.log(`🔍 Debug Schema: http://localhost:${PORT}/api/debug/schema`);
  console.log(`🤖 ML API URL: ${ML_API_URL}`);
  console.log("============================================\n");
});