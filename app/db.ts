import mysql from "mysql2/promise";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.resolve(__dirname, "..", ".env") });

const pool = mysql.createPool({
  host: process.env.DB_HOST ?? "127.0.0.1",
  user: process.env.DB_USER ?? "root",
  password: process.env.DB_PASSWORD ?? "",
  database: process.env.DB_NAME ?? "letterboxd_proj_db",
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

export async function query<T = any>(sql: string, params?: any[]) {
  const [rows] = await pool.query<any>(sql, params);
  return rows as T[];
}